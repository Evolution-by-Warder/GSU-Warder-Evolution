"""Production helpers keep routine diagnostics out of disk and console logs."""
import ast
import contextlib
import importlib.util
import io
from pathlib import Path
import types
import unittest
from unittest.mock import patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'


class CleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.plugin=load(ROOT)

    def test_legacy_logger_has_no_side_effects(self):
        with patch('builtins.open',side_effect=AssertionError('Unexpected log write')),contextlib.redirect_stdout(io.StringIO()) as output:
            self.plugin.Writelog('routine event')
        self.assertEqual(output.getvalue(),'')

    def test_autostart_logger_creates_no_file_or_stdout(self):
        spec=importlib.util.spec_from_file_location('quiet_autostart',ROOT/'native_autostart.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with patch.object(module.os,'open',side_effect=AssertionError('Unexpected file')),contextlib.redirect_stdout(io.StringIO()) as output:
            module.log_event('autocheck running')
        self.assertEqual(output.getvalue(),'')

    def test_bitrate_output_still_updates_ui_without_diagnostic_writes(self):
        screen=self.plugin.channelInfoCenter(types.SimpleNamespace())
        with patch('builtins.open',side_effect=AssertionError('Unexpected bitrate log')):
            screen.dataAvail(b'100 200 150 180\n20 40 30 32\n')
        self.assertIn('180',screen['bit_act'].text)
        self.assertIn('32',screen['bit_act'].text)

    def test_dmesg_collection_is_memory_only(self):
        screen=self.plugin.GlassSysInfoBrowser(types.SimpleNamespace())
        with patch.object(self.plugin,'_commandLines',return_value=[' kernel message ']) as command,patch('builtins.open',side_effect=AssertionError('Unexpected temporary file')):
            self.assertEqual(screen.getDmesg(),'kernel message\n')
        command.assert_called_once_with(['dmesg'])

    def test_no_automatic_file_logging_in_bitrate_callbacks(self):
        tree=ast.parse((ROOT/'plugin.py').read_text())
        cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='channelInfoCenter')
        for method in cls.body:
            if isinstance(method,ast.FunctionDef) and method.name in ('startBitrate','dataAvail'):
                self.assertFalse(any(isinstance(n,ast.Constant) and n.value=='/tmp/gsu-bitrate.log' for n in ast.walk(method)))
