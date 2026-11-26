import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src/GlassSysUtil"))
from warder_centres import legacy_routes
from warder_telemetry import cpu_counters,cpu_percent,memory_values,network_counters,network_rates,History

class CentreTests(unittest.TestCase):
    def test_all_legacy_actions_preserved_once(self):
        ids = "0 1 2 3 4 6 7 8 9 17 16 future".split()
        entries = [(i,i,"description") for i in ids]
        groups = legacy_routes(entries)
        self.assertEqual(sorted(e[0] for _,_,g in groups for e in g),sorted(ids))
        self.assertEqual(groups[-1][0],"other")
        with self.assertRaises(ValueError):
            legacy_routes(entries+entries[:1])

class TelemetryTests(unittest.TestCase):
    def test_cpu(self):
        self.assertEqual(cpu_percent(cpu_counters("cpu 10 0 10 80"),cpu_counters("cpu 20 0 20 160")),20)
        self.assertIsNone(cpu_percent((100,80),(90,70)))
        self.assertIsNone(cpu_counters("cpu bad"))
        self.assertIsNone(cpu_percent(None,(100,80)))
    def test_memory(self):
        m=memory_values("MemTotal: 1000 kB\nMemFree: 100 kB\nMemAvailable: 600 kB\nSwapTotal: 0 kB\nSwapFree: 0 kB")
        self.assertEqual(m["ram_available"],600*1024)
        self.assertEqual(m["ram_basis"],"MemAvailable")
        self.assertEqual(memory_values("MemFree: 50 kB")["ram_basis"],"MemFree")
        self.assertIsNone(memory_values("")["ram_total"])
        self.assertIsNone(memory_values("MemTotal: 1 kB\nMemAvailable: 2 kB")["ram_available"])
    def test_network(self):
        a=network_counters("eth0: 100 0 0 0 0 0 0 0 200 0 0 0 0 0 0 0")
        self.assertEqual(network_rates(a,{"eth0":(120,240)},2),{"eth0":(10,20)})
        self.assertEqual(network_rates(a,{"eth0":(1,2)},2),{})
        self.assertEqual(network_rates(a,a,0),{})
    def test_history(self):
        t=[0]
        h=History(seconds=60,capacity=2,clock=lambda:t[0])
        for i in range(3):
            t[0]=i;h.append({"cpu":i})
        self.assertEqual(len(h.snapshot()),2)
        t[0]=63
        self.assertEqual(h.snapshot(),())
