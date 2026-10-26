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
        self.host.navigate('files','http://192.0.2.1/','demo','test')
        proxy=self.host.panes['files'].model.session
        proxy.open(self.plugin.oscam_Files_detailed,'http://192.0.2.1/files','demo','test','oscam.conf')
        self.assertEqual(self.host.current,'file')
        self.assertEqual(self.host.panes['file'].model.titleFile,'oscam.conf')
        self.host.back();self.assertEqual(self.host.current,'files')
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
            self.assertEqual(self.host.move(1),0)
            self.assertEqual(self.host.choose(),0)
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
            self.assertTrue(value['text'].startswith(pane.model.allLabelsCRD[index]+':'))
            self.assertLessEqual(value['pos'][0]+value['size'][0],1010)
            self.assertLessEqual(value['pos'][1]+value['size'][1],160)
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
