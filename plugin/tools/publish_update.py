"""CI only: publish the verified stable IPK, then advance compatible update feeds."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src/GlassSysUtil'))
from plugin_update import PACKAGE_ID, REPOSITORY, parse_release, validate_ipk


def run(*args):
    return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).stdout


def manifest(path,version,notes):
    return {'schema':1,'product':'Glass System Utility Warder Evolution','channel':'original-python314',
            'release':{'version':version,'tag':'v'+version,'url':'https://github.com/'+REPOSITORY+'/releases/download/v'+version+'/'+path.name,
                       'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'notes':notes}}


def publish():
    if os.environ.get('GITHUB_REF')!='refs/heads/original-python314':
        raise RuntimeError('Only the restoration branch can publish this feed')
    version=(BASE/'src/GlassSysUtil/version').read_text().strip()
    if (BASE/'update/release-request').read_text().strip()!=version:
        raise RuntimeError('Explicit release request does not match runtime version')
    path=BASE/'dist'/('%s_%s_all.ipk' % (PACKAGE_ID,version))
    notes=(BASE/'update/RELEASE-NOTES.md').read_text()
    document=manifest(path,version,notes)
    release=parse_release(json.dumps(document),'0.0-r0')
    validate_ipk(path,release)
    # Existing immutable releases may be retried, but must match byte for byte.
    releases=json.loads(run('gh','api','repos/'+REPOSITORY+'/releases','--paginate','--slurp'))
    tag='v'+version
    existing=next((item for page in releases for item in page if item['tag_name']==tag),None)
    if existing is None:
        run('gh','release','create',tag,str(path),str(path)+'.sha256','--repo',REPOSITORY,'--target',os.environ['GITHUB_SHA'],
            '--latest','--title','GSU Warder Evolution '+version,'--notes-file',str(BASE/'update/RELEASE-NOTES.md'))
    elif existing.get('draft'):
        raise RuntimeError('Stable release must be public')
    with tempfile.TemporaryDirectory(prefix='gsu-published-') as folder:
        run('gh','release','download',tag,'--repo',REPOSITORY,'--pattern',path.name,'--dir',folder)
        published=Path(folder)/path.name
        if published.read_bytes()!=path.read_bytes():
            raise RuntimeError('Published IPK differs from the tested build; feed unchanged')
    if existing is not None and existing.get('prerelease'):
        run('gh','release','edit',tag,'--repo',REPOSITORY,'--prerelease=false','--latest')
    feed=BASE/'update/candidate.json'
    payload=json.dumps(document,ensure_ascii=False,indent=2)+'\n'
    compatibility=BASE.parent/'restoration/update/candidate.json'
    feeds={feed:payload}
    if compatibility.is_file():
        # Installed r49 and older validate the historical repository URL exactly.
        # GitHub redirects its download endpoint to the renamed repository.
        legacy=copy.deepcopy(document)
        legacy['release']['url']=legacy['release']['url'].replace(
            REPOSITORY,'Evolution-by-Warder/Glass-System-Utility-Warder-Evolution',1)
        feeds[compatibility]=json.dumps(legacy,ensure_ascii=False,indent=2)+'\n'
    if all(item.read_text()==text for item,text in feeds.items()):return
    for item,text in feeds.items():item.write_text(text)
    run('git','add',*(str(item) for item in feeds))
    run('git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com',
        'commit','-m','Advance original-runtime update feed to '+version)
    # Never force a ref that moved while tests/build were running.
    run('git','push','origin','HEAD:original-python314')


if __name__=='__main__':publish()
