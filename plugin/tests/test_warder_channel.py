import importlib
from pathlib import Path
import types
import unittest
from xml.etree import ElementTree as ET
from unittest.mock import patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'


class ChannelLayoutTests(unittest.TestCase):
    def test_preserves_all_named_widgets_and_live_converters_at_every_resolution(self):
        plugin=load(ROOT)
        for suffix,w,h in (('',1280,720),('_FHD',1920,1080),('_UHD',3840,2160)):
            original=importlib.import_module('Plugins.Extensions.GlassSysUtil.GSU_skins'+suffix).channelInfo_Center
            before=ET.fromstring(original);after=ET.fromstring(plugin._warder_channel.channel_skin(original,w,h))
            names=lambda root:{n.get('name') for n in root if n.get('name')}
            self.assertEqual(names(after),names(before)|{'day','date','clock','seconds','version_title','version','glass_header_art'})
            def sources(root):
                return sorted((n.get('source'),n.get('render'),tuple((c.get('type'),c.text.strip()) for c in n.findall('convert'))) for n in root if n.get('source'))
            self.assertEqual(sources(before),sources(after))
            self.assertEqual(after.find("widget[@name='glass_header_art']").get('zPosition'),'-3')
            self.assertFalse(any(n.get('pixmap','').endswith('/frame.png') for n in after))
            for n in after:
                x,y=map(int,n.get('position').split(','));iw,ih=map(int,n.get('size').split(','))
                self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,0)
                self.assertLessEqual(x+iw,w);self.assertLessEqual(y+ih,h)
                if n.get('name') in names(before)-{'red'}:
                    self.assertGreaterEqual(y,round(180*h/1080))
                    self.assertLessEqual(y+ih,round(980*h/1080))
            for name in ('ecmlabels','ecmValues','tp_lab','tp_values'):
                n=after.find("widget[@name='%s']"%name)
                self.assertEqual(n.get('transparent'),'1')
                self.assertEqual(n.get('backgroundColor'),'#ff000000')
            ecm=after.find("widget[@name='ecmValues']")
            icon=after.find("widget[@name='picchannel']")
            self.assertLess(int(ecm.get('position').split(',')[0])+int(ecm.get('size').split(',')[0]),int(icon.get('position').split(',')[0]))

    def test_header_is_independent_and_stops_on_close(self):
        plugin=load(ROOT)
        screen=plugin.channelInfoCenter(types.SimpleNamespace())
        header=screen._warder_header
        self.assertIn(header.cleanup,screen.onClose)
        self.assertIn(header.prepare,screen.onLayoutFinish)
        self.assertIsNone(screen.runECMTimer1)
        self.assertIsNone(screen.runBitTimer1)
        header.prepare()
        header.cleanup()
        self.assertTrue(header.closed)
        previous=screen['clock'].text
        header.tick()
        self.assertEqual(screen['clock'].text,previous)

    def test_translated_captions_do_not_translate_received_service_values(self):
        plugin=load(ROOT)
        with patch.object(plugin,'GSU_PATH',str(ROOT)+'/'), patch.object(plugin.config.osd.language,'value','sk_SK'), patch.object(plugin.config.plugins.GlassSysUtil.par62,'value',True):
            plugin.config.osd.language.value='fr_FR'
            screen=plugin.channelInfoCenter(types.SimpleNamespace())
            self.assertEqual(screen['tp_lab_sat'].text,'Satellite :')
            self.assertEqual(screen['tp_lab_ref'].text,'Référence :')
            self.assertIn('Fréquence :',screen['tp_lab'].text)
            self.assertEqual(screen['tp_values'].text,'')
            screen['tp_values'].setText('DVB-S2\n12207 MHz')
            self.assertEqual(screen['tp_values'].text,'DVB-S2\n12207 MHz')

    def test_layout_callbacks_match_native_openatv_dispatch_and_align_satellite(self):
        plugin=load(ROOT)
        for width,height in ((1280,720),(1920,1080),(3840,2160)):
            screen=plugin.channelInfoCenter(types.SimpleNamespace())
            # OpenATV executes bound methods directly and passes other entries to exec.
            for callback in screen.onLayoutFinish:
                self.assertIsInstance(callback,type(screen.close))
            callback=next(c for c in screen.onLayoutFinish if c.__name__=='align_satellite')
            desktop=types.SimpleNamespace(size=lambda:types.SimpleNamespace(width=lambda:width,height=lambda:height))
            with patch.object(plugin,'getDesktop',lambda index:desktop), patch('enigma.ePoint',lambda x,y:(x,y)), patch('enigma.eSize',lambda w,h:(w,h)):
                callback()
            for name in ('tp_lab_sat','tp_sat'):
                x,y,w,h,_=plugin._warder_channel.SLOTS[name]
                self.assertEqual(screen[name]._position,(round(x*width/1920),round(y*height/1080)))
                self.assertEqual(screen[name]._size,(round(w*width/1920),round(h*height/1080)))
