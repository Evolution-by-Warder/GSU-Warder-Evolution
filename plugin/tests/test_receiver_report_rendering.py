"""Regression for physical receiver reports: native ScrollLabel parent is at z=0."""
from pathlib import Path
import importlib
import unittest
from unittest.mock import MagicMock,patch
from xml.etree import ElementTree as ET
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
def mod(name):
    return importlib.import_module('Plugins.Extensions.GlassSysUtil.'+name)

class ReceiverRenderingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api=vars(load(ROOT))
        cls.ui=mod('warder_centre_ui')

    def test_all_dashboard_backings_behind_native_scroll_container(self):
        for width,height in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            root=ET.fromstring(mod('warder_dashboard').skin(width,height,'detail'))
            target=root.find("widget[@name='file_info']")
            x,y=map(int,target.get('position').split(','))
            w,h=map(int,target.get('size').split(','))
            # Native OpenATV ScrollLabel.applySkin forwards zPosition only to
            # its child eLabels. The eWidget container stays at layer zero.
            for node in root:
                if node.tag not in ('eLabel','ePixmap'):continue
                nx,ny=map(int,node.get('position').split(','))
                nw,nh=map(int,node.get('size').split(','))
                if nx<x+w and nx+nw>x and ny<y+h and ny+nh>y:
                    self.assertLess(int(node.get('zPosition','0')),0,(width,height,node.attrib))
            for name in ('red','green','yellow','blue'):
                self.assertEqual(root.find("widget[@name='%s']"%name).get('noWrap'),'1')

    def test_blank_translation_bypasses_real_legacy_catalogue_metadata(self):
        i18n=mod('i18n')
        fake=MagicMock(return_value='Project-Id-Version: GSU')
        api=dict(self.api,_=fake)
        for lang in i18n.LANGUAGES:
            with patch.object(i18n,'catalog',side_effect=AssertionError('empty text must bypass catalogue')):
                self.assertEqual(i18n.translate('',lang),'')
                self.assertEqual(i18n.for_api(api,''),'')
        fake.assert_not_called()

    def test_every_report_route_displays_data_or_explicit_state(self):
        routes=mod('warder_centres').DIAGNOSTICS
        kinds={'system-processes','system-log','tuner-details','transponder-services',
               'storage-overview','storage-categories','network-overview','network-test',
               'service-health','service-ipk','forum-report'}
        for kind in kinds:
            with self.subTest(kind=kind):
                session=MagicMock()
                self.ui.open_diagnostic(session,self.api,kind)
                session.open.assert_called_once_with(self.ui.Report,self.api,kind,routes[kind][0])
                report=self.ui.Report(session,self.api,kind,routes[kind][0])
                self.assertEqual(report['green'].getText(),report.tr('TV') if kind=='transponder-services' else '')
                report.done('Receiver content')
                self.assertIn('Receiver content',report['file_info'].getText())
                for value in ('',None,'   '):
                    report.done(value)
                    self.assertEqual(report['file_info'].getText(),report.tr('Unavailable'))
                report.failed(None)
                self.assertEqual(report['file_info'].getText(),report.tr('Unavailable'))
                report.cancelled.set()
                report.done('late')
                self.assertNotIn('late',report['file_info'].getText())
        self.assertEqual(set(routes)-kinds,{'projects','signal-quick','system-overview','system-live','signal-live','tuner-native'})

    def test_all_five_project_reports_share_visible_layout_and_empty_state(self):
        for project in mod('warder_projects').PROJECTS:
            report=self.ui.ProjectReport(MagicMock(),self.api,project)
            self.assertEqual(report['green'].getText(),'')
            report.done('Version 1.0.0')
            self.assertIn('Version 1.0.0',report['file_info'].getText())
            report.done(None)
            self.assertEqual(report['file_info'].getText(),report.tr('Unavailable'))

    def test_ram_card_title_does_not_expose_or_wrap_memory_basis(self):
        screen=mod('warder_overview').Overview(MagicMock(),self.api)
        screen.done({'values':[2,44,None,70,None,48], 'basis':'MemAvailable',
                     'health':{'state':'ok','score':100,'coverage':(2,2)}})
        self.assertNotIn('MemAvailable',screen['label1'].getText())
        self.assertEqual(screen['value1'].getText(),'44 %')

    def test_worker_routes_call_the_correct_provider(self):
        cases=(
            ('system-processes','warder_system_data','detail_text','processes'),
            ('system-log','warder_system_data','detail_text','log'),
            ('storage-overview','warder_storage','report',None),
            ('storage-categories','warder_storage','report',None),
            ('network-test','warder_network','diagnostics',None),
            ('service-health','warder_service','health',None),
            ('service-ipk','warder_ipk','review',None),
        )
        for kind,module,method,argument in cases:
            with self.subTest(kind=kind):
                report=self.ui.Report(MagicMock(),self.api,kind,'Overview')
                with patch.object(mod(module),method,return_value='provider data') as provider:
                    report.done(report.collect())
                    provider.assert_called_once()
                    if argument is not None:
                        self.assertEqual(provider.call_args.args[0],argument)
                    if kind.startswith('storage-'):
                        self.assertEqual(provider.call_args.args[-1],kind=='storage-categories')
                    self.assertIn('provider data',report['file_info'].getText())
        report=self.ui.Report(MagicMock(),self.api,'network-overview','Overview')
        with patch.object(mod('warder_network'),'collect',return_value={'fixture':1}) as collect, patch.object(mod('warder_network'),'summary',return_value='network data') as summary:
            report.done(report.collect())
            collect.assert_called_once()
            self.assertEqual(summary.call_args.args[0],{'fixture':1})
            self.assertIn('network data',report['file_info'].getText())
        report=self.ui.Report(MagicMock(),self.api,'forum-report','Overview')
        with patch.object(mod('warder_service'),'forum_snapshot',return_value={'schema':2}) as snapshot:
            report.done(report.collect())
            snapshot.assert_called_once()
            self.assertIn('"schema": 2',report.preview)

    def test_native_routes_collect_on_gui_thread(self):
        report=self.ui.Report(MagicMock(),self.api,'tuner-details','Overview')
        with patch.object(mod('warder_tuners'),'details',return_value='Tuner fixture') as provider:
            report.start()
            provider.assert_called_once()
            self.assertEqual(report['file_info'].getText(),'Tuner fixture')
        report=self.ui.Report(MagicMock(),self.api,'transponder-services','Overview')
        with patch.object(mod('warder_services'),'services',return_value=[('tv','ref','Channel fixture')]) as provider:
            report.start()
            provider.assert_called_once()
            self.assertEqual(report['file_info'].getText(),'Channel fixture')
