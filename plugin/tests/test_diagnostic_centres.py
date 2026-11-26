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
        self.assertEqual(json.loads(preview),{'schema':1,'available_percent':{'RAM':51.8,'Flash':None}})
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
