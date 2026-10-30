#!/usr/bin/env python3
"""CI-only removal of explicitly verified duplicate release filenames."""
import base64
import hashlib
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request,urlopen

ROOT=Path.cwd()

def git_hash(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()

def main():
    cfg=json.loads((ROOT/'docs/short-only-publication-20261030.json').read_text())
    repo=cfg['repository'];assert os.environ['GITHUB_REPOSITORY']==repo
    assert os.environ['GITHUB_REF']=='refs/heads/maintenance/short-only-packages-20261030'
    token=os.environ['GH_TOKEN'];api='https://api.github.com/repos/'+repo
    def request(method,path,data=None):
        req=Request(api+path,data=None if data is None else json.dumps(data).encode(),method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'Warder-short-filenames-maintenance'})
        with urlopen(req,timeout=90) as response:
            body=response.read()
            return json.loads(body) if body else None
    def public(url,maximum):
        assert url.startswith(('https://github.com/'+repo+'/releases/download/','https://raw.githubusercontent.com/'+repo+'/'))
        for attempt in range(3):
            try:
                with urlopen(Request(url,headers={'Cache-Control':'no-cache','User-Agent':'Warder-short-file-verification'}),timeout=60) as response:raw=response.read(maximum+1)
                assert len(raw)<=maximum
                return raw
            except (HTTPError,OSError):
                if attempt==2:raise
                time.sleep(2)
    def tree(head):
        commit=request('GET','/git/commits/'+head)
        data=request('GET','/git/trees/'+commit['tree']['sha']+'?recursive=1');assert not data.get('truncated')
        return commit['tree']['sha'],{x['path']:x for x in data['tree'] if x['type']=='blob'}
    def head(branch):return request('GET','/git/ref/heads/'+quote(branch,safe=''))['object']['sha']
    def advance(branch,old,new):
        assert head(branch)==old,'Branch advanced: '+branch
        request('PATCH','/git/refs/heads/'+quote(branch,safe=''),{'sha':new,'force':False})
    def commit(parent,base_tree,entries,message):
        made=request('POST','/git/trees',{'base_tree':base_tree,'tree':entries})
        return request('POST','/git/commits',{'parents':[parent],'tree':made['sha'],'message':message})['sha']
    # All branch, file, active-feed and byte checks precede every deletion.
    state={}
    for branch,expected in cfg['targets'].items():
        assert head(branch)==expected,'Unexpected branch head: '+branch
        base_tree,files=tree(expected)
        for path,original_sha in cfg['original_files'].items():
            assert files.get(path,{}).get('sha')==original_sha,(branch,path)
        for item in cfg['remove_paths']:
            long,short=item
            assert files[long]['sha']==files[short]['sha'],(branch,long)
            for path in (long+'.sha256',short+'.sha256'):assert path in files
        for path,digest in cfg['protected_files'].items():
            assert files[path]['sha']==digest,(branch,path)
        state[branch]={'head':expected,'tree':base_tree,'files':files}
    for feed in cfg['feeds']:
        raw=public(feed['url'],65536);assert hashlib.sha256(raw).hexdigest()==feed['sha256']
    release_proofs=[];deletions=[]
    for spec in cfg['releases']:
        release=request('GET','/releases/tags/'+spec['tag']);assert not release['draft'] and not release['prerelease']
        assets={a['name']:a for a in release['assets']}
        short=spec['short'];long=spec['long'];digest=spec['sha256'];size=spec['bytes']
        assert assets[short]['size']==size and assets[short]['digest']=='sha256:'+digest
        raw=public(assets[short]['browser_download_url'],size);assert len(raw)==size and hashlib.sha256(raw).hexdigest()==digest
        checksum=public(assets[short+'.sha256']['browser_download_url'],1024).decode().split();assert checksum==[digest,short]
        if long in assets:
            alias=assets[long];assert alias['size']==size and alias['digest']=='sha256:'+digest
            raw=public(alias['browser_download_url'],size);assert len(raw)==size and hashlib.sha256(raw).hexdigest()==digest
            deletions.append(alias)
        if long+'.sha256' in assets:
            alias=assets[long+'.sha256'];assert public(alias['browser_download_url'],1024).decode().split()==[digest,long]
            deletions.append(alias)
        release_proofs.append(dict(spec,short_public_bytes_verified=True))
    entries=[]
    for path in cfg['original_files']:
        assert path.startswith(('tools/','plugin/tools/','plugin/tests/','.github/workflows/','docs/'))
        assert 'Trezor' not in path and 'trezor' not in path
        raw=(ROOT/path).read_bytes()
        obj=request('POST','/git/blobs',{'encoding':'base64','content':base64.b64encode(raw).decode()});assert obj['sha']==git_hash(raw)
        entries.append({'path':path,'mode':next(iter(state.values()))['files'].get(path,{}).get('mode','100644'),'type':'blob','sha':obj['sha']})
    for long,short in cfg['remove_paths']:
        assert long.startswith('packages/enigma2-plugin-skins-fullhdglass-warder-evolution_')
        for path in (long,long+'.sha256'):entries.append({'path':path,'mode':'100644','type':'blob','sha':None})
    for branch,current in state.items():
        sha=commit(current['head'],current['tree'],entries,'Publish only short installation filenames; preserve runtime and migration targets [skip ci]')
        advance(branch,current['head'],sha);current['head']=sha
    # Release deletion is limited to the exact duplicates already byte-verified.
    for asset in deletions:
        request('DELETE','/releases/assets/'+str(asset['id']))
        print('Removed duplicate asset:',asset['name'],flush=True)
    for spec in cfg['releases']:
        release=request('GET','/releases/tags/'+spec['tag']);assets={a['name']:a for a in release['assets']}
        assert spec['long'] not in assets and spec['long']+'.sha256' not in assets
        assert spec['short'] in assets and spec['short']+'.sha256' in assets
        raw=public(assets[spec['short']]['browser_download_url'],spec['bytes']);assert len(raw)==spec['bytes'] and hashlib.sha256(raw).hexdigest()==spec['sha256']
    for feed in cfg['feeds']:
        assert hashlib.sha256(public(feed['url'],65536)).hexdigest()==feed['sha256']
    evidence={'status':'PRODUCTION_VERIFIED','repository':repo,'source_commit':os.environ['GITHUB_SHA'],'workflow_run':int(os.environ['GITHUB_RUN_ID']),'releases':release_proofs,'removed_release_assets':[x['name'] for x in deletions],'removed_repository_paths':[p+s for p,_ in cfg['remove_paths'] for s in ('','.sha256')],'active_feeds_unchanged':True,'runtime_unchanged':True,'internal_package_identity_unchanged':True,'new_ipk_required':False,'trezor_accessed':False}
    report='reports/short-only-publication-20261030.json';raw=(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n').encode()
    obj=request('POST','/git/blobs',{'encoding':'base64','content':base64.b64encode(raw).decode()})
    report_entry={'path':report,'mode':'100644','type':'blob','sha':obj['sha']}
    for branch,current in state.items():
        current_tree,files=tree(current['head'])
        for path,digest in cfg['protected_files'].items():assert files[path]['sha']==digest
        sha=commit(current['head'],current_tree,[report_entry],'Record verified short-only releases and unchanged updater targets [skip ci]')
        advance(branch,current['head'],sha)
        print('Verified branch:',branch,sha,flush=True)
    (ROOT/'reports').mkdir(exist_ok=True);(ROOT/report).write_bytes(raw)
    print(json.dumps(evidence,indent=2),flush=True)

if __name__=='__main__':main()
