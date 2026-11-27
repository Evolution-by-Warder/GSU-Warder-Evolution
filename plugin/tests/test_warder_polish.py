import importlib
from pathlib import Path
import types
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree as ET
from receiver_stubs import load
ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'

class PolishTests(unittest.TestCase):
    def setUp(self):self.plugin=load(ROOT)
    def test_system_information_uses_six_cards_and_settings_use_large_glass_window(self):
        for width,height in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            root=ET.fromstring(self.plugin._warder_system.information_skin(width,height))
            self.assertIsNone(root.find("widget[@name='ProccessInfo']"))
            self.assertIsNone(root.find("widget[@name='DmesgInfo']"))
            self.assertIsNotNone(root.find("widget[@name='value5']"))
            settings=ET.fromstring(self.plugin._warder_settings.skin(width,height))
            self.assertEqual(settings.get('size'),'%d,%d'%(width,height))
            self.assertIsNotNone(settings.find("widget[@name='config']"))
            self.assertIsNotNone(settings.find("widget[@name='glass_header_art']"))
    def test_editable_mark_changes_only_rendered_text_and_restores_original_method(self):
        ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_editable')
        setting=types.SimpleNamespace(value=500,getMulti=lambda selected:('mtext','0500',[0]))
        model=type('Model',(dict,),{})();model['config']=types.SimpleNamespace(list=[('Threshold',setting)])
        original=setting.getMulti;ui.mark(model);ui.mark(model)
        self.assertEqual(len(model._editable_marks),1);self.assertIn('✎',setting.getMulti(False)[1]);self.assertEqual(setting.value,500)
        ui.restore(model);self.assertIs(setting.getMulti,original)
    def test_default_static_position_is_separate_and_old_manual_position_migrates(self):
        ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.osd_layout')
        cfg=self.plugin.config.plugins.GlassSysUtil
        self.assertEqual((cfg.static_osd_x.value,cfg.static_osd_y.value),(1306,50))
        cfg.par3.value=True;self.assertIs(ui.position_settings(vars(self.plugin))[0],cfg.static_osd_x)
        cfg.par3.value=False;self.assertIs(ui.position_settings(vars(self.plugin))[0],cfg.par1)
        cfg.par1.value=1450;cfg.par2.value=55;cfg.par1.saved_value='1450'
        ui.init_static_position(vars(self.plugin));self.assertEqual((cfg.static_osd_x.value,cfg.static_osd_y.value),(1450,55))
    def test_about_is_inside_main_right_panel(self):
        session=MagicMock();s=self.plugin.SysUtilMngMain(session);s.aboutPlugin()
        self.assertEqual(s._rightpane.kind,'about');session.open.assert_not_called()
        self.assertIn('GSU Warder Evolution',s['right_scroll'].getText())
