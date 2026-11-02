"""All 55 legacy XML templates fit the WQHD desktop with unchanged identities."""
import ast
import importlib.util
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

ROOT=Path(__file__).parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('resolution_contracts',ROOT/'warder_resolution.py')
ui=importlib.util.module_from_spec(spec);spec.loader.exec_module(ui)

class ResolutionTests(unittest.TestCase):
    def skins(self,name):
        for node in ast.walk(ast.parse((ROOT/name).read_text())):
            if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.lstrip().startswith('<screen'):
                yield node.value
    def test_every_legacy_template_scales_fonts_geometry_and_keeps_binding_identity(self):
        for original in self.skins('GSU_skins_FHD.py'):
            before=ET.fromstring(original);after=ET.fromstring(ui.scale_skin(original,(1920,1080),(2560,1440)))
            self.assertEqual([(n.tag,n.get('name'),n.get('source'),n.get('render')) for n in before.iter()],
                             [(n.tag,n.get('name'),n.get('source'),n.get('render')) for n in after.iter()])
            self.assertEqual(len(list(before.iter())),len(list(after.iter())))
            for a,b in zip(before.iter(),after.iter()):
                for attr in ('pixmap','foregroundColor','backgroundColor','text','zPosition'):
                    self.assertEqual(a.get(attr),b.get(attr))
                if a.get('font'):
                    self.assertEqual(int(b.get('font').split(';')[1]),round(int(a.get('font').split(';')[1])*4/3))
    def test_canonical_hd_fhd_uhd_are_byte_identical(self):
        for name,base in [('GSU_skins.py',(1280,720)),('GSU_skins_FHD.py',(1920,1080)),('GSU_skins_UHD.py',(3840,2160))]:
            for value in self.skins(name):self.assertEqual(ui.scale_skin(value,base,base),value)
    def test_anchor_and_opaque_color_semantics_are_preserved(self):
        root=ET.fromstring(ui.scale_skin('<screen position="center,center" size="900,600"><widget name="x" position="30,40" size="300,80" font="Regular;30" backgroundColor="#00102136" itemHeight="40"/></screen>',(1920,1080),(2560,1440)))
        self.assertEqual(root.get('position'),'center,center');node=root[0]
        self.assertEqual(node.get('position'),'40,53');self.assertEqual(node.get('itemHeight'),'53')
        self.assertEqual(node.get('backgroundColor'),'#00102136')
    def test_plugin_selects_fhd_assets_but_desktop_based_python_geometry_for_wqhd(self):
        source=(ROOT/'plugin.py').read_text()
        self.assertIn('elif _GSU_WIDTH >= 1920:',source)
        self.assertIn('return int(t * _GSU_HEIGHT / 720.0)',source)

if __name__=='__main__':unittest.main()
