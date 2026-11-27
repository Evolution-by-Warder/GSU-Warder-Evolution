"""Regression contracts for the modern stable publication path, no network writes."""
import copy
import json
import runpy
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
publisher=runpy.run_path(str(ROOT/'compatibility/publish-modern.py'))

class ModernPublisherTests(unittest.TestCase):
    def setUp(self):
        self.previous=json.loads((ROOT/'plugin/update/stable-modern.json').read_text())
        self.prior=self.previous['release']
        self.record=json.loads((ROOT/'PRODUCTION.json').read_text())
        self.feed=copy.deepcopy(self.previous)
        self.feed['release'].update(version='0.41.9999',tag='v0.41.9999',
            url='https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/releases/download/v0.41.9999/enigma2-plugin-extensions-gsu_0.41.9999_all.ipk',
            sha256='a'*64)

    def test_forward_release_requires_exact_active_predecessor(self):
        verify=publisher['verified_predecessor']
        self.assertEqual(verify(self.previous,self.record,self.feed,self.prior),self.prior)
        for changed in ({},dict(self.record,release=dict(self.prior,sha256='b'*64))):
            with self.assertRaises(ValueError):
                verify(self.previous,changed,self.feed,self.prior)
        with self.assertRaises(ValueError):
            verify(self.previous,self.record,self.feed,dict(self.prior,sha256='c'*64))
        with self.assertRaises(ValueError):
            verify(self.previous,self.record,self.previous,self.prior)

    def test_readme_preflight_changes_only_current_release_references(self):
        previous=self.prior['version']
        version=publisher['VERSION']
        item=dict(self.feed['release'],notes_i18n={'sk':'Opravy zobrazenia.'})
        old=(ROOT/'README.md').read_text()
        rendered=publisher['render_readme'](old,previous,item)
        self.assertIn('## Stabilné vydanie '+version,rendered)
        self.assertIn(publisher['URL'],rendered)
        self.assertIn('13.41-r6',rendered)
        self.assertIn('Opravy zobrazenia.',rendered)
        with self.assertRaises(ValueError):
            publisher['render_readme']('Unrecognized README',previous,item)

    def test_runtime_release_request_and_notes_agree(self):
        version=publisher['VERSION']
        self.assertEqual((ROOT/'plugin/update/release-request').read_text().strip(),version)
        data=json.loads((ROOT/'plugin/update/RELEASE-NOTES.i18n.json').read_text())
        self.assertEqual(data['version'],version)
        self.assertEqual(data['entries'][0]['version'],version)
        self.assertEqual(set(data['notes']),publisher['LANGS'])
        self.assertTrue(all(data['notes'].values()))
