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
            ('system-log','warder_system_data','detail_text','log'),
            ('storage-overview','warder_storage','report',None),
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
                    if kind=='storage-overview':
                        self.assertIs(provider.call_args.args[-1],False)
                    self.assertIn('provider data',report['file_info'].getText())
        report=self.ui.Report(MagicMock(),self.api,'network-overview','Overview')
        with patch.object(mod('warder_network'),'collect',return_value={'fixture':1}) as collect, patch.object(mod('warder_network'),'overview_panels',return_value=('network data','connection data')) as panels:
            report.done(report.collect())
            collect.assert_called_once_with(include_addresses=True)
            self.assertEqual(panels.call_args.args[0],{'fixture':1})
            self.assertTrue(report.network_visible)
            self.assertEqual(report['network_body0'].getText(),'network data')
            self.assertEqual(report['network_body1'].getText(),'connection data')
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
            self.assertIn('Channel fixture',report['file_info'].getText())
            self.assertIn('TV  ·  1',report['file_info'].getText())

    def test_process_table_and_category_rows_are_bound_to_measured_values(self):
        ui=self.ui
        report=ui.Report(MagicMock(),self.api,'system-processes','Process Info')
        rows=[(42,'enigma2','S',1536,12.5),(7,'kernel','R',None,None)]
        with patch.object(mod('warder_system_data'),'process_table',return_value=rows) as provider:
            report.done(report.collect())
            provider.assert_called_once_with(report.cancelled,False)
        self.assertTrue(report.table_visible)
        content=report['process_list'].l.list
        self.assertEqual(content[0][0],42)
        self.assertEqual([entry['text'] for entry in content[0][1:]],['42','enigma2','S','1.5','12.5'])
        self.assertEqual([entry['text'] for entry in content[1][-2:]],['—','—'])
        report.done([])
        self.assertFalse(report.table_visible)
        self.assertEqual(report['file_info'].getText(),report.tr('Unavailable'))

        report=ui.Report(MagicMock(),self.api,'storage-categories','Space by category')
        rows=[('Picons',1048576,True),('Skins',1048576,True),('Plugins',0,True),
              ('EPG',0,True),('Cache',0,True),('Logs',0,False)]
        with patch.object(mod('warder_storage'),'category_snapshot',return_value=rows) as provider:
            report.done(report.collect())
            provider.assert_called_once_with()
        self.assertEqual(report['category_size0'].getText(),'1.0 MiB')
        self.assertEqual(report['category_state5'].getText(),report.tr('Partial result'))
        self.assertIn('2.0 MiB',report['report_status'].getText())
        self.assertIn(report.tr('Partial result'),report['report_status'].getText())

    def test_header_lifecycle_preserves_footer_and_version(self):
        report=self.ui.Report(MagicMock(),self.api,'network-overview','Network overview')
        header=report._diagnostic_header
        header.timer=MagicMock()
        footer=report['yellow'].getText()
        header.prepare()
        self.assertEqual(report['version'].getText(),(ROOT/'version').read_text().strip())
        self.assertEqual(report['yellow'].getText(),footer)
        self.assertTrue(report['clock'].getText())
        header.suspend()
        header.timer.stop.assert_called()
        header.cleanup()
        header.timer.reset_mock()
        header.resume()
        header.timer.start.assert_not_called()

    def test_new_modes_fit_all_resolutions_and_keep_native_backings_behind_content(self):
        view=mod('warder_dashboard')
        for w,h in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            for mode in ('menu','overview','chart','detail','process','categories','network'):
                root=ET.fromstring(view.skin(w,h,mode))
                names=[n.get('name') for n in root if n.get('name')]
                self.assertEqual(len(names),len(set(names)),mode)
                for n in root:
                    x,y=map(int,n.get('position').split(','))
                    width,height=map(int,n.get('size').split(','))
                    self.assertGreaterEqual(min(x,y),0,(mode,n.attrib))
                    self.assertGreater(min(width,height),0,(mode,n.attrib))
                    self.assertLessEqual(x+width,w,(mode,n.attrib))
                    self.assertLessEqual(y+height,h,(mode,n.attrib))
                for name in ('day','date','clock','seconds','version_title','version'):
                    self.assertIn(name,names)
                if mode in ('detail','process','categories','network'):
                    target=root.find("widget[@name='file_info']")
                    x,y=map(int,target.get('position').split(','))
                    tw,th=map(int,target.get('size').split(','))
                    for n in root:
                        if n.tag not in ('eLabel','ePixmap'):continue
                        nx,ny=map(int,n.get('position').split(','))
                        nw,nh=map(int,n.get('size').split(','))
                        if nx<x+tw and nx+nw>x and ny<y+th and ny+nh>y:
                            self.assertLess(int(n.get('zPosition','0')),0,(mode,n.attrib))

    def test_forum_preview_is_readable_and_retains_exact_export(self):
        import json
        report=self.ui.Report(MagicMock(),self.api,'forum-report','Forum report')
        snapshot={'schema':2,'gsu':'0.41.5','python':[3,14],'architecture':'aarch64',
                  'available_percent':{'RAM':55.2,'Flash':None},'temperature_c':48.0,
                  'crash_classes':['TypeError']}
        raw=json.dumps(snapshot)
        report.done(raw)
        shown=report['file_info'].getText()
        self.assertIn('3.14',shown)
        self.assertIn('55.2 %',shown)
        self.assertIn('48.0 °C',shown)
        self.assertIn('TypeError',shown)
        self.assertEqual(report.preview,raw)
        self.assertNotIn('"available_percent"',shown)
        raw_unknown=json.dumps(dict(snapshot,extra='not hidden'))
        report.done(raw_unknown)
        self.assertEqual(report['file_info'].getText(),raw_unknown)

    def test_transponder_preview_separates_tv_and_radio_without_mutation(self):
        rows=[('tv','ref1','TV station'),('radio','ref2','Radio station')]
        expected=list(rows)
        value=mod('warder_services').display(rows,str)
        self.assertIn('TV  ·  1',value)
        self.assertIn('Radio  ·  1',value)
        self.assertIn('Radio station',value)
        self.assertEqual(rows,expected)
        self.assertEqual(mod('warder_services').display([],str),'Unavailable')

    def test_network_panels_keep_actual_addresses_and_missing_data(self):
        network=mod('warder_network')
        data={'interfaces':[{'name':'eth0','state':'up','speed':1000,'addresses':['192.0.2.1','2001:db8::1']}],
              'gateways':['192.0.2.254'],'dns':[],'network_mounts':0}
        left,right=network.overview_panels(data,str)
        self.assertIn('1000 Mb/s',left)
        self.assertIn('2001:db8::1',left)
        self.assertIn('192.0.2.254',right)
        self.assertIn('—',right)
        report=self.ui.Report(MagicMock(),self.api,'network-overview','Network overview')
        report.done((left,right))
        self.assertTrue(report.network_visible)
        report.scroll(1,True)
        self.assertEqual(report.network_focus,1)
        report.done(None)
        self.assertFalse(report.network_visible)
        self.assertEqual(report['file_info'].getText(),report.tr('Unavailable'))

    def test_diagnostic_descriptions_are_explanatory_in_all_languages(self):
        centres=mod('warder_centres')
        i18n=mod('i18n')
        for lang in i18n.LANGUAGES:
            tr=lambda key:i18n.translate(key,lang)
            for ident,(_,hint) in centres.DIAGNOSTICS.items():
                value=centres.description(ident,tr,tr(hint))
                self.assertNotEqual(value,tr(hint),(lang,ident))
                self.assertGreater(len(value),15,(lang,ident))
                self.assertNotIn('%s',value)
        value=centres.description('system-overview',lambda k:i18n.translate(k,'sk'))
        self.assertIn('CPU',value)
        self.assertIn('teplotu',value)
        self.assertIn('flash',value)
