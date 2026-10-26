import importlib
from pathlib import Path
import types
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree as ET
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'

class WarderCamTests(unittest.TestCase):
    def setUp(self):
        self.plugin=load(ROOT);self.ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_cam')
        self.session=MagicMock();self.screen=self.plugin.univCamMng(self.session);self.controls=self.screen._warder_cam
        self.screen['config'].list=[('CAM',types.SimpleNamespace(value='first',choices=[('first','First'),('second','Second')]))]
        for name in ('select_pict','txt0','txt1','txt2','txt3','txt4','txt6','txt7','txt8'):
            self.screen[name].instance=MagicMock()
    def test_layout_keeps_all_backend_components_and_common_header_in_three_resolutions(self):
        for width,height in ((1280,720),(1920,1080),(3840,2160)):
            original=self.plugin._srv_skin(self.plugin._compact_cam_menu(self.plugin.UCM))
            root=ET.fromstring(self.ui.cam_skin(original,width,height))
            names={n.get('name') for n in root if n.get('name')}
            self.assertTrue({n.get('name') for n in ET.fromstring(original) if n.get('name') and n.get('name')!='blue'}<=names)
            self.assertTrue({'day','date','clock','seconds','version_title','version','focus_hint'}<=names)
            self.assertEqual(len(names),len([n for n in root if n.get('name')]))
            for node in root:
                x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
                self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,0)
                self.assertLessEqual(x+w,width);self.assertLessEqual(y+h,height)
            selection=root.find("widget[@name='select_pict']")
            self.assertEqual(selection.get('backgroundColor'),self.ui.main.SELECTION)
            self.assertIsNone(selection.get('pixmap'))
    def test_focus_switch_does_not_start_stop_or_select_cam(self):
        with patch.object(self.screen,'start') as start,patch.object(self.screen,'stop') as stop:
            self.controls.left();self.assertFalse(self.controls.menu);self.assertFalse(self.screen['select_pict'].visible)
            self.controls.right();self.assertTrue(self.controls.menu)
            start.assert_not_called();stop.assert_not_called()
        self.assertEqual(self.screen['config'].list[0][1].value,'first')
    def test_menu_wrap_and_reverse_skip_retired_and_absent_server_actions(self):
        s=self.screen;s.numSrv=0;s.idxAllFnc=0
        self.controls.up();self.assertEqual(s.idxAllFnc,8)
        self.controls.down();self.assertEqual(s.idxAllFnc,0)
        s.idxAllFnc=6;self.controls.down();self.assertEqual(s.idxAllFnc,8)
        s.numSrv=1;s.idxAllFnc=6;self.controls.down();self.assertEqual(s.idxAllFnc,7)
    def test_ok_on_right_activates_only_selected_action(self):
        with patch.object(self.screen,'ActivateselectedFnc') as activate:
            self.controls.choose();activate.assert_called_once()
        self.session.openWithCallback.assert_not_called()
    def test_left_ok_selects_value_without_starting_cam_and_cancel_preserves_value(self):
        self.controls.left();self.controls.choose()
        self.session.openWithCallback.assert_not_called()
        self.assertIsNotNone(self.screen._cam_panes.choice)
        self.screen._cam_panes.close_choice(None)
        self.assertEqual(self.screen['config'].list[0][1].value,'first')
        self.controls.left();self.controls.choose()
        self.screen._cam_panes.close_choice(('Second','second'))
        self.assertEqual(self.screen['config'].list[0][1].value,'second')
    def test_legacy_color_buttons_keep_native_start_stop_and_activate_handlers(self):
        actions=self.screen['actions'].actions
        self.assertEqual(actions['green'],self.screen.start);self.assertEqual(actions['red'],self.screen.stop)
        self.assertEqual(actions['yellow'],self.screen.ActivateselectedFnc)
        self.assertEqual(actions['cancel'],self.screen.exit)

    def test_glass_matches_oscam_and_has_no_opaque_panel_backing(self):
        original=self.plugin._srv_skin(self.plugin._compact_cam_menu(self.plugin.UCM))
        root=ET.fromstring(self.ui.cam_skin(original,1920,1080))
        self.assertEqual(root.get('backgroundColor'),self.ui.CLEAR)
        self.assertFalse(any(n.get('pixmap')==self.ui.main.BACKGROUND for n in root))
        self.assertIsNotNone(root.find("widget[@name='header_art']"))
        glass=[n for n in root if n.get('backgroundColor')==self.ui.PANEL_GLASS]
        self.assertEqual(len(glass),2)
        for name in ('config','helpTXT','fullEcmLine','CAID_info','activCam','txt0','focus_hint'):
            n=root.find("widget[@name='%s']"%name)
            self.assertEqual(n.get('backgroundColor'),self.ui.CLEAR)
            self.assertEqual(n.get('transparent'),'1')
        for n in root:
            if n.tag=='eLabel' and n.get('backgroundColor') in (self.ui.main.BASE,self.ui.main.CYAN):
                x,y=map(int,n.get('position').split(','));w,h=map(int,n.get('size').split(','))
                self.assertFalse(x<1103 and x+w>57 and y<978 and y+h>182)

    def test_blue_is_absent_and_consumed_without_moving_selection(self):
        root=ET.fromstring(self.screen.skin)
        self.assertIsNone(root.find("widget[@name='blue']"))
        before=self.screen.idxAllFnc
        self.screen['cam_panel_actions'].actions['blue']()
        self.assertEqual(self.screen.idxAllFnc,before)
        footers=[root.find("widget[@name='%s']"%name) for name in ('red','green','yellow')]
        self.assertEqual(len({n.get('size') for n in footers}),1)
