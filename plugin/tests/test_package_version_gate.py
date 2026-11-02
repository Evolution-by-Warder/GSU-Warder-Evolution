"""A package builder must reject versions its installed updater cannot read."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

BASE=Path(__file__).parents[1]
spec=importlib.util.spec_from_file_location('version_gate_builder',BASE/'tools/build_ipk.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)

class PackageVersionGateTests(unittest.TestCase):
    def test_unknown_version_fails_before_packaging_or_publication(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            if hasattr(builder,'RUNTIME'):
                runtime=root/'runtime';runtime.mkdir()
                (runtime/'version.txt').write_text('0.1.39-unknown1\n')
                (runtime/'warder_update.py').write_bytes((builder.RUNTIME/'warder_update.py').read_bytes())
                attribute,value='RUNTIME',runtime
            else:
                runtime=root/'src/GlassSysUtil';runtime.mkdir(parents=True)
                (runtime/'version').write_text('13.40-r95-unknown1\n')
                (runtime/'plugin_update.py').write_bytes((builder.BASE/'src/GlassSysUtil/plugin_update.py').read_bytes())
                attribute,value='BASE',root
            with patch.object(builder,attribute,value),self.assertRaisesRegex(ValueError,'Invalid .*version'):
                builder.build(root/'out')
            self.assertFalse((root/'out').exists())

if __name__=='__main__':unittest.main()
