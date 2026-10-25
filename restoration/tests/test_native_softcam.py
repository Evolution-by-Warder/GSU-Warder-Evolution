import importlib.util
import pathlib
import os
import shutil
import signal
import subprocess
import tempfile
import select
import sys
import types
import unittest
from unittest.mock import MagicMock, patch
from receiver_stubs import load

ROOT=pathlib.Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('native_softcam_under_test',ROOT/'native_softcam.py')
native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)


class NativeSoftcamTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # GUI action callbacks run inside the installed plugin package.
        global native
        load(ROOT)
        native=__import__('Plugins.Extensions.GlassSysUtil.native_softcam',fromlist=['NativeSoftcam'])

    def test_real_worker_lock_serializes_commands_without_holding_gui_thread(self):
        with tempfile.TemporaryDirectory() as folder:
            lock=str(pathlib.Path(folder)/'operation.lock')
            code='''import importlib.util,sys
spec=importlib.util.spec_from_file_location('cam',sys.argv[1])
cam=importlib.util.module_from_spec(spec);spec.loader.exec_module(cam)
print('ready',flush=True)
with cam.command_lock(sys.argv[2]): print('acquired',flush=True)
'''
            with native.command_lock(lock):
                worker=subprocess.Popen([sys.executable,'-u','-c',code,str(ROOT/'native_softcam.py'),lock],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                self.addCleanup(lambda:worker.kill() if worker.poll() is None else None)
                self.assertTrue(select.select([worker.stdout],[],[],5)[0])
                self.assertEqual(worker.stdout.readline().strip(),'ready')
                self.assertFalse(select.select([worker.stdout],[],[],0.15)[0])
            out,error=worker.communicate(timeout=5)
            self.assertEqual(worker.returncode,0,error);self.assertEqual(out.strip(),'acquired')

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=pathlib.Path(self.temp.name)
        self.init=self.root/'init';self.binary=self.root/'bin';self.proc=self.root/'proc'
        for d in (self.init,self.binary,self.proc):d.mkdir()
        self.script=self.init/'softcam.oscam-uni';self.script.write_text('#!/bin/sh\nexit 0\n');self.script.chmod(0o755)
        self.exe=self.binary/'oscam-uni';self.exe.write_text('test binary');self.exe.chmod(0o755)
        self.link=self.init/'softcam';self.link.symlink_to(self.script)
        self.cam=native.NativeSoftcam(self.init,self.binary,self.proc)

    def running(self):
        pid=self.proc/'3013';pid.mkdir(exist_ok=True)
        (pid/'exe').symlink_to(self.exe)
        (pid/'stat').write_text('3013 (oscam-uni) S '+'0 '*18+'12345 0\n')

    def test_selected_script_and_process_must_match_real_executable(self):
        self.assertEqual(self.cam.selected(),'oscam-uni')
        self.assertFalse(self.cam.running())
        pid=self.proc/'3012';pid.mkdir();(pid/'comm').write_text('oscam-uni\n')
        self.assertFalse(self.cam.running())
        self.running();self.assertTrue(self.cam.running())
        self.exe.chmod(0o644);self.assertIsNone(self.cam.selected());self.assertFalse(self.cam.running())

    def test_names_are_discovered_dynamically_including_binary_symlinks(self):
        for name in ('oscam-stable','oscam-custom','my-softcam'):
            with self.subTest(name=name):
                self.link.unlink()
                script=self.init/('softcam.'+name)
                script.write_text('#!/bin/sh\nexit 0\n');script.chmod(0o755)
                binary=self.binary/name
                binary.symlink_to(self.exe)
                self.link.symlink_to(script)
                self.assertEqual(self.cam.selected(),name)
                if not (self.proc/'3013').exists():self.running()
                self.assertTrue(self.cam.running())
                self.assertIn('--action restart --name '+name,self.cam.command(name,'restart'))

    def test_reject_none_missing_binary_and_script_outside_init_directory(self):
        self.link.unlink();other=self.root/'softcam.oscam-uni';other.write_text('test');other.chmod(0o755)
        self.link.symlink_to(other);self.assertIsNone(self.cam.selected())
        self.link.unlink();none=self.init/'softcam.None';none.write_text('test');none.chmod(0o755)
        self.link.symlink_to(none);self.assertIsNone(self.cam.selected())
        self.link.unlink();self.link.symlink_to(self.script);self.exe.unlink();self.assertIsNone(self.cam.selected())

    def test_command_is_bounded_to_installed_scripts_and_supported_actions(self):
        self.assertIn('--action restart --name oscam-uni',self.cam.command('oscam-uni','restart'))
        for name,action in [('oscam-uni','reload'),('other','start'),('oscam-uni','stop; reboot')]:
            with self.assertRaises(ValueError):self.cam.command(name,action)
        self.link.unlink()
        self.assertIn('--switch oscam-uni',self.cam.command('oscam-uni','start'))

    def add_master(self):
        script=self.init/'softcam.oscam-master';script.write_text('#!/bin/sh\nexit 0\n');script.chmod(0o755)
        binary=self.binary/'oscam-master';binary.write_text('master');binary.chmod(0o755)

    def test_all_installed_cams_remain_available_when_selected_cam_is_stopped(self):
        self.add_master()
        self.assertEqual(self.cam.available(),['oscam-master','oscam-uni'])
        self.assertEqual(self.cam.selected(),'oscam-uni')
        self.assertIsNone(self.cam.active_name())
        self.assertIn('--switch oscam-master',self.cam.command('oscam-master','start'))

    def test_registered_package_ownership_is_distinct_from_manual_binary(self):
        self.add_master();info=self.root/'info';info.mkdir()
        package='enigma2-plugin-softcams-oscam-master'
        (info/(package+'.list')).write_text(str(self.binary/'oscam-master')+'\n')
        self.cam.info_dirs=[info]
        self.assertEqual(self.cam.package_for('oscam-master'),package)
        self.assertIsNone(self.cam.package_for('oscam-uni'))

    def test_registry_recognizes_installed_package_without_assuming_info_file_locations(self):
        self.add_master()
        self.cam.registered_packages={'enigma2-plugin-softcams-oscam-master','softcam-feed-universal','enigma2-plugin-extensions-oscamstatus'}
        self.assertEqual(self.cam.package_for('oscam-master'),'enigma2-plugin-softcams-oscam-master')
        self.assertIsNone(self.cam.package_for('oscam-uni'))

    def test_registry_reader_uses_installed_packages_with_a_timeout(self):
        result=types.SimpleNamespace(returncode=0,stdout=b'enigma2-plugin-softcams-oscam-master - 11968-r3\nsoftcam-feed-universal - 4.8-r0\n')
        with patch.object(native.shutil,'which',return_value='/usr/bin/opkg'),patch.object(native.subprocess,'run',return_value=result) as run:
            self.assertEqual(self.cam.read_package_registry(),{'enigma2-plugin-softcams-oscam-master','softcam-feed-universal'})
        self.assertEqual(run.call_args.args[0],['/usr/bin/opkg','list-installed'])
        self.assertEqual(run.call_args.kwargs['timeout'],8)

    def test_switch_stops_old_cam_before_selecting_and_starting_new_one(self):
        self.add_master();state={'oscam-uni':True,'oscam-master':False};calls=[]
        def run(name,action):
            calls.append((name,action,self.cam.selected()))
            if action=='start':self.assertFalse(any(state.values()))
            state[name]=action=='start';return 0
        with patch.object(self.cam,'running',side_effect=lambda name=None:state[name or self.cam.selected()]),patch.object(self.cam,'_run_script',side_effect=run):
            self.assertEqual(self.cam.switch_to('oscam-master','oscam-uni'),0)
        self.assertEqual(calls,[('oscam-uni','stop','oscam-uni'),('oscam-master','start','oscam-master')])
        self.assertEqual(self.cam.selected(),'oscam-master')
        self.assertEqual(state,{'oscam-uni':False,'oscam-master':True})

    def test_failed_start_restores_previous_selection_and_running_cam(self):
        self.add_master();state={'oscam-uni':True,'oscam-master':False};calls=[]
        def run(name,action):
            calls.append((name,action))
            if name=='oscam-master' and action=='start':return 1
            state[name]=action=='start';return 0
        with patch.object(self.cam,'running',side_effect=lambda name=None:state[name or self.cam.selected()]),patch.object(self.cam,'_run_script',side_effect=run):
            with self.assertRaises(OSError):self.cam.switch_to('oscam-master','oscam-uni')
        self.assertEqual(self.cam.selected(),'oscam-uni')
        self.assertTrue(state['oscam-uni']);self.assertFalse(state['oscam-master'])
        self.assertEqual(calls[-1],('oscam-uni','start'))

    def test_failed_stop_never_starts_second_cam_or_changes_selection(self):
        self.add_master()
        with patch.object(self.cam,'running',side_effect=lambda name=None:(name or self.cam.selected())=='oscam-uni'),patch.object(self.cam,'_wait_stopped',return_value=False),patch.object(self.cam,'_signal_matching'),patch.object(self.cam,'_run_script',return_value=1) as run:
            with self.assertRaises(OSError):self.cam.switch_to('oscam-master','oscam-uni')
        run.assert_called_once_with('oscam-uni','stop')
        self.assertEqual(self.cam.selected(),'oscam-uni')

    def test_stale_selection_and_regular_selection_file_are_not_overwritten(self):
        self.add_master()
        with patch.object(self.cam,'_run_script') as run:
            with self.assertRaises(OSError):self.cam.switch_to('oscam-master','wrong')
        run.assert_not_called()
        self.link.unlink();self.link.write_text('custom startup')
        with self.assertRaises(OSError):self.cam.switch_to('oscam-master','')
        self.assertEqual(self.link.read_text(),'custom startup')

    def test_stop_uses_worker_and_ignores_script_exit_when_process_is_gone(self):
        self.assertIn('--action stop --name oscam-uni',self.cam.command('oscam-uni','stop'))
        with patch.object(self.cam,'_run_script',return_value=1) as run,patch.object(self.cam,'_signal_matching') as send:
            self.assertEqual(self.cam.stop_verified('oscam-uni'),0)
        run.assert_called_once_with('oscam-uni','stop');send.assert_not_called()

    def test_stop_waits_and_escalates_only_if_cam_survives(self):
        with patch.object(self.cam,'_run_script',return_value=0),patch.object(self.cam,'_wait_stopped',side_effect=[False,False,True]) as wait,patch.object(self.cam,'_signal_matching') as send:
            self.assertEqual(self.cam.stop_verified('oscam-uni'),0)
        self.assertEqual([c.args for c in send.call_args_list],[('oscam-uni',signal.SIGTERM),('oscam-uni',signal.SIGKILL)])
        self.assertEqual([c.args for c in wait.call_args_list],[('oscam-uni',2),('oscam-uni',2),('oscam-uni',1)])
        with patch.object(self.cam,'_run_script',side_effect=subprocess.TimeoutExpired('stop',20)),patch.object(self.cam,'_wait_stopped',side_effect=[False,True]),patch.object(self.cam,'_signal_matching') as send:
            self.assertEqual(self.cam.stop_verified('oscam-uni'),0)
        send.assert_called_once_with('oscam-uni',signal.SIGTERM)

    def test_pid_reuse_and_zombies_are_not_signalled(self):
        self.running()
        (self.proc/'3013'/'stat').write_text('3013 (oscam-uni) Z '+'0 '*18+'12345 0\n')
        self.assertFalse(self.cam.running())
        with patch.object(self.cam,'_matching_pids',return_value={3013:'old'}),patch.object(self.cam,'_identity',return_value='new'),patch.object(native.os,'pidfd_open',return_value=42,create=True),patch.object(native.signal,'pidfd_send_signal',create=True) as send,patch.object(native.os,'close') as close,patch.object(native.os,'kill') as kill:
            self.cam._signal_matching('oscam-uni',signal.SIGKILL)
        send.assert_not_called();kill.assert_not_called();close.assert_called_once_with(42)

    def test_old_kernel_signal_fallback_rechecks_process_identity(self):
        with patch.object(self.cam,'_matching_pids',return_value={3013:'same'}),patch.object(self.cam,'_identity',return_value='same'),patch.object(native.os,'pidfd_open',side_effect=OSError(native.errno.ENOSYS,'old kernel'),create=True),patch.object(native.os,'kill') as kill:
            self.cam._signal_matching('oscam-uni',signal.SIGTERM)
        kill.assert_called_once_with(3013,signal.SIGTERM)

    def test_restart_does_not_start_until_stop_succeeds(self):
        calls=[]
        with patch.object(self.cam,'stop_verified',side_effect=lambda n:calls.append('stop')),patch.object(self.cam,'_run_script',side_effect=lambda n,a:calls.append(a) or 0),patch.object(self.cam,'running',return_value=True):
            self.assertEqual(self.cam.restart_verified('oscam-uni'),0)
        self.assertEqual(calls,['stop','start'])
        with patch.object(self.cam,'stop_verified',side_effect=OSError('still running')),patch.object(self.cam,'_run_script') as run:
            with self.assertRaises(OSError):self.cam.restart_verified('oscam-uni')
        run.assert_not_called()

    @unittest.skipUnless(pathlib.Path('/proc/self/stat').exists() and shutil.which('sleep'),'Linux process integration')
    def test_real_process_without_pidfile_is_stopped_and_other_binary_survives(self):
        # Exercise actual PID identity and signals with harmless host sleep copies.
        shutil.copyfile(shutil.which('sleep'),self.exe);self.exe.chmod(0o755)
        other=self.binary/'unrelated';shutil.copyfile(shutil.which('sleep'),other);other.chmod(0o755)
        unrelated=subprocess.Popen([str(other),'60'])
        try:
            self.cam.proc_dir=pathlib.Path('/proc')
            original_wait=self.cam._wait_stopped
            for ignore in (False,True):
                process=subprocess.Popen([str(self.exe),'60'],preexec_fn=(lambda:signal.signal(signal.SIGTERM,signal.SIG_IGN)) if ignore else None)
                try:
                    # Some test hosts expose an outer /proc PID namespace.
                    # Map the child's namespace PID to its actual proc entry.
                    self.cam.proc_dir=pathlib.Path('/proc')
                    host_pids=self.cam._matching_pids('oscam-uni')
                    self.assertEqual(len(host_pids),1)
                    entry=self.proc/str(process.pid)
                    entry.symlink_to(pathlib.Path('/proc')/str(next(iter(host_pids))),target_is_directory=True)
                    self.cam.proc_dir=self.proc
                    self.assertTrue(self.cam.running('oscam-uni'))
                    with patch.object(self.cam,'_wait_stopped',side_effect=lambda n,t:original_wait(n,min(t,0.2))):
                        self.assertEqual(self.cam.stop_verified('oscam-uni'),0)
                    process.wait(timeout=2)
                    self.assertEqual(process.returncode,-(signal.SIGKILL if ignore else signal.SIGTERM))
                    self.assertIsNone(unrelated.poll())
                    self.assertFalse(self.cam.running('oscam-uni'))
                finally:
                    if process.poll() is None:process.kill()
                    process.wait(timeout=2)
                    entry.unlink(missing_ok=True)
        finally:
            unrelated.terminate();unrelated.wait(timeout=2)

    def screen(self,index=0,choice='oscam-uni'):
        class Screen(dict):pass
        screen=Screen();screen.nativeSoftcam=self.cam;screen.enCommand=True
        screen.statcommPics=MagicMock()
        screen['config']=types.SimpleNamespace(getCurrent=lambda:('CAM',types.SimpleNamespace(getText=lambda:choice)),getCurrentIndex=lambda:index)
        for key in ('statCamSrvcmd','statCamSrvbin','activCam'):
            screen[key]=types.SimpleNamespace(setText=MagicMock())
        return screen

    def test_start_restart_stop_are_async_and_confirm_real_state_for_all_signal_apis(self):
        for api in ('connect','get','list'):
            for action,running in [('start',False),('start',True),('stop',True)]:
                with self.subTest(api=api,action=action,running=running):
                    screen=self.screen();callbacks=[];operation='restart' if action=='start' and running else action
                    signal=callbacks if api=='list' else types.SimpleNamespace(**{api:(lambda callback:callbacks.append(callback)) if api=='connect' else lambda:callbacks})
                    container=types.SimpleNamespace(appClosed=signal,execute=MagicMock(return_value=0))
                    with patch.object(self.cam,'running',return_value=running) as state:
                        self.assertTrue(native.handle_action(screen,action,lambda:container,lambda s:s))
                        self.assertFalse(screen.enCommand)
                        container.execute.assert_called_once_with(self.cam.command('oscam-uni',operation))
                        self.assertEqual(len(callbacks),1)
                        state.return_value=operation!='stop'
                        callbacks[0](0)
                        self.assertTrue(screen.enCommand)
                        screen['statCamSrvbin'].setText.assert_called_with('CAM Running' if operation != 'stop' else 'No Running CAM')
                        screen.statcommPics.assert_any_call('comm','green')

    def test_failed_execution_and_failed_start_never_report_success(self):
        for launch_error in (True,False):
            screen=self.screen();callbacks=[]
            container=types.SimpleNamespace(appClosed=callbacks,execute=MagicMock(return_value=-1 if launch_error else 0))
            self.assertTrue(native.handle_action(screen,'start',lambda:container,lambda s:s))
            if not launch_error:callbacks[0](0) # script exits zero but no process appeared
            self.assertTrue(screen.enCommand)
            screen.statcommPics.assert_any_call('comm','red')
            screen['statCamSrvcmd'].setText.assert_called_with('oscam-uni Error')

    def test_busy_guard_and_legacy_conflict_do_not_launch_commands(self):
        factory=MagicMock();screen=self.screen();screen.enCommand=False
        self.assertTrue(native.handle_action(screen,'start',factory,lambda s:s));factory.assert_not_called()
        screen=self.screen(index=1,choice='legacy-server')
        with patch.object(self.cam,'running',return_value=True):
            self.assertTrue(native.handle_action(screen,'start',factory,lambda s:s))
        factory.assert_not_called()
        with patch.object(self.cam,'running',return_value=False):
            self.assertFalse(native.handle_action(screen,'start',factory,lambda s:s))
        self.assertEqual(self.link.resolve(),self.script) # no image selection mutation


if __name__=='__main__':unittest.main()
