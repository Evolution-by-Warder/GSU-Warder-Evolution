import importlib
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'

class SystemLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin=load(ROOT)
        cls.ui=cls.plugin._warder_system

    def test_preserves_every_system_component_and_scroll_area_at_all_resolutions(self):
        header={'day','date','clock','seconds','version_title','version'}
        for suffix,w,h in (('',1280,720),('_FHD',1920,1080),('_UHD',3840,2160)):
            original=importlib.import_module('Plugins.Extensions.GlassSysUtil.GSU_skins'+suffix).GlassSysInfo
            old=ET.fromstring(original);root=ET.fromstring(self.ui.system_skin(original,w,h))
            before={n.get('name') for n in old if n.get('name')}
            after={n.get('name') for n in root if n.get('name')}
            self.assertEqual(after,before|header)
            self.assertEqual(root.get('backgroundColor'),'#00071627')
            self.assertFalse(root.findall("widget[@render='Pig']"))
            # Native ScrollLabel applies zPosition to its labels, leaving its
            # parent at zero. Every full-screen backing must stay below zero.
            for backing in root:
                if backing.tag=='eLabel' and int(backing.get('size','0,0').split(',')[1])>h//2:
                    self.assertLess(int(backing.get('zPosition','0')),0)
            self.assertEqual(root.find('ePixmap').get('zPosition'),'-3')
            for name in before-{'red','green','yellow'}:
                n=root.find("widget[@name='%s']"%name)
                y=int(n.get('position').split(',')[1]);height=int(n.get('size').split(',')[1])
                self.assertGreaterEqual(y,round(180*h/1080))
                self.assertLessEqual(y+height,round(980*h/1080))
            for name in ('ProccessInfo','DmesgInfo'):
                n=root.find("widget[@name='%s']"%name)
                self.assertEqual(n.get('transparent'),'1')
                self.assertEqual(n.get('backgroundColor'),'#00102136')

    def test_larger_device_icons_fit_reserved_slots_and_lower_meters_share_bottoms(self):
        for suffix,w,h in (('',1280,720),('_FHD',1920,1080),('_UHD',3840,2160)):
            source=importlib.import_module('Plugins.Extensions.GlassSysUtil.GSU_skins'+suffix).GlassSysInfo
            old=ET.fromstring(source);root=ET.fromstring(self.ui.system_skin(source,w,h))
            pictures=[n for n in root if n.tag=='ePixmap' and '/system-' in n.get('pixmap','') and 'status' not in n.get('pixmap','')]
            devices=[n for n in pictures if not n.get('pixmap').endswith(('system-lr.png','system-updown.png'))]
            originals=[n for n in old if '/devices/' in n.get('pixmap','')]
            self.assertEqual(len(devices),len(originals))
            for before,after in zip(originals,devices):
                x,y=map(int,before.get('position').split(','));iw,ih=map(int,before.get('size').split(','))
                nx,ny=map(int,after.get('position').split(','));nw,nh=map(int,after.get('size').split(','))
                slot_y=round((190+(y/(h/1080)-75)*.84)*(h/1080))
                self.assertEqual(nw,nh)
                self.assertGreater(nw,iw)
                self.assertLessEqual(abs((nx+nw/2)-(x+iw/2)),1)
                self.assertGreaterEqual(ny,slot_y)
                self.assertLessEqual(ny+nh,slot_y+round(ih*.84))
            lower=[n for n in devices if int(n.get('position').split(',')[1])>700*h/1080]
            for name in ('hddtempbar','hddstate','cpubar','tempDBbar'):
                meter=root.find("widget[@name='%s']"%name)
                mx,my=map(int,meter.get('position').split(','));mw,mh=map(int,meter.get('size').split(','))
                icon=min((n for n in lower if int(n.get('position').split(',')[0])>mx),key=lambda n:int(n.get('position').split(',')[0])-mx)
                ix,iy=map(int,icon.get('position').split(','));iw,ih=map(int,icon.get('size').split(','))
                self.assertLess(mx+mw,ix)
                self.assertEqual(my+mh,iy+ih)
                backing=[n for n in root if n.get('pixmap','').endswith('/barm_back.png') and n.get('position')==meter.get('position')]
                self.assertEqual(len(backing),1)
                self.assertEqual(backing[0].get('size'),meter.get('size'))

if __name__=='__main__':unittest.main()

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

    def test_every_system_picture_is_mapped_to_a_shipped_asset_without_distortion(self):
        plugin=load(ROOT)
        for suffix,w,h in (('',1280,720),('_FHD',1920,1080),('_UHD',3840,2160)):
            old=importlib.import_module('Plugins.Extensions.GlassSysUtil.GSU_skins'+suffix).GlassSysInfo
            root=ET.fromstring(plugin._warder_system.system_skin(old,w,h))
            found=0
            for n in root:
                path=n.get('pixmap','')
                self.assertNotIn('/devices/',path)
                self.assertNotIn('/bp_icons/',path)
                if '/system-' not in path:continue
                self.assertTrue((ROOT/'images'/Path(path).name).is_file())
                self.assertEqual(n.get('scale'),'1')
                if n.tag=='ePixmap' and 'status' not in path:
                    iw,ih=map(int,n.get('size').split(','));self.assertEqual(iw,ih)
                found+=1
            self.assertGreaterEqual(found,20)

    def test_user_approved_status_assets_are_unchanged(self):
        import hashlib
        expected={
            'status-green':'3295bdbd000c309b6fc8da1c4af8433fa7d730b8cb3c95319f5b374f65404477',
            'status-red':'a428de7ec9d2d338d286dd2c5ea419e197e8f9a74729dc6d20628bdac4bc1443',
        }
        for name,digest in expected.items():
            self.assertEqual(hashlib.sha256((ROOT/'images'/('system-'+name+'.png')).read_bytes()).hexdigest(),digest)
