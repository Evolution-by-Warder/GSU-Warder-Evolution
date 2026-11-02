"""Native API geometry contracts for the plugin-scoped Screen, without hardware."""
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

RUNTIME = Path(__file__).parents[1] / 'src'
TARGET = next(RUNTIME.rglob('warder_screen.py'))

class Size:
    def __init__(self,w,h):self.w,self.h=w,h
    def width(self):return self.w
    def height(self):return self.h

class Listbox:
    orVertical,orHorizontal,orGrid=1,2,3
    def __init__(self,h=615,row=45):self.dim=Size(1560,h);self.row=row;self.orientation=1
    def getOrientation(self):return self.orientation
    def getItemHeight(self):return self.row
    def size(self):return self.dim
    def resize(self,value):self.dim=value

class NativeScreen(dict):
    def applySkin(self):
        for callback in getattr(self,'callbacks',[]):callback()
        return 'native-result'
    def show(self):return 'shown'

native=ModuleType('Screens.Screen');native.Screen=NativeScreen
engine=ModuleType('enigma');engine.eListbox=Listbox;engine.eSize=Size
with patch.dict(sys.modules,{'Screens.Screen':native,'enigma':engine}):
    spec=importlib.util.spec_from_file_location('isolated_viewport_contracts',TARGET)
    ui=importlib.util.module_from_spec(spec);spec.loader.exec_module(ui)

class ViewportTests(unittest.TestCase):
    def component(self,h=615,row=45,**attrs):
        return SimpleNamespace(instance=Listbox(h,row),skinAttributes=list(attrs.items()))
    def test_allocation_is_reused_when_row_height_changes(self):
        c=self.component();self.assertTrue(ui.fit(c));self.assertEqual(c.instance.size().height(),585)
        c.instance.row=60;ui.fit(c);self.assertEqual(c.instance.size().height(),600)
        c.instance.row=45;ui.fit(c);self.assertEqual(c.instance.size().height(),585)
    def test_repeated_show_does_not_shrink_or_change_selection_data(self):
        c=self.component();c.list=['a','b'];screen=ui.Screen();screen['list']=c
        for unused in range(10):self.assertEqual(screen.show(),'shown')
        self.assertEqual(c.instance.size().height(),585);self.assertEqual(c.list,['a','b'])
    def test_native_layout_callbacks_finish_before_fit(self):
        c=self.component();screen=ui.Screen();screen['list']=c
        screen.callbacks=[lambda:setattr(c.instance,'row',60)]
        self.assertEqual(screen.applySkin(),'native-result')
        self.assertEqual(c.instance.size().height(),600)
        self.assertEqual(NativeScreen.applySkin.__qualname__,'NativeScreen.applySkin')
    def test_new_instance_and_resized_allocation_are_detected(self):
        c=self.component();ui.fit(c);c.instance=Listbox(700,48);ui.fit(c)
        self.assertEqual(c.instance.size().height(),672)
        c.instance.resize(Size(1600,800));ui.fit(c);self.assertEqual(c.instance.size().height(),768)
    def test_grid_horizontal_and_spaced_widgets_keep_native_packing(self):
        for orientation in (2,3):
            c=self.component();c.instance.orientation=orientation
            self.assertFalse(ui.fit(c));self.assertEqual(c.instance.size().height(),615)
        c=self.component(itemSpacing='0,4');self.assertFalse(ui.fit(c))
    def test_missing_geometry_and_oversize_rows_are_left_usable(self):
        self.assertFalse(ui.fit(SimpleNamespace(instance=None)))
        c=self.component(h=20,row=45);self.assertFalse(ui.fit(c));self.assertEqual(c.instance.size().height(),20)

if __name__=='__main__':unittest.main()
