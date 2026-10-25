import importlib.util
from pathlib import Path
import types
import unittest
from xml.etree import ElementTree
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('osd_layout_test',ROOT/'osd_layout.py')
layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)


class OsdLayoutTests(unittest.TestCase):
    def test_scrolling_strip_uses_half_screen_width_and_keeps_text_size_in_all_resolutions(self):
        for filename,width in (('GSU_skins.py',1280),('GSU_skins_FHD.py',1920),('GSU_skins_UHD.py',3840)):
            namespace={};exec(compile((ROOT/filename).read_text(),filename,'exec'),namespace)
            original=ElementTree.fromstring(namespace['onScreenEcm_scr'])
            result=ElementTree.fromstring(layout.rolling_skin(namespace['onScreenEcm_scr'],width))
            self.assertEqual(int(result.get('size').split(',')[0]),width//2)
            self.assertLessEqual(int(result.get('position').split(',')[0])+width//2,width)
            before=next(n for n in original if n.get('name')=='OSD_Ecm_info')
            after=next(n for n in result if n.get('name')=='OSD_Ecm_info')
            self.assertEqual(after.get('font'),before.get('font'))
            self.assertGreater(int(after.get('size').split(',')[0]),int(before.get('size').split(',')[0]))
            self.assertEqual(len([n for n in result if n.tag=='eLabel']),2)

    def test_overlay_and_position_preview_use_identical_wide_skin(self):
        plugin=load(ROOT);settings=plugin.config.plugins.GlassSysUtil;previous=settings.par3.value
        try:
            settings.par3.value=False
            with patch.object(plugin,'eTimer',return_value=MagicMock()),patch.object(plugin,'iPlayableService',types.SimpleNamespace(evStopped=1,evTunedIn=2)):
                overlay=plugin.OnScreenEcmScreen(types.SimpleNamespace())
                preview=plugin.SelectPosition(types.SimpleNamespace())
            self.assertEqual(overlay.skin,preview.skin)
            self.assertEqual(ElementTree.fromstring(overlay.skin).get('size').split(',')[0],'960')
        finally:settings.par3.value=previous

    def test_display_clamps_without_saving_old_coordinates_and_editor_updates_them(self):
        settings=types.SimpleNamespace(par1=types.SimpleNamespace(value=1030),par2=types.SimpleNamespace(value=2000))
        screen=types.SimpleNamespace(instance=types.SimpleNamespace(size=lambda:types.SimpleNamespace(width=lambda:960,height=lambda:51),move=MagicMock()))
        api={'config':types.SimpleNamespace(plugins=types.SimpleNamespace(GlassSysUtil=settings)),
             'getDesktop':lambda i:types.SimpleNamespace(size=lambda:types.SimpleNamespace(width=lambda:1920,height=lambda:1080)),
             'ePoint':lambda x,y:(x,y)}
        layout.place(screen,api);screen.instance.move.assert_called_with((960,1029))
        self.assertEqual((settings.par1.value,settings.par2.value),(1030,2000))
        layout.place(screen,api,editing=True)
        self.assertEqual((settings.par1.value,settings.par2.value),(960,1029))
