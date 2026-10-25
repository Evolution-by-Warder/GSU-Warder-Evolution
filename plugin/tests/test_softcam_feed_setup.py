import importlib.util
import pathlib
import tempfile
import unittest
from unittest.mock import patch

ROOT=pathlib.Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('softcam_feed_setup_under_test',ROOT/'softcam_feed_setup.py')
setup=importlib.util.module_from_spec(spec);spec.loader.exec_module(setup)


class SoftcamFeedSetupTests(unittest.TestCase):
    def setUp(self):
        self.verifier=patch.object(setup,'verify_feed')
        self.verify=self.verifier.start();self.addCleanup(self.verifier.stop)

    def test_derive_address_from_each_receivers_metadata(self):
        cases=[('6.0','cortexa15hf-neon-vfpv4','cortexa15hf-neon-vfpv4'),('5.4','aarch64','aarch64'),('4.4','mips32el','mips32el'),('5.3','cortexa7hf','cortexa7hf-vfp'),('4.3','sh4','sh4')]
        for version,arch,expected in cases:
            with self.subTest(version=version,arch=arch):
                actual=setup.feed_parameters({'distro':'openatv','oe':'OE-Alliance '+version,'architecture':arch})
                self.assertEqual(actual,(expected,version,'http://updates.mynonpublic.com/oea/'+version+'/'+expected))

    def test_unknown_metadata_never_guesses_arm_or_accepts_path_injection(self):
        good={'distro':'openatv','oe':'OE-Alliance 6.0','architecture':'aarch64'}
        for change in ({'distro':'otherimage'},{'oe':'unknown'},{'oe':'../../6.0'},{'oe':'OE-Alliance 3.0'},{'architecture':'unknown'},{'architecture':'arm'},{'architecture':'../../aarch64'}):
            with self.subTest(change=change),self.assertRaises(OSError):setup.feed_parameters(good|change)

    def test_clean_image_gets_only_one_feed_configuration_and_second_run_preserves_it(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);conf=root/'opkg';conf.mkdir()
            metadata=root/'enigma.info';metadata.write_text("architecture='cortexa15hf-neon-vfpv4'\ndistro='openatv'\noe='OE-Alliance 6.0'\n")
            result=setup.ensure_softcam_feed(conf,metadata)
            target=conf/'cortexa15hf-neon-vfpv4-3rdparty-secret-feed.conf'
            self.assertTrue(result['created'])
            self.assertEqual(target.read_text(),'src/gz cortexa15hf-neon-vfpv4-3rdparty-secret-feed http://updates.mynonpublic.com/oea/6.0/cortexa15hf-neon-vfpv4\n')
            before=target.stat().st_mtime_ns
            self.assertFalse(setup.ensure_softcam_feed(conf,metadata)['created'])
            self.assertEqual(target.stat().st_mtime_ns,before)
            self.assertEqual(sorted(p.name for p in conf.iterdir()),[target.name])

    def test_existing_custom_softcam_feed_is_preserved_without_reading_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);existing=root/'custom.conf'
            content='src/gz my-softcam-feed https://example.invalid/cams\n';existing.write_text(content)
            self.assertFalse(setup.ensure_softcam_feed(root,root/'absent')['created'])
            self.assertEqual(existing.read_text(),content)

    def test_unrelated_config_and_cam_files_are_not_removed(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp);conf=root/'opkg';conf.mkdir()
            unrelated=conf/'base.conf';unrelated.write_text('src/gz base https://example.invalid/base\n')
            cam=root/'custom.emu';cam.write_text('keep me')
            metadata=root/'enigma.info';metadata.write_text("distro='openatv'\noe='OE-Alliance 6.0'\narchitecture='aarch64'\n")
            setup.ensure_softcam_feed(conf,metadata)
            self.assertEqual(cam.read_text(),'keep me')
            self.assertEqual(unrelated.read_text(),'src/gz base https://example.invalid/base\n')

    def test_missing_metadata_leaves_no_partial_feed(self):
        with tempfile.TemporaryDirectory() as temp:
            root=pathlib.Path(temp)
            with self.assertRaises(OSError):setup.ensure_softcam_feed(root,root/'absent')
            self.assertEqual(list(root.iterdir()),[])

    def old_feed(self,root):
        conf=root/'opkg';conf.mkdir()
        target=conf/'cortexa15hf-neon-vfpv4-3rdparty-secret-feed.conf'
        target.write_text('# keep comment\nsrc/gz cortexa15hf-neon-vfpv4-3rdparty-secret-feed http://updates.mynonpublic.com/oea/5.6/cortexa15hf-neon-vfpv4\n')
        metadata=root/'enigma.info'
        metadata.write_text("distro='openatv'\noe='OE-Alliance 6.0'\narchitecture='cortexa15hf-neon-vfpv4'\n")
        return conf,target,metadata

    def test_old_known_feed_migrates_to_current_image_with_backup_and_refresh_marker(self):
        with tempfile.TemporaryDirectory() as temp:
            conf,target,metadata=self.old_feed(pathlib.Path(temp));original=target.read_text()
            result=setup.ensure_softcam_feed(conf,metadata)
            self.assertTrue(result['updated']);self.assertTrue(result['requires_refresh'])
            self.assertIn('/oea/6.0/cortexa15hf-neon-vfpv4',target.read_text())
            self.assertTrue(target.read_text().startswith('# keep comment\n'))
            self.assertEqual(pathlib.Path(str(target)+'.warder-backup').read_text(),original)
            again=setup.ensure_softcam_feed(conf,metadata)
            self.assertFalse(again['updated']);self.assertTrue(again['requires_refresh'])
            setup.finish_refresh(again)
            self.assertFalse(setup.ensure_softcam_feed(conf,metadata)['requires_refresh'])
            self.verify.assert_called_once()

    def test_unavailable_new_feed_preserves_old_configuration_without_sidecars(self):
        with tempfile.TemporaryDirectory() as temp:
            conf,target,metadata=self.old_feed(pathlib.Path(temp));original=target.read_text()
            self.verify.side_effect=OSError('unreachable')
            with self.assertRaises(OSError):setup.ensure_softcam_feed(conf,metadata)
            self.assertEqual(target.read_text(),original)
            self.assertEqual(list(conf.iterdir()),[target])

    def test_validation_requires_matching_architecture_in_real_gzip_metadata(self):
        import gzip,io
        self.verifier.stop()
        data=gzip.compress(b'Package: enigma2-plugin-softcams-oscam-master\nArchitecture: aarch64\n\n')
        with patch.object(setup.urllib.request,'urlopen',return_value=io.BytesIO(data)):
            setup.verify_feed('https://example.invalid/6.0/aarch64','aarch64')
        with patch.object(setup.urllib.request,'urlopen',return_value=io.BytesIO(data)):
            with self.assertRaises(OSError):setup.verify_feed('https://example.invalid/6.0/mips32el','mips32el')


if __name__=='__main__':unittest.main()
