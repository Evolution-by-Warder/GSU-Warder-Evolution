import importlib
import json
from pathlib import Path
import unittest
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
load(ROOT)
network=importlib.import_module('Plugins.Extensions.GlassSysUtil.warder_network')
i18n=importlib.import_module('Plugins.Extensions.GlassSysUtil.i18n')

class Probe:
    def entries(self,path,limit):return ['lo','eth0','wlan0','../bad']
    def text(self,path,limit):
        return {'/sys/class/net/eth0/operstate':'up',
                '/sys/class/net/eth0/speed':'1000',
                '/sys/class/net/wlan0/operstate':'down',
                '/sys/class/net/wlan0/speed':'-1',
                '/proc/net/route':'Iface Destination Gateway Flags RefCnt Use Metric Mask\neth0 00000000 0101A8C0 0003 0 0 0 00000000',
                '/etc/resolv.conf':'nameserver 192.168.1.1\nnameserver invalid\nnameserver 2001:db8::1'}.get(path,'')

class NetworkTests(unittest.TestCase):
    def test_local_network_values_and_missing_speed(self):
        result=network.collect(Probe())
        self.assertEqual(result['gateways'],['192.168.1.1'])
        self.assertEqual(result['dns'],['192.168.1.1','2001:db8::1'])
        self.assertEqual(result['interfaces'],[{'name':'eth0','state':'up','speed':1000},{'name':'wlan0','state':'down','speed':None}])
        self.assertIn('1000 Mb/s',network.summary(result,lambda x:x))
    def test_centre_translation_coverage(self):
        data=json.loads((ROOT/'locale/centres.json').read_text(encoding='utf-8'))
        self.assertEqual(set(data),set(i18n.LANGUAGES))
        for lang in i18n.LANGUAGES:
            self.assertEqual(set(data[lang]),set(data['en']))
            for key,value in data[lang].items():
                self.assertTrue(value)
                self.assertEqual(i18n.translate(key,lang),value)
