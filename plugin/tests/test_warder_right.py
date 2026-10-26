import importlib
from pathlib import Path
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree as ET
from receiver_stubs import load
ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'

class RightWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.plugin=load(ROOT);self.session=MagicMock();self.screen=self.plugin.SysUtilMngMain(self.session)
        self.view=self.screen._rightpane
        self.pig=type('Pig',(),{})();self.pig.instance=MagicMock();self.pig.onHide=MagicMock();self.pig.onShow=MagicMock()
        self.screen.renderer=[self.pig]
    def test_idle_keeps_opaque_backings_and_live_preview_below_no_opaque_video_overlay(self):
        root=ET.fromstring(self.screen.skin)
        self.assertEqual(root.get('backgroundColor'),self.view.api['_warder_right'].CLEAR)
        for side in ('left','right'):
            node=root.find("widget[@name='right_opaque_%s']"%side)
            self.assertLess(int(node.get('zPosition')),int(root.find("widget[@render='Pig']").get('zPosition')))
        self.assertTrue(all(w.visible for w in self.view.backings))
        self.assertTrue(all(not w.visible for w in self.view.widgets))
    def test_tools_is_embedded_and_back_restores_preview_without_retuning(self):
        self.view.enter('tools')
        self.assertEqual(self.view.model.entries[0][0],'bundle')
        self.session.open.assert_not_called();self.assertTrue(self.screen['right_list'].visible)
        self.assertTrue(all(not w.visible for w in self.view.backings))
        self.view.back();self.assertFalse(self.view.active);self.pig.onShow.assert_called_once()
        self.session.nav.stopService.assert_not_called();self.session.nav.playService.assert_not_called()
    def test_diagnostic_runs_in_same_panel_and_return_restores_tools(self):
        ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_tools_ui')
        request=MagicMock()
        with patch.object(ui,'deferToThread',return_value=request):
            self.view.enter('tools');self.view.choose()
        self.assertEqual(self.view.kind,'diagnostic');model=self.view.model
        self.session.open.assert_not_called();self.session.openWithCallback.assert_not_called()
        model.done({'path':'/tmp/gsu-test.tar.gz','bytes':1024})
        self.assertIn('/tmp/gsu-test.tar.gz',self.screen['right_scroll'].getText())
        self.view.back();self.assertTrue(model.closed);self.assertEqual(self.view.kind,'tools')
    def test_swap_create_keeps_original_store_and_busy_exit_guard(self):
        swap=importlib.import_module('Plugins.Extensions.GlassSysUtil.swap_ui')
        with patch.object(swap,'swaps',return_value=[]),patch.object(swap,'deferToThread',return_value=MagicMock()):
            self.view.enter('swap');self.view.green()
        self.assertEqual(self.view.kind,'create');self.assertTrue(self.screen['right_config'].visible)
        self.assertTrue(self.view.model._swap_busy)
        self.view.back();self.assertEqual(self.view.kind,'create')
        self.view.model._swap_busy=False;self.view.back();self.assertEqual(self.view.kind,'swap')
        self.session.open.assert_not_called();self.session.openWithCallback.assert_not_called()
    def test_ecm_uses_same_glass_and_restores_idle_backing(self):
        ecm=self.screen._inline_ecm
        with patch.object(ecm.model,'startSearchInfo'):ecm.show()
        self.assertTrue(all(not w.visible for w in self.view.backings+self.view.decorations))
        ecm.hide();self.assertTrue(all(w.visible for w in self.view.backings+self.view.decorations))
    def test_focus_moves_only_active_panel_and_suspend_closes_callbacks(self):
        self.view.enter('tools');self.view.left();self.assertFalse(self.view.focus_right)
        self.view.right();self.assertTrue(self.view.focus_right)
        self.view.suspend();self.assertFalse(self.view.active);self.pig.onShow.assert_not_called()
        self.assertTrue(all(w.visible for w in self.view.backings))
    def test_right_widgets_are_bounded_at_all_resolutions(self):
        ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_right')
        for width,height in ((1280,720),(1920,1080),(3840,2160)):
            xml,_=ui.prepare(ui.main.main_skin(width,height),width,height);root=ET.fromstring(xml)
            for name in ('title','text','list','config','scroll'):
                node=root.find("widget[@name='right_%s']"%name)
                x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
                self.assertGreaterEqual(x,round(1137*width/1920));self.assertLessEqual(x+w,round(1863*width/1920))
                self.assertGreaterEqual(y,round(182*height/1080));self.assertLessEqual(y+h,round(978*height/1080))
    def test_osd_menu_is_embedded_toggles_fields_and_cancel_stops_timer(self):
        cfg=self.plugin.config.plugins.GlassSysUtil;cfg.par0.value=False
        self.view.enter('osd');model=self.view.model;timer=model.chckTimer
        self.assertIs(model['config'],self.screen['right_config'])
        self.session.open.assert_not_called();self.session.openWithCallback.assert_not_called()
        with patch.object(model,'changeShow'):
            self.view.choose();self.assertTrue(cfg.par0.value);self.assertGreater(len(model.list),1)
            with patch.object(cfg.par0,'cancel') as cancel:self.view.back();cancel.assert_called_once()
        self.assertFalse(self.view.active);self.assertIsNone(model.chckTimer)
    def test_osd_save_uses_original_save_and_does_not_cancel_saved_values(self):
        cfg=self.plugin.config.plugins.GlassSysUtil;cfg.par0.value=False
        self.view.enter('osd');model=self.view.model
        with patch.object(cfg.par0,'save') as save,patch.object(cfg.par0,'cancel') as cancel:
            self.view.green();save.assert_called_once();cancel.assert_not_called()
        self.assertFalse(self.view.active);self.assertIsNone(model.chckTimer)
    def test_modal_editor_keeps_workspace_until_callback_and_restores_full_video_under_it(self):
        self.view.enter('tools');model=self.view.model
        ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_right')
        callback=MagicMock()
        ui.Session(self.view).openWithCallback(callback,self.plugin.ChoiceBox,title='Edit',list=[])
        self.view.suspend();self.assertIs(self.view.model,model)
        done=self.session.openWithCallback.call_args.args[0];done(None)
        self.assertEqual(self.view.modal,0);callback.assert_called_once_with(None)
        self.assertIs(self.view.model,model);self.pig.instance.hide.assert_called()
