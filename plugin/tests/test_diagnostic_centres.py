from pathlib import Path
import csv
import importlib
import json
import os
from tempfile import TemporaryDirectory
from threading import Event
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch
from xml.etree import ElementTree as ET
from receiver_stubs import load

ROOT = Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
api = vars(load(ROOT))


def module(name):
    return importlib.import_module('Plugins.Extensions.GlassSysUtil.'+name)


class DiagnosticTests(unittest.TestCase):
    def test_remote_tuner_selection_is_passive_and_hides_unrelated_current_service(self):
        tuner=module('warder_tuners')
        from Components.NimManager import nimmanager
        class Slot:
            slot=1
            def getSlotName(self):return 'Tuner B'
            def getFriendlyFullDescription(self):return 'DVB-T2 receiver'
            def getTunerTypesEnabled(self):return ['DVB-T','DVB-T2']
        nav=MagicMock()
        nav.getCurrentService.return_value.frontendInfo.return_value.getAll.return_value={'tuner_number':0,'frequency':123456}
        nav.getRecordings.return_value=[]
        with patch.object(nimmanager,'nim_slots',[Slot()],create=True):
            self.assertEqual(tuner.slots(),[('Tuner B',1)])
            value=tuner.details(SimpleNamespace(nav=nav),api,str,1)
        self.assertIn('DVB-T / DVB-T2',value)
        self.assertNotIn('123456',value)
        nav.stopService.assert_not_called()
        nav.playService.assert_not_called()

    def test_network_probes_distinguish_feed_failure_from_external_failure(self):
        network=module('warder_network')
        probe=MagicMock()
        probe.text.return_value=''
        net={'interfaces':[],'gateways':['192.0.2.1'],'dns':[]}
        def web(url,timeout):
            if url!='https://warder-evolution.eu/':
                raise OSError()
            result=MagicMock()
            result.__enter__.return_value.geturl.return_value=url
            result.__enter__.return_value.read.return_value=b'<'
            return result
        with patch.object(network,'collect',return_value=net),patch.object(network,'ping',return_value=(0,1.0)):
            self.assertIn('Internet reachable',network.diagnostics(str,Event(),probe,web))
            self.assertIn('Gateway reachable; external checks failed',network.diagnostics(str,Event(),probe,MagicMock(side_effect=OSError)))
        cancel=Event();cancel.set();opener=MagicMock()
        self.assertEqual(network.diagnostics(str,cancel,probe,opener),'')
        opener.assert_not_called()

    def test_backup_recreates_native_files_privately_and_ignores_settings(self):
        from hashlib import sha256
        backup = module('warder_scan_backup')
        with TemporaryDirectory() as d:
            root=Path(d)/'enigma2';root.mkdir()
            original={'lamedb':b'new\x00lines','userbouquet.favourites.tv':b'#NAME Favourite'}
            for name,value in original.items():
                (root/name).write_bytes(value)
            (root/'settings').write_bytes(b'private')
            saved=Path(backup.create(root,d))
            checks=json.loads((saved/'SHA256.json').read_text())
            self.assertEqual(set(checks),set(original))
            self.assertEqual(saved.stat().st_mode & 0o777,0o700)
            for name,value in original.items():
                self.assertEqual((saved/name).read_bytes(),value)
                self.assertEqual(checks[name],sha256(value).hexdigest())
            (root/'userbouquet.link.tv').symlink_to(root/'settings')
            with self.assertRaises(OSError):
                backup.create(root,d)
            self.assertEqual(len(list(Path(d).glob('gsu-channel-backup-*'))),1)

    def test_native_package_database_handles_alternative_and_virtual_dependencies(self):
        packages=module('warder_package_status')
        with TemporaryDirectory() as d:
            root=Path(d);db=root/'var/lib/opkg/status';db.parent.mkdir(parents=True)
            db.write_text('Package: receiver\nStatus: install user installed\nDepends: bad | enigma2 (>= 5), skin\nArchitecture: all\n\nPackage: enigma2\nStatus: hold ok installed\nVersion: 6\nProvides: skin\n')
            records,manager=packages.database(root)
            compare=MagicMock(return_value=True)
            self.assertEqual(packages.dependency_state('receiver',records,manager,compare),'Ready')
            compare.assert_called_once_with('opkg','6','>=','5')
            self.assertEqual(packages.dependency_state('receiver',records,manager,lambda *a:False),'Check plugin dependencies')
            self.assertEqual(packages.dependency_state('missing',records,manager),'Unavailable')

    def test_hisilicon_sensor_only_accepts_explicit_temperature(self):
        tools=module('warder_tools')
        with TemporaryDirectory() as d:
            probe=tools.Probe(d);path=probe.path('/proc/hisi/msp/pm_cpu');path.parent.mkdir(parents=True)
            path.write_text('CPU clock = 1800 MHz\nCPU temperature = 61 C\n')
            self.assertEqual([s['celsius'] for s in probe.temperatures(probe.sensor_paths())],[61])
            path.write_text('CPU clock = 42 MHz\n')
            self.assertEqual(probe.temperatures(probe.sensor_paths()),[])

    def test_project_selection_and_canonical_update_status(self):
        ui=module('warder_centre_ui')
        projects=module('warder_projects')
        session=MagicMock()
        menu=ui.ProjectMenu(session,api)
        self.assertEqual([r[0] for r in menu.entries()],[p[0] for p in projects.PROJECTS])
        menu['list'].getCurrent=lambda:['GSU'];menu.select()
        session.open.assert_called_once_with(ui.ProjectReport,api,projects.PROJECTS[-1])
        view=ui.ProjectReport(session,api,projects.PROJECTS[-1])
        view.update_status('checking')
        self.assertEqual(view['file_info'].text,'checking')
        self.assertEqual(view.readVersion(),(ROOT/'version').read_text().strip())
        with patch.object(module('plugin_update_ui'),'StartupUpdateCheck') as updater:
            view.action();view.action()
        updater.assert_called_once_with(view,api)
        self.assertEqual(updater.return_value.request.call_count,2)

    def test_every_new_layout_fits_and_binds(self):
        layouts = module('warder_dashboard')
        for w, h in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            for mode, widget in [('menu','list'),('detail','file_info'),('chart','metric')]:
                root = ET.fromstring(layouts.skin(w,h,mode))
                self.assertIsNotNone(root.find("widget[@name='%s']" % widget))
                for element in root:
                    x,y = map(int,element.get('position').split(','))
                    width,height = map(int,element.get('size').split(','))
                    self.assertGreaterEqual(min(x,y),0)
                    self.assertGreater(min(width,height),0)
                    self.assertLessEqual(x+width,w)
                    self.assertLessEqual(y+height,h)

    def test_current_frontend_units_unknown_service_and_loss_count(self):
        radio = module('warder_signal')
        status = {'tuner_signal_quality':65535, 'tuner_signal_power':0, 'tuner_locked':True,
                  'tuner_bit_error_rate':3, 'tuner_signal_quality_db':1283}
        nav = MagicMock()
        service = nav.getCurrentService.return_value
        fe = service.frontendInfo.return_value
        fe.getFrontendStatus.return_value = status
        ref = nav.getCurrentlyPlayingServiceReference.return_value
        ref.toString.return_value = 'service-a'
        monitor = radio.SignalMonitor(nav)
        v = monitor.sample()
        self.assertAlmostEqual(v['snr'],100)
        self.assertEqual((v['agc'],v['db'],v['ber'],v['lock']),(0,12.83,3,1))
        status['tuner_locked'] = False
        monitor.sample()
        self.assertEqual(radio.lock_losses(monitor.history.snapshot()),1)
        nav.getCurrentService.return_value = None
        ref.toString.return_value = 'other'
        monitor.sample()
        self.assertEqual(len(monitor.history.snapshot()),1)
        self.assertTrue(all(v is None for v in monitor.history.snapshot()[0][1].values()))
        self.assertIsNone(radio.measurements({'tuner_signal_quality_db':0x12345678})['db'])
        nav.stopService.assert_not_called()
        with TemporaryDirectory() as temp:
            p=Path(radio.export(monitor.history.snapshot(),temp))
            self.assertEqual(p.stat().st_mode & 0o777,0o600)
            self.assertNotIn('other',p.read_text())
            self.assertEqual(len(list(csv.reader(p.read_text().splitlines()))),2)

    def test_live_worker_close_and_no_overlapping_measurements(self):
        chart = module('warder_chart')
        screen = chart.LiveChart(MagicMock(),api)
        screen.timer = MagicMock()
        with patch.object(chart,'deferToThread') as defer:
            screen.tick()
            screen.tick()
            defer.assert_called_once()
            screen.cleanup()
            screen.complete(None)
            screen.tick()
            screen.timer.start.assert_not_called()
            screen.timer.stop.assert_called_once()
        canvas = MagicMock()
        chart.draw(canvas,[(0,{'cpu':None}),(1,{'cpu':0}),(2,{'cpu':55})],'cpu',20,12,100)
        for item in canvas.fill.call_args_list:
            x,y,w,h,_ = item.args
            self.assertLessEqual(x+w,20)
            self.assertLessEqual(y+h,12)
        canvas.flush.assert_called_once()

    def test_storage_hardlinks_nested_mounts_symlinks_bounds(self):
        storage = module('warder_storage')
        with TemporaryDirectory() as tmp:
            p = storage.Probe(tmp)
            root = p.path('/usr/share/enigma2')
            icons = root/'picon'
            icons.mkdir(parents=True)
            (icons/'a').write_bytes(b'x'*8192)
            os.link(icons/'a',icons/'b')
            (root/'linked').symlink_to(icons, target_is_directory=True)
            (root/'foreign').mkdir()
            (root/'foreign/big').write_bytes(b'y'*65536)
            table = [('host:/','/usr/share/enigma2/foreign','nfs',False)]
            totals = storage.usage_categories(p,table)
            self.assertEqual(totals['Picons'],((icons/'a').stat().st_blocks*512,True))
            self.assertEqual(totals['Skins'],(0,True))
            self.assertFalse(all(complete for value,complete in storage.usage_categories(p,table,budget=1).values()))
        with patch.object(storage.shutil,'which',return_value='smartctl'):
            runner = MagicMock(return_value=SimpleNamespace(stdout='SMART overall-health self-assessment test result: PASSED',returncode=0))
            self.assertEqual(storage.smart('/dev/sda1',runner),('PASSED',None))
            self.assertIn('standby',runner.call_args.args[0])
            self.assertIsNone(storage.smart('/dev/unknown',runner))

    def test_tuner_actions_fail_closed_and_recheck_after_confirmation(self):
        tuner = module('warder_tuners')
        nav = MagicMock()
        nav.getCurrentService.return_value = None
        nav.getRecordings.return_value = []
        nav.getAnyRecordingsCount.return_value = 0
        nav.RecordTimer.getNextRecordingTime.return_value = 1200
        self.assertFalse(tuner.recording_safe(nav,lambda:1000))
        nav.RecordTimer.getNextRecordingTime.return_value = -1
        self.assertTrue(tuner.recording_safe(nav))
        self.assertFalse(tuner.recording_safe(object()))
        session = MagicMock(nav=nav)
        action = MagicMock()
        from Screens.MessageBox import MessageBox
        with patch.object(MessageBox,'TYPE_YESNO',0,create=True), patch.object(MessageBox,'TYPE_INFO',1,create=True), patch.object(tuner,'native_tools',return_value=[('satfinder',action)]):
            tuner.choose_native(session,lambda k:k)
            session.openWithCallback.call_args.args[0](('satfinder',action))
            confirm = session.openWithCallback.call_args.args[0]
            confirm(False)
            nav.getRecordings.return_value = [object()]
            confirm(True)
            action.assert_not_called()

    def test_forum_report_allowlist_preview_and_private_mode(self):
        service = module('warder_service')
        data = {'checks':[{'name':'RAM','available_percent':51.768},{'name':'Flash','available_percent':None},
                          {'name':'private','available_percent':0}], 'gateway':'secret','logs':'secret'}
        with patch.object(service,'overview',return_value=data):
            preview=json.dumps(service.forum_snapshot())
        cleaned=json.loads(preview)
        self.assertEqual(set(cleaned),{'schema','gsu','python','architecture','available_percent','temperature_c','crash_classes'})
        self.assertEqual(cleaned['schema'],2)
        self.assertEqual(cleaned['available_percent'],{'RAM':51.8,'Flash':None})
        self.assertNotIn('secret',preview)
        with TemporaryDirectory() as d:
            out=Path(service.save_preview(preview,d))
            self.assertEqual(out.read_text(),preview+'\n')
            self.assertEqual(out.stat().st_mode & 0o777,0o600)

    def test_project_feeds_validate_exact_origin_and_identity(self):
        projects = module('warder_projects')
        for p in projects.PROJECTS:
            name,repo,path,identity,pkg,prefix,tag_prefix=p
            version='0.41.5'
            tag=tag_prefix+version
            if identity:
                item={'tag':tag,'version':version,'url':projects.RELEASES+repo+'/releases/download/'+tag+'/'+prefix+'_'+version+'_all.ipk',
                      'bytes':200,'sha256':'a'*64,'notes':'Release','notes_i18n':{'sk':'Vydanie'}}
                feed={'schema':1,'product':identity,'channel':'stable-modern' if name=='GSU' else 'stable','release':item}
            else:
                item=feed={'version':version,'package_url':projects.RAW+repo+'/main/packages/'+prefix+'_'+version+'_all.ipk',
                           'sha256':'a'*64,'changelog':'Release','changelog_i18n':{'sk':'Vydanie'}}
            self.assertEqual(projects.release(p,json.dumps(feed),'sk'),(version,'Vydanie'))
            item['url' if identity else 'package_url']='https://example.invalid/file.ipk'
            with self.assertRaises(ValueError):
                projects.release(p,json.dumps(feed),'sk')
        cancelled=Event()
        cancelled.set()
        opener=MagicMock()
        self.assertEqual(projects.report(str,'sk',cancelled,opener),'')
        opener.assert_not_called()

    def test_ping_loss_is_distinct_from_unsupported_ping(self):
        net=module('warder_network')
        good=MagicMock(return_value=SimpleNamespace(stdout='3 packets transmitted, 2 received, 33% packet loss\nrtt min/avg/max = 1.0/2.0/3.0 ms'))
        self.assertEqual(net.ping('192.0.2.1',good),(33.0,2.0))
        self.assertIsNone(net.ping('name;command',good))
        good.assert_called_once()

    def test_report_ignores_late_network_response_after_close(self):
        ui=module('warder_centre_ui')
        s=ui.Report(MagicMock(),api,'network-test','Connection test')
        with patch.object(ui,'deferToThread') as thread:
            s.start()
            s.start()
            thread.assert_called_once()
        s.cancelled.set()
        s.done('late')
        self.assertNotEqual(s['file_info'].getText(),'late')
        self.assertFalse(s.history)

    def test_ipk_inspection_reads_control_without_installing_or_extracting(self):
        from io import BytesIO
        import tarfile
        import gzip
        import hashlib
        ipk=module('warder_ipk')
        with TemporaryDirectory() as d:
            out=BytesIO()
            with tarfile.open(fileobj=out,mode='w') as tar:
                for name, data in [('control',b'Package: example\nVersion: 2\nArchitecture: all\nDepends: enigma2\n'),('preinst',b'exit 1')]:
                    m=tarfile.TarInfo('./'+name);m.size=len(data);tar.addfile(m,BytesIO(data))
            raw=gzip.compress(out.getvalue())
            ar=b'!<arch>\n'+('%-16s%-12s%-6s%-6s%-8s%-10s`\n'%('control.tar.gz/',0,0,0,'100644',len(raw))).encode()+raw
            path=Path(d)/'example.ipk';path.write_bytes(ar+b'\n'*(len(raw)%2))
            before=hashlib.sha256(path.read_bytes()).hexdigest()
            fields,hooks=ipk.inspect(path)
            self.assertEqual((fields['Package'],fields['Depends'],hooks),('example','enigma2',['preinst']))
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),before)
            (Path(d)/'linked.ipk').symlink_to(path)
            self.assertNotIn('linked',ipk.review(str,d))
            path.write_bytes(b'!<arch>\n'+b'x'*60)
            with self.assertRaises(ValueError):ipk.inspect(path)

    def test_summary_cards_and_classic_cam_widgets_preserve_native_bindings(self):
        dashboard=module('warder_dashboard')
        overview=module('warder_overview')
        for w,h in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            skin=ET.fromstring(dashboard.skin(w,h,'overview'))
            self.assertEqual(len([e for e in skin if (e.get('name') or '').startswith('value')]),6)
            for name,value in api.items():
                if name.startswith(('cccam_','mbox_')) and isinstance(value,str) and value.lstrip().startswith('<screen'):
                    original=ET.fromstring(value)
                    current=ET.fromstring(dashboard.cam_panel(value,w,h,str))
                    self.assertEqual(sorted(n.get('name') for n in original.findall('widget')),
                                     sorted(n.get('name') for n in current.findall('widget')))
                    for node in current:
                        x,y=map(int,node.get('position').split(','));width,height=map(int,node.get('size').split(','))
                        self.assertGreaterEqual(min(x,y),0)
                        self.assertLessEqual(x+width,w+1)
                        self.assertLessEqual(y+height,h+1)
        screen=overview.Overview(MagicMock(),api)
        self.assertFalse(screen.alerts().value)
        screen.done({'values':[2,44,None,70,None,48], 'basis':'MemAvailable', 'health':{'state':'ok','score':100,'coverage':(2,2)}})
        self.assertEqual(screen['value2'].getText(),'—')
        self.assertEqual(screen['value5'].getText(),'48.0 °C')
        screen.cancelled.set()
        screen.done(None)
        screen.session.open.assert_not_called()

    def test_bouquet_export_filters_non_dvb_and_never_overwrites(self):
        services=module('warder_services')
        ident='1:0:19:A:1:2:30000:0:0:0:'
        with TemporaryDirectory() as directory:
            rows=[('tv',ident,'First\n#SERVICE injected'),('tv','http://user:secret@invalid','IPTV')]
            first=Path(services.export(rows,'tv',directory))
            second=Path(services.export(rows,'tv',directory))
            self.assertNotEqual(first,second)
            self.assertEqual(first.read_bytes(),second.read_bytes())
            self.assertEqual(first.read_text().count('\n#SERVICE '),1)
            self.assertNotIn('secret',first.read_text())
            self.assertIsNone(services.export(rows,'radio',directory))
        ref=MagicMock()
        ref.toString.return_value=ident
        ref.getUnsignedData.side_effect=lambda ix:{4:0x30000,2:1,3:2}[ix]
        end=MagicMock()
        end.valid.return_value=False
        center=MagicMock()
        center.list.return_value.getNext.side_effect=[ref,ref,end]
        center.info.return_value.getName.return_value='First'
        nav=MagicMock()
        nav.getCurrentlyPlayingServiceReference.return_value=ref
        self.assertEqual(services.services(nav,center,str),[('tv',ident,'First')])

    def test_quick_meter_is_read_only_and_audio_is_off_by_default(self):
        quick=module('warder_quick')
        session=MagicMock()
        session.nav.getCurrentlyPlayingServiceReference.return_value=None
        session.nav.getCurrentService.return_value=None
        with patch.object(quick.shutil,'which',return_value=None):
            screen=quick.QuickSignal(session,api)
            screen.timer=MagicMock()
            screen.tick()
            screen.toggle()
            self.assertFalse(screen.sound)
            self.assertIn('—',screen['level'].getText())
            screen.cleanup()
            screen.tick()
            screen.timer.start.assert_called_once_with(1000,True)
            screen.timer.stop.assert_called_once()
            session.nav.stopService.assert_not_called()

    def test_empty_modern_project_feed_can_show_official_bridge(self):
        projects=module('warder_projects')
        class Response:
            def __init__(self,url,blob):self.url,self.blob=url,blob
            def __enter__(self):return self
            def __exit__(self,*unused):pass
            def read(self,size):return self.blob[:size]
            def geturl(self):return self.url
        def opener(url,timeout):
            name='stable.json' if url==projects.FEED_URL else 'stable-modern.json'
            blob=json.loads((ROOT.parents[1]/'update'/name).read_bytes())
            if name=='stable-modern.json':
                blob['release']=None
            return Response(url,json.dumps(blob).encode())
        with patch.object(projects,'PROJECTS',projects.PROJECTS[-1:]), patch.object(projects,'installed',return_value='13.41-r5'):
            report=projects.report(str,'en',Event(),opener)
            self.assertIn('13.41-r6',report)
            self.assertIn('Update',report)
        self.assertEqual(projects.status_label('Warder Radio','0.2.2-1','0.2.2'),'Ready')

    def test_paused_recording_guard_never_opens_native_setup(self):
        nav=MagicMock()
        nav.getCurrentService.return_value.timeshift.return_value.isTimeshiftActive.return_value=True
        self.assertFalse(module('warder_tuners').recording_safe(nav))
