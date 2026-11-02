"""Updater startup and immutable release records without optional dataclasses."""
import builtins
import importlib.util
import io
import json
from pathlib import Path
import re
import runpy
import ssl
import subprocess
import sys
import tarfile
import tempfile
from unittest import TestCase
from unittest.mock import patch
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
PICON=ROOT/'src/Plugins/Extensions/WarderPiconHub/warder_update.py'
SCRIPT=PICON if PICON.exists() else ROOT/'src/GlassSysUtil/plugin_update.py'

class MinimalPythonUpdateTests(TestCase):
    def load_without_dataclasses(self):
        original=builtins.__import__
        def minimal(name,*args,**kwargs):
            if name=='dataclasses' or name.startswith('dataclasses.'):
                raise ModuleNotFoundError("No module named 'dataclasses'")
            return original(name,*args,**kwargs)
        with patch('builtins.__import__',side_effect=minimal):
            return runpy.run_path(str(SCRIPT))

    def test_updater_import_and_feed_parser_need_no_dataclasses(self):
        updater=self.load_without_dataclasses()
        picon=SCRIPT.name=='warder_update.py'
        version='0.1.39-test3' if picon else '13.41-r2'
        updater['version_key'](version)
        feed={'schema':1,'product':'PiconHub Warder Evolution' if picon else 'Glass System Utility Warder Evolution','channel':'stable' if picon else 'original-python314','release':None}
        self.assertIsNone(updater['parse_release'](json.dumps(feed),version))

    def test_release_fields_are_immutable_and_default_notes_are_independent(self):
        Release=self.load_without_dataclasses()['Release']
        first=Release('1','url','a'*64,3);second=Release('1','url','a'*64,3)
        first.notes_i18n['sk']='test'
        self.assertEqual(second.notes_i18n,{})
        self.assertEqual(first.notes,'')
        self.assertEqual(first.bytes,3)
        with self.assertRaises(AttributeError):first.version='changed'
        self.assertIsNone(Release('1','url','a'*64,3,notes_i18n=None).notes_i18n)
