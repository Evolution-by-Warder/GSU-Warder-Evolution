import importlib.util
from pathlib import Path
import types
import unittest
import tempfile
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('native_autostart_test',ROOT/'native_autostart.py')
boot=importlib.util.module_from_spec(spec);spec.loader.exec_module(boot)


class NativeAutostartTests(unittest.TestCase):
    def setUp(self):
        self.log=patch.object(boot,'log_event');self.log.start();self.addCleanup(self.log.stop)
        self.publish=patch.object(boot,'publish_guard');self.publish.start();self.addCleanup(self.publish.stop)
        self.native=MagicMock();self.native.selected.return_value='oscam-master'
        self.native.active_name.return_value=None;self.native.start_verified.return_value=0

    def test_wait_uses_timer_and_starts_worker_only_after_expiry_once(self):
        timer=MagicMock();container=MagicMock();container.execute.return_value=0
        factory=MagicMock(return_value=container)
        delayed=boot.DelayedNativeStart(self.native,lambda:timer,factory,10)
        self.assertTrue(delayed.schedule());timer.startLongTimer.assert_called_once_with(10)
        factory.assert_not_called();self.native.start_verified.assert_not_called()
        delayed.fire()
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
        plugin.config.plugins.GlassSysUtil.par50.value=False
        with patch.object(native_module,'NativeSoftcam',return_value=self.native),patch.object(helper,'log_event'),patch.object(helper,'publish_guard'),patch.object(plugin,'eTimer',return_value=timer):
            plugin.autocams.autoStartCheck(object())
        timer.startLongTimer.assert_called_once_with(10)
        self.assertEqual(plugin.autocams.nativeDelayedStart.name,'oscam-master')
        with patch.object(helper,'publish_guard'),patch.object(helper,'log_event'):plugin.sessionAutostart(1)
        self.assertTrue(plugin.autocams.nativeDelayedStart.cancelled)
        helper._ACTIVE=None

    def test_session_hook_retains_independent_mount_checker(self):
        plugin=load(ROOT)
        helper=__import__('Plugins.Extensions.GlassSysUtil.native_autostart',fromlist=['begin'])
        native_module=__import__('Plugins.Extensions.GlassSysUtil.native_softcam',fromlist=['NativeSoftcam'])
        owner=types.SimpleNamespace(chckCifsNfs=MagicMock())
        config=types.SimpleNamespace(plugins=types.SimpleNamespace(GlassSysUtil=types.SimpleNamespace(par48=types.SimpleNamespace(value=10),par50=types.SimpleNamespace(value=False),par57=types.SimpleNamespace(value='1'))))
        api={'config':config,'eTimer':MagicMock(),'eConsoleAppContainer':MagicMock()}
        with patch.object(native_module,'NativeSoftcam',return_value=self.native),patch.object(helper,'log_event'),patch.object(helper,'publish_guard'):
            self.assertTrue(helper.begin(owner,api))
        owner.chckCifsNfs.assert_called_once()
        helper._ACTIVE=None

    def controller(self,enabled=True):
        self.setting=types.SimpleNamespace(value=enabled)
        self.timers=[MagicMock(),MagicMock()]
        self.container=MagicMock();self.container.execute.return_value=0
        self.factory=MagicMock(return_value=self.container)
        controller=boot.DelayedNativeStart(self.native,iter(self.timers).__next__,self.factory,10,lambda:self.setting.value)
        controller.schedule();controller.fired=True;controller.configure()
        return controller

    def test_autocheck_schedules_15_seconds_and_rearms_only_after_worker(self):
        controller=self.controller()
        self.timers[1].startLongTimer.assert_called_with(15)
        self.factory.assert_not_called()
        controller.check()
        self.assertIn('--autocheck oscam-master --guard ',self.container.execute.call_args.args[0])
        controller.check();self.factory.assert_called_once()
        controller.finished(0)
        self.timers[1].startLongTimer.assert_called_with(15)
        controller.check();self.assertEqual(self.factory.call_count,2)

    def test_disabled_control_has_no_periodic_worker_and_toggle_is_live(self):
        controller=self.controller(False)
        self.timers[1].startLongTimer.assert_not_called()
        controller.check();self.factory.assert_not_called()
        self.setting.value=True;controller.configure()
        self.timers[1].startLongTimer.assert_called_once_with(15)
        self.setting.value=False;controller.configure();controller.check()
        self.factory.assert_not_called()

    def test_manual_stop_invalidates_queued_worker_and_pauses_recovery(self):
        controller=self.controller();old=controller.token
        ticket=controller.manual_begin('oscam-master','stop')
        self.assertNotEqual(controller.token,old)
        controller.manual_end(ticket,True)
        controller.check();controller.fire();self.factory.assert_not_called()
        ticket=controller.manual_begin('oscam-master','start')
        controller.check();self.factory.assert_not_called()
        controller.manual_end(ticket,True);controller.check()
        self.factory.assert_called_once()

    def test_failed_stop_restores_monitoring_but_failed_start_keeps_manual_pause(self):
        controller=self.controller()
        ticket=controller.manual_begin('oscam-master','stop');controller.manual_end(ticket,False)
        self.assertNotIn('oscam-master',controller.paused)
        ticket=controller.manual_begin('oscam-master','stop');controller.manual_end(ticket,True)
        ticket=controller.manual_begin('oscam-master','start');controller.manual_end(ticket,False)
        controller.check();self.factory.assert_not_called()

    def test_autocheck_follows_current_selection_and_does_not_guess_none(self):
        controller=self.controller();self.native.selected.return_value=None
        controller.check();self.factory.assert_not_called()
        self.native.selected.return_value='oscam-uni';controller.check()
        self.assertIn('--autocheck oscam-uni ',self.container.execute.call_args.args[0])

    def test_spawn_failure_releases_inflight_and_delays_retry(self):
        controller=self.controller();self.container.execute.side_effect=OSError('spawn failed')
        controller.check();self.assertFalse(controller.inflight)
        self.timers[1].startLongTimer.assert_called_with(30)
        self.container.execute.side_effect=None;controller.check()
        self.assertEqual(self.factory.call_count,2)

    def test_repeated_failure_backoff_is_bounded_and_success_resets_it(self):
        controller=self.controller()
        for interval in (30,60,120,240,300,300,300):
            controller.check();controller.finished(1)
            self.timers[1].startLongTimer.assert_called_with(interval)
        controller.check();controller.finished(0)
        self.timers[1].startLongTimer.assert_called_with(15)

    def test_manual_action_and_new_selection_clear_previous_failure_delay(self):
        controller=self.controller();controller.check();controller.finished(1)
        ticket=controller.manual_begin('oscam-master','start');controller.manual_end(ticket,True)
        self.timers[1].startLongTimer.assert_called_with(15)
        controller.check();controller.finished(1)
        self.native.selected.return_value='oscam-uni'
        controller.check();controller.finished(1)
        self.timers[1].startLongTimer.assert_called_with(30)

    def test_cancelled_worker_failure_does_not_extend_current_session_retry(self):
        controller=self.controller();controller.check();old=controller.token
        ticket=controller.manual_begin('oscam-master','start')
        controller.finished(1,old);controller.manual_end(ticket,True)
        self.timers[1].startLongTimer.assert_called_with(15)

    def test_periodic_timer_cannot_bypass_initial_30_second_startup_delay(self):
        timers=[MagicMock(),MagicMock()];factory=MagicMock()
        factory.return_value.execute.return_value=0
        controller=boot.DelayedNativeStart(self.native,iter(timers).__next__,factory,30,lambda:True)
        controller.schedule();controller.configure();controller.check()
        timers[0].startLongTimer.assert_called_once_with(30)
        timers[1].startLongTimer.assert_not_called();factory.assert_not_called()
        controller.fire();controller.finished(0)
        timers[1].startLongTimer.assert_called_once_with(15)

    def test_native_autocheck_help_has_new_interval_and_slovak_text(self):
        api={'_':lambda text:text,'config':types.SimpleNamespace(osd=types.SimpleNamespace(language=types.SimpleNamespace(value='sk_SK')))}
        self.assertIn('15 sekúnd',boot.autocheck_help(api))

    def test_stale_guard_or_disabled_recovery_cannot_start_cam(self):
        with tempfile.TemporaryDirectory() as folder,patch.object(boot,'GUARD',Path(folder)/'guard.json'):
            # Use real atomic guard publication for this test only.
            self.publish.stop()
            boot.publish_guard('one',True)
            self.assertTrue(boot.guard_valid('one',True))
            boot.publish_guard('two',False)
            self.assertFalse(boot.guard_valid('one'))
            self.assertFalse(boot.guard_valid('two',True))
            self.assertTrue(boot.guard_valid('two'))
            boot.start_if_needed(self.native,'oscam-master','one',True)
            boot.start_if_needed(self.native,'oscam-master','two',True)
            self.native.start_verified.assert_not_called()

    def test_enable_toggle_keeps_initial_boot_guard_but_disables_queued_periodic_worker(self):
        controller=self.controller();old=controller.token
        self.setting.value=False;controller.configure()
        self.assertEqual(controller.token,old)
        self.assertEqual(boot.publish_guard.call_args.args,(old,False))

    def test_shutdown_invalidates_pending_request_and_stops_both_timers(self):
        controller=self.controller();old=controller.token;controller.cancel()
        self.assertNotEqual(controller.token,old)
        controller.check();controller.fire();self.factory.assert_not_called()
        for timer in self.timers:timer.stop.assert_called()

    def test_original_toggle_notifies_native_controller_without_gui_restart(self):
        plugin=load(ROOT)
        plugin.config.plugins.GlassSysUtil.par50.value=False
        screen=types.SimpleNamespace(enaAutochckChck=MagicMock())
        with patch.object(plugin,'_native_autostart_configure') as configure:
            plugin.univCamMng.enaAutochck(screen)
            self.assertTrue(plugin.config.plugins.GlassSysUtil.par50.value)
            configure.assert_called_once_with(plugin.autocams)


if __name__=='__main__':unittest.main()
