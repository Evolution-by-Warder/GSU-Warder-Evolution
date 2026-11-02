#!/usr/bin/env python3
"""Prepare authorized stable versions from SHA-pinned, previously tested IPKs."""
import hashlib, importlib.util, io, json, re, subprocess, sys, tarfile
from pathlib import Path
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'docs/COMMON-STABLE-20261102.json').read_text())
def write_json(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def payload(raw):
    parts={};offset=8
    assert raw.startswith(b'!<arch>\n')
    while offset<len(raw):
        header=raw[offset:offset+60];size=int(header[48:58]);name=header[:16].decode().strip().rstrip('/')
        parts[name]=raw[offset+60:offset+60+size];offset+=60+size+size%2
    with tarfile.open(fileobj=io.BytesIO(parts['data.tar.gz'])) as arc:
        return {m.name.removeprefix('./'):arc.extractfile(m).read() for m in arc if m.isfile()}
def candidate():
    with urlopen(C['candidate_url'],timeout=120) as response:raw=response.read(25000000)
    assert hashlib.sha256(raw).hexdigest()==C['candidate_sha'],'Candidate SHA mismatch'
    out=ROOT/'reports/common-stable';out.mkdir(parents=True,exist_ok=True)
    (out/'candidate.ipk').write_bytes(raw)
    return payload(raw)
def main():
    old=candidate();runtime=ROOT/C['runtime'];version=C['version'];notes=C['notes_i18n']
    if C['key']=='full':
        sys.path.insert(0,str(ROOT/'tools'))
        spec=importlib.util.spec_from_file_location('prepare_openpli',ROOT/'tools/prepare-openpli-ipk.py')
        prep=importlib.util.module_from_spec(spec);spec.loader.exec_module(prep);prep.VERSION=version;prep.main()
        prefix='usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/'
        for filename,lang in [('history.txt','en'),('history.txtSk','sk')]:
            history=old[prefix+filename].decode()
            (runtime/filename).write_text('FullHDGlass '+version+' — 02.11.2026\n'+notes[lang]+'\n\n'+history)
    else:
        name='version' if C['key']=='gsu' else 'version.txt'
        (runtime/name).write_text(version+'\n')
        history_path=('usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/release-history.json' if C['key']=='gsu' else 'usr/lib/enigma2/python/Plugins/Extensions/WarderPiconHub/data/release-notes.json')
        previous=json.loads(old[history_path]);entries=previous.get('entries',[])
        # TEST builds remain documented in their own release notes, not as stable history.
        entries=[e for e in entries if 'test' not in e['version'] and e['version'] not in ('13.41-r1','13.41-r2','13.41-r3',version)]
        history={'version':version,'notes':notes,'entries':[{'version':version,'date':'02.11.2026','notes':notes}]+entries}
        write_json(ROOT/'plugin/update/RELEASE-NOTES.i18n.json',history)
        (ROOT/'plugin/update/RELEASE-NOTES.md').write_text(C['product']+' '+version+'\n\n'+notes['sk']+'\n\n'+notes['en']+'\n')
        if C['key']=='picon':
            path=ROOT/'plugin/project.json';project=json.loads(path.read_text());project['development_version']=version;write_json(path,project)
        else:(ROOT/'plugin/update/release-request').write_text(version+'\n')
    print('Prepared stable '+C['product']+' '+version+'; public feeds unchanged')
if __name__=='__main__':main()
