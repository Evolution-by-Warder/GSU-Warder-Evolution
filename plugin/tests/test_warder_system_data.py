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


    def test_selected_process_pss_is_separate_from_rss_and_identity_checked(self):
        from unittest.mock import patch
        p=Probe()
        original=p.text
        p.text=lambda path,limit:('Rss: 2048 kB\nPss: 1024 kB\nPrivate_Dirty: 512 kB'
                                  if path=='/proc/12/smaps_rollup' else original(path,limit))
        with patch.object(data,'process_ticks',side_effect=[(12,1),(12,3)]):
            report=data.process_memory(12,'enigma2',str,p)
            self.assertIn('Rss   2.00 MiB',report)
            self.assertIn('Pss   1.00 MiB',report)
            self.assertIn('SwapPss   —',report)
        with patch.object(data,'process_ticks',side_effect=[(12,1),(13,3)]):
            self.assertEqual(data.process_memory(12,'enigma2',str,p),'Unavailable')
        with patch.object(data,'process_ticks',return_value=(12,1)):
            self.assertEqual(data.process_memory(12,'other',str,p),'Unavailable')
