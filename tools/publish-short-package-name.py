#!/usr/bin/env python3
"""Add a short download name to immutable production bytes; keep update URLs."""
from pathlib import Path
import hashlib
import io
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

ROOT=Path(__file__).resolve().parents[1]


def gh(*args):
    return subprocess.check_output(['gh',*args],text=True)


def verify(data,config):
    assert len(data)==config['bytes']
    assert hashlib.sha256(data).hexdigest()==config['sha256']


def publish():
    config=json.loads((ROOT/'docs/short-package-name-20261030.json').read_text())
    repo=config['repository'];tag=config['tag'];name=config['download_filename']
    assert repo==os.environ['GITHUB_REPOSITORY']
    assert name.endswith('_all.ipk') and '/' not in name
    release=json.loads(gh('api','repos/'+repo+'/releases/tags/'+tag))
    assert not release['draft'] and not release['prerelease']
    assets={item['name']:item for item in release['assets']}
    original=assets[config['previous_filename']]
    assert original['size']==config['bytes']
    assert original['digest']=='sha256:'+config['sha256']
    with tempfile.TemporaryDirectory(prefix='warder-short-package-') as folder:
        folder=Path(folder)
        gh('release','download',tag,'--repo',repo,'--pattern',config['previous_filename'],'--dir',str(folder))
        old=folder/config['previous_filename'];data=old.read_bytes();verify(data,config)
        control_raw=subprocess.check_output(['ar','p',str(old),'control.tar.gz'])
        with tarfile.open(fileobj=io.BytesIO(control_raw),mode='r:gz') as archive:
            member=next(m for m in archive if m.name.lstrip('./')=='control')
            control=archive.extractfile(member).read().decode()
        fields=dict(line.split(': ',1) for line in control.splitlines() if ': ' in line)
        assert fields['Package']==config['package_id']
        assert fields['Version']==config['control_version'] and fields['Architecture']=='all'
        short=folder/name;short.write_bytes(data)
        checksum=short.with_suffix('.ipk.sha256')
        checksum.write_text(config['sha256']+'  '+name+'\n')
        for path in [short,checksum]:
            blob=path.read_bytes();existing=assets.get(path.name)
            if existing:
                assert existing['size']==len(blob)
                assert existing['digest']=='sha256:'+hashlib.sha256(blob).hexdigest()
            else:
                # Never clobber a release asset, even on a retry.
                gh('release','upload',tag,str(path),'--repo',repo)
        url='https://github.com/'+repo+'/releases/download/'+tag+'/'+name
        request=urllib.request.Request(url,headers={'User-Agent':'Warder-package-name-verifier','Cache-Control':'no-cache'})
        with urllib.request.urlopen(request,timeout=60) as response:
            public=response.read(config['bytes']+1)
        verify(public,config)
        if config.get('raw_package_path'):
            target=ROOT/config['raw_package_path'];target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(short,target)
            shutil.copyfile(checksum,target.with_suffix('.ipk.sha256'))
    evidence=dict(config,status='PUBLIC_SHORT_NAME_VERIFIED',public_download_url=url,
                  all_bytes_identical=True,package_identity_preserved=True,
                  previous_assets_retained=True,update_feeds_preserved=True,
                  workflow_run=int(os.environ['GITHUB_RUN_ID']))
    report=ROOT/'reports/short-package-name-20261030.json'
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
    print('VERIFIED',name,config['bytes'],'bytes',config['sha256'])


if __name__=='__main__':publish()
