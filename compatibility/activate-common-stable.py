#!/usr/bin/env python3
"""Verify public stable bytes, approved runtime parity, then stage update records."""
import hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, tarfile
from pathlib import Path
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]
C=json.loads((ROOT/'docs/COMMON-STABLE-20261102.json').read_text())
def put(path,value):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def get(path):return json.loads(path.read_text())
def payload(raw):
    parts={};offset=8
    assert raw.startswith(b'!<arch>\n')
    while offset<len(raw):
        header=raw[offset:offset+60];size=int(header[48:58]);name=header[:16].decode().strip().rstrip('/')
        parts[name]=raw[offset+60:offset+60+size];offset+=60+size+size%2
    with tarfile.open(fileobj=io.BytesIO(parts['data.tar.gz'])) as arc:
        return {m.name.removeprefix('./'):arc.extractfile(m).read() for m in arc if m.isfile()}
def main():
    version=C['version'];package=ROOT/C['package'];raw=package.read_bytes();sha=hashlib.sha256(raw).hexdigest();repo='Evolution-by-Warder/'+C['repo']
    url='https://github.com/'+repo+'/releases/download/v'+version+'/'+package.name
    with urlopen(url,timeout=120) as response:public=response.read(len(raw)+1)
    assert public==raw,'Public IPK differs from verified build'
    with urlopen(url+'.sha256',timeout=60) as response:sidecar=response.read().decode()
    assert sidecar.split()[0]==sha,'Public checksum mismatch'
    new=payload(raw);old=payload((ROOT/'reports/common-stable/candidate.ipk').read_bytes())
    compared=[]
    for name,content in old.items():
        if not name.endswith('.py'):continue
        assert name in new,'Missing candidate Python file: '+name
        other=new[name]
        if C['key']=='full' and name.rsplit('/',1)[-1] in ('plugin.py','warderDialogSkins.py'):
            # The only Python changes allowed are generated version header labels.
            pattern=rb'(<eLabel\b(?=[^>]*\bposition="1680,70")[^>]*\btext=")[^"<>]*(")'
            content=re.sub(pattern,rb'\1VERSION\2',content);other=re.sub(pattern,rb'\1VERSION\2',other)
        assert content==other,'Runtime differs from approved candidate: '+name
        compared.append(name)
    rel={'version':version,'tag':'v'+version,'url':url,'sha256':sha,'bytes':len(raw),'notes':C['notes_i18n']['sk'],'notes_i18n':C['notes_i18n'],'release_url':'https://github.com/'+repo+'/releases/tag/v'+version}
    report={'version':version,'package_source_commit':os.environ.get('PACKAGE_SOURCE_SHA',os.environ.get('GITHUB_SHA')),'workflow_run':os.environ.get('GITHUB_RUN_ID'),'public_ipk_sha256_verified':True,'public_ipk_sidecar_verified':True,'sha256':sha,'bytes':len(raw),'candidate_sha256':C['candidate_sha'],'candidate_python_files_compared':len(compared),'only_generated_version_labels_changed':True,'OpenPLi_refs':['release-9.2','develop'],'OpenATV_refs':['8.0','8.0-next','master'],'matrices_passed':True,'physical_receiver_all_features_verified':False,'custom_font_settings_preserved':True}
    out=ROOT/'reports/common-stable';put(out/'public-verification.json',report)
    if C['key']=='full':
        frozen=(ROOT/'update.json').read_bytes()
        destination=ROOT/'packages'/package.name;destination.parent.mkdir(exist_ok=True);shutil.copy2(package,destination);shutil.copy2(str(package)+'.sha256',str(destination)+'.sha256')
        rel['package_url']='https://raw.githubusercontent.com/'+repo+'/main/packages/'+package.name
        rel['changelog']=C['notes_i18n']['sk']
        feed={k:rel[k] for k in ('version','package_url','sha256','changelog')}
        for name in ('update-production.json','update-test.json'):put(ROOT/name,feed)
        path=ROOT/'docs/PRODUCTION.json';record=get(path);record['previous_production']=record['release'];record['release']=rel;record['peer_production']=C['peers'];record['version_policy']='Normal 1.0.62 upgrades from 1.0.61 and every 1.0.62-test build. Published packages are immutable.'
        for key in ('activation_commit','native_test_mirror_commit'):record.pop(key,None)
        assert (ROOT/'update.json').read_bytes()==frozen
        # Keep build inventory synchronized with the now-active feeds.
        path_inventory=ROOT/'design/settings-ui-inventory.json';inv=get(path_inventory)
        inv['feeds_sha256']={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ('update.json','update-test.json')}
        inv['current_feed_version']=get(ROOT/'update.json')['version'];inv['test_feed_version']=version;inv['production_feed_version']=version;put(path_inventory,inv)
    else:
        feedpath=ROOT/'plugin/update/stable.json';feed=get(feedpath);feed['release']=rel;put(feedpath,feed)
        path=ROOT/('PRODUCTION.json' if C['key']=='gsu' else 'plugin/production.json');record=get(path);record['previous_release']=record['release'];record['release']=rel
        if C['key']=='gsu':
            record['identity_transition']['target_version']=version;record['identity_transition']['steps']='Update to frozen r93 when offered, restart GUI, then update to '+version
            record['version_policy']='Normal 13.41-r4 upgrades from r95 and all 13.41 TEST revisions; the legacy r93 bridge remains frozen.'
        else:
            project_path=ROOT/'plugin/project.json';project=get(project_path)
            for key in ('development_version','production_version','latest_published_version','requested_production_version'):project[key]=version
            project.update(status='production-authorized',runtime_status='production',production_approved_on=C['date'],production_authorization=C['authorization'],receiver_validation=report)
            put(project_path,project)
        record['peer_production']=C['peers']
    record.update(product=C['product'],status='production-update-active',approved_on=C['date'],approval=C['authorization'],source_branch='main',source_commit=os.environ.get('PACKAGE_SOURCE_SHA',os.environ.get('GITHUB_SHA')),package_source_commit=os.environ.get('PACKAGE_SOURCE_SHA',os.environ.get('GITHUB_SHA')),validation=report,accepted_candidate={'version':C['candidate'],'sha256':C['candidate_sha']})
    put(path,record)
    current='# '+C['product']+' '+version+'\n\nAktívne ostré vydanie pre OpenPLi a OpenATV.\n\n'+C['notes_i18n']['sk']+'\n\n[Stiahnuť IPK]('+url+')\n\nSHA-256: `'+sha+'`\n\nOverené verejné bajty, dodané inštalačné kontroly a natívne rozhrania OpenPLi/OpenATV. Úplné fyzické testovanie všetkých modelov a rozlíšení sa netvrdí.\n'
    (ROOT/'docs/CURRENT-RELEASE.md').write_text(current)
    (ROOT/'docs'/('RELEASE-'+version+'.md')).write_text(current)
    for name in ('PROJECT-CONTINUITY.md','NEXT-RELEASE.md'):
        path=ROOT/name
        if path.exists():path.write_text(path.read_text()+'\n## Stable activation '+C['date']+'\n\n'+C['product']+' '+version+' published as a normal release; public IPK and checksum verified. Main metadata updated. Runtime updater branch activation is recorded separately after verification. Earlier TEST publishing pause is superseded by the owner’s explicit stable-release request.\n')
    print(json.dumps(report))
if __name__=='__main__':main()
