import importlib.util
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('srv_test',ROOT/'srv_visibility.py')
srv=importlib.util.module_from_spec(spec);spec.loader.exec_module(srv)


class ServerDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        root=Path(self.temp.name);self.scripts=root/'scripts';self.bins=root/'bin'
        self.scripts.mkdir();self.bins.mkdir()
        self.script=self.scripts/'NewCS_Srv.sh'
        self.script.write_text('#!/bin/sh\nSrvBin="newcs" # installed server\nexit 0\n');self.script.chmod(0o755)
        self.binary=self.bins/'newcs';self.binary.write_text('not executed');self.binary.chmod(0o755)

    def status(self,name='NewCS'):return srv.binary_status(name,self.scripts,self.bins)

    def test_valid_installed_script_and_executable_are_detected_without_execution(self):
        self.assertEqual(self.status(),'Ok')
        self.binary.chmod(0o644);self.assertEqual(self.status(),'Missing BIN')
        self.binary.unlink();self.assertEqual(self.status(),'Missing BIN')

    def test_missing_or_nonexecutable_script_is_not_a_supported_server(self):
        self.script.chmod(0o644);self.assertEqual(self.status(),'Error Reading Script')
        self.script.unlink();self.assertEqual(self.status(),'Error Reading Script')

    def test_unsafe_or_dynamic_binary_names_and_external_script_alias_are_rejected(self):
        for value in ('../../bin/newcs','$(touch /tmp/not-run)','$SERVER','newcs other'):
            self.script.write_text('#!/bin/sh\nSrvBin='+value+'\n')
            self.assertEqual(self.status(),'Undefined BIN')
        self.assertEqual(self.status('../NewCS'),'Error Reading Script')
        outside=self.scripts.parent/'outside.sh';outside.write_text('SrvBin=newcs\n');outside.chmod(0o755)
        self.script.unlink();self.script.symlink_to(outside)
        self.assertEqual(self.status(),'Error Reading Script')


class ServerVisibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.plugin=load(ROOT)

    def screen(self):
        plugin=self.plugin;native=MagicMock();native.available.return_value=['oscam-master'];native.selected.return_value='oscam-master';native.active_name.return_value=None
        with patch.object(plugin,'NativeSoftcam',return_value=native):screen=plugin.univCamMng(types.SimpleNamespace())
        screen.getSrvName=lambda:'None';screen.getCamName=lambda:'None'
        screen.checkSrvBin=lambda name:'Ok';screen.readSrvName=lambda name:'NewCS'
        return screen

    def test_empty_server_list_hides_controls_and_navigation_skips_restart(self):
        plugin=self.plugin;screen=self.screen()
        with patch.object(plugin,'listDir',return_value=[]):screen.CamSrvList()
        self.assertEqual(len(screen.list),1);self.assertEqual(screen.title,'CAM Manager')
        for name in ('activSrv','SrvPic','txt7','srvArrowLeft','srvArrowRight'):self.assertFalse(screen[name].visible)
        self.assertEqual(screen['txt1'].text,'Download CAM')
        self.assertEqual(screen['config']._size.height(),42)
        self.assertEqual(screen['txt8'].position().y(),int(screen.srvLayout['txt7']['position'].split(',')[1]))
        screen.idxAllFnc=6;screen.selectFnc();self.assertEqual(screen.idxAllFnc,8)
        screen.idxAllFnc=7
        with patch.object(screen,'enaSrvRestart') as restart:screen.ActivateselectedFnc();restart.assert_not_called()

    def test_refresh_restores_supported_server_and_hides_it_again_after_removal(self):
        plugin=self.plugin;screen=self.screen()
        with patch.object(plugin,'listDir',return_value=[]):screen.CamSrvList()
        with patch.object(plugin,'listDir',return_value=['NewCS_Srv.sh']):screen.CamSrvList()
        self.assertEqual(screen.numSrv,1);self.assertEqual(len(screen.list),2)
        self.assertEqual(screen.title,'CAM/SRV Manager');self.assertEqual(screen['txt1'].text,'Download CAM/SRV')
        self.assertEqual(screen['config']._size.height(),82)
        self.assertEqual(screen['txt8'].position().y(),int(screen.srvLayout['txt8']['position'].split(',')[1]))
        for name in ('activSrv','SrvPic','txt7','srvArrowLeft','srvArrowRight'):self.assertTrue(screen[name].visible)
        screen.idxAllFnc=6;screen.selectFnc();self.assertEqual(screen.idxAllFnc,7)
        with patch.object(screen,'enaSrvRestart') as restart:screen.ActivateselectedFnc();restart.assert_called_once()
        with patch.object(plugin,'listDir',return_value=[]):screen.CamSrvList()
        self.assertEqual(screen.idxAllFnc,8);self.assertFalse(screen['txt7'].visible)

    def test_broken_server_or_backup_filename_does_not_show_server_controls(self):
        plugin=self.plugin;screen=self.screen();screen.checkSrvBin=lambda name:'Missing BIN'
        with patch.object(plugin,'listDir',return_value=['NewCS_Srv.sh','NewCS_Srv.sh.bak']):screen.CamSrvList()
        self.assertEqual(screen.numSrv,0);self.assertEqual(len(screen.list),1)

    def test_all_original_resolutions_keep_first_row_arrows_and_name_second_row(self):
        for filename in ('GSU_skins.py','GSU_skins_FHD.py','GSU_skins_UHD.py'):
            namespace={};exec(compile((ROOT/filename).read_text(),filename,'exec'),namespace)
            original=ElementTree.fromstring(namespace['UCM']);prepared=ElementTree.fromstring(srv.prepare_skin(namespace['UCM']))
            static=[n for n in prepared if n.tag=='ePixmap' and n.get('pixmap','').endswith(('/left.png','/right.png'))]
            named=[n for n in prepared if n.get('name') in ('srvArrowLeft','srvArrowRight')]
            self.assertEqual(len(static),2);self.assertEqual(len(named),2)
            self.assertEqual(len(original),len(prepared))


if __name__=='__main__':unittest.main()
