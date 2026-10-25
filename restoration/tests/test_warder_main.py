import ast
from datetime import datetime
import hashlib
import importlib
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree as ET
from receiver_stubs import load

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE/'src/GlassSysUtil'
sys.path.insert(0,str(ROOT))
import warder_main as ui


class WarderMainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.plugin=load(ROOT)

    def test_scaled_opaque_layout_fits_eleven_rows_and_contains_all_dynamic_widgets(self):
        required={'list','info','selection','day','date','clock','seconds','version_title','version','menu_title','purpose','red','green','yellow'}
        for width,height in ((1280,720),(1920,1080),(3840,2160)):
            root=ET.fromstring(ui.main_skin(width,height))
            self.assertEqual(root.get('backgroundColor'),ui.BASE)
            self.assertEqual(root.get('flags'),'wfNoBorder')
            widgets={n.get('name'):n for n in root.findall('widget')}
            self.assertEqual(set(widgets),required)
            self.assertNotIn('blue',widgets)
            for n in root:
                x,y=map(int,n.get('position').split(','));w,h=map(int,n.get('size').split(','))
                self.assertGreaterEqual(min(x,y),0)
                self.assertLessEqual(x+w,width)
                self.assertLessEqual(y+h,height)
            rows_height=int(widgets['list'].get('size').split(',')[1])
            self.assertGreaterEqual(rows_height,11*round(58*height/1080))
            for a,b in (('day','version_title'),('date','version')):
                self.assertEqual(widgets[a].get('position').split(',')[1],widgets[b].get('position').split(',')[1])
            for name in ('list','info','selection'):
                self.assertEqual(widgets[name].get('transparent'),'0')
                self.assertEqual(widgets[name].get('backgroundColor'),ui.PANEL)

    def test_language_dates_and_seconds_are_local_without_locale_mutation(self):
        instant=datetime(2026,10,25,15,32,9)
        self.assertEqual(ui.clock_values(instant,'sk'),('Nedeľa','25. októbra 2026','15:32',':09'))
        self.assertEqual(ui.clock_values(instant,'cs')[0],'Neděle')
        for lang in ui.DAYS:
            self.assertEqual(len(ui.DAYS[lang]),7)
            self.assertEqual(len(ui.MONTHS[lang]),12)
            for month in range(1,13):
                values=ui.clock_values(instant.replace(month=month,day=1),lang)
                self.assertIn(ui.MONTHS[lang][month-1],values[1])
        self.assertEqual(ui.clock_values(instant,'unknown')[2:],('15:32',':09'))

    def test_header_both_native_timer_signals_stops_and_ignores_late_tick(self):
        for modern in (False,True):
            screen=self.plugin.SysUtilMngMain(MagicMock())
            screen._warder_header.cleanup()
            callbacks=[];signal=types.SimpleNamespace(get=lambda:callbacks)
            if modern:signal.connect=lambda cb:callbacks.append(cb)
            timer=MagicMock(timeout=signal);api=dict(vars(self.plugin));api['eTimer']=lambda:timer
            header=ui.Header(screen,api)
            for name in ('day','date','clock','seconds'):
                screen[name].setText=MagicMock()
            fixed=datetime(2026,10,25,15,32,9)
            with patch.object(ui,'datetime') as clock:
                clock.now.return_value=fixed
                header.prepare();header.tick()
                for name in ('day','date','clock','seconds'):self.assertEqual(screen[name].setText.call_count,1)
                clock.now.return_value=fixed.replace(second=10)
                header.tick()
                self.assertEqual(screen['seconds'].setText.call_count,2)
                self.assertEqual(screen['clock'].setText.call_count,1)
                header.cleanup();header.tick()
                self.assertEqual(screen['seconds'].setText.call_count,2)
            timer.start.assert_called_once_with(1000)
            timer.stop.assert_called_once()
            self.assertEqual(callbacks,[header.tick])
            self.assertEqual(screen['version_title'].text,'Verzia:')
            self.assertEqual(screen['green'].text,'Vybrať s OK')
            self.assertEqual(screen['yellow'].text,'Nastavenia')
            self.assertTrue(all(getattr(c,'__self__',None) is not None for c in screen.onLayoutFinish))

    def test_existing_menu_ids_status_and_actions_survive_new_presentation(self):
        module=self.plugin;session=MagicMock()
        screen=module.SysUtilMngMain(session)
        with patch.object(module,'countServers',return_value=(True,True)),patch.object(screen,'checkCam',return_value=False),patch.object(screen,'cccamRunning',return_value=False),patch.object(screen,'mboxRunning',return_value=False),patch.object(module,'oscamRunning',return_value=True):
            screen.updatemenulist()
        self.assertEqual([row[0] for row in screen.list],['0','1','2','3','4','6','7','8','9','17','16'])
        self.assertFalse(screen.status['2']);self.assertFalse(screen.status['4']);self.assertTrue(screen.status['3'])
        for entry in screen.menuListAll:
            screen['list'].getCurrent=lambda e=entry:[e[0]]
            screen.reactivate()
            self.assertEqual(screen['selection'].text,entry[1])
            self.assertEqual(screen['info'].text,entry[2])
        screen.status['3']=True;screen['list'].getCurrent=lambda:['3'];screen.enaNonLocalOscam=True
        screen.selectedmenuitem();session.open.assert_called_with(module.oscamInfo)
        self.assertIs(screen['actions'].actions['green'].__self__,screen)
        self.assertEqual(screen['actions'].actions['green'],screen['actions'].actions['ok'])
        self.assertEqual(screen['actions'].actions['yellow'],screen.cfgGsu)

    def test_rows_keep_identity_and_render_status_without_loading_images(self):
        api=dict(vars(self.plugin));api['LoadPixmap']=MagicMock(side_effect=AssertionError('row must not decode images'))
        for enabled,color in ((True,0x39ff59),(False,0xff526a)):
            row=ui.menu_row(api,'3','OScam informácie',enabled,1920,1080)
            self.assertEqual(row[0],'3');self.assertEqual(row[1]['text'],'OScam informácie')
            self.assertEqual(row[2]['color'],color)
        api['LoadPixmap'].assert_not_called()

    def test_transformation_is_idempotent_and_original_class_interfaces_retained(self):
        sys.path.insert(0,str(BASE/'tools'))
        from warder_main_port import port_warder_main
        source=(ROOT/'plugin.py').read_text()
        self.assertEqual(port_warder_main(source),source)
        tree=ast.parse(source);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='SysUtilMngMain')
        self.assertIn('selectedmenuitem',[n.name for n in cls.body if isinstance(n,ast.FunctionDef)])
        self.assertNotIn('wfNoBorder',ast.unparse(cls))

    def test_background_identity_is_pinned_and_small_enough_for_receiver_package(self):
        manifest=json.loads((BASE/'artwork/warder-main.json').read_text())
        raw=(ROOT/'images/warder-main.png').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),manifest['sha256'])
        self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
        self.assertLess(len(raw),2*1024*1024)

    def test_plugin_icon_uses_shared_template_with_transparent_native_canvas(self):
        import struct
        icon=json.loads((BASE/'artwork/warder-main.json').read_text())['plugin_icon']
        raw=(ROOT/icon['path']).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),icon['sha256'])
        self.assertEqual(struct.unpack('>II',raw[16:24]),(160,96))
        self.assertIn(raw[25],(4,6))  # PNG grayscale-alpha or RGBA, no opaque matte.
        self.assertIn("icon='images/warder-plugin.png'",(ROOT/'plugin.py').read_text())
        self.assertLess(len(raw),30000)

if __name__=='__main__':unittest.main()
