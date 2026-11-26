#!/usr/bin/env python3
"""One authorized r6 release. Never modify the two frozen r93 feeds or existing assets."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Evolution-by-Warder/GSU-Warder-Evolution'
VERSION = '13.41-r6'
PREVIOUS = '13.41-r5'
PREVIOUS_SHA = '17de1b2624dd90b77d2c8c05ceba997e683c2d66d888212dda21e31233ef7085'
COMPAT = 'original-python314'
COMPAT_HEAD = None
FEED = 'plugin/update/stable.json'
FROZEN = ('plugin/update/candidate.json', 'restoration/update/candidate.json')
PACKAGE = ROOT / 'plugin/dist/enigma2-plugin-extensions-gsu_13.41-r6_all.ipk'
REPORT = 'reports/gsu-13.41-r6'
TAG = 'v' + VERSION
URL = 'https://github.com/' + REPO + '/releases/download/' + TAG + '/' + PACKAGE.name
LANGUAGES = set('en sk cs de pl hu ru fr it es al el et fa lt nl pt ro tr uk zh'.split())

def run(*args, cwd=ROOT):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()

def git(*args, cwd=ROOT):
    return run('git', *args, cwd=cwd)

def encoded(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(encoded(value), encoding='utf-8')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def public(url, limit):
    with urlopen(Request(url, headers={'Cache-Control':'no-cache', 'User-Agent':'Warder-release-verifier'}), timeout=90) as response:
        return response.read(limit + 1)

def check():
    assert (ROOT/'plugin/src/GlassSysUtil/version').read_text().strip() == VERSION
    assert (ROOT/'plugin/update/release-request').read_text().strip() == VERSION
    notes = read_json(ROOT/'plugin/update/RELEASE-NOTES.i18n.json')
    assert notes['version'] == VERSION and set(notes['notes']) == LANGUAGES
    raw = PACKAGE.read_bytes()
    digest = sha(raw)
    assert PACKAGE.with_suffix('.ipk.sha256').read_text().split() == [digest, PACKAGE.name]
    installed = read_json(ROOT/REPORT/'install.json')
    assert installed['sha256'] == digest and installed['bytes'] == len(raw)
    item = dict(version=VERSION, tag=TAG, url=URL, sha256=digest, bytes=len(raw),
                notes=notes['notes']['sk'], notes_i18n=notes['notes'],
                release_url='https://github.com/'+REPO+'/releases/tag/'+TAG)
    feed = dict(schema=1, product='Glass System Utility Warder Evolution', channel=COMPAT, release=item)
    payload = encoded(feed)
    assert len(payload.encode()) <= 65536
    # Verify the built package against both the candidate and the last published
    # updater source, not merely against the newly written manifest.
    runtime = 'plugin/src/GlassSysUtil/plugin_update.py'
    with tempfile.TemporaryDirectory() as temp:
        old = Path(temp)/'previous.py'
        old.write_text(git('show', 'v'+PREVIOUS+':'+runtime), encoding='utf-8')
        for script in (old, ROOT/runtime):
            updater = runpy.run_path(str(script))
            offered = updater['parse_release'](payload, PREVIOUS)
            assert offered.version == VERSION and offered.sha256 == digest
            updater['validate_ipk'](PACKAGE, offered)
            assert updater['parse_release'](payload, VERSION) is None
    return item, feed, raw, installed

def publish():
    item, feed, raw, install = check()
    assert os.environ['GITHUB_REPOSITORY'] == REPO
    assert os.environ['GITHUB_REF'] == 'refs/heads/main'
    revision = os.environ['GITHUB_SHA']
    git('fetch', 'origin', 'main', COMPAT, '--tags')
    assert git('rev-parse','HEAD') == revision == git('rev-parse','origin/main')
    compat_head = git('rev-parse','origin/'+COMPAT)
    for ref in ('origin/main','origin/'+COMPAT):
        previous = json.loads(git('show', ref+':'+FEED))['release']
        assert previous['version'] == PREVIOUS and previous['sha256'] == PREVIOUS_SHA
        for path in FROZEN:
            assert json.loads(git('show', ref+':'+path))['release']['version'] == '13.40-r93'
    frozen = {ref:{path:git('rev-parse',ref+':'+path) for path in FROZEN}
              for ref in ('origin/main','origin/'+COMPAT)}
    existing = subprocess.run(['gh','release','view',TAG,'--repo',REPO,'--json','isDraft,isPrerelease'],cwd=ROOT,capture_output=True,text=True)
    if existing.returncode != 0:
        assert not git('ls-remote','--tags','origin','refs/tags/'+TAG), 'Existing tag cannot be reused'
        run('gh','release','create',TAG,str(PACKAGE),str(PACKAGE)+'.sha256',
            '--repo',REPO,'--target',revision,'--title','GSU Warder Evolution '+VERSION,
            '--notes-file',str(ROOT/'plugin/update/RELEASE-NOTES.md'),'--latest=false')
    else:
        status = json.loads(existing.stdout)
        assert not status['isDraft'] and not status['isPrerelease'], 'Existing release not normal stable'
    git('fetch','origin','--tags')
    assert git('rev-parse','refs/tags/'+TAG+'^{commit}') == revision
    assert public(URL,len(raw)) == raw, 'Public IPK differs from tested bytes'
    sidecar = public(URL+'.sha256',512)
    assert sidecar == PACKAGE.with_suffix('.ipk.sha256').read_bytes(), 'Public SHA sidecar mismatch'
    validation = dict(version=VERSION,package_source_commit=revision,workflow_run=int(os.environ['GITHUB_RUN_ID']),
                      public_ipk_sha256_verified=True,public_ipk_sidecar_verified=True,
                      bytes=len(raw),sha256=item['sha256'],matrices_passed=True,
                      OpenPLi_refs=['release-9.2','develop'],OpenATV_refs=['8.0','8.0-next','master'],
                      installed_r5_updater_accepts_ipk=True,packaged_install=install,
                      physical_receiver_all_features_verified=False)
    record = read_json(ROOT/'PRODUCTION.json')
    record['previous_release'] = record['release']
    record.update(release=item,source_branch='main',source_commit=revision,package_source_commit=revision,
                  approved_on='2026-11-26',approval='Owner-approved independent GSU numbering migration',
                  validation=validation,status='production-update-active',
                  version_policy='Stable r6 compatibility bridge; frozen r93 identity bridges unchanged. New 0.41.x feed is separate.',
                  documentation_checkpoint=dict(date='2026-11-26',status='web-sync-pending',
                      continuation='Sync official website after release; verify Pages.'))
    record['identity_transition'].update(target_version=VERSION,legacy_feed_frozen=True,
        steps='Update to frozen r93 when offered, restart GUI, then update to '+VERSION)
    record.pop('accepted_candidate',None)
    record.pop('live_updater_activation_commit',None)
    modern_feed = dict(schema=1, product='Glass System Utility Warder Evolution', channel='stable-modern', release=None)
    modern_path = 'plugin/update/stable-modern.json'
    assert not (ROOT/modern_path).exists(), 'Modern feed already exists; do not overwrite'
    put(ROOT/modern_path,modern_feed)
    put(ROOT/FEED,feed)
    put(ROOT/'PRODUCTION.json',record)
    put(ROOT/REPORT/'public-verification.json',validation)
    current='# GSU '+VERSION+'\n\n'+item['notes']+'\n\n[Stiahnuť IPK]('+URL+')\n\nSHA-256: `'+item['sha256']+'`\n\nOverené verejné bajty, inštalačný test a natívne CI; fyzické prijímače neboli testované.\n'
    (ROOT/'docs/CURRENT-RELEASE.md').write_text(current,encoding='utf-8')
    (ROOT/('docs/RELEASE-'+VERSION+'.md')).write_text(current,encoding='utf-8')
    readme=ROOT/'README.md'
    text=readme.read_text()
    start=text.index('## Spoločné ostré vydanie')
    end=text.index('\nPlugin pre Enigma2',start)
    text=text[:start]+'## Spoločné ostré vydanie — 26. november 2026\n\n**GSU '+VERSION+'** pre OpenPLi a OpenATV. [Poznámky k vydaniu](docs/CURRENT-RELEASE.md). [Stiahnuť IPK]('+URL+').\n'+text[end:]
    text=text.replace('**Stabilné vydanie: 13.40-r94.', '**Stabilné vydanie: '+VERSION+'.')
    text=text.replace('enigma2-plugin-extensions-gsu_13.40-r94_all.ipk',PACKAGE.name)
    text=text.replace('r93 → reštart GUI → r94','r93 → reštart GUI → '+VERSION)
    text=text.replace('po reštarte GUI nasleduje r94','po reštarte GUI nasleduje '+VERSION)
    a=text.index('Rozhranie sleduje jazyk prijímača:')
    b=text.index('\n\n',a)
    text=text[:a]+'Rozhranie sleduje jazyk prijímača a podporuje 21 jazykov. Dni, mesiace, aktualizácie a 431 udržiavaných spoločných a doplnkových textov; pôvodné preklady a anglický fallback sú zachované. [Rozsah lokalizácie](plugin/LOCALIZATION.md).'+text[b:]
    readme.write_text(text,encoding='utf-8')
    log=ROOT/'NEXT-RELEASE.md'
    log.write_text('# 2026-11-26 — stable r6 publication\n\nPR #15, source `'+revision+'`, workflow '+str(validation['workflow_run'])+', public IPK SHA-256 `'+item['sha256']+'`, '+str(len(raw))+' bytes. Both native matrices and packaged install gate passed. Feed activation via atomic fast-forward below; website verification remains pending.\n\n---\n\n'+log.read_text(),encoding='utf-8')
    localization=ROOT/'plugin/LOCALIZATION.md'
    localization.write_text(localization.read_text().replace(' (pracovný kandidát r5; stabilná r4 bez zmeny)',''),encoding='utf-8')
    paths=[FEED,modern_path,'PRODUCTION.json',REPORT+'/public-verification.json','docs/CURRENT-RELEASE.md','docs/RELEASE-'+VERSION+'.md','README.md','NEXT-RELEASE.md','plugin/LOCALIZATION.md']
    git('config','user.name','github-actions[bot]')
    git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
    git('add','--',*paths)
    git('diff','--cached','--check')
    git('commit','-m','Activate verified GSU 13.41-r6 stable release [skip ci]')
    main_commit=git('rev-parse','HEAD')
    with tempfile.TemporaryDirectory() as temp:
        mirror=Path(temp)/'compat'
        git('worktree','add','--detach',str(mirror),'origin/'+COMPAT)
        try:
            put(mirror/FEED,feed)
            git('add','--',FEED,cwd=mirror)
            git('diff','--cached','--check',cwd=mirror)
            git('commit','-m','Activate verified GSU 13.41-r6 stable updater [skip ci]',cwd=mirror)
            compat_commit=git('rev-parse','HEAD',cwd=mirror)
            for path in FROZEN:
                assert git('rev-parse',main_commit+':'+path)==frozen['origin/main'][path]
                assert git('rev-parse',compat_commit+':'+path)==frozen['origin/'+COMPAT][path]
            git('fetch','origin','main',COMPAT)
            assert git('rev-parse','origin/main')==revision and git('rev-parse','origin/'+COMPAT)==compat_head
            # No force: both refs advance together or neither advances.
            git('push','--atomic','origin',main_commit+':refs/heads/main',compat_commit+':refs/heads/'+COMPAT)
        finally:
            git('worktree','remove',str(mirror))
    for branch, commit in [('main',main_commit),(COMPAT,compat_commit)]:
        url='https://raw.githubusercontent.com/'+REPO+'/'+branch+'/'+FEED
        for attempt in range(6):
            try:
                if json.loads(public(url+'?revision='+commit,65536))==feed:break
            except (OSError, ValueError):
                pass
            time.sleep(5)
        else:raise RuntimeError('Live feed not verified: '+branch)
    modern_url = 'https://raw.githubusercontent.com/'+REPO+'/main/'+modern_path
    assert json.loads(public(modern_url+'?revision='+main_commit,65536)) == modern_feed
    run('gh','release','edit',TAG,'--repo',REPO,'--latest')
    validation.update(main_activation_commit=main_commit,compatibility_activation_commit=compat_commit,
                      live_feeds_verified=True,frozen_bridge_blobs=frozen)
    put(ROOT/REPORT/'production.json',validation)
    print(encoded(validation))

if __name__ == '__main__':
    if sys.argv[1:] == ['--check-only']:
        check()
        print('Exact r6 package and both updater validators passed')
    else:
        assert not sys.argv[1:]
        publish()
