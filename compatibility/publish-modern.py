"""Publish the verified generation change and activate only its official modern feed."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import tempfile
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Evolution-by-Warder/GSU-Warder-Evolution'
VERSION = '0.41.5'
TAG = 'v'+VERSION
FILENAME = 'enigma2-plugin-extensions-gsu_'+VERSION+'_all.ipk'
MODERN = 'plugin/update/stable-modern.json'
BRIDGE = 'plugin/update/stable.json'
HISTORIC = (BRIDGE,'plugin/update/candidate.json','restoration/update/candidate.json')
BASES = {'main':'e064e426d1c7388200b9ed4727aacbf5e5705bc8',
         'original-python314':'b8f1b45b2795d88987915fd27c871d3179eec27b'}
URL = 'https://github.com/'+REPO+'/releases/download/'+TAG+'/'+FILENAME
LANGS = set('en sk cs de pl hu ru fr it es al el et fa lt nl pt ro tr uk zh'.split())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def command(*args):
    return subprocess.check_output(args,cwd=ROOT,text=True).strip()


def encode(value):
    return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')


def check(directory):
    package = directory/FILENAME
    raw = package.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(package.with_suffix('.ipk.sha256').read_text().split()==[digest,FILENAME],'package sidecar')
    install = json.loads((directory/'install.json').read_text())
    require(install.get('version')==VERSION and install.get('bytes')==len(raw) and install.get('sha256')==digest
            and install.get('shipped_postinst_verifier_exit')==0 and install.get('installed_version_parser_passed') is True,
            'independent installation report')
    require((ROOT/'plugin/src/GlassSysUtil/version').read_text().strip()==VERSION,'public version')
    require((ROOT/'plugin/update/release-request').read_text().strip()==VERSION,'release request')
    notes = json.loads((ROOT/'plugin/update/RELEASE-NOTES.i18n.json').read_text())
    require(notes['version']==VERSION and set(notes['notes'])==LANGS and all(notes['notes'].values()),'release translations')
    item = dict(version=VERSION,tag=TAG,url=URL,sha256=digest,bytes=len(raw),notes=notes['notes']['en'],
                notes_i18n=notes['notes'],release_url='https://github.com/'+REPO+'/releases/tag/'+TAG)
    feed = dict(schema=1,product='Glass System Utility Warder Evolution',channel='stable-modern',release=item)
    payload = encode(feed)
    require(len(payload)<=65536,'feed capacity')
    updater = runpy.run_path(str(ROOT/'plugin/src/GlassSysUtil/plugin_update.py'))
    result = updater['parse_release'](payload,'13.41-r6','stable-modern')
    updater['validate_ipk'](package,result)
    require(result.version==VERSION and updater['parse_release'](payload,VERSION,'stable-modern') is None,'upgrade order')
    return feed, install


def verify_public(url, expected):
    for attempt in range(6):
        try:
            request = Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Warder-release-check'})
            with urlopen(request,timeout=30) as response:
                if response.read(len(expected)+1)==expected:
                    return
        except OSError:
            pass
        if attempt<5:
            time.sleep(5*(attempt+1))
    raise ValueError('Public bytes differ or are unavailable: '+url)


def stable_assets(directory,revision):
    # Normal, non-forced tag creation. Existing tags can only name this exact source.
    command('git','fetch','origin','--tags')
    tag_ref='refs/tags/'+TAG
    listed=command('git','tag','--list',TAG)
    if not listed:
        command('git','push','origin',revision+':'+tag_ref)
        command('git','fetch','origin',tag_ref+':'+tag_ref)
    require(command('git','rev-parse',tag_ref+'^{commit}')==revision,'immutable tag target')
    result=subprocess.run(['gh','release','view',TAG,'--repo',REPO,'--json','isDraft,isPrerelease,assets'],capture_output=True,text=True)
    if result.returncode:
        require('release not found' in result.stderr.lower() or '404' in result.stderr,'release lookup failed')
        command('gh','release','create',TAG,'--repo',REPO,'--verify-tag','--draft','--title','GSU Warder Evolution '+VERSION,
                '--notes-file',str(ROOT/'plugin/update/RELEASE-NOTES.md'))
    status=json.loads(command('gh','release','view',TAG,'--repo',REPO,'--json','isDraft,isPrerelease,assets'))
    require(not status['isPrerelease'],'existing release is not stable')
    expected=(FILENAME,FILENAME+'.sha256')
    existing={asset['name'] for asset in status['assets']}
    require(existing.issubset(expected),'unexpected existing release assets')
    for name in expected:
        if name not in existing:
            require(status['isDraft'],'published assets are immutable')
            command('gh','release','upload',TAG,str(directory/name),'--repo',REPO)
    with tempfile.TemporaryDirectory() as temp:
        command('gh','release','download',TAG,'--repo',REPO,'--dir',temp)
        for name in expected:
            require((Path(temp)/name).read_bytes()==(directory/name).read_bytes(),'unexpected stored asset: '+name)
    if status['isDraft']:
        command('gh','release','edit',TAG,'--repo',REPO,'--draft=false','--latest')
    for name in expected:
        verify_public(URL.rsplit('/',1)[0]+'/'+name,(directory/name).read_bytes())


def historic_feeds():
    for branch,baseline in BASES.items():
        command('git','fetch','origin','refs/heads/'+branch+':refs/remotes/origin/'+branch)
        for path in HISTORIC:
            require(command('git','rev-parse',baseline+':'+path)==command('git','rev-parse','origin/'+branch+':'+path),
                    'historic feed changed: '+branch+'/'+path)
    require(command('git','rev-parse','v13.41-r6^{commit}')=='45a9fad7be6e20a6eae6055c0cb59551be45b9f9','bridge tag changed')


def publish(directory,feed,install):
    require(os.environ.get('GITHUB_REF')=='refs/heads/main' and os.environ.get('GITHUB_REPOSITORY')==REPO,'production context')
    revision=os.environ['GITHUB_SHA']
    historic_feeds()
    require(revision==command('git','rev-parse','HEAD'),'wrong checkout')
    previous=json.loads(command('git','show','origin/main:'+MODERN))
    require(previous==dict(feed,release=None) or previous==feed,'another release is active')
    if previous==feed:
        recorded=json.loads(command('git','show','origin/main:reports/gsu-'+VERSION+'/public-verification.json'))
        tag_source=command('git','rev-parse',TAG+'^{commit}')
        require(recorded['source_commit']==tag_source,'active feed source')
        command('git','merge-base','--is-ancestor',tag_source,'origin/main')
        for name in (FILENAME,FILENAME+'.sha256'):
            verify_public(URL.rsplit('/',1)[0]+'/'+name,(directory/name).read_bytes())
    else:
        require(revision==command('git','rev-parse','origin/main'),'main advanced')
        stable_assets(directory,revision)
    item=feed['release']
    record=json.loads((ROOT/'PRODUCTION.json').read_text())
    evidence=dict(source_commit=revision,workflow_run=int(os.environ['GITHUB_RUN_ID']),release=TAG,
                  public_bytes=item['bytes'],public_sha256=item['sha256'],public_sidecar_verified=True,
                  installed_regular_file_bytes=int((directory/'installed-bytes').read_text()),packaged_install=install,
                  physical_receiver_tested=False)
    if previous!=feed:
        require(record['release']['version']=='13.41-r6' and record['release']['sha256']=='a8e79609147666b27f18460b3340e099bb013664478a787746bcf56bb28052e2','production register has changed')
        record.update(previous_release=record['release'],release=item,source_commit=revision,package_source_commit=revision,
                      status='production-update-active',validation=evidence,approved_on='2026-11-26',
                      approval='Owner-approved stable GSU 0.41.5 release',version_policy='Public 0.41.x, OPKG epoch 1. Immutable r6 and r93 migration feeds.',
                      documentation_checkpoint={'status':'web-sync-pending','continuation':'Update SK/EN/DE/RU and verify Pages.'})
        record['identity_transition'].update(target_version=VERSION,steps='r93 → restart → 13.41-r6 → restart → 0.41.5')
        report=ROOT/'reports'/('gsu-'+VERSION)/'public-verification.json'
        report.parent.mkdir(parents=True,exist_ok=True)
        report.write_bytes(encode(evidence))
        (ROOT/MODERN).write_bytes(encode(feed))
        (ROOT/'PRODUCTION.json').write_bytes(encode(record))
        notes='# GSU '+VERSION+'\n\n'+item['notes_i18n']['sk']+'\n\n[IPK]('+URL+') · [Vydanie]('+item['release_url']+')\n\nSHA-256 '+item['sha256']+'\n'
        (ROOT/'docs/CURRENT-RELEASE.md').write_text(notes)
        (ROOT/('docs/RELEASE-'+VERSION+'.md')).write_text(notes)
        readme=ROOT/'README.md'
        old=readme.read_text()
        start=old.index('## Spoločné ostré vydanie')
        end=old.index('\nPlugin pre Enigma2',start)
        old=old[:start]+'## Stabilné vydanie '+VERSION+'\n\n'+item['notes_i18n']['sk']+' [Poznámky](docs/CURRENT-RELEASE.md) · [IPK]('+URL+').\n'+old[end:]
        old=old.replace('**Stabilné vydanie: 13.41-r6.', '**Stabilné vydanie: '+VERSION+'.').replace('`enigma2-plugin-extensions-gsu_13.41-r6_all.ipk`','`'+FILENAME+'`')
        old=old.replace('Rozhranie a prejdené funkcie schválil používateľ na GigaBlue Quad 4K Pro s OpenATV 8.', 'Fyzická skúška na GigaBlue Quad 4K Pro sa týkala predchádzajúcej generácie.')
        old=old.replace('431 udržiavaných spoločných a doplnkových textov','texty diagnostických centier')
        old=old.replace('r93 → reštart GUI → 13.41-r6.', 'r93 → reštart GUI → 13.41-r6 → reštart GUI → '+VERSION+'.')
        readme.write_text(old)
        log=ROOT/'NEXT-RELEASE.md'
        log.write_text('# Produkčná aktivácia '+TAG+'\n\nZdroj '+revision+', workflow '+str(evidence['workflow_run'])+
                       ', overených '+str(item['bytes'])+' bajtov, SHA-256 '+item['sha256']+
                       '. Samostatný stabilný feed je aktívny. Ďalší krok je aktualizácia webu SK/EN/DE/RU a kontrola Pages.\n\n'+log.read_text())
        changed=[MODERN,'PRODUCTION.json','README.md','NEXT-RELEASE.md','docs/CURRENT-RELEASE.md','docs/RELEASE-'+VERSION+'.md',str(report.relative_to(ROOT))]
        command('git','add','--',*changed)
        command('git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com',
                'commit','-m','Activate verified GSU '+VERSION+' modern stable feed')
        command('git','push','origin','HEAD:refs/heads/main')
    raw='https://raw.githubusercontent.com/'+REPO+'/'
    verify_public(raw+'main/'+MODERN,encode(feed))
    for branch in BASES:
        for path in HISTORIC:
            expected=subprocess.check_output(['git','show',BASES[branch]+':'+path],cwd=ROOT)
            verify_public(raw+branch+'/'+path,expected)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('directory',type=Path)
    parser.add_argument('--publish',action='store_true')
    args=parser.parse_args()
    feed,install=check(args.directory)
    if args.publish:
        publish(args.directory,feed,install)
    print(feed['release']['bytes'],feed['release']['sha256'])
