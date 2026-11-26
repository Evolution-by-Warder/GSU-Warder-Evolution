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
            for mode in ('menu','overview','chart','multichart','detail','process','categories','network'):
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


    def test_centre_inline_result_keeps_navigation_and_ignores_stale_worker(self):
        ui=self.ui
        session=MagicMock()
        menu=ui.CentreMenu(session,self.api,[('system-overview','System health check','memory'),
                   ('system-log','Log view','log')],{'system-overview':True,'system-log':True},'system')
        menu.render()
        with patch.object(ui,'deferToThread') as worker:
            menu.select()
            self.assertEqual(worker.call_count,1)
            self.assertEqual(menu['result_status'].getText(),mod('i18n').for_api(menu.api,'Loading…'))
            old=worker.return_value.addCallbacks.call_args.args[0]
            menu['list'].moveToIndex(1)
            menu.describe()
            menu.select()
            self.assertEqual(worker.call_count,1)
            old({'values':(99,10,0,20,None,50),'health':{'score':100,'coverage':(2,2)}})
            self.assertEqual(worker.call_count,2)
            done=worker.return_value.addCallbacks.call_args.args[0]
            done('Kernel log content')
            self.assertEqual(menu['descriptions'].getText(),'Kernel log content')
            session.open.assert_not_called()
            menu.full_result()
            session.open.assert_called_once_with(ui.Report,self.api,'system-log','Log view')
            session.open.reset_mock()
            menu.refresh_result()
            late=worker.return_value.addCallbacks.call_args.args[0]
            menu.close_results()
            late('stale')
            self.assertNotEqual(menu['descriptions'].getText(),'stale')
        menu.full_result()
        session.open.assert_not_called()

    def test_menu_panels_are_disjoint_and_backings_cannot_cover_result(self):
        for w,h in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            root=ET.fromstring(mod('warder_dashboard').skin(w,h,'menu'))
            left=root.find("widget[@name='list']")
            right=root.find("widget[@name='descriptions']")
            x,y=map(int,left.get('position').split(','))
            lw,lh=map(int,left.get('size').split(','))
            rx,ry=map(int,right.get('position').split(','))
            rw,rh=map(int,right.get('size').split(','))
            self.assertLess(x+lw,rx)
            for n in root:
                if n.tag not in ('eLabel','ePixmap'):continue
                nx,ny=map(int,n.get('position').split(','))
                nw,nh=map(int,n.get('size').split(','))
                if nx<rx+rw and nx+nw>rx and ny<ry+rh and ny+nh>ry:
                    self.assertLess(int(n.get('zPosition','0')),0,n.attrib)


    def test_live_system_dashboard_binds_six_real_metrics_and_one_sampler(self):
        chart=mod('warder_chart')
        screen=chart.LiveChart(MagicMock(),self.api)
        samples=[(10,{'cpu':None,'ram':18,'swap':0,'temp':78.9,'rx':None,'tx':None}),
                 (12,{'cpu':62,'ram':19,'swap':0,'temp':79.4,'rx':2048,'tx':1024})]
        screen.source=MagicMock()
        screen.source.history.snapshot.return_value=samples
        with patch.object(chart,'draw_trend') as draw:
            screen.render()
        self.assertEqual(screen.source.history.snapshot.call_count,1)
        self.assertEqual(draw.call_count,6)
        self.assertEqual([call.args[2] for call in draw.call_args_list],[key for key,_,_ in chart.SYSTEM])
        self.assertEqual([screen['metric_value%d'%i].getText() for i in range(6)],
                         ['62.0 %','19.0 %','0.0 %','79.4 °C','2.0 KiB/s','1.0 KiB/s'])
        self.assertEqual(screen['stat_value0_0'].getText(),'62.0')
        self.assertEqual(screen['stat_value1_2'].getText(),'18.5')
        screen.source.history.snapshot.return_value=[]
        screen.render()
        self.assertEqual(screen['metric_value0'].getText(),'— %')
        self.assertEqual(screen['stat_value0_0'].getText(),'—')

    def test_trends_do_not_connect_missing_or_old_samples(self):
        chart=mod('warder_chart')
        canvas=MagicMock()
        chart.draw_trend(canvas,[(0,{'cpu':10}),(2,{'cpu':None}),(4,{'cpu':20}),
                                (6,{'cpu':30}),(20,{'cpu':40})],'cpu',30,12,100,2)
        canvas.line.assert_called_once()
        for call in canvas.fill.call_args_list:
            x,y,w,h,_=call.args
            self.assertGreaterEqual(min(x,y),0)
            self.assertLessEqual(x+w,30)
            self.assertLessEqual(y+h,12)
        canvas.flush.assert_called_once()


    def test_centre_and_project_rows_include_cached_navigation_picons(self):
        ui=self.ui
        api=dict(self.api,LoadPixmap=MagicMock(return_value=object()))
        menu=ui.CentreMenu(MagicMock(),api,[('system-overview','System health check','health'),
                             ('system-log','Log view','log')],{'system-overview':True,'system-log':True},'system')
        menu.render()
        for row in menu['list'].l.list:
            self.assertEqual(len(row),3)
            self.assertIn('png',row[2])
        menu.render()
        self.assertEqual(api['LoadPixmap'].call_count,2)
        projects=ui.ProjectMenu(MagicMock(),api)
        projects.render()
        self.assertEqual(len(projects['list'].l.list),5)
        self.assertTrue(all(len(row)==3 for row in projects['list'].l.list))


    def test_inline_system_cards_show_real_values_and_clear_on_navigation(self):
        ui=self.ui
        menu=ui.CentreMenu(MagicMock(),self.api,[('system-overview','System health check','health'),
            ('system-log','Log view','log')],{'system-overview':True,'system-log':True},'system')
        menu.render()
        value={'values':(62,18,0,29,465*1073741824,79.4),
               'disk_mount':'/media/hdd','temperature_source':'/sys/class/thermal/cpu',
               'health':{'score':100,'coverage':(2,2),'state':'ok'}}
        with patch.object(ui,'deferToThread') as worker:
            menu.select()
            worker.return_value.addCallbacks.call_args.args[0](value)
            self.assertTrue(menu.cards_visible)
            self.assertFalse(menu['descriptions'].visible)
            self.assertEqual([menu['inline_value%d'%i].getText() for i in range(6)],
                ['62 %','18 %','0 %','29 %','465.0 GiB','79.4 °C'])
            self.assertTrue(menu['inline_meter2'].visible)
            self.assertFalse(menu['inline_meter4'].visible)
            self.assertEqual(menu['inline_note4'].getText(),'/media/hdd')
            self.assertEqual(menu['inline_note5'].getText(),'cpu')
            self.assertIn('100/100',menu['inline_summary'].getText())
            menu.refresh_result()
            self.assertFalse(menu.cards_visible)
            callback=worker.return_value.addCallbacks.call_args.args[0]
            callback(dict(value,values=(None,18,0,29,None,None)))
            self.assertEqual(menu['inline_value0'].getText(),'—')
            self.assertFalse(menu['inline_meter0'].visible)
            menu['list'].moveToIndex(1)
            menu.describe()
            self.assertFalse(menu.cards_visible)
            self.assertTrue(menu['descriptions'].visible)
            self.assertFalse(menu['inline_bg0'].visible)

    def test_inline_storage_cards_do_not_show_percentages_for_partial_scans(self):
        ui=self.ui
        names=('Picons','Skins','Plugins','EPG','Cache','Logs')
        complete=[(n,1048576,True) for n in names]
        cards,summary=ui.card_result('storage-categories',complete,str)
        self.assertEqual(cards[0],('Picons','1.0 MiB',17,''))
        partial=complete[:-1]+[('Logs',0,False)]
        cards,summary=ui.card_result('storage-categories',partial,str)
        self.assertTrue(all(c[2] is None for c in cards))
        self.assertEqual(cards[-1],('Logs','—',None,'Partial result'))
        self.assertIn('≥ 5.0 MiB',summary)
        self.assertIn('Partial result',summary)

    def test_inline_card_widgets_stay_within_the_right_panel(self):
        for w,h in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            root=ET.fromstring(mod('warder_dashboard').skin(w,h,'menu'))
            area=root.find("widget[@name='descriptions']")
            ax,ay=map(int,area.get('position').split(','))
            aw,ah=map(int,area.get('size').split(','))
            for widget in root.findall('widget'):
                if not widget.get('name','').startswith('inline_'):continue
                x,y=map(int,widget.get('position').split(','))
                ww,hh=map(int,widget.get('size').split(','))
                self.assertGreaterEqual(x,ax)
                self.assertGreaterEqual(y,ay)
                self.assertLessEqual(x+ww,ax+aw)
                self.assertLessEqual(y+hh,ay+ah)


    def test_project_logo_provenance_and_optional_radio_fallback(self):
        import hashlib
        import json
        import tempfile
        from pathlib import Path
        icons=mod('warder_menu_icons')
        manifest=json.loads((ROOT.parents[1]/'artwork/warder-project-logos.json').read_text())
        for name,path in (('fullhdglass','project-fullhdglass.png'),('piconhub','project-piconhub.png'),
                          ('youtube','project-youtube.png'),('gsu','warder-plugin.png')):
            raw=(ROOT/'images'/path).read_bytes()
            blob=hashlib.sha1(('blob %d\0'%len(raw)).encode()+raw).hexdigest()
            self.assertEqual(blob,manifest[name]['blob_sha'])
        api=dict(self.api,LoadPixmap=MagicMock(return_value=object()))
        icons.cached.cache_clear()
        icons.project_cached.cache_clear()
        with tempfile.TemporaryDirectory() as folder:
            radio=Path(folder)/'plugin.png'
            with patch.dict(icons.PROJECT_ASSETS,{'Warder Radio':radio}):
                entry=icons.pixmap_entry(api,'Warder Radio',(0,0),(120,58),project=True)
                self.assertIsNotNone(entry)
                api['LoadPixmap'].assert_called_once_with(path=str(ROOT/'images/nav-signal.png'),cached=True)
                radio.write_bytes(b'fixture')
                icons.project_cached.cache_clear()
                api['LoadPixmap'].reset_mock()
                entry=icons.pixmap_entry(api,'Warder Radio',(0,0),(120,58),project=True)
                self.assertIsNotNone(entry)
                api['LoadPixmap'].assert_called_once_with(path=str(radio),cached=True)
        icons.cached.cache_clear()
        icons.project_cached.cache_clear()
