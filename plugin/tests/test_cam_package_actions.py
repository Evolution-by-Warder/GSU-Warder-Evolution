import importlib
import pathlib
import types
import unittest
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=pathlib.Path(__file__).resolve().parents[1]/'src/GlassSysUtil'


class CamPackageActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin=load(ROOT)
        cls.actions=importlib.import_module('Plugins.Extensions.GlassSysUtil.cam_package_actions')

    def make_screen(self,package='enigma2-plugin-softcams-oscam-master'):
        class Screen(dict):pass
        screen=Screen();screen.enCommand=True;screen.onClose=[]
        screen.session=types.SimpleNamespace(open=MagicMock(),openWithCallback=MagicMock())
        screen.nativeSoftcam=MagicMock();screen.nativeSoftcam.available.return_value=['oscam-master','oscam-uni']
        screen.nativeSoftcam.package_for.return_value=package
        screen['config']=types.SimpleNamespace(getCurrent=lambda:('CAM',types.SimpleNamespace(getText=lambda:'oscam-master')),getCurrentIndex=lambda:0)
        for key in ('txt3','txt4','statCamSrvcmd'):screen[key]=MagicMock()
        screen.inicializeUCM=MagicMock();screen.updateList=MagicMock();screen.cmd=package
        return screen

    def api(self):
        return {'_':lambda text:text,'oscamRunning':MagicMock(return_value=False),'MessageBox':types.SimpleNamespace(TYPE_YESNO=2,TYPE_ERROR=1,TYPE_INFO=0),'Console':object()}

    def test_registry_refresh_is_async_and_ignores_results_after_window_close(self):
        screen=self.make_screen();pending=MagicMock()
        with patch.object(self.actions,'deferToThread',return_value=pending) as background:
            self.actions.refresh_registry(screen)
        background.assert_called_once_with(screen.nativeSoftcam.read_package_registry)
        done=pending.addCallback.call_args.args[0]
        packages={'enigma2-plugin-softcams-oscam-master'}
        done(packages)
        self.assertEqual(screen.nativeSoftcam.registered_packages,packages)
        for callback in screen.onClose:callback()
        done(set())
        self.assertEqual(screen.nativeSoftcam.registered_packages,packages)

    def test_native_start_editor_accepts_manual_oscam_but_package_update_needs_ownership(self):
        for package in ('enigma2-plugin-softcams-oscam-master',None):
            screen=self.make_screen(package)
            self.assertTrue(self.actions.controls(screen))
            self.assertTrue(screen.enaBlue)
            screen['txt4'].color1.assert_called_once()
            if package:screen['txt3'].color1.assert_called_once()
            else:screen['txt3'].color2.assert_called_once()

    def test_update_requires_confirmation_and_refreshes_before_exact_package_install(self):
        screen=self.make_screen();api=self.api()
        self.assertTrue(self.actions.update(screen,api))
        confirm=screen.session.openWithCallback.call_args.args[0]
        confirm(False);self.assertEqual(screen.session.openWithCallback.call_count,1)
        pending=MagicMock()
        with patch.object(self.actions.shutil,'which',return_value='/usr/bin/opkg'),patch.object(self.actions,'deferToThread',return_value=pending):confirm(True)
        self.assertFalse(screen.enCommand)
        pending.addCallback.call_args.args[0]({'created':False})
        self.assertTrue(screen.enCommand)
        self.assertEqual(screen.session.openWithCallback.call_args.kwargs['cmdlist'],['/usr/bin/opkg update && /usr/bin/opkg install enigma2-plugin-softcams-oscam-master'])

    def test_update_feed_preparation_failure_never_launches_package_install(self):
        screen=self.make_screen();api=self.api()
        self.actions.update(screen,api)
        confirm=screen.session.openWithCallback.call_args.args[0];pending=MagicMock()
        with patch.object(self.actions.shutil,'which',return_value='/usr/bin/opkg'),patch.object(self.actions,'deferToThread',return_value=pending):confirm(True)
        pending.addErrback.call_args.args[0](None)
        self.assertTrue(screen.enCommand)
        self.assertEqual(screen.session.openWithCallback.call_count,1)
        screen.session.open.assert_called_once()

    def test_running_cam_and_manual_binary_cannot_be_updated_as_package(self):
        for package,running in [(None,False),('enigma2-plugin-softcams-oscam-master',True)]:
            screen=self.make_screen(package);api=self.api();api['oscamRunning'].return_value=running
            self.assertTrue(self.actions.update(screen,api))
            screen.session.open.assert_called_once()
            screen.session.openWithCallback.assert_not_called()

    def test_running_native_cam_cannot_be_uninstalled_but_stopped_package_can(self):
        for running in (False,True):
            screen=self.make_screen();api=self.api();cam=MagicMock()
            cam.available.return_value=['oscam-master'];cam.package_for.return_value=None;cam.running.return_value=running
            with patch.object(self.actions,'NativeSoftcam',return_value=cam),patch.object(self.actions.shutil,'which',return_value='/usr/bin/opkg'):
                self.assertTrue(self.actions.remove(screen,api))
            if running:
                screen.session.open.assert_called_once();screen.session.openWithCallback.assert_not_called()
            else:self.assertEqual(screen.session.openWithCallback.call_args.kwargs['cmdlist'],['/usr/bin/opkg remove enigma2-plugin-softcams-oscam-master'])

    def test_uninstall_list_accepts_modern_cam_packages_and_excludes_feed_and_status_tools(self):
        module=self.plugin
        lines=['enigma2-plugin-softcams-oscam-master - 11968-r3','softcam-feed-universal - 4.8-r0','enigma2-plugin-extensions-oscamstatus - 7.50','glasssysutil-srv.oscam - 1.0']
        screen=module.ipk_uninstall_center(types.SimpleNamespace(),what='ucm')
        with patch.object(module,'chckPckgList',return_value=lines):screen.updateList()
        self.assertEqual([row[0] for row in screen.list],[lines[0],lines[3]])

    def test_shared_removal_screen_defaults_to_cam_only_after_general_installer_retirement(self):
        module=self.plugin
        screen=module.ipk_uninstall_center(types.SimpleNamespace())
        lines=['enigma2-plugin-softcams-oscam-master - 11968-r4','enigma2 - 8.0','enigma2-plugin-glasssysutil - 13.40-r38']
        with patch.object(module,'chckPckgList',return_value=lines):screen.updateList()
        self.assertEqual(screen.what,'ucm')
        self.assertEqual([row[0] for row in screen.list],[lines[0]])


if __name__=='__main__':unittest.main()
