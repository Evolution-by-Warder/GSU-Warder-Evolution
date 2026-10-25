import importlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tarfile
import tempfile
import types
import unittest
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
sys.path.insert(0,str(ROOT))
import warder_tools as tools


class WarderToolsTests(unittest.TestCase):
    def fixture(self,root):
        files={
            '/proc/meminfo':'MemTotal: 1024000 kB\nMemFree: 1024 kB\nMemAvailable: 512000 kB\n',
            '/proc/mounts':'/dev/root / ext4 rw 0 0\n/dev/sda1 /media/hdd ext4 rw 0 0\nserver:/share /media/net/test nfs rw 0 0\n/dev/loop0 /readonly squashfs ro 0 0\n',
            '/proc/10/comm':'enigma2\n','/proc/10/status':'State:\tS (sleeping)\n',
            '/proc/20/comm':'oscam-master\n','/proc/20/status':'State:\tS (sleeping)\n',
            '/proc/21/comm':'oscam-master\n','/proc/21/status':'State:\tZ (zombie)\n',
            '/sys/class/net/eth0/operstate':'up\n','/sys/class/net/lo/operstate':'unknown\n',
            '/proc/net/route':'Iface Destination Gateway Flags\neth0 00000000 0101A8C0 0003\n',
            '/etc/resolv.conf':'nameserver 192.168.1.1\n',
            '/sys/class/thermal/thermal_zone0/temp':'55000\n','/sys/class/thermal/thermal_zone0/type':'CPU\n',
            '/proc/bus/nim_sockets':'NIM Socket 0:\n Type: DVB-S2\n',
            '/etc/enigma2/settings':'config.plugins.GlassSysUtil.par48=10\nconfig.private.password=should-not-be-collected\n',
            '/run/gsu-softcam-session.json':'{"token":"private-worker-token","enabled":true}',
            '/usr/lib/enigma.info':"distro='openatv'\noe='OE-Alliance 6.0'\narchitecture='armhf'\nserial='private-serial'\n",
        }
        for name,content in files.items():
            p=Path(root)/name.lstrip('/');p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        p=Path(root)/'etc/init.d/softcam';p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to('/etc/init.d/softcam.oscam-master')
        usage=MagicMock(return_value=types.SimpleNamespace(total=1000*1048576,free=500*1048576))
        return tools.Probe(root,usage),usage

    def test_readonly_snapshot_uses_available_memory_skips_network_stat_and_zombies(self):
        with tempfile.TemporaryDirectory() as folder:
            probe,usage=self.fixture(folder);report=probe.collect()
        self.assertEqual(report['memory']['MemAvailable'],512000)
        self.assertEqual(report['gateway'],'192.168.1.1')
        self.assertEqual(report['interfaces'],[{'name':'eth0','state':'up'}])
        self.assertEqual(report['network_mounts'],1)
        self.assertEqual([p['pid'] for p in report['processes']],[10,20])
        self.assertEqual(report['temperatures'][0]['celsius'],55)
        self.assertEqual(report['gsu_settings']['par50'],'True')
        self.assertIs(report['autocheck_guard_enabled'],True)
        self.assertEqual(report['selected_cam'],'softcam.oscam-master')
        self.assertEqual(usage.call_count,2)
        serialized=json.dumps(report)
        for secret in ('private-worker-token','should-not-be-collected','private-serial'):self.assertNotIn(secret,serialized)
        self.assertIn('50.0%',tools.summary(report))

    def test_unavailable_disk_is_not_reported_as_healthy_and_missing_data_is_info(self):
        with tempfile.TemporaryDirectory() as folder:
            probe,usage=self.fixture(folder);usage.side_effect=OSError('unavailable')
            result=tools.summary(probe.collect())
            self.assertIn('[Info] Storage: / — Unavailable',result)
            self.assertNotIn('[OK] Storage',result)
        with tempfile.TemporaryDirectory() as folder:
            report=tools.Probe(folder).collect()
            self.assertIn('[Info] Available memory: Not exposed',tools.summary(report))
            self.assertIsNone(report['autocheck_guard_enabled'])

    def test_low_memory_space_and_down_link_are_visible_without_fault_claim_for_unknown_link(self):
        with tempfile.TemporaryDirectory() as folder:
            probe,usage=self.fixture(folder)
            (Path(folder)/'proc/meminfo').write_text('MemTotal: 1000 kB\nMemAvailable: 10 kB\n')
            (Path(folder)/'sys/class/net/eth0/operstate').write_text('down')
            usage.return_value=types.SimpleNamespace(total=1000,free=1)
            report=probe.collect();text=tools.summary(report)
            self.assertIn('[Warning] Available memory',text)
            self.assertIn('[Warning] Storage',text)
            self.assertIn('[Warning] Network link',text)
            report['interfaces'][0]['state']='unknown'
            self.assertIn('[Info] Network link',tools.summary(report))

    def test_mount_escapes_and_bad_sensor_values_are_handled(self):
        with tempfile.TemporaryDirectory() as folder:
            probe,usage=self.fixture(folder)
            (Path(folder)/'proc/mounts').write_text('/dev/sda1 /media/my\\040disk ext4 rw 0 0\n')
            (Path(folder)/'sys/class/thermal/thermal_zone0/temp').write_text('invalid')
            report=probe.collect()
            self.assertEqual(report['disks'][0]['mount'],'/media/my disk')
            self.assertEqual(report['temperatures'],[])

    def test_bundle_is_private_contains_valid_json_and_no_configurations_or_credentials(self):
        with tempfile.TemporaryDirectory() as folder:
            probe,_=self.fixture(folder);report=probe.collect()
            log=Path(folder)/'input.log';log.write_text('manual start ok\npassword = secret-value\nhttp://alice:secret-url@example.invalid/x\n--guard private-guard\n')
            report['system']['image']['model']='token=embedded-secret'
            result=tools.write_bundle(report,folder,{'softcam.log':str(log)})
            self.assertEqual(stat.S_IMODE(Path(result['path']).stat().st_mode),0o600)
            with tarfile.open(result['path']) as archive:
                self.assertEqual(set(archive.getnames()),{'README.txt','health.txt','report.json','softcam.log'})
                contents={m.name:archive.extractfile(m).read().decode() for m in archive}
            self.assertEqual(json.loads(contents['report.json'])['schema'],1)
            joined='\n'.join(contents.values())
            for secret in ('secret-value','secret-url','private-guard','embedded-secret','private-worker-token','should-not-be-collected'):self.assertNotIn(secret,joined)
            self.assertIn('manual start ok',joined)

    def test_log_size_binary_symlink_and_fifo_are_bounded_or_skipped(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder);log=base/'large.log';log.write_text('a'*40000+'tail')
            self.assertEqual(len(tools.read(log,tools.LOG_LIMIT,True)),tools.LOG_LIMIT)
            self.assertTrue(tools.read(log,tools.LOG_LIMIT,True).endswith('tail'))
            (base/'binary').write_bytes(b'x\x00y')
            (base/'link').symlink_to(log)
            os.mkfifo(base/'fifo')
            for path in ('binary','link','fifo'):self.assertEqual(tools.read(base/path,tools.LOG_LIMIT,True),'')

    def test_bundle_write_failure_removes_partial_archive(self):
        with tempfile.TemporaryDirectory() as folder:
            probe,_=self.fixture(folder)
            with patch.object(tools.tarfile,'open',side_effect=OSError('no space')),self.assertRaises(OSError):tools.write_bundle(probe.collect(),folder,{})
            self.assertEqual(list(Path(folder).glob('gsu-diagnostics-*.tar.gz')),[])

    def test_subprocess_is_bounded_and_invalid_or_failed_collection_cannot_create_bundle(self):
        runner=MagicMock(side_effect=subprocess.TimeoutExpired('collect',20))
        with self.assertRaises(subprocess.TimeoutExpired):tools.run_task('health',runner)
        self.assertEqual(runner.call_args.kwargs['timeout'],20)
        self.assertEqual(runner.call_args.args[0][-1],'--collect')
        for value in (types.SimpleNamespace(returncode=1,stdout=''),types.SimpleNamespace(returncode=0,stdout='not json'),types.SimpleNamespace(returncode=0,stdout='{}')):
            with patch.object(tools,'write_bundle') as bundle,self.assertRaises((OSError,ValueError)):
                tools.run_task('bundle',MagicMock(return_value=value))
            bundle.assert_not_called()

    def test_real_worker_returns_snapshot_without_importing_enigma_gui(self):
        report=tools.run_task('health')
        self.assertEqual(report['schema'],1)
        self.assertIn('memory',report)
        self.assertIn('processes',report)


class WarderToolsUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin=load(ROOT)
        cls.ui=cls.plugin._warder_tools_ui

    def test_main_menu_tools_dispatch_and_two_useful_entries(self):
        session=MagicMock();screen=self.plugin.SysUtilMngMain(session)
        self.assertIn(('17','Nástroje'),[(item[0],item[1]) for item in screen.menuListAll])
        screen.status={'17':True};screen['list'].getCurrent=lambda:['17']
        screen.selectedmenuitem();session.open.assert_called_once_with(self.ui.ToolsScreen,vars(self.plugin))
        menu=self.ui.ToolsScreen(session,vars(self.plugin));menu.prepare()
        self.assertEqual([row[0] for row in menu['list'].list],['bundle','about'])
        self.assertIn('Vytvorenie',menu['descriptions'].text)
        menu['list'].moveToIndex(0);menu.select()
        session.open.assert_called_with(self.ui.DiagnosticScreen,'bundle',vars(self.plugin))
        menu['list'].moveToIndex(1);menu.select()
        session.open.assert_called_with(self.ui.AboutScreen,vars(self.plugin))
        with self.assertRaises(ValueError):self.ui.DiagnosticScreen(session,'health',vars(self.plugin))

    def test_about_uses_installed_version_matching_local_notes_and_honest_attribution(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/'version').write_text('13.40-r40\n')
            (Path(folder)/'release-notes.txt').write_text('GSU 13.40-r40\n\n- Nové O plugine.\n- Kontrola stavu odstránená.\n')
            text=self.ui.about_text(vars(self.plugin),folder)
        self.assertIn('Verzia: 13.40-r40',text)
        self.assertIn('Pôvodný projekt: Glass System Utility 13.20',text)
        self.assertIn('Vývoj a úpravy: Warder Evolution',text)
        self.assertIn('Zmeny v tejto verzii',text)
        self.assertIn('Nové O plugine.',text)
        self.assertEqual(text.count('13.40-r40'),1)

    def test_about_does_not_show_notes_for_a_different_version_or_fail_with_missing_files(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder)/'version').write_text('13.40-r40\n')
            (Path(folder)/'release-notes.txt').write_text('GSU 13.40-r39\nOld changes must not appear')
            text=self.ui.about_text(vars(self.plugin),folder)
            self.assertNotIn('Old changes',text)
            self.assertIn('Informácie o zmenách nie sú dostupné.',text)
            (Path(folder)/'version').unlink()
            self.assertIn('Verzia: Nedostupné',self.ui.about_text(vars(self.plugin),folder))

    def test_collection_is_deferred_once_and_late_callbacks_after_close_are_ignored(self):
        screen=self.ui.DiagnosticScreen(MagicMock(),'bundle',vars(self.plugin));pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending) as worker:
            screen.start();screen.start();worker.assert_called_once_with(self.ui.run_task,'bundle')
        screen.cleanup();previous=screen['file_info'].text
        pending.addCallback.call_args.args[0]({})
        pending.addErrback.call_args.args[0](object())
        self.assertEqual(screen['file_info'].text,previous)

    def test_bundle_path_and_error_use_existing_screen_without_modal_dialog(self):
        session=MagicMock();screen=self.ui.DiagnosticScreen(session,'bundle',vars(self.plugin))
        screen.done({'path':'/tmp/gsu-diagnostics-test.tar.gz','bytes':2048})
        self.assertIn('/tmp/gsu-diagnostics-test.tar.gz',screen['file_info'].text)
        self.assertIn('2 KiB',screen['file_info'].text)
        screen.failed(object())
        self.assertEqual(screen['file_info'].text,'Zber diagnostiky sa nepodaril.')
        session.open.assert_not_called()

    def test_about_screen_has_slovak_title_and_scroll_navigation_without_background_work(self):
        scroll=self.ui.ScrollLabel('');scroll.pageDown=MagicMock();scroll.pageUp=MagicMock()
        with patch.object(self.ui,'ScrollLabel',return_value=scroll),patch.object(self.ui,'about_text',return_value='Informácie o plugine'),patch.object(self.ui,'deferToThread') as worker:
            screen=self.ui.AboutScreen(MagicMock(),vars(self.plugin));screen.prepare()
            worker.assert_not_called()
        self.assertEqual(screen.title,'O plugine')
        self.assertEqual(screen['file_info'].text,'Informácie o plugine')
        self.assertEqual(screen['red'].text,'Naspäť')
        screen['actions'].actions['down']();scroll.pageDown.assert_called_once()
        screen['actions'].actions['up']();scroll.pageUp.assert_called_once()

    def test_original_sd_fhd_uhd_skins_have_required_widgets_and_bound_layout_callbacks(self):
        from xml.etree import ElementTree
        for suffix in ('','_FHD','_UHD'):
            skins=importlib.import_module('Plugins.Extensions.GlassSysUtil.GSU_skins'+suffix)
            api=dict(vars(self.plugin));api.update(ipkScript_center=skins.ipkScript_center,oscam_Files_scr2=skins.oscam_Files_scr2)
            menu=self.ui.ToolsScreen(MagicMock(),api)
            diagnostic=self.ui.DiagnosticScreen(MagicMock(),'bundle',api)
            about=self.ui.AboutScreen(MagicMock(),api)
            for screen,required in ((menu,{'list','descriptions','red','green'}),(diagnostic,{'file_info','red'}),(about,{'file_info','red'})):
                widgets={node.get('name') for node in ElementTree.fromstring(screen.skin).iter('widget')}
                self.assertTrue(required.issubset(widgets))
                self.assertTrue(all(getattr(callback,'__self__',None) is screen for callback in screen.onLayoutFinish))


if __name__=='__main__':unittest.main()
