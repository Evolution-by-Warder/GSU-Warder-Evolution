import types
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
import unittest
from unittest.mock import MagicMock,patch
from receiver_stubs import load
from test_oscam_readers import fixture

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'


class ReaderActionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin=load(ROOT)
        cls.ui=cls.plugin._oscam_readers_ui

    def test_change_encodes_exact_label_and_verifies_a_fresh_read(self):
        name='TV & Vývoj + 23.5E'
        encoded='TV &amp; Vývoj + 23.5E'
        transport=MagicMock(side_effect=[[],fixture(encoded,enabled=False)])
        result=self.ui.set_enabled('http://box/','u','p',transport,name,False)
        query=parse_qs(urlsplit(transport.call_args_list[0].args[0]).query)
        self.assertEqual(query,{'label':[name],'action':['disable']})
        self.assertEqual(transport.call_args_list[1].args[0],'http://box/readers.html')
        self.assertEqual(result,fixture(encoded,enabled=False))

    def test_unchanged_missing_and_ambiguous_readers_do_not_report_success(self):
        for data in (fixture(),[],fixture(enabled=False)+fixture(enabled=False),['<html>authentication failed</html>']):
            with self.subTest(data=data),self.assertRaises(ValueError):
                self.ui.set_enabled('http://box/','','',MagicMock(side_effect=[[],data]),'server',False)

    def test_failed_transport_or_action_is_not_a_verified_change(self):
        for side_effect in ([None], [[],None]):
            with self.subTest(side_effect=side_effect),self.assertRaises(ValueError):
                self.ui.set_enabled('http://box/','','',MagicMock(side_effect=side_effect),'server',False)
        with self.assertRaises(ValueError):self.ui.fetch('http://box/','','',MagicMock(return_value=None))


class ReaderScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin=load(ROOT)
        cls.ui=cls.plugin._oscam_readers_ui

    def setUp(self):
        self.timer=MagicMock()
        with patch.object(self.plugin,'eTimer',return_value=self.timer):
            self.screen=self.plugin.oscam_readers(MagicMock(),'http://box/','','')
        self.api=vars(self.plugin)
        mock=patch.object(self.plugin,'MessageBox',types.SimpleNamespace(TYPE_INFO=0,TYPE_ERROR=1,TYPE_YESNO=2))
        mock.start();self.addCleanup(mock.stop)

    def render(self,data=None):self.ui.render(self.screen,self.api,fixture() if data is None else data)

    def test_one_deferred_request_keeps_transport_off_gui_and_rearms_after_result(self):
        pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending) as worker,patch.object(self.plugin,'getUrlData') as transport:
            self.screen.oscamreaders();self.screen.oscamreaders()
            worker.assert_called_once();transport.assert_not_called()
        pending.addCallback.call_args.args[0](fixture())
        self.assertEqual(self.screen['status_values_0'].text,'0 / 1 / 2 / 3\n4 / 5 / 6 / 7')
        self.assertEqual(self.screen['blue_button'].text,'Disable')
        self.timer.start.assert_called_with(8000,True)

    def test_no_wrap_or_skin_changes_and_selection_survives_reordered_rows(self):
        skin=self.screen.skin
        self.render(fixture('first')+fixture('second'))
        self.screen['list'].moveToIndex(1)
        self.render(fixture('second')+fixture('first'))
        self.assertEqual(self.ui.selected(self.screen)['label'],'second')
        self.assertEqual(self.screen.skin,skin)

    def test_confirmation_defaults_no_and_cancel_does_not_change_reader(self):
        self.render()
        with patch.object(self.ui,'deferToThread') as worker:
            self.screen.chngState();self.screen.chngState()
            self.screen.session.openWithCallback.assert_called_once()
            question=self.screen.session.openWithCallback.call_args
            self.assertFalse(question.kwargs['default'])
            self.assertIn('server',question.args[2])
            self.screen.oscamreaders();worker.assert_not_called()
            question.args[0](False);worker.assert_not_called()
        self.assertFalse(self.screen.readersConfirming)

    def test_confirmed_change_captures_reader_and_updates_only_from_verified_response(self):
        self.render(fixture('first')+fixture('second'))
        self.screen.chngState()
        callback=self.screen.session.openWithCallback.call_args.args[0]
        self.screen['list'].moveToIndex(1)
        pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending) as worker:
            callback(True);self.screen.chngState();self.screen.entitlements()
            worker.assert_called_once()
        self.assertEqual(worker.call_args.args[-2:],('first',False))
        self.screen.session.open.assert_not_called()
        pending.addCallback.call_args.args[0](fixture('first',enabled=False)+fixture('second'))
        self.screen['list'].moveToIndex(0);self.screen.reactivate()
        self.assertEqual(self.screen['blue_button'].text,'Enable')
        self.screen.session.open.assert_not_called()  # No unconditional success popup.

    def test_action_failure_clears_stale_state_and_does_not_show_success(self):
        self.render();self.screen.chngState()
        pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending):
            self.screen.session.openWithCallback.call_args.args[0](True)
        pending.addErrback.call_args.args[0](object())
        self.assertEqual(self.screen.readerRecords,{})
        self.assertEqual(self.screen['blue_button'].text,'')
        self.assertEqual(self.screen['status_values_0'].text,'')
        self.assertEqual(self.screen.session.open.call_args.args[-1],1)
        self.timer.start.assert_called_with(8000,True)

    def test_network_failure_keeps_window_open_clears_details_and_retries(self):
        self.render();pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending):self.screen.oscamreaders()
        pending.addErrback.call_args.args[0](object())
        self.assertFalse(self.screen.readersClosed)
        self.assertEqual(self.screen.readerRecords,{})
        self.assertEqual(self.screen['status_values_1'].text,'')
        self.timer.start.assert_called_with(8000,True)

    def test_closing_during_fetch_ignores_late_result_and_error(self):
        pending=MagicMock()
        with patch.object(self.ui,'deferToThread',return_value=pending):self.screen.oscamreaders()
        self.screen.exit()
        with patch.object(self.ui,'render') as render:
            pending.addCallback.call_args.args[0](fixture())
            pending.addErrback.call_args.args[0](object())
            render.assert_not_called()
        self.assertIsNone(self.screen.refreshTimer)
        self.screen.session.open.assert_not_called()

    def test_confirmation_answer_after_closing_sends_no_action(self):
        self.render();self.screen.chngState()
        callback=self.screen.session.openWithCallback.call_args.args[0]
        self.screen.exit()
        with patch.object(self.ui,'deferToThread') as worker:callback(True);worker.assert_not_called()

    def test_entitlements_url_encodes_real_label_and_rejects_unsupported_protocol(self):
        self.render(fixture('TV &amp; news +',protocol='internal'))
        self.screen.entitlements()
        self.assertEqual(self.screen.session.open.call_args.args[2],'TV%20%26%20news%20%2B')
        self.render(fixture(protocol='cs378x'));self.screen.entitlements()
        self.assertIs(self.screen.session.open.call_args.args[0],self.plugin.MessageBox)

    def test_empty_table_clears_previous_counters_and_cannot_change_a_reader(self):
        self.render();self.render([])
        self.assertEqual(self.screen.readerRecords,{})
        self.assertEqual(self.screen['status_values_0'].text,'')
        self.screen.chngState();self.screen.session.openWithCallback.assert_not_called()


if __name__=='__main__':unittest.main()
