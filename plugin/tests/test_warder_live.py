import importlib
from pathlib import Path
import unittest
from receiver_stubs import load
ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
load(ROOT)
live=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_live')

class Probe:
    def __init__(self):self.n=1
    def text(self,path,limit):
        n=self.n
        return {'/proc/stat':'cpu %d 0 %d %d'%(10*n,10*n,80*n),
                '/proc/meminfo':'MemTotal: 100 kB\nMemAvailable: 60 kB\nSwapTotal: 20 kB\nSwapFree: 10 kB',
                '/proc/net/dev':'eth0: %d 0 0 0 0 0 0 0 %d 0 0 0 0 0 0 0'%(100*n,200*n)}.get(path,'')

class LiveTests(unittest.TestCase):
    def test_deltas_and_reset(self):
        p=Probe();t=[0];s=live.Sampler(p,lambda:t[0])
        first=s.sample()
        self.assertIsNone(first['cpu'])
        self.assertEqual(first['ram'],40)
        self.assertEqual(first['swap'],50)
        p.n=2;t[0]=2
        second=s.sample()
        self.assertEqual(second['cpu'],20)
        self.assertEqual(second['rx'],50)
        self.assertEqual(second['tx'],100)
        self.assertEqual(live.statistics(s.history.snapshot(),'cpu'),(20,20,20))
        s.reset()
        self.assertIsNone(s.sample()['cpu'])
    def test_absent_swap_unknown(self):
        self.assertIsNone(live.used(0,0))
        self.assertIsNone(live.used(100,None))
