#!/usr/bin/env python3
"""Execute shipped install verification and version checks on the final IPK.

No Enigma2 imports, opkg mutations, network requests or changes to host paths.
"""
import argparse
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import tempfile

parser=argparse.ArgumentParser()
parser.add_argument('package',type=Path)
parser.add_argument('--product',required=True,choices=('piconhub','gsu'))
parser.add_argument('--version',required=True)
parser.add_argument('--report',type=Path)
args=parser.parse_args()
raw=args.package.read_bytes()
assert raw.startswith(b'!<arch>\n'),'Expected an ar IPK'
parts={};offset=8
while offset<len(raw):
    header=raw[offset:offset+60]
    assert len(header)==60 and header[-2:]==b'`\n','Invalid ar header'
    size=int(header[48:58]);name=header[:16].decode().strip().rstrip('/')
    assert name not in parts,'Duplicate ar entry'
    parts[name]=raw[offset+60:offset+60+size]
    assert len(parts[name])==size,'Truncated ar entry'
    offset+=60+size+size%2
assert parts['debian-binary']==b'2.0\n'
with tarfile.open(fileobj=io.BytesIO(parts['control.tar.gz'])) as arc:
    control=arc.extractfile('./control').read().decode()
    postinst=arc.extractfile('./postinst').read().decode()
fields=dict(line.split(': ',1) for line in control.splitlines() if ': ' in line)
identity='enigma2-plugin-extensions-'+args.product+'-warder-evolution'
assert fields['Package']==identity and fields['Version']==args.version,'Package identity/version mismatch'
with tempfile.TemporaryDirectory(prefix='warder-install-gate-') as temp:
    root=Path(temp)
    with tarfile.open(fileobj=io.BytesIO(parts['data.tar.gz'])) as arc:
        for member in arc:
            relative=PurePosixPath(member.name)
            assert not relative.is_absolute() and '..' not in relative.parts,'Unsafe payload path'
            assert not member.issym() and not member.islnk(),'Unexpected payload link'
            if not member.isfile():continue
            target=root/relative;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(arc.extractfile(member).read())
    family='WarderPiconHub' if args.product=='piconhub' else 'GlassSysUtil'
    runtime=root/'usr/lib/enigma2/python/Plugins/Extensions'/family
    version_file='version.txt' if args.product=='piconhub' else 'version'
    assert (runtime/version_file).read_text().strip()==args.version,'Runtime/control version mismatch'
    verifier='warder_update.py' if args.product=='piconhub' else 'install_health.py'
    switch='--verify-installed-files' if args.product=='piconhub' else '--files-only'
    assert verifier in postinst and switch in postinst,'Gate must execute the shipped postinst verifier'
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    result=subprocess.run([sys.executable,str(runtime/verifier),switch],env=env,capture_output=True,text=True)
    assert result.returncode==0,'Shipped postinst verifier failed: '+result.stdout+result.stderr
    # Reproduce minimal receiver images: the updater must cold-import without
    # dataclasses. Preload standard-library dependencies first, because newer
    # desktop Python versions may internally use it for unrelated modules.
    minimal_code = """
import builtins, hashlib, io, json, pathlib, re, runpy, ssl, subprocess, sys, tarfile, tempfile
from urllib.request import Request, urlopen
original_import = builtins.__import__
def minimal_import(name, *args, **kwargs):
    if name == 'dataclasses' or name.startswith('dataclasses.'):
        raise ModuleNotFoundError("No module named 'dataclasses'")
    return original_import(name, *args, **kwargs)
builtins.__import__ = minimal_import
script, switch = sys.argv[1:]
if switch == 'startup':
    updater = runpy.run_path(script)
    record = updater['Release']('1', 'url', 'a' * 64, 1)
    assert record.notes_i18n == {}
else:
    sys.argv = [script, switch]
    runpy.run_path(script, run_name='__main__')
"""
    minimal=subprocess.run([sys.executable,'-c',minimal_code,str(runtime/verifier),switch],env=env,capture_output=True,text=True)
    assert minimal.returncode==0,'Minimal-Python postinst failed: '+minimal.stdout+minimal.stderr
    module_file='warder_update.py' if args.product=='piconhub' else 'plugin_update.py'
    startup=subprocess.run([sys.executable,'-c',minimal_code,str(runtime/module_file),'startup'],env=env,capture_output=True,text=True)
    assert startup.returncode==0,'Minimal-Python updater import failed: '+startup.stdout+startup.stderr
    spec=importlib.util.spec_from_file_location('extracted_install_version_gate',runtime/module_file)
    updater=importlib.util.module_from_spec(spec);sys.modules[spec.name]=updater;spec.loader.exec_module(updater)
    updater.version_key(args.version)
    product='PiconHub Warder Evolution' if args.product=='piconhub' else 'Glass System Utility Warder Evolution'
    channel='stable' if args.product=='piconhub' else 'original-python314'
    assert updater.parse_release(json.dumps({'schema':1,'product':product,'channel':channel,'release':None}),args.version) is None
report={'version':args.version,'package':identity,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
        'shipped_postinst_verifier_exit':0,'installed_version_parser_passed':True,'updater_empty_feed_passed':True,'minimal_python_without_dataclasses_passed':True}
if args.report:
    args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
