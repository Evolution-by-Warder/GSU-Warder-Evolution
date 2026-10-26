import importlib
from pathlib import Path
import tempfile
import subprocess
import unittest
from contextlib import nullcontext
from unittest.mock import MagicMock,patch
from receiver_stubs import load
ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
load(ROOT)
recovery=importlib.import_module('Plugins.Extensions.GlassSysUtil.oscam_client_recovery')

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.config=self.root/'cfg';self.config.mkdir()
        self.proc=self.root/'proc';(self.proc/'42').mkdir(parents=True)
        (self.proc/'42/cmdline').write_bytes(('/usr/bin/oscam-custom\0--config-dir\0'+str(self.config)+'\0').encode())
        (self.config/'oscam.conf').write_text('[dvbapi]\nenabled=1\nuser=Gigablue\n[webif]\nhttpport=8888\n')
        self.native=MagicMock();self.native.proc_dir=self.proc
        self.native.selected.return_value='oscam-custom';self.native._matching_pids.return_value={42:'identity'}
        self.base='http://127.0.0.1:8888/'
    def test_target_uses_live_process_config_and_exact_user_and_webif(self):
        self.assertEqual(recovery.recovery_target(self.base,'Gigablue',self.native),'oscam-custom')
        for base,user in (('http://192.0.2.1:8888/','Gigablue'),('http://127.0.0.1:8889/','Gigablue'),('https://127.0.0.1:8888/','Gigablue'),(self.base,'Other')):
            self.assertIsNone(recovery.recovery_target(base,user,self.native))
        (self.config/'oscam.conf').write_text('[dvbapi]\nenabled=0\nuser=Gigablue\n[webif]\nhttpport=8888')
        self.assertIsNone(recovery.recovery_target(self.base,'Gigablue',self.native))
    def test_missing_running_process_or_malformed_config_does_not_guess_target(self):
        self.native._matching_pids.return_value={}
        self.assertIsNone(recovery.recovery_target(self.base,'Gigablue',self.native))
        self.native._matching_pids.return_value={42:'identity'}
        (self.config/'oscam.conf').write_text('invalid')
        self.assertIsNone(recovery.recovery_target(self.base,'Gigablue',self.native))
    def change(self,disabled=False,**kwargs):
        return recovery.change_account(self.base,'u','p',MagicMock(),'Gigablue',disabled,native=self.native,lock=nullcontext,**kwargs)
    def test_only_verified_enable_restarts_once_then_waits_and_returns_fresh_records(self):
        events=[];records=[{'name':'Gigablue','connected':True}]
        with patch.object(recovery,'set_enabled',side_effect=lambda *args:events.append('enable')):
            self.native.restart_verified.side_effect=lambda name:events.append('restart')
            def ready(*args):events.append('wait');return records
            result=self.change(wait=ready)
        self.assertEqual(events,['enable','restart','wait'])
        self.native.restart_verified.assert_called_once_with('oscam-custom')
        self.assertEqual(result,{'restarted':True,'records':records})
    def test_disable_remote_and_other_account_do_not_restart_or_wait(self):
        wait=MagicMock()
        with patch.object(recovery,'set_enabled',return_value=True):
            self.change(disabled=True,wait=wait)
            recovery.change_account('http://192.0.2.1/','','',MagicMock(),'Gigablue',False,native=self.native,lock=nullcontext,wait=wait)
            recovery.change_account(self.base,'','',MagicMock(),'Other',False,native=self.native,lock=nullcontext,wait=wait)
        self.native.restart_verified.assert_not_called();wait.assert_not_called()
    def test_failed_enable_cannot_restart(self):
        with patch.object(recovery,'set_enabled',side_effect=recovery.ClientError('not confirmed')):
            with self.assertRaises(recovery.ClientError):self.change()
        self.native.restart_verified.assert_not_called()
    def test_selection_change_after_enable_prevents_restart(self):
        def changed(*args):self.native.selected.return_value='another-cam'
        with patch.object(recovery,'set_enabled',side_effect=changed):
            with self.assertRaises(recovery.RecoveryError):self.change()
        self.native.restart_verified.assert_not_called()
    def test_restart_or_reconnect_failure_reports_partial_success_without_retrying_restart(self):
        for restart_error in (OSError("failed"),subprocess.TimeoutExpired("restart",20),None):
            self.native.restart_verified.reset_mock()
            self.native.restart_verified.side_effect=restart_error
            with patch.object(recovery,'set_enabled',return_value=True):
                with self.assertRaises(recovery.RecoveryError):self.change(wait=MagicMock(side_effect=recovery.ClientError('offline')))
            self.native.restart_verified.assert_called_once()
    def test_wait_requires_original_dvbapi_identity_then_fetches_actual_combined_records(self):
        status=lambda name:'<oscam><status><client type="c" name="'+name+'" protocol="dvbapi"/></status></oscam>'
        fetch=MagicMock(side_effect=[None,status('anonymous'),status('Gigablue')])
        ticks=iter([0,1,2,3]);sleep=MagicMock()
        with patch.object(recovery,'fetch_clients',return_value=['fresh']) as fresh:
            result=recovery.wait_ready(self.base,'u','p',fetch,'Gigablue',clock=lambda:next(ticks),sleep=sleep)
        self.assertEqual(result,['fresh']);self.assertEqual(sleep.call_count,2)
        fresh.assert_called_once_with(self.base,'u','p',fetch)
    def test_wait_timeout_does_not_treat_anonymous_as_recovered(self):
        ticks=iter([0,1,2,3]);fetch=MagicMock(return_value='<oscam><status><client type="c" name="anonymous" protocol="dvbapi"/></status></oscam>')
        with self.assertRaises(recovery.RecoveryError):
            recovery.wait_ready(self.base,'','',fetch,'Gigablue',timeout=3,clock=lambda:next(ticks),sleep=lambda _:None)
