"""Installed About notes stay offline, localized and bound to their version."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('release_notes_contracts',ROOT/'release_history.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


class ReleaseNotesTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.path=Path(self.temp.name)/'notes.json'
        self.path.write_text(json.dumps({'version':'0.1.12','notes':{'sk':'Slovenské zmeny','en':'English changes'}}))

    def test_uses_installed_notes_and_normalizes_system_language(self):
        self.assertEqual(module.load_notes(self.path,'0.1.12','sk_SK'),'Slovenské zmeny')
        self.assertEqual(module.load_notes(self.path,'0.1.12','en-GB'),'English changes')

    def test_unsupported_language_falls_back_to_english(self):
        self.assertEqual(module.load_notes(self.path,'0.1.12','nl_NL'),'English changes')

    def test_version_blocks_are_separated_limited_to_five_and_localized(self):
        data={'version':'0.1.12','notes':{'en':'latest'},'entries':[
            {'version':'0.1.'+str(v),'notes':{'sk':'Zmena '+str(v),'en':'Change '+str(v)}} for v in range(12,6,-1)]}
        self.path.write_text(json.dumps(data))
        text=module.load_notes(self.path,'0.1.12','sk_SK')
        self.assertEqual(text.count('GSU '),5)
        self.assertEqual(text.count('────────────────────────'),4)
        self.assertIn('Zmena 12',text)
        self.assertIn('0.1.8',text)
        self.assertNotIn('0.1.7',text)

    def test_each_history_description_fits_two_lines_and_keeps_full_source_notes(self):
        data={'version':'0.1.12','notes':{'en':'latest'},'entries':[
            {'version':'0.1.12','date':'2026-11-02','notes':{'en':'Long release description ' * 30}}]}
        original=json.dumps(data);self.path.write_text(original)
        text=module.load_notes(self.path,'0.1.12','sk_SK')
        lines=text.splitlines()
        self.assertIn('2026-11-02',lines[0])
        self.assertEqual(len(lines),3)
        self.assertTrue(lines[-1].endswith('…'))
        self.assertTrue(all(len(line)<=72 for line in lines[1:]))
        self.assertEqual(self.path.read_text(),original)

    def test_notes_from_another_version_are_never_displayed(self):
        self.assertEqual(module.load_notes(self.path,'0.1.11','sk'),'')
        self.assertEqual(module.load_notes(self.path,'0.1.13','sk'),'')

    def test_missing_or_invalid_notes_do_not_break_about(self):
        for content in ('bad json','[]','{"version":"0.1.12","notes":[]}',
                        '{"version":"0.1.12","notes":{"sk":42}}'):
            self.path.write_text(content)
            self.assertEqual(module.load_notes(self.path,'0.1.12','sk'),'')
        self.path.unlink()
        self.assertEqual(module.load_notes(self.path,'0.1.12','sk'),'')
