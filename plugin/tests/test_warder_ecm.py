import importlib
from pathlib import Path
import types
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree as ET
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
class InlineECMTests(unittest.TestCase):
    def setUp(self):
        self.plugin=load(ROOT);self.ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_ecm')
        self.session=MagicMock();self.screen=self.plugin.SysUtilMngMain(self.session);self.view=self.screen._inline_ecm
        self.pig=type('Pig',(),{})();self.pig.instance=MagicMock();self.pig.onHide=MagicMock();self.pig.onShow=MagicMock()
        self.screen.renderer=[self.pig]
        for widget in self.view.widgets:widget.instance=MagicMock()
    def test_widgets_start_hidden_and_original_backend_and_menu_owning_screen_are_preserved(self):
        self.assertTrue(all(not widget.visible for widget in self.view.widgets))
        self.assertIsInstance(self.view.model,self.plugin.ECMInfo)
        self.assertNotIn(self.view.model['actions'],list(self.screen.values()))
        self.assertIs(self.screen['inline_ecm_values'],self.view.model['ecmValues'])
        self.assertIs(self.screen['inline_ecm_labels'],self.view.model['ecmlabels'])
        self.assertIs(self.screen['inline_ecm_picon'],self.view.model['piccode'])
        self.session.open.assert_not_called()
    def test_ecm_menu_selection_uses_right_panel_without_session_dialog(self):
        self.screen.status={'6':True};self.screen['list'].l.setList([['6']])
        with patch.object(self.view.model,'startSearchInfo') as start:self.screen.selectedmenuitem()
        start.assert_called_once();self.assertTrue(self.view.active)
        self.session.open.assert_not_called()
        self.pig.onHide.assert_called_once();self.pig.instance.hide.assert_called_once()
        self.assertFalse(self.screen['selection'].visible);self.assertFalse(self.screen['info'].visible)
        self.assertTrue(all(w.visible for w in self.view.widgets))
    def test_first_back_restores_live_video_second_back_exits_main(self):
        self.view.original_back=MagicMock()
        with patch.object(self.view.model,'startSearchInfo'):self.view.show()
        self.screen['actions'].actions['red']()
        self.assertFalse(self.view.active);self.pig.onShow.assert_called_once();self.pig.instance.show.assert_called_once()
        self.assertTrue(self.screen['selection'].visible);self.assertTrue(self.screen['info'].visible)
        self.assertTrue(all(not w.visible for w in self.view.widgets))
        self.view.original_back.assert_not_called()
        self.screen['actions'].actions['back']();self.view.original_back.assert_called_once()
        self.session.nav.stopService.assert_not_called();self.session.nav.playService.assert_not_called()
    def test_suspending_for_another_screen_stops_polling_and_keeps_preview_ready_for_return(self):
        with patch.object(self.view.model,'startSearchInfo'):self.view.show()
        self.view.suspend()
        self.assertFalse(self.view.active);self.pig.onShow.assert_not_called();self.pig.instance.show.assert_called_once()
        callback=MagicMock();self.view.timer.callback[:]=[callback];self.view.timer.fire();callback.assert_not_called()
    def test_original_ecm_parser_and_refresh_fill_real_values_while_timer_is_gated(self):
        self.view.cleanup()
        api=dict(vars(self.plugin));native=MagicMock();api['eTimer']=lambda:native
        api['iServiceInformation']=types.SimpleNamespace(sIsCrypted=1)
        api['ECMparser']=MagicMock(return_value=('r11968\n','OSCam\n','Irdeto\n','0668\n','M7 Group\n','03EA1F\n','1234\n','local\n','camd.socket\n','0\n','0\n','123 ms\n','Irdeto','cw0\n','cw1\n'))
        api['findPicon']=lambda *args:'/example/irdeto.png'
        other=self.ui.InlineECM(self.screen,api)
        other.model['piccode'].instance=MagicMock()
        other.timer.fire();api['ECMparser'].assert_not_called()
        other.show()
        api['ECMparser'].assert_called_once_with(cl=24)
        self.assertIn('M7 Group',other.model['ecmValues'].text)
        self.assertIn('0668',other.model['ecmValues'].text)
        self.assertIn('123 ms',other.model['ecmValues'].text)
        other.model['piccode'].instance.setPixmapFromFile.assert_called_once_with('/example/irdeto.png')
        native.start.assert_called_with(5000,True)
        other.hide();other.timer.fire();api['ECMparser'].assert_called_once()
        other.cleanup();self.assertIsNone(other.timer.native)
    def test_labels_translate_without_changing_parser_label_substitution_or_values(self):
        original=self.view.model.e
        mapping={'Provider:':'Operátor:','ECM Time:':'Čas ECM:'}
        with patch.object(self.ui.main,'text',side_effect=lambda api,key:mapping.get(key,key)):
            self.view.model['ecmlabels'].setText('Provider:\nCHID:\nECM Time:')
        self.assertEqual(self.screen['inline_ecm_labels'].text,'Operátor:\nCHID:\nČas ECM:')
        self.assertEqual(self.view.model.e,original)
        self.assertIn('CHID:',self.screen['inline_ecm_labels'].text)
    def test_overlay_geometry_stays_within_right_panel_at_all_resolutions(self):
        main=self.ui.main
        for width,height in ((1280,720),(1920,1080),(3840,2160)):
            root=ET.fromstring(main.main_skin(width,height))
            for node in root:
                if not node.get('name','').startswith('inline_ecm_'):continue
                x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
                self.assertGreaterEqual(x,round(1137*width/1920));self.assertLessEqual(x+w,round(1863*width/1920))
                self.assertGreaterEqual(y,round(182*height/1080));self.assertLessEqual(y+h,round(978*height/1080))
            self.assertEqual(len(root.findall("widget[@render='Pig']")),1)
