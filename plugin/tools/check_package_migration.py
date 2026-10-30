#!/usr/bin/env python3
"""Offline opkg replacement and actual prerm hook checks, in a disposable root."""
from pathlib import Path
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src/GlassSysUtil'))
import plugin_update as update
import build_ipk

opkg=Path(sys.argv[1]).resolve()
bridge=BASE/'dist/bridge/enigma2-plugin-glasssysutil_13.40-r93_all.ipk'
current=BASE/'dist/enigma2-plugin-extensions-gsu_13.40-r94_all.ipk'
with tempfile.TemporaryDirectory(prefix='gsu-opkg-migration-') as folder:
    folder=Path(folder);root=folder/'root';root.mkdir()
    config=folder/'opkg.conf';config.write_text('dest root /\narch all 10\n')
    (root/'var/lock').mkdir(parents=True)
    (root/'usr/lib/opkg').mkdir(parents=True)
    def run(*args):
        p=subprocess.run([str(opkg),'-f',str(config),'-o',str(root),*args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        print('OPKG',args, p.stdout,flush=True)
        if p.returncode:raise RuntimeError(p.stdout)
        return p.stdout
    with tarfile.open(fileobj=io.BytesIO(update._control_archive(bridge)),mode='r:*') as control:
        text=control.extractfile(next(m for m in control if m.name.lstrip('./')=='control')).read().decode()
    deps=next(line.split(': ',1)[1] for line in text.splitlines() if line.startswith('Depends:'))
    metadata=('Package: gsu-test-prerequisites\nVersion: 1.0\nArchitecture: all\nProvides: '+deps+'\nDescription: isolated receiver dependency fixture\n').encode()
    data=bytearray(b'!<arch>\n')
    for name,raw in [('debian-binary',b'2.0\n'),('control.tar.gz',build_ipk.archive([('control',metadata,0o644)])),('data.tar.gz',build_ipk.archive([]))]:
        data.extend(('%-16s%-12s%-6s%-6s%-8s%-10s`\n' % (name+'/',0,0,0,'100644',len(raw))).encode());data.extend(raw)
        if len(raw)%2:data.extend(b'\n')
    fixture=folder/'prerequisites.ipk';fixture.write_bytes(data)
    run('install',str(fixture))
    run('install',str(bridge))
    settings=root/'etc/enigma2/settings';settings.parent.mkdir(parents=True,exist_ok=True);settings.write_bytes(b'config.plugins.glasssysutil.preserve=yes\n')
    picon=root/'usr/share/enigma2/picon/user.png';picon.parent.mkdir(parents=True,exist_ok=True);picon.write_bytes(b'user-owned')
    run('install',str(current))
    installed=run('list-installed')
    assert update.PACKAGE_ID+' - 13.40-r94' in installed,installed
    assert update.LEGACY_PACKAGE_ID+' -' not in installed,installed
    assert settings.read_bytes()==b'config.plugins.glasssysutil.preserve=yes\n' and picon.read_bytes()==b'user-owned'
    plugin=root/'usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/plugin.py'
    assert plugin.exists()
    run('remove',update.PACKAGE_ID)
    assert not plugin.exists()
    assert settings.exists() and picon.exists()
    # Execute the exact bridge prerm in a real chroot, never against host paths.
    shell=Path('/bin/sh').resolve();dest=root/'bin/sh';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(shell,dest);dest.chmod(0o755)
    libraries=subprocess.check_output(['ldd',str(shell)],text=True)
    for name in set(re.findall(r'/[^\s()]+',libraries)):
        src=Path(name);target=root/src.relative_to('/');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
    helper=root/'usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/native_start_config.py';helper.parent.mkdir(parents=True,exist_ok=True);helper.write_text('hook fixture')
    python=root/'usr/bin/python3';python.parent.mkdir(parents=True,exist_ok=True);python.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> /restore-called\n');python.chmod(0o755)
    with tarfile.open(fileobj=io.BytesIO(update._control_archive(bridge)),mode='r:*') as archive:
        member=next(m for m in archive if m.name.lstrip('./')=='prerm');(root/'prerm').write_bytes(archive.extractfile(member).read())
    env=dict(os.environ,D='')
    subprocess.run(['chroot',str(root),'/bin/sh','/prerm','remove'],env=env,check=True)
    called=root/'restore-called';before=called.read_bytes();assert b'--restore-all' in before
    flag=root/'var/lib/warder-gsu/package-rename-in-progress';flag.parent.mkdir(parents=True,exist_ok=True);flag.write_text('13.40-r94\n')
    subprocess.run(['chroot',str(root),'/bin/sh','/prerm','remove'],env=env,check=True);assert called.read_bytes()==before
    flag.unlink()
    subprocess.run(['chroot',str(root),'/bin/sh','/prerm','upgrade'],env=env,check=True);assert called.read_bytes()==before
print('PASS: real offline opkg r93→r94 replacement, one installed identity, removal, user settings/picons preserved; actual prerm preserves CAM state only during rename.')
