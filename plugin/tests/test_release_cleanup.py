import copy
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'tools'))
import cleanup_releases as cleanup
from build_ipk import archive


def package():
    control=archive([('control',('Package: '+cleanup.PACKAGE_ID+'\nVersion: 13.40-r52\nArchitecture: all\n').encode(),0o644)])
    raw=b'!<arch>\n'
    for name,data in [('debian-binary',b'2.0\n'),('control.tar.gz',control)]:
        raw+=('%-16s%-12s%-6s%-6s%-8s%-10s`\n'%(name+'/',0,0,0,'100644',len(data))).encode()+data
        if len(data)%2:raw+=b'\n'
    return raw


class ReleaseCleanupTests(unittest.TestCase):
    def setUp(self):
        self.data=package();self.filename=cleanup.PACKAGE_ID+'_13.40-r52_all.ipk'
        self.feed={'schema':1,'product':'Glass System Utility Warder Evolution','channel':'original-python314',
                   'release':{'version':'13.40-r52','tag':'v13.40-r52','url':'https://github.com/'+cleanup.REPOSITORY+'/releases/download/v13.40-r52/'+self.filename,'bytes':len(self.data),'sha256':hashlib.sha256(self.data).hexdigest()}}
        self.request={'schema':1,'repository':cleanup.REPOSITORY,'keep':'v13.40-r52','delete':[{'id':10,'tag':'v13.40-r51'}]}
        self.releases=[{'id':11,'tag_name':'v13.40-r52','draft':False,'assets':[{'name':self.filename,'size':len(self.data)}]},
                       {'id':10,'tag_name':'v13.40-r51'}, {'id':9,'tag_name':'v13.40-r50'}]

    def test_only_explicit_old_release_ids_are_selected_and_missing_ids_are_idempotent(self):
        release,selected=cleanup.plan(self.request,self.feed,self.feed,self.releases)
        self.assertEqual([r['id'] for r in selected],[10])
        self.assertEqual(cleanup.plan(self.request,self.feed,self.feed,self.releases[:1])[1],[])

    def test_current_newer_duplicate_and_changed_identities_are_rejected(self):
        for entries in ([{'id':11,'tag':'v13.40-r52'}],[{'id':12,'tag':'v13.40-r53'}],
                        [{'id':10,'tag':'v13.40-r51'}]*2,[{'id':10,'tag':'v13.40-r50'}]):
            request=copy.deepcopy(self.request);request['delete']=entries
            with self.subTest(entries=entries),self.assertRaises(ValueError):cleanup.plan(request,self.feed,self.feed,self.releases)

    def test_disagreeing_feeds_or_missing_current_asset_block_cleanup(self):
        legacy=copy.deepcopy(self.feed);legacy['release']['version']='13.40-r51'
        with self.assertRaises(ValueError):cleanup.plan(self.request,self.feed,legacy,self.releases)
        releases=copy.deepcopy(self.releases);releases[0]['assets']=[]
        with self.assertRaises(ValueError):cleanup.plan(self.request,self.feed,self.feed,releases)

    def test_actual_retained_package_is_verified_before_any_delete(self):
        for valid in (False,True):
            with self.subTest(valid=valid),tempfile.TemporaryDirectory() as folder:
                root=Path(folder)/'plugin';(root/'update').mkdir(parents=True)
                legacy=Path(folder)/'restoration/update';legacy.mkdir(parents=True)
                for p in (root/'update/candidate.json',legacy/'candidate.json'):p.write_text(json.dumps(self.feed))
                request=Path(folder)/'request.json';request.write_text(json.dumps(self.request));calls=[]
                def run(*args):
                    calls.append(args)
                    if args[:2]==('gh','api') and '--method' not in args:return json.dumps([self.releases])
                    if args[:3]==('gh','release','download'):(Path(args[-1])/self.filename).write_bytes(self.data if valid else b'bad')
                    return ''
                with patch.object(cleanup,'BASE',root),patch.object(cleanup,'run',side_effect=run),patch.dict(os.environ,GITHUB_REF='refs/heads/original-python314'):
                    if valid:self.assertEqual(cleanup.cleanup(request),1)
                    else:
                        with self.assertRaises(ValueError):cleanup.cleanup(request)
                deletes=[c for c in calls if 'DELETE' in c]
                self.assertEqual(deletes,[('gh','api','--method','DELETE','repos/'+cleanup.REPOSITORY+'/releases/10')] if valid else [])

    def test_protected_asset_name_comes_from_validated_feed_including_short_filename(self):
        short='enigma2-plugin-extensions-gsu_13.40-r52_all.ipk'
        feed=copy.deepcopy(self.feed);feed['release']['url']=feed['release']['url'].rsplit('/',1)[0]+'/'+short
        releases=copy.deepcopy(self.releases);releases[0]['assets'][0]['name']=short
        release,selected=cleanup.plan(self.request,feed,feed,releases)
        self.assertEqual(release.url.rsplit('/',1)[-1],short)
        self.assertEqual([r['id'] for r in selected],[10])

    def test_other_branches_cannot_delete_releases(self):
        with patch.dict(os.environ,GITHUB_REF='refs/heads/main'),patch.object(cleanup,'run') as run:
            with self.assertRaises(RuntimeError):cleanup.cleanup('unused')
            run.assert_not_called()
