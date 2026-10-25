import importlib
import importlib.util
import pathlib
import subprocess
import types
import unittest
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=pathlib.Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('cam_feed_under_test',ROOT/'cam_feed.py')
feed=importlib.util.module_from_spec(spec);spec.loader.exec_module(feed)
CATALOGUE='''enigma2-plugin-softcams-oscam-uni - 11968 - OSCam current
oscam-stable - 11966 - OSCam stable
enigma2-plugin-softcams-cccam - 2.3.2 - CCcam
softcam-ncam - 15.0 - NCam
oscam-stable - 11968 - Second candidate
python3-oscam-tools - 1.0 - Exclude unrelated tool
softcam-feed-universal - 1.0 - Exclude feed installer
enigma2-plugin-picons-oscam - 1.0 - Exclude image
malicious;reboot - 1.0 - Exclude shell injection
'''


class CamFeedTests(unittest.TestCase):
    def test_catalogue_filters_names_and_preserves_distinct_versions(self):
        result=feed.parse_catalogue(CATALOGUE)
        self.assertEqual([p['name'] for p in result],['enigma2-plugin-softcams-cccam','enigma2-plugin-softcams-oscam-uni','oscam-stable','softcam-ncam'])
        self.assertEqual(result[2]['versions'],['11966','11968'])
        self.assertFalse(feed.is_cam_package('../../oscam'))
        self.assertTrue(feed.is_cam_package('enigma2-plugin-softcams-camd3'))
        self.assertTrue(feed.is_cam_package('enigma2-plugin-softcams-wicardd'))

    def test_refresh_and_list_use_existing_manager_with_finite_timeouts(self):
        result=types.SimpleNamespace(returncode=0,stdout=CATALOGUE.encode(),stderr=b'')
        with patch.object(feed.shutil,'which',return_value='/usr/bin/opkg'),patch.object(feed.subprocess,'run',return_value=result) as run:
            catalogue=feed.read_catalogue()
        self.assertFalse(catalogue['warning']);self.assertEqual(len(catalogue['packages']),4)
        self.assertEqual([call.args[0] for call in run.call_args_list],[['/usr/bin/opkg','update'],['/usr/bin/opkg','list']])
        self.assertEqual([call.kwargs['timeout'] for call in run.call_args_list],[45,15])

    def test_failed_refresh_keeps_cached_catalogue_and_reports_warning(self):
        result=types.SimpleNamespace(returncode=0,stdout=CATALOGUE.encode(),stderr=b'')
        for failure in (subprocess.TimeoutExpired('opkg',45),types.SimpleNamespace(returncode=1)):
            with self.subTest(failure=failure),patch.object(feed.shutil,'which',return_value='/usr/bin/opkg'),patch.object(feed.subprocess,'run',side_effect=[failure,result]):
                catalogue=feed.read_catalogue()
            self.assertTrue(catalogue['warning']);self.assertEqual(len(catalogue['packages']),4)

    def test_no_manager_or_bad_catalogue_has_clear_failure(self):
        with patch.object(feed.shutil,'which',return_value=None):
            with self.assertRaises(OSError):feed.read_catalogue()
        result=types.SimpleNamespace(returncode=1,stdout=b'',stderr=b'fail')
        with patch.object(feed.shutil,'which',return_value='/usr/bin/opkg'),patch.object(feed.subprocess,'run',return_value=result) as run:
            with self.assertRaises(OSError):feed.read_catalogue(False)
        run.assert_called_once()


class Pending:
    def addCallback(self,cb):self.completed=cb;return self
    def addErrback(self,cb):self.failed=cb;return self


class CamFeedScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin=load(ROOT)
        cls.ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.cam_feed_ui')

    def make_screen(self):
        session=types.SimpleNamespace(open=MagicMock(),openWithCallback=MagicMock())
        return self.plugin.ftp_center(session,None)

    def test_loading_returns_before_result_and_close_ignores_late_callback(self):
        screen=self.make_screen();pending=Pending()
        with patch.object(self.ui,'deferToThread',return_value=pending) as start:
            screen.updatemenulist()
        self.assertEqual(screen.list[0][0],'*')
        self.assertIn('Loading',screen.list[0][1]['text'])
        start.assert_called_once_with(self.ui.read_catalogue,True)
        for callback in screen.onClose:callback()
        pending.completed({'packages':feed.parse_catalogue(CATALOGUE),'warning':False})
        self.assertEqual(screen.feedPackages,{})
        self.assertIn('Loading',screen.list[0][1]['text'])

    def test_catalogue_install_requires_confirmation_and_uses_no_force_flags(self):
        screen=self.make_screen();pending=Pending()
        with patch.object(self.ui,'deferToThread',return_value=pending):screen.updatemenulist()
        pending.completed({'packages':feed.parse_catalogue(CATALOGUE),'warning':True})
        self.assertIn('cached',screen.list[0][1]['text'])
        screen['list'].index=1
        with patch.object(self.plugin,'oscamRunning',return_value=False),patch.object(self.plugin,'MessageBox',types.SimpleNamespace(TYPE_YESNO=2)):
            screen.doSelection()
        confirm=screen.session.openWithCallback.call_args.args[0]
        self.assertEqual(screen.session.openWithCallback.call_count,1)
        confirm(False);self.assertEqual(screen.session.openWithCallback.call_count,1)
        with patch.object(self.ui.shutil,'which',return_value='/usr/bin/opkg'):confirm(True)
        args=screen.session.openWithCallback.call_args.kwargs
        self.assertEqual(args['cmdlist'],['/usr/bin/opkg install enigma2-plugin-softcams-cccam'])
        self.assertNotIn('--force',args['cmdlist'][0])

    def test_empty_and_error_rows_are_not_installable(self):
        for failed in (False,True):
            screen=self.make_screen();pending=Pending()
            with patch.object(self.ui,'deferToThread',return_value=pending):screen.updatemenulist()
            if failed:pending.failed(None)
            else:pending.completed({'packages':[],'warning':False})
            screen.doSelection()
            screen.session.openWithCallback.assert_not_called()
            self.assertEqual(screen.list[0][0],'*')

    def test_installed_oscam_requires_stop_before_package_change(self):
        screen=self.make_screen();pending=Pending()
        with patch.object(self.ui,'deferToThread',return_value=pending):screen.updatemenulist()
        pending.completed({'packages':[{'name':'oscam-stable','versions':['11968'],'description':''}],'warning':False})
        with patch.object(self.plugin,'oscamRunning',return_value=True),patch.object(self.plugin,'MessageBox',types.SimpleNamespace(TYPE_ERROR=1)):
            screen.doSelection()
        screen.session.open.assert_called_once()
        screen.session.openWithCallback.assert_not_called()


if __name__=='__main__':unittest.main()
