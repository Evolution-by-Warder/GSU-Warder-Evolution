from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'


class NativeStartConfigUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin=load(ROOT)
        cls.ui=__import__('Plugins.Extensions.GlassSysUtil.native_start_config_ui',fromlist=['NativeStartConfigScreen'])

    def snapshot(self):
        return {'name':'oscam-master','script_sha256':'hash','pidfile':'/var/tmp/oscam-master.pid','supported':['config_dir','temp_dir','debug','restart','pending','capture'],
            'values':{'config_dir':'/etc/tuxbox/config/oscam-master','temp_dir':'/tmp/.oscam','debug':0,'restart':2,'pending':32,'capture':False}}

    def api(self):
        return {'_':lambda s:s,'oscam_start':'<screen/>','MessageBox':types.SimpleNamespace(TYPE_INFO=0,TYPE_ERROR=1),'dirBrowser':object()}

    def make_screen(self):
        self.session=types.SimpleNamespace(open=MagicMock(),openWithCallback=MagicMock())
        self.store=MagicMock()
        return self.ui.NativeStartConfigScreen(self.session,self.snapshot(),self.store,self.api())

    def test_local_edits_and_cancel_do_not_write_or_change_legacy_global_settings(self):
        previous=self.plugin.config.plugins.GlassSysUtil.par17.value
        screen=self.make_screen()
        screen.settings['config_dir'].value='/another/config'
        screen.settings['restart'].value='0'
        self.assertEqual(screen.values()['restart'],0)
        screen.cancel()
        self.assertEqual(screen.result,(False,));self.store.save.assert_not_called()
        self.assertEqual(self.plugin.config.plugins.GlassSysUtil.par17.value,previous)

    def test_save_runs_in_worker_and_closes_after_the_information_dialog(self):
        screen=self.make_screen();screen.settings['debug'].value=128
        pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending) as background:screen.save()
        self.assertTrue(screen.saving)
        self.assertEqual(background.call_args.args[0],self.store.save)
        self.assertEqual(background.call_args.args[2]['debug'],128)
        pending.addCallback.call_args.args[0](None)
        self.assertFalse(hasattr(screen,'result'))
        confirm=self.session.openWithCallback.call_args.args[0]
        confirm(None)
        self.assertEqual(screen.result,(True,))

    def test_save_error_keeps_editor_open_and_can_be_retried(self):
        screen=self.make_screen();pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending):screen.save()
        pending.addErrback.call_args.args[0](types.SimpleNamespace(value=OSError('changed init script')))
        self.assertFalse(screen.saving);self.assertFalse(hasattr(screen,'result'))
        self.session.open.assert_called_once()
        self.assertIn('changed init script',self.session.open.call_args.args[1])

    def test_probe_is_async_and_does_not_open_editor_after_manager_closes(self):
        manager={'statCamSrvcmd':MagicMock()}
        class Manager(dict):pass
        screen=Manager(manager);screen.enCommand=True;screen.nativeRegistryClosed=False
        screen.nativeSoftcam=types.SimpleNamespace(init_dir='/etc/init.d',bin_dir='/usr/bin')
        screen.session=types.SimpleNamespace(open=MagicMock(),openWithCallback=MagicMock())
        screen.inicializeUCM=MagicMock();pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending):
            self.assertTrue(self.ui.open_start_config(screen,self.api(),'oscam-master'))
        self.assertFalse(screen.enCommand)
        screen.nativeRegistryClosed=True
        pending.addCallback.call_args.args[0](self.snapshot())
        self.assertTrue(screen.enCommand);screen.session.openWithCallback.assert_not_called()


if __name__=='__main__':unittest.main()
