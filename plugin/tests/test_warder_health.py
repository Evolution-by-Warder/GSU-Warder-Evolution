import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src/GlassSysUtil"))
from warder_health import resource_check,health_summary

class HealthTests(unittest.TestCase):
    def test_thresholds_and_invalid_values(self):
        for free,state in [(20,"ok"),(10,"warning"),(1,"critical"),(-1,"unknown"),(101,"unknown")]:
            self.assertEqual(resource_check("flash",100,free)["state"],state)
        self.assertEqual(resource_check("ram",0,0)["state"],"unknown")
    def test_coverage(self):
        known=resource_check("ram",100,50)
        unknown=resource_check("flash",None,None)
        self.assertEqual(health_summary([known,unknown])["coverage"],(1,2))
        self.assertEqual(health_summary([known,unknown])["state"],"unknown")
        self.assertIsNone(health_summary([unknown])["score"])
        self.assertEqual(health_summary([known,resource_check("flash",100,1)])["state"],"critical")
