"""Execute an explicit release-ID cleanup request after protecting both live feeds."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src/GlassSysUtil'))
from plugin_update import REPOSITORY, PACKAGE_ID, parse_release, validate_ipk


def run(*args):
    return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).stdout


def plan(request,canonical,compatibility,releases):
    release=parse_release(json.dumps(canonical),'0.0-r0')
    if release is None:raise ValueError('The live feed has no release')
    keep='v'+release.version
    if request.get('schema')!=1 or request.get('repository')!=REPOSITORY or request.get('keep')!=keep:
        raise ValueError('Cleanup request does not match the live repository/release')
    for field in ('version','tag','sha256','bytes'):
        if compatibility.get('release',{}).get(field)!=canonical['release'].get(field):
            raise ValueError('Live feeds disagree; no releases may be removed')
    keeper=next((r for r in releases if r['tag_name']==keep),None)
    if keeper is None or keeper.get('draft'):raise ValueError('The protected release is not public')
    required=PACKAGE_ID+'_'+release.version+'_all.ipk'
    if not any(a['name']==required and a['size']==release.bytes for a in keeper.get('assets',[])):
        raise ValueError('The protected release lacks the expected IPK')
    entries=request.get('delete')
    if not isinstance(entries,list) or len(entries)>100:raise ValueError('Invalid explicit cleanup list')
    ids=set();tags=set();selected=[]
    current={r['id']:r for r in releases}
    for item in entries:
        ident,tag=item.get('id'),item.get('tag')
        if type(ident) is not int or ident<=0 or ident in ids or not isinstance(tag,str) or tag in tags:
            raise ValueError('Invalid or duplicate release identity')
        ids.add(ident);tags.add(tag)
        match=re.fullmatch(r'v(\d+)\.(\d+)-(?:r|w)(\d+)',tag)
        if tag==keep or ident==keeper['id'] or not match:
            raise ValueError('Protected or unknown release in cleanup list')
        if tuple(map(int,match.groups()))>=tuple(map(int,re.fullmatch(r'(\d+)\.(\d+)-r(\d+)',release.version).groups())):
            raise ValueError('Cleanup cannot target the current or newer version')
        if ident in current:
            if current[ident]['tag_name']!=tag:raise ValueError('Remote release identity changed')
            selected.append(current[ident])
    return release,selected


def cleanup(request_path):
    if os.environ.get('GITHUB_REF')!='refs/heads/original-python314':
        raise RuntimeError('Cleanup is restricted to the active publishing branch')
    request=json.loads(Path(request_path).read_text())
    canonical=json.loads((BASE/'update/candidate.json').read_text())
    compatibility=json.loads((BASE.parent/'restoration/update/candidate.json').read_text())
    pages=json.loads(run('gh','api','repos/'+REPOSITORY+'/releases','--paginate','--slurp'))
    release,selected=plan(request,canonical,compatibility,[r for page in pages for r in page])
    filename=PACKAGE_ID+'_'+release.version+'_all.ipk'
    with tempfile.TemporaryDirectory(prefix='gsu-retained-release-') as folder:
        run('gh','release','download','v'+release.version,'--repo',REPOSITORY,'--pattern',filename,'--dir',folder)
        path=Path(folder)/filename
        if path.stat().st_size!=release.bytes or hashlib.sha256(path.read_bytes()).hexdigest()!=release.sha256:
            raise ValueError('Retained IPK does not match live feeds; cleanup aborted')
        validate_ipk(path,release)
    for item in selected:
        run('gh','api','--method','DELETE','repos/'+REPOSITORY+'/releases/'+str(item['id']))
        print('Removed release '+item['tag_name'])
    print('Retained v'+release.version+'; removed '+str(len(selected))+' explicitly selected releases; Git tags unchanged.')
    return len(selected)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--request',required=True)
    cleanup(parser.parse_args().request)
