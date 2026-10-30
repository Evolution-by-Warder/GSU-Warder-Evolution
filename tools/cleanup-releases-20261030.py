#!/usr/bin/env python3
"""Execute the owner's exact obsolete-release list after checking live downloads."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import urllib.request

ROOT=Path(__file__).resolve().parents[1]


def gh(method,path,payload=None):
    command=['gh','api','--method',method,path]
    data=None
    if payload is not None:
        command+=['--input','-'];data=json.dumps(payload)
    value=subprocess.run(command,input=data,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
    return json.loads(value) if value.strip() else None


def verify_url(item):
    request=urllib.request.Request(item['url'],headers={'User-Agent':'Warder-release-cleanup-verifier','Cache-Control':'no-cache'})
    with urllib.request.urlopen(request,timeout=90) as response:raw=response.read()
    assert hashlib.sha256(raw).hexdigest()==item['sha256'],item['url']
    if 'bytes' in item:assert len(raw)==item['bytes']


def verify_feeds(feeds):
    for entry in feeds:
        request=urllib.request.Request(entry['url'],headers={'Cache-Control':'no-cache'})
        with urllib.request.urlopen(request,timeout=45) as response:doc=json.load(response)
        item=doc.get('release',doc)
        assert item['version']==entry['version'] and item['sha256']==entry['sha256'],entry['url']
        assert item.get('url',item.get('package_url'))==entry['package_url'],entry['url']


def same_release(expected,current):
    assert current['id']==expected['id'] and current['tag_name']==expected['tag_name']
    before={(a['id'],a['name'],a['size'],a.get('digest')) for a in expected['assets']}
    after={(a['id'],a['name'],a['size'],a.get('digest')) for a in current['assets']}
    assert before==after,('Release assets changed; refusing deletion',expected['tag_name'])


def main():
    plan=json.loads((ROOT/'.github/releases-cleanup-20261030.json').read_text())
    repo=plan['repository'];assert repo==os.environ['GITHUB_REPOSITORY']
    assert os.environ['GITHUB_REF']=='refs/heads/cleanup/releases-20261030'
    api='repos/'+repo
    protected={r['id'] for r in plan['keep']};targets={r['id'] for r in plan['delete']}
    assert len(protected)==len(plan['keep']) and len(targets)==len(plan['delete'])
    assert not protected&targets
    assert plan['authorization']=='ok, skontroluj to a premaz'
    verify_feeds(plan['feeds'])
    for asset in plan['verify_downloads']:verify_url(asset)
    for release in plan['keep']:
        current=gh('GET',api+'/releases/'+str(release['id']))
        assert current['tag_name']==release['tag_name']
        wanted={a['id'] for a in release['assets']}
        assert wanted<={a['id'] for a in current['assets']}
    existing=gh('GET',api+'/releases?per_page=100')
    assert len(existing)<100
    current_by_id={r['id']:r for r in existing}
    previously_absent=[r for r in plan['delete'] if r['id'] not in current_by_id]
    for release in plan['delete']:
        if release['id'] in current_by_id:same_release(release,current_by_id[release['id']])
    print('GUARDS PASSED:',len(protected),'retained releases; live feeds and',len(plan['verify_downloads']),'public downloads verified',flush=True)
    removed=[]
    for release in plan['delete']:
        if release['id'] not in current_by_id:continue
        same_release(release,gh('GET',api+'/releases/'+str(release['id'])))
        gh('DELETE',api+'/releases/'+str(release['id']))
        removed.append({'id':release['id'],'tag':release['tag_name']})
        print('DELETED',release['tag_name'],flush=True)
    removed_assets=[]
    for item in plan.get('remove_auxiliary_ipks',[]):
        assert item['release_id'] in protected
        release=gh('GET',api+'/releases/'+str(item['release_id']))
        current=next((a for a in release['assets'] if a['id']==item['id']),None)
        if current is None:continue
        assert (current['name'],current['size'],current.get('digest'))==(item['name'],item['size'],item.get('digest'))
        assert item['name'].endswith(('.ipk','.ipk.sha256'))
        gh('DELETE',api+'/releases/assets/'+str(item['id']))
        removed_assets.append({'id':item['id'],'name':item['name']})
    for change in plan.get('rename',[]):
        assert change['id'] in protected
        fields={k:v for k,v in change.items() if k!='id'}
        gh('PATCH',api+'/releases/'+str(change['id']),fields)
    gh('PATCH',api+'/releases/'+str(plan['current_release_id']),{'make_latest':'true'})
    pages=[];page=1
    while True:
        rows=gh('GET',api+'/releases?per_page=100&page='+str(page));pages.extend(rows)
        if len(rows)<100:break
        page+=1
    after={r['id'] for r in pages}
    assert protected<=after and not targets&after
    latest=gh('GET',api+'/releases/latest');assert latest['id']==plan['current_release_id']
    verify_feeds(plan['feeds'])
    for asset in plan['verify_downloads']:verify_url(asset)
    report=dict(status='COMPLETED',repository=repo,authorization=plan['authorization'],deleted_releases=removed,
                deleted_release_count=len(removed)+len(previously_absent),already_absent_release_ids=[r['id'] for r in previously_absent],deleted_auxiliary_ipk_assets=removed_assets,
                kept_releases=[{'id':r['id'],'tag':r['tag_name']} for r in pages],remaining_release_count=len(pages),
                all_live_feeds_unchanged=True,all_protected_public_downloads_verified=True,
                git_tags_unchanged=True,source_and_ipks_in_git_unchanged=True,workflow_run=int(os.environ['GITHUB_RUN_ID']))
    folder=ROOT/'reports';folder.mkdir(exist_ok=True)
    (folder/'releases-cleanup-20261030.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('COMPLETE',len(removed),'releases deleted;',len(pages),'remaining',flush=True)


if __name__=='__main__':main()
