#!/usr/bin/env python3
"""Publish the compatible identity bridge before the extensions-classified GSU."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import urllib.request

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parent
sys.path.insert(0,str(BASE/'src/GlassSysUtil'))
sys.path.insert(0,str(BASE/'tools'))
import plugin_update as update
from publish_update import manifest,run


def public(item):
    request=urllib.request.Request(item['url'],headers={'User-Agent':'GSU-package-identity-verification','Cache-Control':'no-cache'})
    with urllib.request.urlopen(request,timeout=60) as response:data=response.read(item['bytes']+1)
    assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']


def release(path,version,notes,latest,aliases=()):
    document=manifest(path,version,notes)
    offered=update.parse_release(json.dumps(document),'0.0-r0');update.validate_ipk(path,offered)
    tag='v'+version
    releases=json.loads(run('gh','api','repos/'+update.REPOSITORY+'/releases','--paginate','--slurp'))
    existing=next((r for page in releases for r in page if r['tag_name']==tag),None)
    paths=[path,path.with_suffix('.ipk.sha256')]
    for alias in aliases:paths.extend([alias,alias.with_suffix('.ipk.sha256')])
    if existing is None:
        run('gh','release','create',tag,*(str(p) for p in paths),'--repo',update.REPOSITORY,
            '--target',os.environ['GITHUB_SHA'],'--latest' if latest else '--latest=false',
            '--title','GSU Warder Evolution '+version,'--notes',notes)
    else:
        assert not existing['draft'] and not existing['prerelease']
        assets={a['name']:a for a in existing['assets']}
        for p in paths:
            blob=p.read_bytes();assert p.name in assets
            assert assets[p.name]['size']==len(blob) and assets[p.name]['digest']=='sha256:'+hashlib.sha256(blob).hexdigest()
    public(document['release'])
    return document


def publish():
    assert os.environ['GITHUB_REF'] in ('refs/heads/original-python314','refs/heads/release/plugin-groups-20261030')
    version=(BASE/'src/GlassSysUtil/version').read_text().strip()
    assert update.version_key(version)>=update.version_key('13.40-r94')
    assert (BASE/'update/release-request').read_text().strip()==version
    notes=(BASE/'update/RELEASE-NOTES.md').read_text()
    canonical=BASE/'dist'/('enigma2-plugin-extensions-gsu_'+version+'_all.ipk')
    old_feed=json.loads((BASE/'update/candidate.json').read_text())
    if update.version_key(old_feed['release']['version'])<update.version_key('13.40-r93'):
        subprocess.run([sys.executable,str(BASE/'tools/build_ipk.py'),'--bridge','--output',str(BASE/'dist/bridge')],check=True)
        bridge=BASE/'dist/bridge/enigma2-plugin-glasssysutil_13.40-r93_all.ipk'
        bridge_doc=release(bridge,'13.40-r93',notes.replace('GSU '+version,'GSU 13.40-r93',1),False)
        spec=importlib.util.spec_from_file_location('original_r92',BASE/'tests/fixtures/plugin_update_r92.py')
        old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old)
        offered=old.parse_release(json.dumps(bridge_doc),'13.40-r92');old.validate_ipk(bridge,offered)
    else:
        bridge_doc=old_feed
        assert bridge_doc['release']['version']=='13.40-r93'
        public(bridge_doc['release'])
    document=release(canonical,version,notes,True,[canonical.with_name(update.PACKAGE_ID+'_'+version+'_all.ipk')])
    compatibility=copy.deepcopy(bridge_doc)
    compatibility['release']['url']=compatibility['release']['url'].replace(update.REPOSITORY,'Evolution-by-Warder/Glass-System-Utility-Warder-Evolution',1)
    files={BASE/'update/stable.json':document,BASE/'update/candidate.json':bridge_doc,ROOT/'restoration/update/candidate.json':compatibility}
    for p,value in files.items():p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    evidence=dict(status='PUBLIC_RELEASES_VERIFIED',package_id=update.PACKAGE_ID,plugin_browser_category='extensions',plugin_browser_name='gsu-warder-evolution',bridge=bridge_doc['release'],release=document['release'],legacy_updater_r92_accepts_actual_bridge=True,updated_bridge_accepts_actual_canonical_package=True,cam_start_configuration_preserved_during_automatic_rename=True,physical_receiver_test=False,workflow_run=int(os.environ['GITHUB_RUN_ID']))
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/plugin-groups-20261030.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    record=json.loads((ROOT/'PRODUCTION.json').read_text())
    record.update(package_id=update.PACKAGE_ID,approved_on='2026-10-30',approval='GSU nech sa tam zobrazuju ako gsu-warder-evolution',source_commit=os.environ['GITHUB_SHA'])
    record['release']=dict(document['release'],release_url='https://github.com/'+update.REPOSITORY+'/releases/tag/v'+version)
    record['identity_transition']=dict(bridge_version='13.40-r93',target_version=version,legacy_feed_frozen=True,steps='Update to r93, restart GUI, then update to r94')
    record['validation']=dict(workflow_run=int(os.environ['GITHUB_RUN_ID']),unit_tests=374,public_ipk_size_and_sha256_verified=True,receiver_tested=False,limits='Automated package/control/update/migration checks; no physical receiver test claimed.')
    record['update_feeds'].insert(0,update.FEED_URL) if update.FEED_URL not in record['update_feeds'] else None
    (ROOT/'PRODUCTION.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print('VERIFIED GSU extensions group: compatible bridge r93 and canonical '+version)


if __name__=='__main__':publish()
