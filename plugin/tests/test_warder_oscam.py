"""Workspace routing, timer isolation and preservation of original controllers."""
import importlib
from pathlib import Path
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree as ET
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'

class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.plugin=load(ROOT)
        self.ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_oscam')
        self.session=MagicMock()
        self.host=self.ui.OscamWorkspace(self.session,vars(self.plugin))
        for pane in self.host.panes.values():
            pane.model.onLayoutFinish=[]
            for component in pane.widgets.values():component.instance=MagicMock()
        self.host.begin()
        intro=self.host.panes['intro'].model
        intro.status={kind:True for kind in ('summary','readers','users','log','files')}
        intro.list=[[kind] for kind in intro.status];intro['list'].l.setList(intro.list)
    def test_openatv_native_layout_dispatch_accepts_all_registered_callbacks(self):
        # OpenATV Screens/Screen.py createGUIScreen executes non-bound callbacks
        # as source strings; a lambda raises the receiver's reported TypeError.
        with patch.object(self.host._warder_header,'tick'),patch.object(self.host,'activate') as activate:
            self.host.select_server=True
            for method in self.host.onLayoutFinish:
                if not isinstance(method,type(self.host.close)):
                    exec(method,{}, {})
                else:method()
            activate.assert_called_once_with('servers')

    def test_all_primary_results_stay_in_one_screen_and_return(self):
        intro=self.host.panes['intro'].model
        for index,kind in enumerate(intro.status):
            intro['list'].moveToIndex(index);self.host.choose()
            self.assertEqual(self.host.current,kind)
            self.assertFalse(self.host.menu_focus)
            self.host.back();self.assertEqual(self.host.current,'intro')
        self.session.open.assert_not_called()
        with patch.object(self.host,'close') as close:self.host.back();close.assert_called_once()
    def test_nested_file_and_card_use_left_pane_and_back_parent(self):
        self.host.navigate('files','http://192.0.2.1/','demo','test');self.host.left()
        proxy=self.host.panes['files'].model.session
        proxy.open(self.plugin.oscam_Files_detailed,'http://192.0.2.1/files','demo','test','oscam.conf')
        self.assertEqual(self.host.current,'file')
        self.assertEqual(self.host.panes['file'].model.titleFile,'oscam.conf')
        self.host.back();self.assertEqual(self.host.current,'files');self.assertFalse(self.host.menu_focus)
        self.host.navigate('readers','http://192.0.2.1/','demo','test')
        self.host.panes['readers'].model.session.open(self.plugin.oscam_entitlements,'http://192.0.2.1/','reader','demo','test')
        self.assertEqual(self.host.panes['entitlements'].model.reader,'reader')
        self.host.back();self.assertEqual(self.host.current,'readers')
        self.session.open.assert_not_called()
    def test_direction_switches_focus_and_native_controls(self):
        self.host.navigate('users','http://192.0.2.1/','','')
        action=self.host.panes['users'].actions[0]
        with patch.object(action,'setEnabled') as enable:
            self.host.right();enable.assert_called_with(False)
            self.assertEqual(self.host.move(1),1)
            self.host.left();enable.assert_called_with(True)
            self.assertEqual(self.host.move(1),1)
            self.assertEqual(self.host.choose(),1)
    def test_opening_results_automatically_controls_left_until_explicit_right(self):
        intro=self.host.panes['intro'].model
        intro['list'].moveToIndex(0);self.host.choose()
        self.assertEqual(self.host.current,'summary');self.assertFalse(self.host.menu_focus)
        left=self.host.panes['summary'].model['list'];right=intro['list']
        with patch.object(right,'moveToIndex') as move,patch.object(left,'down') as down:
            self.host.move(1);down.assert_called_once();move.assert_not_called()
            self.host.right();self.host.move(1);move.assert_called_once()
            self.host.left();self.host.move(1);self.assertEqual(down.call_count,2)

    def test_ok_on_client_and_summary_updates_details_without_leaving(self):
        for kind in ('users','summary'):
            self.host.activate(kind);self.host.left()
            pane=self.host.panes[kind]
            with patch.object(pane.model,'reactivate') as details,patch.object(pane.model,'exit') as exit_screen:
                self.assertEqual(self.host.choose(),1);details.assert_called_once()
                exit_screen.assert_not_called()
                self.assertEqual(self.host.current,kind);self.assertFalse(self.host.menu_focus)
        self.session.open.assert_not_called()
    def test_ok_keeps_readonly_results_but_passes_real_nested_actions(self):
        for kind in ('log','file','entitlements'):
            self.host.activate(kind);self.host.left()
            self.assertEqual(self.host.choose(),1)
            self.assertEqual(self.host.current,kind);self.assertFalse(self.host.menu_focus)
        for kind in ('readers','files'):
            self.host.activate(kind);self.host.left();self.assertEqual(self.host.choose(),0)

    def test_results_arrows_drive_only_the_selected_left_list(self):
        right=self.host.panes['intro'].model['list']
        for kind,name in (('summary','list'),('readers','list'),('users','list'),('files','list'),('log','log_info'),('entitlements','entitlements_list')):
            self.host.activate(kind);self.host.left()
            widget=self.host.panes[kind].model[name]
            with patch.object(widget,'up') as up,patch.object(widget,'down') as down,patch.object(right,'moveToIndex') as menu_move:
                self.assertEqual(self.host.move(-1),1);up.assert_called_once()
                self.assertEqual(self.host.move(1),1);down.assert_called_once()
                menu_move.assert_not_called()
                self.host.right();self.host.move(1);menu_move.assert_called_once()
                down.assert_called_once()
                self.host.left();self.host.move(-1);self.assertEqual(up.call_count,2)
    def test_file_arrows_scroll_text_and_do_not_move_menu(self):
        self.host.activate('file');widget=self.host.panes['file'].model['file_info']
        with patch.object(widget,'pageUp') as up,patch.object(widget,'pageDown') as down:
            self.assertEqual(self.host.move(-1),1);up.assert_called_once()
            self.assertEqual(self.host.move(1),1);down.assert_called_once()
    def test_only_current_panel_has_selection_enabled(self):
        right=self.host.panes['intro'].model['list'];left=self.host.panes['summary'].model['list']
        with patch.object(right,'selectionEnabled') as r,patch.object(left,'selectionEnabled') as l:
            self.host.activate('summary');r.assert_called_with(0);l.assert_called_with(1)
            self.host.right();r.assert_called_with(1);l.assert_called_with(0)
            self.host.left();r.assert_called_with(0);l.assert_called_with(1)

    def test_hidden_timer_cannot_run_or_restart_until_pane_active(self):
        pane=self.host.panes['readers'];timer=pane.timers[0];timer.native=MagicMock()
        callback=MagicMock();timer.callback[:]=[callback]
        timer.start(100);timer.native.start.assert_not_called();timer.fire();callback.assert_not_called()
        self.host.activate('readers');timer.start(100);timer.fire()
        callback.assert_called_once();timer.native.start.assert_called_once_with(100)
        self.host.back();timer.fire();callback.assert_called_once()
        self.host.shutdown();self.assertIsNone(timer.native)
    def test_async_hidden_widget_stays_hidden_and_closed_modal_is_ignored(self):
        pane=self.host.panes['readers'];component=pane.model['blue_button']
        component.show();component.instance.show.assert_not_called()
        callback=MagicMock();pane.model.session.openWithCallback(callback,self.plugin.MessageBox,'Test',0)
        saved=self.session.openWithCallback.call_args.args[0]
        saved(True);callback.assert_called_once_with(True)
        self.host.shutdown();saved(False);callback.assert_called_once()
    def test_switch_server_updates_all_credentials_in_same_workspace(self):
        self.host.navigate('intro','http://192.0.2.2/','Demo','demo','test')
        for pane in self.host.panes.values():
            self.assertEqual((pane.model.url,pane.model.login,pane.model.passwd),('http://192.0.2.2/','demo','test'))
        self.assertEqual(self.host.panes['intro'].model.srv_name,'Demo')
    def test_intro_is_not_reloaded_on_each_return(self):
        pane=self.host.panes['intro'];callback=MagicMock();pane.model.onLayoutFinish=[callback]
        pane.loaded=False;self.host.activate('intro');callback.assert_called_once()
        self.host.navigate('summary','http://192.0.2.1/','','');self.host.back();callback.assert_called_once()
    def test_shared_header_no_video_and_every_widget_is_bound_and_inside_screen(self):
        for width,height in ((1280,720),(1920,1080),(3840,2160)):
            self.host.width,self.host.height=width,height;self.host.sx,self.host.sy=width/1920,height/1080
            root=ET.fromstring(self.ui.skin(self.host))
            self.assertFalse(root.findall("widget[@render='Pig']"))
            for node in root:
                name=node.get('name')
                if name:self.assertIn(name,self.host)
                x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
                self.assertGreaterEqual(min(x,y,w,h),0)
                self.assertLessEqual(x+w,width);self.assertLessEqual(y+h,height)
            self.assertEqual(root.find("widget[@name='intro_list']").get('position').split(',')[0],str(round(1155*width/1920)))
    def test_entitlement_cards_preserve_all_eight_values_and_field_names(self):
        pane=self.host.panes['entitlements']
        values=[]
        for index,x in enumerate((30,125,200,300,500,650,805,960)):
            values.append(pane.text(pos=(self.plugin.fhd(x),0),size=(450,38),font=1,text='value%d'%index))
        for index,value in enumerate(values):
            self.assertIn('value%d'%index,value['text'])
            label={'TypeCRD':'Type','CAIDcrd':'CAID'}.get(pane.model.allLabelsCRD[index],pane.model.allLabelsCRD[index])
            self.assertTrue(value['text'].startswith(self.ui.main.text(vars(self.plugin),label)+':'))
            self.assertLessEqual(value['pos'][0]+value['size'][0],1010)
            self.assertLessEqual(value['pos'][1]+value['size'][1],160)
    def test_all_selection_backgrounds_are_opaque_and_card_icon_cannot_cover_text(self):
        root=ET.fromstring(self.ui.skin(self.host))
        for kind,pane in self.host.panes.items():
            for name in ('list','log_info','entitlements_list'):
                if name not in pane.widgets:continue
                node=root.find("widget[@name='%s_%s']"%(kind,name))
                self.assertEqual(node.get('backgroundColorSelected'),'#002a70ad')
                self.assertEqual(node.get('transparent'),'1')
        pane=self.host.panes['entitlements']
        icon=pane.pixmap(pos=(0,self.plugin.fhd(3)),size=(self.plugin.fhd(15),self.plugin.fhd(16)),png=object())
        text=pane.text(pos=(self.plugin.fhd(30),0),size=(450,38),font=1,text='chid')
        self.assertGreater(text['pos'][0],icon['pos'][0]+icon['size'][0])

    def test_glass_panels_have_only_one_alpha_layer_and_no_opaque_art_beneath(self):
        root=ET.fromstring(self.ui.skin(self.host))
        self.assertEqual(root.get('backgroundColor'),self.ui.CLEAR)
        self.assertFalse(root.findall('ePixmap'))
        panels=[n for n in root if n.get('backgroundColor')==self.ui.PANEL_GLASS]
        self.assertEqual(len(panels),2)
        for panel in panels:
            x,y=map(int,panel.get('position').split(','));w,h=map(int,panel.get('size').split(','))
            for node in root:
                if node is panel or node.get('name') or int(node.get('zPosition','0'))>=-1:continue
                nx,ny=map(int,node.get('position').split(','));nw,nh=map(int,node.get('size').split(','))
                self.assertFalse(nx<x+w and nx+nw>x and ny<y+h and ny+nh>y)
        for name in ('intro_list','intro_server_name','summary_list','file_file_info','readers_list'):
            node=root.find("widget[@name='%s']"%name)
            self.assertEqual(node.get('backgroundColor'),self.ui.CLEAR)
            self.assertEqual(node.get('transparent'),'1')
        self.assertEqual(root.find("widget[@name='red']").get('transparent'),'0')
    def test_native_header_scales_child_inside_clipped_header_parent(self):
        for width,height in ((1280,720),(1920,1080),(3840,2160)):
            parent=MagicMock();child=MagicMock();header=self.ui.HeaderArtwork(width,height)
            with patch.object(importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_glass'),'ePixmap',return_value=child) as pixmap:
                header.postWidgetCreate(parent)
            pixmap.assert_called_once_with(parent)
            full=child.resize.call_args.args[0]
            self.assertEqual((full.width(),full.height()),(width,height))
            child.setScale.assert_called_once_with(1)
            child.setPixmapFromFile.assert_called_once_with(self.ui.main.BACKGROUND)
            child.show.assert_called_once()
            self.assertIs(header.GUI_WIDGET,self.ui.eWidget)
            self.assertIs(header.picture,child)
            header.preWidgetRemove(parent);self.assertIsNone(header.picture)

    def test_log_wrap_preserves_content_and_allows_reading(self):
        pane=self.host.panes['log'];value='long OSCam log message '*15
        row=pane.text(pos=(0,0),size=(1770,26),font=1,text=value)
        self.assertEqual(row['text'].replace('\n',''),value)
        self.assertLessEqual(row['size'][0],1010)
        self.assertGreater(row['size'][1],42)
    def test_original_reader_renderer_and_identity_are_retained(self):
        pane=self.host.panes['readers']
        pane.old_width=1290
        data=(ROOT.parents[1]/'tests/fixtures/oscam_readers_11968.html')
        pane.model.renderReaders(data.read_text().splitlines())
        self.assertTrue(pane.model.list)
        self.assertTrue(all(row[0] for row in pane.model.list))

if __name__=='__main__':unittest.main()
