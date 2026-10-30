import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/GlassSysUtil'))
sys.path.insert(0,str(ROOT/'tools'))
import plugin_update as update
import build_ipk
import publish_update

spec=importlib.util.spec_from_file_location('gsu_r92_updater',Path(__file__).parent/'fixtures/plugin_update_r92.py')
old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old)


class PackageIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder=tempfile.TemporaryDirectory()
        root=Path(cls.folder.name)
        cls.bridge=build_ipk.build(root/'bridge',bridge=True)
        cls.current=build_ipk.build(root/'current')
        cls.bridge_doc=publish_update.manifest(cls.bridge,'13.40-r93','Compatible transition')
        short=cls.current.with_name('enigma2-plugin-extensions-gsu_13.40-r94_all.ipk')
        cls.current_doc=publish_update.manifest(short,'13.40-r94','Correct plugin group')
        cls.release=update.parse_release(json.dumps(cls.current_doc),'13.40-r93')

    @classmethod
    def tearDownClass(cls):cls.folder.cleanup()

    def test_original_r92_accepts_actual_bridge_bytes_and_rejects_new_identity(self):
        offered=old.parse_release(json.dumps(self.bridge_doc),'13.40-r92')
        old.validate_ipk(self.bridge,offered)
        with self.assertRaises(old.UpdateError):old.parse_release(json.dumps(self.current_doc),'13.40-r92')

    def test_bridge_updater_accepts_new_identity_and_same_native_runtime_directory(self):
        update.validate_ipk(self.current,self.release)
        self.assertEqual(self.release.package_id,'enigma2-plugin-extensions-gsu-warder-evolution')
        self.assertEqual(update.FEED_URL.rsplit('/',1)[-1],'stable.json')
        self.assertEqual(self.current_doc['release']['sha256'],hashlib.sha256(self.current.read_bytes()).hexdigest())

    def install(self,legacy_version,returncode=0):
        data=self.current.read_bytes();calls=[]
        with tempfile.TemporaryDirectory() as folder:
            flag=Path(folder)/'state/rename'
            def runner(command,**kwargs):
                calls.append(command[:2])
                if command[1]=='status':return types.SimpleNamespace(returncode=0,stdout='Package: '+update.LEGACY_PACKAGE_ID+'\nVersion: '+legacy_version+'\nStatus: install ok installed\n')
                self.assertTrue(flag.is_file())
                self.assertEqual(flag.read_text(),'13.40-r94\n')
                return types.SimpleNamespace(returncode=returncode,stdout='opkg result')
            with patch.object(update,'MIGRATION_FLAG',flag):
                if returncode or legacy_version=='13.40-r92':
                    with self.assertRaises(update.UpdateError):update.install_release(self.release,lambda *a,**k:io.BytesIO(data),runner)
                else:self.assertEqual(update.install_release(self.release,lambda *a,**k:io.BytesIO(data),runner),'13.40-r94')
            self.assertFalse(flag.exists())
        return calls

    def test_rename_preserves_cam_settings_during_opkg_and_removes_temporary_marker(self):
        self.assertEqual(self.install('13.40-r93'),[['opkg','status'],['opkg','install']])

    def test_marker_is_removed_when_opkg_reports_failure(self):
        self.install('13.40-r93',1)

    def test_installed_pre_bridge_cannot_be_renamed_directly(self):
        self.assertEqual(self.install('13.40-r92'),[['opkg','status']])
