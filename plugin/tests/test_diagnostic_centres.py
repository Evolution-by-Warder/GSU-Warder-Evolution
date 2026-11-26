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
    def test_remote_mount_is_never_used_for_a_channel_backup(self):
        backup=module('warder_scan_backup')
        storage=module('warder_storage')
        with TemporaryDirectory() as temp:
            src=Path(temp);(src/'lamedb').write_bytes(b'tv')
            with patch.object(storage,'mounts',return_value=[('server:/private','/media/hdd','nfs',False)]), patch.object(backup.tempfile,'mkdtemp',wraps=backup.tempfile.mkdtemp) as make:
                out=Path(backup.create(src))
                try:
                    self.assertEqual(make.call_args.kwargs['dir'],Path('/tmp'))
                    self.assertEqual((out/'lamedb').read_bytes(),b'tv')
                finally:
                    backup.shutil.rmtree(out)

    def test_thermal_polling_reuses_observation_with_age_and_refreshes(self):
        live=module('warder_live')
        p=MagicMock()
        p.text.return_value=''
        p.sensor_paths.return_value=[('temp','')]
        p.temperatures.side_effect=[[{'celsius':51}],[{'celsius':52}]]
        now=[0]
        sampler=live.Sampler(p,lambda:now[0])
        self.assertEqual(sampler.sample()['temp'],51)
        now[0]=2
        self.assertEqual(sampler.sample()['temp_age'],2)
        now[0]=5
        self.assertEqual(sampler.sample()['temp'],52)
        self.assertEqual(p.temperatures.call_count,2)

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

    def test_openwebif_ports_use_native_handles_not_generic_socket_numbers(self):
        import sys
        network=module('warder_network')
        name='Plugins.Extensions.OpenWebif.httpserver'
        self.assertIsNone(network.openwebif_ports({}))
        self.assertIsNone(network.openwebif_ports({name:SimpleNamespace(listener=None)}))
        self.assertEqual(network.openwebif_ports({name:SimpleNamespace(listener=[])}),[])
        listeners=[SimpleNamespace(connected=True,port=8080),
                   SimpleNamespace(connected=1,port=443),
                   SimpleNamespace(connected=True,port=8080),
                   SimpleNamespace(connected=False,port=80)]
        native=SimpleNamespace(listener=listeners)
        self.assertEqual(network.openwebif_ports({name:native}),[443,8080])
        self.assertIsNone(network.openwebif_ports({name:SimpleNamespace(listener=[object()])}))
        p=MagicMock()
        p.entries.return_value=[]
        p.text.return_value=''
        with patch.dict(sys.modules,{name:native}),patch.object(network,'listening_ports',return_value={'tcp':[80]}):
            result=network.detail_report('network-services',str,Event(),p)
        self.assertIn('OpenWebif   Detected\n    TCP   443, 8080',result)
        self.assertIn('Local ports\nTCP   80',result)
        with patch.dict(sys.modules,{name:None}),patch.object(network,'listening_ports',return_value={'tcp':[80]}):
            result=network.detail_report('network-services',str,Event(),p)
        self.assertIn('OpenWebif   —',result)
        self.assertIn('Local ports\nTCP   80',result)

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
        with patch.object(network,'collect',return_value=net),patch.object(network,'ping',return_value=(0,1.0)),patch.object(network,'resolver_test',return_value=(True,12)):
            result=network.diagnostics(str,Event(),probe,web)
            self.assertIn('Internet reachable',result)
            self.assertIn('DNS / NSS · warder-evolution.eu   OK   12 ms',result)
            self.assertIn('Gateway reachable; external checks failed',network.diagnostics(str,Event(),probe,MagicMock(side_effect=OSError)))
        cancel=Event();cancel.set();opener=MagicMock()
        self.assertEqual(network.diagnostics(str,cancel,probe,opener),'')
        opener.assert_not_called()

    def test_backup_inventory_reads_manifest_only_and_skips_untrusted_directories(self):
        backup=module('warder_scan_backup')
        with TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'tmp').mkdir()
            source=root/'source';source.mkdir()
            (source/'lamedb').write_text('private-channel-data')
            dest=Path(backup.create(source,root/'tmp'))
            public=root/'tmp/gsu-channel-backup-public';public.mkdir(mode=0o755)
            (public/'SHA256.json').write_text('{}')
            (root/'tmp/gsu-channel-backup-link').symlink_to(dest,target_is_directory=True)
            p=module('warder_tools').Probe(root)
            before=(dest/'lamedb').read_bytes()
            result=backup.inventory(str,Event(),p)
            self.assertIn(dest.name,result)
            self.assertIn('SHA256.json   1 · Files',result)
            self.assertNotIn('private-channel-data',result)
            self.assertNotIn('backup-public',result)
            self.assertNotIn('backup-link',result)
            self.assertEqual((dest/'lamedb').read_bytes(),before)
            cancel=Event();cancel.set()
            self.assertEqual(backup.inventory(str,cancel,p),'')

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
        menu['list'].getCurrent=lambda:['GSU']
        with patch.object(ui,'deferToThread') as worker,patch.object(projects,'report',return_value='Installed 0.41.5'):
            menu.select()
            value=worker.call_args.args[0]()
            worker.return_value.addCallbacks.call_args.args[0](value)
        self.assertEqual(menu['descriptions'].getText(),'Installed 0.41.5')
        session.open.assert_not_called()
        menu.full_result()
        session.open.assert_called_once_with(ui.ProjectReport,api,projects.PROJECTS[-1])
        view=ui.ProjectReport(session,api,projects.PROJECTS[-1])
        view.update_status('checking')
        self.assertEqual(view['file_info'].text,'checking')
        self.assertEqual(view.readVersion(),(ROOT/'version').read_text().strip())
        with patch.object(module('plugin_update_ui'),'StartupUpdateCheck') as updater:
            view.action();view.action()
        updater.assert_called_once_with(view,api)
        self.assertEqual(updater.return_value.request.call_count,2)

    def test_project_overview_uses_one_canonical_report_without_installation(self):
        ui=module('warder_centre_ui')
        projects=module('warder_projects')
        session=MagicMock()
        menu=ui.ProjectMenu(session,api)
        menu.render()
        self.assertEqual(menu['green'].getText(),menu.tr('Overview'))
        menu['actions'].actions['green']()
        session.open.assert_called_once_with(ui.ProjectOverview,api)
        view=ui.ProjectOverview(session,api)
        with patch.object(projects,'report',return_value='All five') as report:
            self.assertEqual(view.collect(),'All five')
            report.assert_called_once()
            self.assertTrue(report.call_args.kwargs['compact'])
            self.assertNotIn('projects',report.call_args.kwargs)
        with patch.object(module('warder_package_status'),'database',return_value=({},None)),patch.object(projects,'installed',return_value='0.1.2'),patch.object(projects,'read_feed',return_value=b'fixture') as reader,patch.object(projects,'release',return_value=('0.1.3','Long notes')):
            summary=projects.report(str,'en',Event(),compact=True)
            self.assertEqual(reader.call_count,5)
            for project in projects.PROJECTS:self.assertIn(project[0],summary)
            self.assertNotIn('Long notes',summary)
        cancel=Event();cancel.set()
        self.assertEqual(projects.report(str,'en',cancel,compact=True),'')

    def test_largest_files_are_bounded_local_read_only_and_deduplicated(self):
        storage=module('warder_storage')
        with TemporaryDirectory() as folder:
            p=storage.Probe(folder)
            for directory in ('/media/hdd/movie','/media/hdd/movie/remote','/media/net/movie','/usr/share/enigma2','/etc/enigma2'):
                p.path(directory).mkdir(parents=True,exist_ok=True)
            for path,size in (('/media/hdd/movie/a.ts',8192),('/media/hdd/movie/b.ts',4096),
                              ('/usr/share/enigma2/skin.xml',2048),('/media/hdd/movie/remote/private',32768),
                              ('/media/net/movie/private',65536)):
                p.path(path).write_bytes(b'x'*size)
            os.link(p.path('/media/hdd/movie/a.ts'),p.path('/media/hdd/movie/link.ts'))
            p.path('/usr/share/enigma2/link').symlink_to(p.path('/media/net/movie'),target_is_directory=True)
            table=[('/dev/root','/','ext4',False),('/dev/sda1','/media/hdd','ext4',False),
                   ('server:/private','/media/hdd/movie/remote','nfs',False),
                   ('server:/private','/media/net','nfs',False)]
            rows,complete=storage.largest_files(p,table,Event(),limit=3)
            self.assertTrue(complete)
            self.assertEqual([size for size,_ in rows],[8192,4096,2048])
            self.assertNotIn('private',str(rows))
            self.assertEqual(storage.largest_files(p,[],Event()),([],False))
            self.assertFalse(storage.largest_files(p,table,Event(),budget=1)[1])
            cancel=Event();cancel.set()
            self.assertEqual(storage.largest_files(p,table,cancel),([],False))
            with patch.object(storage,'mounts',return_value=table):
                self.assertIn('Selected local folders only',storage.largest_report(str,Event(),p))
                self.assertEqual(storage.largest_report(str,cancel,p),'')
            self.assertEqual(p.path('/media/hdd/movie/b.ts').stat().st_size,4096)
        ui=module('warder_centre_ui')
        self.assertIn('storage-largest',ui.INLINE_REPORTS)
        self.assertIn('storage-largest',ui.MANUAL_INLINE)

    def test_saved_storage_paths_are_read_only_allowlisted_and_do_not_follow_mounts(self):
        storage=module('warder_storage')
        with TemporaryDirectory() as folder:
            p=storage.Probe(folder)
            settings=p.path('/etc/enigma2/settings')
            settings.parent.mkdir(parents=True)
            settings.write_text('config.misc.epgcache_filename=/media/hdd/epg.dat\n'
                'config.timeshift.path=/media/net/timeshift/\n'
                'config.usage.timeshift_path=/old\n'
                'config.usage.default_path=/media/hdd/movie/\n'
                'config.usage.timer_path=<default>\n'
                'config.usage.instantrec_path=http://user:secret@example.test\n'
                'config.plugins.private.password=secret\n')
            with patch.object(p,'usage',side_effect=AssertionError('must not stat configured path')):
                values=dict(storage.configured_storage_paths(p))
            self.assertEqual(values['EPG'],'/media/hdd/epg.dat')
            self.assertEqual(values['Timeshift'],'/media/net/timeshift/')
            self.assertEqual(values['Recordings'],'/media/hdd/movie/')
            self.assertEqual(values['Timer recordings'],'<default>')
            self.assertIsNone(values['Instant recordings'])
            self.assertNotIn('secret',str(values))

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

    def test_smart_detail_uses_one_bounded_command_and_numeric_allowlist(self):
        storage=module('warder_storage')
        data=('SMART overall-health self-assessment test result: PASSED\n'
              '  5 Reallocated_Sector_Ct 0x0033 100 100 036 Pre-fail Always - 7\n'
              '197 Current_Pending_Sector 0x0012 100 100 000 Old_age Always - 2\n'
              'Power On Hours: 1,234\nPercentage Used: 9%\nSerial Number: private\n')
        with patch.object(storage.shutil,'which',return_value='smartctl'):
            run=MagicMock(return_value=SimpleNamespace(stdout=data,returncode=0))
            result=storage.smart('/dev/sda1',run,detailed=True)
            self.assertEqual(result,('PASSED',None,{'Reallocated_Sector_Ct':7,'Current_Pending_Sector':2,'Power On Hours':1234,'Percentage Used':9}))
            run.assert_called_once()
            self.assertEqual(run.call_args.args[0][-1],'/dev/sda')
            self.assertIn('standby',run.call_args.args[0])
            self.assertEqual(storage.smart_device('/dev/sda2'),'/dev/sda')
            self.assertEqual(storage.smart_device('/dev/nvme0n1p2'),'/dev/nvme0n1')
            self.assertNotIn('private',str(result))
        p=MagicMock()
        p.entries.return_value=['1','2']
        p.text.side_effect=lambda path,*args:'dropbear' if path=='/proc/1/comm' else 'enigma2'
        sysdata=module('warder_system_data')
        self.assertEqual(len(sysdata.observed_services(p)),5)
        self.assertEqual(sysdata.observed_services(p,extended=True)[-1],True)

    def test_storage_profiles_fair_budget_and_cancel(self):
        storage=module('warder_storage')
        with TemporaryDirectory() as tmp:
            p=storage.Probe(tmp)
            for path in ('/media/hdd/XPicons/picon','/media/hdd/custom','/usr/lib/enigma2/python/Plugins','/etc/enigma2','/var/cache'):
                p.path(path).mkdir(parents=True,exist_ok=True)
            p.path('/etc/enigma2/settings').write_text('config.plugins.chocholousekpicons.0.picon_folder=user_defined\nconfig.plugins.chocholousekpicons.0.picon_folder_user=/media/hdd/custom\nconfig.plugins.chocholousekpicons.1.picon_folder=/media/hdd\n')
            for i in range(15):p.path('/media/hdd/XPicons/picon/%d.png'%i).write_bytes(b'x'*4096)
            custom=p.path('/media/hdd/custom/a.png');custom.write_bytes(b'x'*4096)
            p.path('/media/hdd/custom/other.txt').write_bytes(b'x'*65536)
            plugin=p.path('/usr/lib/enigma2/python/Plugins/test.py');plugin.write_bytes(b'x'*4096)
            epg=p.path('/etc/enigma2/epg.dat');epg.write_bytes(b'x'*4096)
            table=[('/dev/sda1','/media/hdd','ext4',False)]
            self.assertEqual(storage.configured_picons(p,['/media/hdd']),('/media/hdd/custom',))
            values=storage.usage_categories(p,table,budget=12,seconds=100)
            self.assertFalse(values['Picons'][1])
            self.assertEqual(values['Plugins'],(plugin.stat().st_blocks*512,True))
            self.assertEqual(values['EPG'],(epg.stat().st_blocks*512,True))
            values=storage.usage_categories(p,table,budget=100,seconds=100)
            self.assertEqual(values['Picons'],(16*custom.stat().st_blocks*512,True))
            from threading import Event
            cancel=Event();cancel.set()
            self.assertTrue(all(not done and size==0 for size,done in storage.usage_categories(p,table,cancelled=cancel).values()))
        self.assertEqual(storage.category_size(4096,False),'≥ 4 KiB')
        self.assertEqual(storage.category_size(0,False),'—')

    def test_tuner_actions_fail_closed_before_backup(self):
        tuner=module('warder_tuners')
        nav=MagicMock()
        nav.getCurrentService.return_value=None
        nav.getRecordings.return_value=[]
        nav.getAnyRecordingsCount.return_value=0
        nav.RecordTimer.getNextRecordingTime.return_value=1200
        self.assertFalse(tuner.recording_safe(nav,lambda:1000))
        nav.RecordTimer.getNextRecordingTime.return_value=-1
        self.assertTrue(tuner.recording_safe(nav))
        self.assertFalse(tuner.recording_safe(object()))
        nav.getRecordings.return_value=[object()]
        session=MagicMock(nav=nav,current_dialog=SimpleNamespace())
        action=MagicMock()
        from Screens.MessageBox import MessageBox
        with patch.object(MessageBox,'TYPE_INFO',1,create=True):
            tuner.open_native(session,str,action)
            action.assert_not_called()
            session.openWithCallback.assert_not_called()
            session.open.assert_called_once()
            self.assertIs(session.open.call_args.args[0],module('warder_dialog').InformationDialog)

    def test_direct_selection_launches_only_after_verified_backup_and_rechecks(self):
        tuner=module('warder_tuners')
        nav=MagicMock()
        owner=SimpleNamespace()
        session=MagicMock(nav=nav,current_dialog=owner)
        action=MagicMock()
        from Screens.MessageBox import MessageBox
        from Tools import Directories
        from twisted.internet import threads
        with patch.object(MessageBox,'TYPE_INFO',1,create=True),patch.object(Directories,'SCOPE_CONFIG',0,create=True),patch.object(threads,'deferToThread') as worker,patch.object(tuner,'recording_safe',return_value=True) as safe:
            tuner.open_native(session,str,action)
            tuner.open_native(session,str,action)
            worker.assert_called_once()
            session.openWithCallback.assert_not_called()
            action.assert_not_called()
            launch,failed=worker.return_value.addCallbacks.call_args.args
            launch('/tmp/verified-backup')
            action.assert_called_once_with(session)
            self.assertEqual(owner._gsu_last_channel_backup,'/tmp/verified-backup')
            action.reset_mock()
            tuner.open_native(session,str,action)
            launch,failed=worker.return_value.addCallbacks.call_args.args
            safe.return_value=False
            launch('/tmp/verified-backup')
            action.assert_not_called()
            safe.return_value=True
            tuner.open_native(session,str,action)
            launch,failed=worker.return_value.addCallbacks.call_args.args
            failed(None)
            action.assert_not_called()
            tuner.open_native(session,str,action)
            launch,failed=worker.return_value.addCallbacks.call_args.args
            session.current_dialog=object()
            launch('/tmp/verified-backup')
            action.assert_not_called()

    def test_native_tuner_layout_and_unknown_driver_values(self):
        ui=module('warder_tuner_ui')
        for width,height in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            for finder in (True,False):
                root=ET.fromstring(ui.skin(width,height,finder,{'config','introduction','key_red','key_green'}))
                names={n.get('name') for n in root}
                self.assertIn('config',names)
                self.assertEqual('warder_metric0' in names,finder)
                for n in root:
                    x,y=map(int,n.get('position').split(','));w,h=map(int,n.get('size').split(','))
                    self.assertLessEqual(x+w,width);self.assertLessEqual(y+h,height)
                self.assertEqual(len(root.findall("widget[@source='key_green']")),0 if finder else 1)
        self.assertEqual(ui.readings({}),(None,None,None,None,None))
        self.assertEqual(ui.readings({'tuner_signal_quality':32768,'tuner_signal_power':65535,
            'tuner_signal_quality_db':1070,'tuner_bit_error_rate':0,'tuner_locked':1}),(50,100,1070,0,1))

    def test_reception_centre_exposes_registered_native_tools_directly(self):
        ui=module('warder_centre_ui')
        tuner=module('warder_tuners')
        session=MagicMock()
        action=MagicMock()
        menu=ui.CentreMenu(session,api,[('signal-quick','Quick signal','SNR'),
                     ('tuner-native','Tuner setup','DiSEqC')],{'signal-quick':True,'tuner-native':True},'reception')
        with patch.object(tuner,'native_tools',return_value=[('SatFinder',action),('Manual scan',MagicMock())]),patch.object(tuner,'open_native') as launch:
            menu.render()
            self.assertEqual([r[0] for r in menu.entries()],['signal-quick','native:0','native:1'])
            menu['list'].getCurrent=lambda:['native:0']
            menu.select()
            self.assertIs(launch.call_args.args[2],action)
            session.openWithCallback.assert_not_called()

    def test_finder_is_measurement_only_without_disabling_native_retune(self):
        from Screens.Screen import Screen
        tuner=module('warder_tuners')
        ui=module('warder_tuner_ui')
        calls=[]
        class Satfinder(Screen):
            def __init__(self,session):
                Screen.__init__(self,session)
                self.frontend=object()
                self['config']=api['Label']('')
                self['Frontend']=api['Label']('')
                self['key_red']=api['Label']('Close')
                self['key_green']=api['Label']('Scan')
                self['introduction']=api['Label']('Press OK to scan')
                self.scan_keys=(self.keyGoScan,self.keyGo,self.startScan)
            def retune(self):calls.append('retune')
            def keyGoScan(self):
                self.frontend=None
                calls.append('scan-key')
            def keyGo(self):calls.append('scan-setup')
            def startScan(self,*args):calls.append('scan-start')
        scope={'Satfinder':Satfinder}
        exec('def SatfinderMain(session):\n    session.open(Satfinder)',scope)
        entry=scope['SatfinderMain']
        wrapped=tuner.styled_satfinder(entry)
        session=MagicMock()
        wrapped(session)
        klass=session.open.call_args.args[0]
        self.assertTrue(issubclass(klass,Satfinder))
        screen=klass(session)
        frontend=screen.frontend
        for callback in screen.scan_keys:callback()
        self.assertIs(screen.frontend,frontend)
        self.assertEqual(calls,[])
        screen.retune()
        self.assertEqual(calls,['retune'])
        self.assertEqual(screen['key_green'].getText(),'')
        self.assertEqual(screen['introduction'].getText(),'')
        for width,height in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            components={'config','Frontend','key_red','key_green','introduction'}
            finder=ET.fromstring(ui.skin(width,height,True,components))
            manual=ET.fromstring(ui.skin(width,height,False,components))
            self.assertIsNone(finder.find("widget[@source='key_green']"))
            self.assertIsNone(finder.find("widget[@name='introduction']"))
            self.assertIsNotNone(manual.find("widget[@source='key_green']"))
            self.assertIsNotNone(manual.find("widget[@name='introduction']"))
        self.assertIs(scope['Satfinder'],Satfinder)
        entry(session)
        self.assertIs(session.open.call_args.args[0],Satfinder)
        self.assertIsNone(tuner.styled_satfinder(lambda session:None))

    def test_finder_quality_history_and_audio_capability(self):
        ui=module('warder_tuner_ui')
        self.assertEqual(ui.quality_color(20,1),0xff526a)
        self.assertEqual(ui.quality_color(50,1),0xffdb52)
        self.assertEqual(ui.quality_color(80,1),0x39ff59)
        self.assertEqual(ui.quality_color(80,0),0xff526a)
        self.assertEqual(ui.quality_color(None,None),0x8291a5)
        canvas=MagicMock()
        ui.draw_quality(canvas,70,1,100,10)
        canvas.fill.assert_called_with(0,0,70,10,0x39ff59)
        from Screens.Screen import Screen
        screen=Screen(MagicMock())
        screen['config']=api['Label']('')
        screen['Frontend']=MagicMock()
        quick=module('warder_quick')
        with patch.object(quick.shutil,'which',return_value=None):
            self.assertTrue(ui.install(screen,api,True))
        header=screen._diagnostic_header
        self.assertEqual(screen['warder_audio_key'].getText(),'')
        header.toggle_audio()
        self.assertFalse(header.audio_enabled)
        header.ready=True
        header.history.append({'snr':70,'lock':1})
        screen['Frontend'].getFrontendStatus.return_value={'tuner_signal_quality':40000,'tuner_locked':0}
        with patch.object(module('warder_chart'),'draw_trend') as draw:
            header.tick()
            draw.assert_called_once()
            self.assertEqual(draw.call_args.args[2],'snr')
            width,height=ui.dashboard.dimensions(api)
            self.assertEqual(draw.call_args.args[3:5],(round(ui.FINDER_PLOT_SIZE[0]*width/1920),round(ui.FINDER_PLOT_SIZE[1]*height/1080)))
        self.assertTrue(screen['warder_lock_losses'].getText().endswith('1'))
        self.assertEqual([screen['warder_metric_name%d'%i].getText() for i in range(4)],['SNR:','AGC:','BER:','LOCK:'])
        header.reset_history()
        self.assertEqual(header.history.snapshot(),())
        header.suspend()
        self.assertFalse(header.audio_enabled)
        header.cleanup()
        for width,height in ((1280,720),(1920,1080),(2560,1440),(3840,2160),(1920,1200)):
            root=ET.fromstring(ui.skin(width,height,True,{'config','Frontend','key_red'}))
            for name in ('warder_quality','warder_signal_history'):
                node=root.find("widget[@source='%s']"%name)
                self.assertIsNotNone(node)
                x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
                self.assertLessEqual(x+w,width);self.assertLessEqual(y+h,height)

    def test_finder_comparison_keeps_explicit_bounded_session_snapshots(self):
        ui=module('warder_tuner_ui')
        signal=module('warder_signal')
        tp=(12304,30000,0,3,2,235,1,2,0,2,-1,0,0,-1,4096)
        native=SimpleNamespace(transponder=tp,scan_nims=SimpleNamespace(value='0'))
        identity=signal.satellite_identity(native)
        self.assertEqual(identity,(0,tp))
        native.transponder=(1,2,3)
        self.assertIsNone(signal.satellite_identity(native))
        rows=[(0,{'snr':70,'agc':80,'db':10,'ber':0,'lock':1}),
              (1,{'snr':10,'lock':0}),(2,{'snr':80,'agc':82,'db':11,'ber':2,'lock':1}),
              (3,{'snr':75,'agc':81,'db':12,'ber':1,'lock':1})]
        self.assertIsNone(signal.measurement_record(identity,rows[:2],'test'))
        record=signal.measurement_record(identity,rows,'test')
        self.assertEqual(record['stats']['snr'],(70,80,75))
        self.assertEqual(record['losses'],1)
        text=signal.comparison_text([record],str)
        self.assertIn('23.5° E',text)
        self.assertIn('12304 H',text)
        self.assertIn('LOCK + SNR   3/4',text)
        from Screens.Screen import Screen
        screen=Screen(MagicMock())
        screen['config']=api['Label']('')
        screen['Frontend']=MagicMock()
        screen._warder_measurement_id=identity
        self.assertTrue(ui.install(screen,api,True))
        header=screen._diagnostic_header
        header.ready=True
        with patch.object(header.history,'snapshot',return_value=tuple(rows)):
            self.assertEqual(header.saved_records(),[])
            for _ in range(14):header.save_measurement()
            self.assertEqual(len(header.saved_records()),12)
            self.assertEqual(screen['warder_compare_key'].getText().split(' · ')[-1],'12')
            header.compare_measurements()
            screen.session.open.assert_called_once()
        header.reset_history()
        self.assertEqual(len(header.saved_records()),12)
        self.assertEqual(screen['warder_save_key'].getText(),'')
        header.cleanup()

    def test_finder_measurements_share_aligned_single_rows_and_larger_plot(self):
        ui=module('warder_tuner_ui')
        for width,height in ((1280,720),(1920,1080),(2560,1440),(3840,2160),(1920,1200)):
            root=ET.fromstring(ui.skin(width,height,True,{'config','Frontend','key_red'}))
            def rect(node):
                return tuple(map(int,node.get('position').split(',')))+tuple(map(int,node.get('size').split(',')))
            previous_bottom=0
            lefts=set()
            for i in range(4):
                caption=root.find("widget[@name='warder_metric_name%d']"%i)
                value=root.find("widget[@name='warder_metric%d']"%i)
                x,y,w,h=rect(caption);vx,vy,vw,vh=rect(value)
                self.assertEqual((y,h),(vy,vh))
                self.assertEqual(caption.get('font'),value.get('font'))
                self.assertLessEqual(x+w,vx)
                self.assertGreater(y,previous_bottom)
                previous_bottom=y+h
                lefts.add((x,vx))
            self.assertEqual(len(lefts),1)
            plot=root.find("widget[@source='warder_signal_history']")
            px,py,pw,ph=rect(plot)
            self.assertGreater(py,previous_bottom)
            self.assertEqual(ph,round(196*height/1080))
            self.assertEqual(pw,round(522*width/1920))
            self.assertLessEqual(px+pw,width)
            self.assertLessEqual(py+ph,height)

    def test_manual_scan_preserves_user_clear_flags_and_recording_guard(self):
        tuner=module('warder_tuners')
        native=importlib.import_module('Screens.ScanSetup')
        from Screens.MessageBox import MessageBox
        import enigma
        calls=[]
        for initial,expected in ((None,['ScanSetup']),(['ScanSetup','Setup'],['ScanSetup','Setup'])):
            class NativeScan:
                def __init__(self,session):
                    self.session=session
                    self.skinName=initial if initial is not None else type(self).__name__
                def startScan(self,tlist,flags,feid,*args,**kwargs):
                    calls.append((tlist,flags,feid,args,kwargs))
            session=MagicMock()
            with patch.object(native,'ScanSetup',NativeScan),patch.object(enigma,'eComponentScan',SimpleNamespace(scanRemoveServices=4)),patch.object(MessageBox,'TYPE_INFO',1,create=True),patch.object(tuner,'recording_safe',return_value=True) as safe:
                tuner.manual_scan(session)
                wrapper=session.open.call_args.args[0]
                screen=wrapper(session)
                self.assertEqual(screen.skinName,expected)
                calls.clear()
                screen.startScan(['tp'],4,0)
                self.assertEqual(calls,[(['tp'],4,0,(),{})])
                safe.return_value=False
                screen.startScan(['tp'],0,0)
                screen.startScan(['tp'],4,0)
                self.assertEqual(calls,[(['tp'],4,0,(),{})])
                safe.return_value=True
                screen.startScan(['tp'],0,0,networkid=1)
                screen.startScan(['tp'],5,1,networkid=123)
                self.assertEqual(calls,[(['tp'],4,0,(),{}),(['tp'],0,0,(),{'networkid':1}),
                                        (['tp'],5,1,(),{'networkid':123})])

    def test_manual_scan_progress_keeps_native_components_and_callbacks(self):
        from Components.Sources.StaticText import StaticText
        from Screens.Screen import Screen
        ui=module('warder_tuner_ui')
        calls=[]
        class ServiceScan(Screen):
            def __init__(self,session,scanList,**kwargs):
                Screen.__init__(self,session)
                self.native_args=(scanList,kwargs)
                self.setTitle('Service scan')
                for name in ui.SCAN_COMPONENTS:self[name]=api['Label']('')
                self['key_red']=StaticText('Cancel')
                self['key_green']=api['Label']('OK')
                self.native_widgets=dict(self)
                self.onLayoutFinish.append(lambda:calls.append('native'))
            def native_completion(self):return 'original result'
        ServiceScan.__module__='Screens.ServiceScan'
        scope={'ServiceScan':ServiceScan}
        exec('def startScan(self,tlist,flags,feid,networkid=0):\n'
             '    self.session.openWithCallback(self.finished_cb,ServiceScan,[{"transponders":tlist,"flags":flags,"feid":feid,"networkid":networkid}],updateBouquets=False)',scope)
        from types import MethodType
        session=MagicMock()
        owner=SimpleNamespace(session=session,finished_cb=MagicMock())
        method=MethodType(scope['startScan'],owner)
        ui.run_with_scan_progress(method,['tp'],0,1,networkid=123)
        callback,screen_class,payload=session.openWithCallback.call_args.args
        kwargs=session.openWithCallback.call_args.kwargs
        self.assertIs(callback,owner.finished_cb)
        self.assertEqual(payload,[{'transponders':['tp'],'flags':0,'feid':1,'networkid':123}])
        self.assertEqual(kwargs,{'updateBouquets':False})
        self.assertIs(scope['ServiceScan'],ServiceScan)
        self.assertTrue(issubclass(screen_class,ServiceScan))
        screen=screen_class(session,payload,**kwargs)
        self.assertEqual(screen.skinName,['WarderServiceScan'])
        self.assertEqual(screen.native_completion(),'original result')
        for name,component in screen.native_widgets.items():self.assertIs(screen[name],component)
        self.assertEqual(screen.native_args,(payload,kwargs))
        screen.onLayoutFinish[0]()
        self.assertEqual(calls,['native'])
        root=ET.fromstring(screen.skin)
        self.assertIsNotNone(root.find("widget[@source='key_red']"))
        self.assertIsNotNone(root.find("widget[@name='key_green']"))
        self.assertIsNotNone(root.find("widget[@name='servicelist']"))
        method(['tp'],0,1)
        self.assertIs(session.openWithCallback.call_args.args[1],ServiceScan)
        for width,height in ((1280,720),(1920,1080),(2560,1440),(3840,2160),(1920,1200)):
            root=ET.fromstring(ui.progress_skin(width,height,ui.SCAN_COMPONENTS|{'key_red','key_green'},{'key_red','key_green'}))
            for node in root:
                x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
                self.assertGreater(min(w,h),0);self.assertLessEqual(x+w,width);self.assertLessEqual(y+h,height)
            node=root.find("widget[@name='servicelist']")
            self.assertEqual(int(node.get('size').split(',')[1])%int(node.get('itemHeight')),0)

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

    def test_network_detail_reports_use_local_counters_and_never_access_remote_mounts(self):
        net=module('warder_network')
        p=MagicMock()
        fixtures={'/proc/net/dev':'eth0: 1048576 12 3 4 0 0 0 0 2097152 20 5 6 0 0 0 0',
                  '/proc/mounts':'//user:secret@host/share /media/net/a cifs rw,username=secret 0 0',
                  '/proc/net/tcp':'header\n  0: 00000000:0016 00000000:0000 0A\n  1: 00000000:0050 00000000:0000 01',
                  '/proc/net/udp':'header\n  0: 00000000:0035 00000000:0000 07',
                  '/sys/class/net/eth0/address':'aa:bb:cc:dd:ee:ff',
                  '/sys/class/net/eth0/duplex':'full','/sys/class/net/eth0/carrier':'1'}
        p.text.side_effect=lambda path,*args:fixtures.get(path,'')
        p.entries.return_value=[]
        with patch.object(net,'collect',return_value={'interfaces':[{'name':'eth0','state':'up','speed':1000,'addresses':['192.0.2.1']}]}):
            output=net.detail_report('network-interfaces',str,Event(),p)
            self.assertIn('aa:bb:cc:dd:ee:ff',output)
            self.assertIn('192.0.2.1',output)
        stats=net.detail_report('network-statistics',str,Event(),p)
        self.assertIn('RX   1.00 MiB',stats)
        self.assertIn('TX   2.00 MiB',stats)
        self.assertIn('Errors 3',stats)
        mounts=net.detail_report('network-mounts',str,Event(),p)
        self.assertIn('/media/net/a',mounts)
        self.assertNotIn('secret',mounts)
        p.usage.assert_not_called()
        self.assertEqual(net.listening_ports(p),{'tcp':[22],'tcp6':None,'udp':[53],'udp6':None})
        output=net.detail_report('network-services',str,Event(),p)
        self.assertIn('TCP   22',output)
        self.assertNotIn('TCP   80',output)
        cancel=Event();cancel.set()
        self.assertEqual(net.detail_report('network-statistics',str,cancel,p),'')

    def test_cpu_details_share_counter_arithmetic_and_report_real_frequency(self):
        sysdata=module('warder_system_data')
        probe=MagicMock()
        before='cpu0 10 0 0 90\ncpu1 0 0 0 100'
        after='cpu0 20 0 0 100\ncpu1 0 0 0 120'
        readings=iter((before,after))
        def read(path,*args):
            if path=='/proc/stat':return next(readings)
            if path.endswith('cpu0/cpufreq/scaling_cur_freq'):return '1500000'
            if path=='/proc/uptime':return '90061.5 0'
            return ''
        probe.text.side_effect=read
        result=sysdata.cpu_details(str,Event(),probe)
        self.assertIn('CPU 0   50.0 %   ·   1500 MHz',result)
        self.assertIn('CPU 1   0.0 %   ·   —',result)
        self.assertIn('1 d  01:01:01',result)

    def test_local_crash_and_package_inventory_reuse_existing_sources(self):
        svc=module('warder_service')
        pkg=module('warder_package_status')
        with TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'tmp').mkdir()
            (root/'tmp/enigma2_crash_a.log').write_text('password=secret\nImportError: private')
            (root/'tmp/enigma2_crash_link.log').symlink_to(root/'tmp/enigma2_crash_a.log')
            p=module('warder_tools').Probe(root)
            out=svc.crash_report(str,Event(),p)
            self.assertIn('ImportError',out)
            self.assertIn('Check plugin dependencies',out)
            self.assertNotIn('secret',out)
            self.assertNotIn('crash_link',out)
            self.assertEqual(svc.crash_summary(p),['ImportError'])
            with patch.object(pkg,'database',return_value=({'enigma2-plugin-extensions-demo':{'Version':'1.2.3','Architecture':'all'},'kernel':{}},'opkg')):
                out=pkg.plugin_inventory(str,Event(),root)
                self.assertIn('enigma2-plugin-extensions-demo',out)
                self.assertIn('1.2.3',out)
                self.assertNotIn('kernel',out)

    def test_memory_and_disk_activity_are_passive_and_keep_unknown_values(self):
        storage=module('warder_storage')
        p=MagicMock()
        p.text.side_effect=lambda path,*args:{'/proc/meminfo':'MemTotal: 1024 kB\nMemFree: 512 kB\nCached: 256 kB',
            '/proc/sys/vm/swappiness':'60'}.get(path,'')
        result=storage.memory_report(str,Event(),p)
        self.assertIn('MemTotal   1.0 MiB',result)
        self.assertIn('MemAvailable   —',result)
        self.assertIn('swappiness   60',result)
        before='8 0 sda 10 0 100 0 20 0 200 0 0 0 0\n8 1 sda1 10 0 100 0 20 0 200 0 0 0 0'
        after='8 0 sda 14 0 120 0 22 0 240 0 0 0 0'
        p.text.side_effect=(before,after)
        clock=iter((0,2))
        result=storage.disk_activity(str,Event(),p,lambda:next(clock))
        self.assertIn('R   5.0 KiB/s   ·   2.0 IOPS',result)
        self.assertIn('W   10.0 KiB/s   ·   1.0 IOPS',result)
        self.assertNotIn('sda1',result)

    def test_smart_diagnostics_reuses_resource_and_installation_checks(self):
        system=module('warder_system_data')
        p=MagicMock()
        p.temperatures.return_value=[]
        model={'checks':[{'name':'RAM','state':'unknown','available_percent':None}],
               'health':{'score':None,'coverage':(0,1),'state':'unknown'}}
        with patch.object(system,'overview',return_value=model),patch.object(module('warder_storage'),'mounts',return_value=[]),patch.object(module('warder_storage'),'disks',return_value=[]),patch.object(module('warder_network'),'collect',return_value={'interfaces':[],'gateways':[],'dns':[]}),patch.object(module('warder_service'),'health',return_value='GSU verified') as health:
            result=system.smart_diagnostics(str,Event(),p)
            self.assertIn('RAM   ·   Not exposed   ·   —',result)
            self.assertIn('Measured checks   0/1',result)
            self.assertIn('GSU verified',result)
            self.assertIn('Internet access, disk integrity and CAM decoding are not tested',result)
            health.assert_called_once_with(str,p)

    def test_resolver_test_is_bounded_and_not_a_shell_command(self):
        import subprocess
        net=module('warder_network')
        runner=MagicMock(return_value=SimpleNamespace(returncode=0))
        self.assertTrue(net.resolver_test(runner)[0])
        self.assertEqual(runner.call_args.kwargs['timeout'],4)
        self.assertIn('warder-evolution.eu',runner.call_args.args[0][-1])
        runner.return_value.returncode=1
        self.assertFalse(net.resolver_test(runner)[0])
        runner.side_effect=subprocess.TimeoutExpired('resolver',4)
        self.assertIsNone(net.resolver_test(runner))

    def test_selected_crash_tail_checks_identity_redacts_and_never_follows_symlink(self):
        svc=module('warder_service')
        with TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'tmp').mkdir()
            path=root/'tmp/enigma2_crash_a.log'
            path.write_text('x'*40000+'\npassword=secret\nImportError: test')
            (root/'tmp/enigma2_crash_link.log').symlink_to(path)
            probe=module('warder_tools').Probe(root)
            rows=svc.crash_inventory(Event(),probe)
            self.assertEqual(len(rows),1)
            identity=rows[0][3]
            result=svc.crash_detail(path,identity,str,Event(),probe)
            self.assertIn('ImportError',result)
            self.assertIn('Check plugin dependencies',result)
            self.assertIn('Partial result',result)
            self.assertNotIn('secret',result)
            self.assertIn('<redacted>',result)
            path.write_text('changed')
            self.assertEqual(svc.crash_detail(path,identity,str,Event(),probe),'Unavailable')
            self.assertEqual(svc.crash_detail(root/'tmp/enigma2_crash_link.log',identity,str,Event(),probe),'Unavailable')

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
