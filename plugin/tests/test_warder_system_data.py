import importlib
from pathlib import Path
import types
import unittest
from receiver_stubs import load
ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
load(ROOT)
data=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_system_data')

class Probe:
    def path(self,path):return path
    def usage(self,path):return types.SimpleNamespace(total=100,free=4)
    def entries(self,path,limit):return ['12','not-a-pid']
    def text(self,path,limit):
        return {'/proc/meminfo':'MemTotal: 1000 kB\nMemAvailable: 600 kB',
                '/proc/12/comm':'enigma2',
                '/proc/12/status':'State: S (sleeping)\nVmRSS: 32 kB'}.get(path,'')

class SystemDataTests(unittest.TestCase):
    def test_overview_pressure_and_coverage(self):
        result=data.overview(Probe())
        self.assertEqual(result['health']['state'],'critical')
        self.assertEqual(result['health']['coverage'],(2,2))
        self.assertEqual(result['health']['score'],50)
    def test_process_details_use_rss(self):
        self.assertEqual(data.processes(Probe()),[(12,'enigma2','S',32)])
    def test_log_bounds_and_failure(self):
        self.assertEqual(len(data.system_log(lambda *a,**k:types.SimpleNamespace(returncode=0,stdout=b'x'*70000))),65536)
        self.assertIsNone(data.system_log(lambda *a,**k:types.SimpleNamespace(returncode=1,stdout=b'')))
