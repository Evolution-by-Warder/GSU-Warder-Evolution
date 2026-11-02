"""Reported OpenPLi startup failure with a strict eLabel surface."""
import unittest
from types import SimpleNamespace
from pathlib import Path
from receiver_stubs import load

class OpenPliLabel:
    def __init__(self):self.nowrap=None
    def setNoWrap(self,value):self.nowrap=value

class LabelApiTests(unittest.TestCase):
    def test_ecm_startup_layout_handles_both_modes_without_setwrap(self):
        plugin=load(Path(__file__).resolve().parents[1]/'src/GlassSysUtil')
        for names in [('OSD_Ecm_info',),('OSD_Ecm_info','ecm_items')]:
            screen={name:SimpleNamespace(instance=OpenPliLabel()) for name in names}
            plugin.OnScreenEcmScreen.prepareOsd(screen)
            for widget in screen.values():self.assertEqual(widget.instance.nowrap,1)
    def test_oscam_detail_layout_uses_the_same_native_no_wrap_contract(self):
        import importlib.util
        path=Path(__file__).resolve().parents[1]/'src/GlassSysUtil/oscam_clients_ui.py'
        import ast
        tree=ast.parse(path.read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='prepare')
        scope={};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(path),'exec'),scope)
        screen={'status_%s_%d'%(kind,index):SimpleNamespace(instance=OpenPliLabel()) for index in range(3) for kind in ('labels','values')}
        scope['prepare'](screen)
        for widget in screen.values():self.assertEqual(widget.instance.nowrap,1)
