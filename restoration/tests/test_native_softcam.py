import importlib.util
import pathlib
import tempfile
import types
import unittest
from unittest.mock import MagicMock, patch

ROOT=pathlib.Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('native_softcam_under_test',ROOT/'native_softcam.py')
native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)


class NativeSoftcamTests(unittest.TestCase):
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
                self.assertTrue(self.cam.command(name,'restart').endswith('softcam.'+name+' restart'))

    def test_reject_none_missing_binary_and_script_outside_init_directory(self):
        self.link.unlink();other=self.root/'softcam.oscam-uni';other.write_text('test');other.chmod(0o755)
        self.link.symlink_to(other);self.assertIsNone(self.cam.selected())
        self.link.unlink();none=self.init/'softcam.None';none.write_text('test');none.chmod(0o755)
        self.link.symlink_to(none);self.assertIsNone(self.cam.selected())
        self.link.unlink();self.link.symlink_to(self.script);self.exe.unlink();self.assertIsNone(self.cam.selected())

    def test_command_is_bounded_to_selected_script_and_supported_actions(self):
        self.assertTrue(self.cam.command('oscam-uni','restart').endswith('softcam.oscam-uni restart'))
        for name,action in [('oscam-uni','reload'),('other','start'),('oscam-uni','stop; reboot')]:
            with self.assertRaises(ValueError):self.cam.command(name,action)
        self.link.unlink()
        with self.assertRaises(ValueError):self.cam.command('oscam-uni','start')

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
                        screen['statCamSrvbin'].setText.assert_called_with('CAM/SRV Running' if operation != 'stop' else 'No Running CAM/SRV')
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
