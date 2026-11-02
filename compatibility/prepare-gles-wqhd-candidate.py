#!/usr/bin/env python3
"""Stage an isolated receiver candidate after the source regression suite."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='13.40-r95-test1'
NAME='GSU'
RUNTIME=ROOT/'plugin/src/GlassSysUtil'
notes={"sk":"OpenATV 8.1: WQHD škálovanie, celé riadky ponúk a história piatich verzií. Testovacia zostava; fyzický GLES test čaká.",
       "en":"OpenATV 8.1: WQHD scaling, whole menu rows and five-entry history. Receiver/GLES validation pending."}
(RUNTIME/'version').write_text(VERSION+'\n')
(ROOT/'plugin/update/RELEASE-NOTES.md').write_text(NAME+' '+VERSION+'\n\n'+notes['sk']+'\n')
path=ROOT/'plugin/update/RELEASE-NOTES.i18n.json';data=json.loads(path.read_text())
data.update(version=VERSION,notes=notes)
data['entries']=[{'version':VERSION,'date':'02.11.2026','notes':notes}]+[entry for entry in data.get('entries',[]) if entry.get('version')!=VERSION]
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(NAME,VERSION,'staged; production manifests unchanged')
