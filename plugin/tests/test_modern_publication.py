"""Exercise immutable release and preactivation guards without contacting a host."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('gsu_publisher',ROOT/'compatibility/publish-modern.py')
publisher=importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)


class ModernPublicationTests(unittest.TestCase):
    def test_opkg_allocation_counts_package_files_only_once(self):
        import runpy
        allocation=runpy.run_path(str(ROOT/'compatibility/verify-modern-migration.py'))['allocated_bytes']
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'usr').mkdir()
            payload=root/'usr/file'
            payload.write_bytes(b'x'*4001)
            os.link(payload,root/'usr/link')
            (root/'etc').mkdir()
            listing='Package example installed in root has the following files:\n/usr/file\n'+str(root/'usr/link')+'\n/etc\n'
            self.assertEqual(allocation(root,listing),payload.stat().st_blocks*512)

    def test_existing_tag_cannot_be_retargeted(self):
        with patch.object(publisher,'command',side_effect=['',publisher.TAG,'different']) as run:
            with self.assertRaisesRegex(ValueError,'immutable tag'):
                publisher.stable_assets(Path('.'),'intended')
        self.assertFalse(any('push' in call.args for call in run.call_args_list))

    def test_existing_public_asset_cannot_be_replaced(self):
        with patch.object(publisher,'command',side_effect=['',publisher.TAG,'intended',json.dumps({'isDraft':False,'isPrerelease':False,'assets':[]})]) as run, patch.object(publisher.subprocess,'run') as lookup:
            lookup.return_value.returncode=0
            with self.assertRaisesRegex(ValueError,'immutable'):
                publisher.stable_assets(Path('.'),'intended')
        self.assertFalse(any('upload' in call.args for call in run.call_args_list))

    def test_rejects_changed_main_and_nonproduction_branch_before_writing(self):
        feed={'release':{}}
        with patch.dict(publisher.os.environ,{'GITHUB_REF':'refs/heads/not-main','GITHUB_REPOSITORY':publisher.REPO}), patch.object(publisher,'stable_assets') as asset:
            with self.assertRaisesRegex(ValueError,'context'):
                publisher.publish(Path('.'),feed,{})
            asset.assert_not_called()
        with patch.dict(publisher.os.environ,{'GITHUB_REF':'refs/heads/main','GITHUB_REPOSITORY':publisher.REPO,'GITHUB_SHA':'expected'}), patch.object(publisher,'historic_feeds'), patch.object(publisher,'command',side_effect=['expected','{"release":null}','new-head']), patch.object(publisher,'stable_assets') as asset:
            with self.assertRaisesRegex(ValueError,'main advanced'):
                publisher.publish(Path('.'),feed,{})
            asset.assert_not_called()

    def test_local_sidecar_mismatch_stops_before_creating_release(self):
        with tempfile.TemporaryDirectory() as tmp:
            package=Path(tmp)/publisher.FILENAME
            package.write_bytes(b'different')
            package.with_suffix('.ipk.sha256').write_text('0'*64+' '+package.name)
            with self.assertRaisesRegex(ValueError,'sidecar'):
                publisher.check(package.parent)
