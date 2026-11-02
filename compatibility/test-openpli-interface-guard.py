#!/usr/bin/env python3
"""Prove that the OpenPLi gate detects invalid imports and call keywords."""
from pathlib import Path
import runpy
import tempfile
import unittest
CHECK=runpy.run_path(str(Path(__file__).with_name('check-openpli-interfaces.py')))

class GuardTests(unittest.TestCase):
    def scan(self,source,native='class List:\n def __init__(self, items, session=None): pass\n'):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);plugin=root/'plugin';plugin.mkdir();upstream=root/'upstream';(upstream/'Components').mkdir(parents=True)
            (upstream/'Components/ConfigList.py').write_text(native)
            (plugin/'plugin.py').write_text(source)
            return CHECK['scan'](plugin,upstream)
    def test_valid_native_keyword_is_accepted(self):
        result=self.scan('from Components.ConfigList import List\nList([],session=None)')
        self.assertEqual(result['calls_checked'],1);self.assertEqual(result['invalid_calls'],[])
    def test_invalid_native_keyword_is_rejected(self):
        result=self.scan('from Components.ConfigList import List\nList([],fullUI=True)')
        self.assertEqual(len(result['invalid_calls']),1)
    def test_missing_required_parameter_is_rejected(self):
        self.assertEqual(len(self.scan('from Components.ConfigList import List\nList()')['invalid_calls']),1)
    def test_missing_module_and_export_are_rejected(self):
        self.assertEqual(len(self.scan('from Components.Absent import List')['missing_imports']),1)
        self.assertEqual(len(self.scan('from Components.ConfigList import Absent')['missing_imports']),1)
    def test_importerror_fallback_is_reported_separately(self):
        result=self.scan('try:\n from Components.Absent import List\nexcept ImportError:\n pass')
        self.assertEqual(result['missing_imports'],[]);self.assertEqual(len(result['guarded_imports']),1)
    def test_finally_does_not_hide_missing_import(self):
        result=self.scan('try:\n from Components.Absent import List\nfinally:\n pass')
        self.assertEqual(len(result['missing_imports']),1)

if __name__=='__main__':unittest.main()
