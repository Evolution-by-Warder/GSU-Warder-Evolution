import importlib
from pathlib import Path
import types
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree as ET
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'


class SystemLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin=load(ROOT);cls.ui=cls.plugin._warder_system

    def test_six_cards_without_processes_or_log_at_all_resolutions(self):
        for width,height in ((1280,720),(1920,1080),(2560,1440),(3840,2160),(1920,1200)):
            root=ET.fromstring(self.ui.information_skin(width,height))
            widgets={n.get('name'):n for n in root if n.get('name')}
            self.assertNotIn('ProccessInfo',widgets);self.assertNotIn('DmesgInfo',widgets)
            self.assertEqual(len([k for k in widgets if k.startswith('value')]),6)
            for i in range(6):
                for key in ('title','value','note'):self.assertIn(key+str(i),widgets)
            for n in root:
                x,y=map(int,n.get('position').split(','));w,h=map(int,n.get('size').split(','))
                self.assertGreaterEqual(min(x,y,w,h),0);self.assertLessEqual(x+w,width);self.assertLessEqual(y+h,height)
            for i in range(6):
                t,v,n=(widgets[k+str(i)] for k in ('title','value','note'))
                def limits(node):
                    x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','));return y,y+h
                self.assertLessEqual(limits(t)[1],limits(v)[0]);self.assertLessEqual(limits(v)[1],limits(n)[0])
            self.assertFalse(root.findall("widget[@render='Pig']"))

    def test_values_keep_capacity_details_and_unknown_values(self):
        cap=types.SimpleNamespace(total=100*1048576,free=40*1048576)
        report={'values':(17,16,None,40,cap.free,81.3),'memory':{'ram_total':cap.total,'ram_available':cap.free,'swap_total':0,'swap_free':0},
            'flash_usage':cap,'disk_usage':cap,'disk_mount':'/media/hdd','temperature_source':'cpu-thermal',
            'disk_temperature':38,'health':{'score':100,'coverage':(2,2)},'services':(True,False,None,True,False)}
        cards,summary,services=self.ui.information_model(report,str)
        self.assertEqual(cards[0][1],'17 %');self.assertEqual(cards[2][1],'—')
        self.assertIsNone(cards[2][3]);self.assertIn('Free: 40.0 MiB',cards[1][2])
        self.assertIn('/media/hdd',cards[4][0]);self.assertIn('38 °C',cards[5][2])
        self.assertIn('100/100',summary);self.assertEqual(services,report['services'])

    def test_actual_screen_binds_every_widget_and_preserves_detail_routes(self):
        session=MagicMock();screen=self.plugin.GlassSysInfoBrowser(session)
        for node in ET.fromstring(screen.skin):
            if node.get('name'):self.assertIn(node.get('name'),screen)
        self.assertNotIn('ProccessInfo',screen);self.assertNotIn('DmesgInfo',screen)
        module=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_centre_ui')
        with patch.object(module,'open_diagnostic') as route:
            screen.live();screen.details()
            self.assertEqual([c.args[-1] for c in route.call_args_list],['system-live','storage-overview'])


class TransparentSystemIconTests(unittest.TestCase):
    def test_all_new_icons_are_rgba_with_empty_top_margin_and_small_native_size(self):
        import struct,zlib
        files=list((ROOT/'images').glob('system-*.png'))
        self.assertEqual(len(files),15)
        for file in files:
            raw=file.read_bytes();self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
            self.assertEqual(struct.unpack('>II',raw[16:24]),(120,120))
            self.assertEqual(raw[25],6)
            chunks=[];offset=8
            while offset<len(raw):
                size=struct.unpack('>I',raw[offset:offset+4])[0]
                if raw[offset+4:offset+8]==b'IDAT':chunks.append(raw[offset+8:offset+8+size])
                offset+=12+size
            first=zlib.decompress(b''.join(chunks))[:481]
            self.assertEqual(set(first[1:]),{0},file.name)
            self.assertLess(len(raw),40000)

    def test_user_approved_status_assets_are_unchanged(self):
        import hashlib
        expected={
            'status-green':'3295bdbd000c309b6fc8da1c4af8433fa7d730b8cb3c95319f5b374f65404477',
            'status-red':'a428de7ec9d2d338d286dd2c5ea419e197e8f9a74729dc6d20628bdac4bc1443',
        }
        for name,digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT/'images'/('system-'+name+'.png')).read_bytes()).hexdigest(),digest)

if __name__=='__main__':unittest.main()
