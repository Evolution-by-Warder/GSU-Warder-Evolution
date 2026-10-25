import importlib
from pathlib import Path
import types
import unittest
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'


class NativeStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load(ROOT);cls.status=importlib.import_module('Plugins.Extensions.GlassSysUtil.native_status')

    def screen(self):
        class Screen(dict):pass
        screen=Screen();screen.enCommand=True;screen.numSrv=0;screen.nativeSoftcam=MagicMock()
        screen.nativeSoftcam.selected.return_value='oscam-master';screen.statcommPics=MagicMock()
        screen['activCam']=MagicMock();screen['statCamSrvbin']=MagicMock()
        return screen

    def test_async_state_changes_set_green_red_and_do_not_rescan_on_gui_thread(self):
        screen=self.screen();pending=MagicMock()
        with patch.object(self.status,'deferToThread',return_value=pending) as worker,patch.object(self.status.time,'monotonic',return_value=10):self.status.request(screen,lambda s:s)
        worker.assert_called_once_with(screen.nativeSoftcam.active_name)
        screen.nativeSoftcam.active_name.assert_not_called()
        pending.addCallback.call_args.args[0]('oscam-master');screen.statcommPics.assert_any_call('stat','green')
        with patch.object(self.status,'deferToThread',return_value=pending),patch.object(self.status.time,'monotonic',return_value=12):self.status.request(screen,lambda s:s)
        pending.addCallback.call_args.args[0](None);screen.statcommPics.assert_any_call('stat','red')
        screen['statCamSrvbin'].setText.assert_called_with('No Running CAM')

    def test_inflight_and_one_second_limit_prevent_duplicate_requests(self):
        screen=self.screen();pending=MagicMock()
        with patch.object(self.status,'deferToThread',return_value=pending) as worker,patch.object(self.status.time,'monotonic',return_value=10):
            self.status.request(screen,lambda s:s);self.status.request(screen,lambda s:s)
            pending.addCallback.call_args.args[0](None)
            self.status.request(screen,lambda s:s);worker.assert_called_once()

    def test_late_result_after_manual_action_or_window_close_is_ignored(self):
        for closed in (False,True):
            screen=self.screen();pending=MagicMock()
            with patch.object(self.status,'deferToThread',return_value=pending):self.status.request(screen,lambda s:s)
            if closed:screen.nativeRegistryClosed=True
            else:screen.nativeStatusGeneration=1
            pending.addCallback.call_args.args[0]('oscam-master')
            screen.statcommPics.assert_not_called()


if __name__=='__main__':unittest.main()
