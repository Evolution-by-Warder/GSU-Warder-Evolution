import importlib.util
import pathlib
import unittest
from xml.etree import ElementTree as ET

ROOT=pathlib.Path(__file__).resolve().parents[1]/'src/GlassSysUtil'

def module(name):
    spec=importlib.util.spec_from_file_location('cam_menu_test_'+name,ROOT/(name+'.py'))
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


class CamMenuTests(unittest.TestCase):
    def test_retired_row_removed_without_gap_at_all_three_resolutions(self):
        compact=module('cam_menu').compact_skin
        for name in ('GSU_skins','GSU_skins_FHD','GSU_skins_UHD'):
            with self.subTest(resolution=name):
                skin=module(name).UCM
                old=ET.fromstring(skin);new=ET.fromstring(compact(skin))
                before={e.get('name'):e for e in old if e.get('name')}
                after={e.get('name'):e for e in new if e.get('name')}
                self.assertNotIn('txt5',after)
                self.assertEqual(set(after),set(before)-{'txt5'})
                previous='txt5'
                for current in ('txt6','txt7','txt8','txt9'):
                    self.assertEqual(after[current].get('position'),before[previous].get('position'))
                    previous=current
                for current in set(after)-{'txt6','txt7','txt8','txt9'}:
                    self.assertEqual(after[current].attrib,before[current].attrib)

    def test_compaction_is_idempotent(self):
        compact=module('cam_menu').compact_skin
        skin=module('GSU_skins_FHD').UCM
        self.assertEqual(compact(compact(skin)),compact(skin))


if __name__=='__main__':unittest.main()
