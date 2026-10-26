import importlib
from pathlib import Path
import types
import unittest
from unittest.mock import MagicMock,patch
from receiver_stubs import load
ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'

class CamPaneTests(unittest.TestCase):
    def setUp(self):
        self.plugin=load(ROOT);self.session=MagicMock();self.screen=self.plugin.univCamMng(self.session)
        self.panes=self.screen._cam_panes;self.ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_cam_panes')
        self.screen.enCommand=True;self.screen.inicializeUCM=MagicMock()
        self.screen['config'].list=[('CAM',types.SimpleNamespace(value='one',choices=[('one','One'),('two','Two')]))]
    def test_download_opens_in_left_without_session_dialog_and_close_gates_late_results(self):
        self.screen.moreCamSrv()
        self.assertEqual(self.panes.kind,'download');model=self.panes.model
        self.assertIs(model['list'],self.screen['workspace_list'])
        self.assertFalse(self.screen['config'].visible);self.assertTrue(self.screen['workspace_list'].visible)
        self.session.openWithCallback.assert_not_called();self.session.open.assert_not_called()
        self.panes.back();self.assertTrue(model.feedClosed);self.assertFalse(self.panes.active)
        self.screen.inicializeUCM.assert_called_once();self.assertTrue(self.screen['config'].visible)
    def test_remove_catalogue_uses_worker_and_rejects_late_result_after_exit(self):
        pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending) as worker:
            self.screen.lessCamSrv()
        self.assertEqual(self.panes.kind,'remove');worker.assert_called_once_with(self.plugin.chckPckgList)
        self.session.openWithCallback.assert_not_called()
        completed=pending.addCallback.call_args.args[0]
        self.panes.back()
        before=list(self.screen['workspace_list'].list)
        completed(['enigma2-plugin-softcams-test - 1'])
        self.assertEqual(self.screen['workspace_list'].list,before)
    def test_delay_is_in_panel_and_cancel_does_not_save(self):
        self.screen.setNewDelay=MagicMock(name='setNewDelay')
        # Keep a named callback because the legacy entry point uses its name.
        def setNewDelay(value):self.screen.setNewDelay(value)
        self.screen.session.openWithCallback(setNewDelay,self.plugin.InputBox,title='Delay')
        self.assertEqual(len(self.screen['workspace_list'].list),30)
        self.session.openWithCallback.assert_not_called()
        self.panes.back();self.screen.setNewDelay.assert_called_once_with(None)
        self.screen.session.openWithCallback(setNewDelay,self.plugin.InputBox,title='Delay')
        self.panes.close_choice(('15 s','15'));self.screen.setNewDelay.assert_called_with('15')
    def test_native_start_settings_are_embedded_and_cancel_preserves_snapshot(self):
        from Plugins.Extensions.GlassSysUtil.native_start_config_ui import NativeStartConfigScreen
        snapshot={'name':'oscam-test','pidfile':'/tmp/test.pid','values':{'debug':0,'restart':1,'config_dir':'/etc/test'}}
        store=MagicMock()
        model=self.panes.open(NativeStartConfigScreen,(snapshot,store,vars(self.plugin)),self.screen.inicializeUCM)
        self.assertIs(model['config'],self.screen['workspace_config'])
        self.session.open.assert_not_called();self.session.openWithCallback.assert_not_called()
        self.panes.edit()  # config_dir invokes browser; not the settings screen itself.
        self.panes.back();self.assertTrue(model.closed);store.save.assert_not_called()
        self.assertEqual(snapshot['values']['debug'],0)
    def test_nested_choice_restores_unsaved_configuration_without_closing_it(self):
        from Plugins.Extensions.GlassSysUtil.native_start_config_ui import NativeStartConfigScreen
        snapshot={'name':'oscam-test','pidfile':'/tmp/test.pid','values':{'restart':1}}
        model=self.panes.open(NativeStartConfigScreen,(snapshot,MagicMock(),vars(self.plugin)),None)
        self.panes.edit();self.assertIsNotNone(self.panes.choice)
        self.panes.close_choice(('2','2'))
        self.assertIs(self.panes.model,model);self.assertEqual(model.settings['restart'].value,'2')
        self.assertFalse(model.closed);self.assertTrue(self.screen['workspace_config'].visible)
    def test_closing_manager_gates_future_session_open_and_restores_conditional_visibility(self):
        self.screen['activSrv'].hide();self.screen.moreCamSrv();self.panes.back()
        self.assertFalse(self.screen['activSrv'].visible)
        self.panes.shutdown();self.screen.moreCamSrv();self.assertFalse(self.panes.active)

    def test_backend_visibility_refresh_cannot_expose_status_over_active_content(self):
        self.screen.moreCamSrv()
        self.screen['activSrv'].show()
        self.assertFalse(self.screen['activSrv'].visible)
        self.panes.back();self.assertTrue(self.screen['activSrv'].visible)
