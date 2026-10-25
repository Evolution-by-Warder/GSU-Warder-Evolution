from pathlib import Path
import types
import unittest
from contextlib import ExitStack
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'


class OsdEcmTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.plugin=load(ROOT)

    def setUp(self):
        self.cfg=self.plugin.config.plugins.GlassSysUtil
        keys=('par0','par1','par2','par3','par4','par5','par78','par80','par81')
        old={k:getattr(self.cfg,k).value for k in keys}
        self.addCleanup(lambda:[setattr(getattr(self.cfg,k),'value',v) for k,v in old.items()])
        self.cfg.par0.value=True;self.cfg.par4.value=500;self.cfg.par5.value=8;self.cfg.par81.value=4
        self.display=MagicMock();p=patch.object(self.plugin,'OnScreenEcm',self.display);p.start();self.addCleanup(p.stop)

    def screen(self,static=False,modern=True):
        self.cfg.par3.value=static;timers=[];callbacks=[]
        def timer():
            slots=[];obj=MagicMock();obj.isActive.return_value=False
            obj.timeout=types.SimpleNamespace(connect=lambda cb:slots.append(cb)) if modern else types.SimpleNamespace(get=lambda:slots)
            timers.append(obj);callbacks.append(slots);return obj
        info=types.SimpleNamespace(getInfo=lambda key:1 if key=='crypted' else 0x1234)
        session=types.SimpleNamespace(nav=types.SimpleNamespace(getCurrentService=lambda:types.SimpleNamespace(info=lambda:info)))
        with patch.object(self.plugin,'eTimer',side_effect=timer),patch.object(self.plugin,'iPlayableService',types.SimpleNamespace(evStopped=1,evTunedIn=2)):
            screen=self.plugin.OnScreenEcmScreen(session)
        screen.sid='1234';screen.cryptService=True
        screen.instance=types.SimpleNamespace(move=MagicMock())
        return screen,timers,callbacks

    def data(self,time='0.100\n',using='server\n'):
        return ('11968\n','OScam\n','Irdeto\n','0624\n','000000\n','000000\n','0B7C\n',using,'127.0.0.1\n','0\n','1\n',time,'Irdeto','cw0','cw1')

    def read(self,screen,stamp=1,data=None):
        with patch.object(self.plugin.os,'stat',return_value=types.SimpleNamespace(st_mtime=stamp)),patch.object(self.plugin,'ECMparser',return_value=data or self.data()) as parser:
            screen.readEcmInfo()
            return parser

    def test_static_and_rolling_widgets_exist_with_both_timer_signal_apis(self):
        for static in (False,True):
            for modern in (False,True):
                screen,timers,callbacks=self.screen(static,modern)
                self.assertIn('OSD_Ecm_info',screen)
                self.assertEqual('ecm_items' in screen,static)
                self.assertEqual(callbacks,[[screen.staticEcm if static else screen.rollText],[screen.readEcmInfo]])
                screen.prepareOsd()

    def test_changed_file_parses_and_displays_static_values_not_rolling_text(self):
        screen,timers,_=self.screen(True)
        screen.StartrollTextInfo=MagicMock()
        parser=self.read(screen)
        parser.assert_called_once_with(10)
        self.assertIn('0624',screen['OSD_Ecm_info'].text)
        self.assertIn('1234',screen['OSD_Ecm_info'].text)
        self.assertIn('OScam',screen['OSD_Ecm_info'].text)
        screen.StartrollTextInfo.assert_not_called();self.display.makeShow.assert_called_with('show')
        timers[0].start.assert_called_with(8000)

    def test_rolling_mode_renders_then_hides_and_resumes_polling(self):
        screen,timers,_=self.screen()
        self.read(screen);self.assertEqual(screen.status,'start')
        screen.rollText();self.assertIn('CAID: 0624',screen['OSD_Ecm_info'].text)
        while screen.status!='end':screen.rollText()
        self.display.makeShow.assert_called_with('hide')
        timers[1].start.assert_called_with(4000,True)

    def test_unchanged_file_and_small_time_changes_do_not_redisplay(self):
        screen,timers,_=self.screen(True);self.read(screen)
        screen.status='end';screen.staticEcmStart=MagicMock()
        self.read(screen).assert_not_called()
        self.read(screen,2,self.data('0.150\n'))
        screen.staticEcmStart.assert_not_called()
        timers[1].start.assert_called_with(4000,True)
        self.read(screen,3,self.data('0.800\n'));screen.staticEcmStart.assert_called_once()

    def test_missing_ecm_file_reschedules_without_uninitialized_fields(self):
        screen,timers,_=self.screen()
        with patch.object(self.plugin.os,'stat',side_effect=FileNotFoundError),patch.object(self.plugin,'ECMparser') as parser:
            screen.readEcmInfo()
        parser.assert_not_called();timers[1].start.assert_called_with(4000,True)

    def test_unsupported_message_uses_selected_mode_and_returns_before_normal_values(self):
        for static in (False,True):
            screen,_,_=self.screen(static)
            screen.staticEcmStart=MagicMock();screen.StartrollTextInfo=MagicMock()
            self.read(screen,data=self.data(using='unsupported CAs\n'))
            (screen.staticEcmStart if static else screen.StartrollTextInfo).assert_called_once()
            (screen.StartrollTextInfo if static else screen.staticEcmStart).assert_not_called()

    def test_disable_stops_timers_and_channel_end_resets_cache(self):
        screen,timers,_=self.screen();self.read(screen)
        self.cfg.par0.value=False
        for timer in timers:timer.isActive.return_value=True
        screen._OnScreenEcmScreen__endShow()
        for timer in timers:timer.stop.assert_called()
        self.assertIsNone(screen.ecmInfo_time);self.assertFalse(screen.cryptService)
        self.display.makeShow.assert_called_with('hide')

    def test_static_free_to_air_never_reuses_old_encrypted_ecm(self):
        screen,timers,_=self.screen(True)
        screen.session.nav.getCurrentService=lambda:types.SimpleNamespace(info=lambda:types.SimpleNamespace(getInfo=lambda key:0))
        with patch.object(self.plugin,'iServiceInformation',types.SimpleNamespace(sIsCrypted='crypted',sSID='sid')):
            screen._OnScreenEcmScreen__startSearchInfo()
        self.assertEqual(screen['OSD_Ecm_info'].text,'Free To Air')
        screen.staticEcm()
        with patch.object(self.plugin,'ECMparser') as parser:screen.readEcmInfo()
        parser.assert_not_called()

    def test_position_window_stops_timer_and_stays_within_real_screen_bounds(self):
        timer=MagicMock()
        with patch.object(self.plugin,'eTimer',return_value=timer):screen=self.plugin.SelectPosition(types.SimpleNamespace())
        screen.instance=types.SimpleNamespace(size=lambda:types.SimpleNamespace(width=lambda:306,height=lambda:261))
        self.cfg.par1.value=9999;self.cfg.par2.value=9999
        screen.right();screen.down()
        self.assertEqual(self.cfg.par1.value,1920-306);self.assertEqual(self.cfg.par2.value,1080-261)
        screen.ok();timer.stop.assert_called_once();self.assertIsNone(screen.moveTimer)

    def test_save_and_cancel_include_options_hidden_after_disabling_osd(self):
        for action in ('save','cancel'):
            self.cfg.par0.value=False
            with patch.object(self.plugin,'eTimer',return_value=MagicMock()):menu=self.plugin.OSD_ECM_Menu(types.SimpleNamespace())
            menu.updatemenulist();self.assertEqual(len(menu.list),1)
            with ExitStack() as stack:
                callbacks=[stack.enter_context(patch.object(getattr(self.cfg,key),action)) for key in ('par0','par4','par5','par78','par80','par81')]
                if action=='save':menu.saveOnly()
                else:menu.exitCancel()
                for callback in callbacks:callback.assert_called_once()
