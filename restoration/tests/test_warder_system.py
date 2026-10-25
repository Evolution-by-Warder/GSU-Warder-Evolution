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
            for name in before-{'red','green','yellow'}:
                n=root.find("widget[@name='%s']"%name)
                y=int(n.get('position').split(',')[1]);height=int(n.get('size').split(',')[1])
                self.assertGreaterEqual(y,round(180*h/1080))
                self.assertLessEqual(y+height,round(980*h/1080))
            for name in ('ProccessInfo','DmesgInfo'):
                n=root.find("widget[@name='%s']"%name)
                self.assertEqual(n.get('transparent'),'0')
                self.assertEqual(n.get('backgroundColor'),'#00102136')

if __name__=='__main__':unittest.main()
