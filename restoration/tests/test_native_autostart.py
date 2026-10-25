import importlib.util
from pathlib import Path
import types
import unittest
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('native_autostart_test',ROOT/'native_autostart.py')
boot=importlib.util.module_from_spec(spec);spec.loader.exec_module(boot)


class NativeAutostartTests(unittest.TestCase):
    def setUp(self):
        self.log=patch.object(boot,'log_event');self.log.start();self.addCleanup(self.log.stop)
        self.native=MagicMock();self.native.selected.return_value='oscam-master'
        self.native.active_name.return_value=None;self.native.start_verified.return_value=0

    def test_wait_uses_timer_and_starts_worker_only_after_expiry_once(self):
        timer=MagicMock();container=MagicMock();container.execute.return_value=0
        factory=MagicMock(return_value=container)
        delayed=boot.DelayedNativeStart(self.native,lambda:timer,factory,10)
        self.assertTrue(delayed.schedule());timer.startLongTimer.assert_called_once_with(10)
        factory.assert_not_called();self.native.start_verified.assert_not_called()
        timer.timeout.connect.call_args.args[0]()
        factory.assert_called_once();self.assertIn('--autostart oscam-master',container.execute.call_args.args[0])
        delayed.fire();factory.assert_called_once()
        self.native.start_verified.assert_not_called()

    def test_classic_list_signals_and_shutdown_cancellation(self):
        timer=types.SimpleNamespace(timeout=[],startLongTimer=MagicMock(),stop=MagicMock())
        factory=MagicMock()
        delayed=boot.DelayedNativeStart(self.native,lambda:timer,factory,10)
        delayed.schedule();delayed.cancel();timer.timeout[0]()
        factory.assert_not_called();timer.stop.assert_called()

    def test_no_native_selection_does_not_schedule(self):
        self.native.selected.return_value=None;timer=MagicMock()
        delayed=boot.DelayedNativeStart(self.native,lambda:timer,MagicMock(),10)
        self.assertFalse(delayed.schedule());timer.startLongTimer.assert_not_called()

    def test_worker_skips_cam_already_started_by_image(self):
        self.native.active_name.return_value='oscam-master'
        self.assertEqual(boot.start_if_needed(self.native,'oscam-master'),0)
        self.native.start_verified.assert_not_called()

    def test_worker_skips_changed_selection_or_another_running_cam(self):
        self.native.selected.return_value='oscam-uni'
        boot.start_if_needed(self.native,'oscam-master');self.native.active_name.assert_not_called()
        self.native.selected.return_value='oscam-master';self.native.active_name.return_value='oscam-uni'
        boot.start_if_needed(self.native,'oscam-master');self.native.start_verified.assert_not_called()

    def test_worker_starts_missing_selected_cam_and_reports_failure(self):
        self.assertEqual(boot.start_if_needed(self.native,'oscam-master'),0)
        self.native.start_verified.assert_called_once_with('oscam-master')
        self.native.start_verified.side_effect=OSError('did not start')
        with self.assertRaises(OSError):boot.start_if_needed(self.native,'oscam-master')

    def test_session_hook_bypasses_legacy_branch_and_shutdown_cancels_timer(self):
        plugin=load(ROOT)
        helper=__import__('Plugins.Extensions.GlassSysUtil.native_autostart',fromlist=['begin'])
        native_module=__import__('Plugins.Extensions.GlassSysUtil.native_softcam',fromlist=['NativeSoftcam'])
        timer=MagicMock();plugin.config.plugins.GlassSysUtil.par57.value='0'
        plugin.config.plugins.GlassSysUtil.par48.value=10
        with patch.object(native_module,'NativeSoftcam',return_value=self.native),patch.object(helper,'log_event'),patch.object(plugin,'eTimer',return_value=timer):
            plugin.autocams.autoStartCheck(object())
        timer.startLongTimer.assert_called_once_with(10)
        self.assertEqual(plugin.autocams.nativeDelayedStart.name,'oscam-master')
        plugin.sessionAutostart(1)
        self.assertTrue(plugin.autocams.nativeDelayedStart.cancelled)

    def test_session_hook_retains_independent_mount_checker(self):
        plugin=load(ROOT)
        helper=__import__('Plugins.Extensions.GlassSysUtil.native_autostart',fromlist=['begin'])
        native_module=__import__('Plugins.Extensions.GlassSysUtil.native_softcam',fromlist=['NativeSoftcam'])
        owner=types.SimpleNamespace(chckCifsNfs=MagicMock())
        config=types.SimpleNamespace(plugins=types.SimpleNamespace(GlassSysUtil=types.SimpleNamespace(par48=types.SimpleNamespace(value=10),par57=types.SimpleNamespace(value='1'))))
        api={'config':config,'eTimer':MagicMock(),'eConsoleAppContainer':MagicMock()}
        with patch.object(native_module,'NativeSoftcam',return_value=self.native),patch.object(helper,'log_event'):
            self.assertTrue(helper.begin(owner,api))
        owner.chckCifsNfs.assert_called_once()


if __name__=='__main__':unittest.main()
