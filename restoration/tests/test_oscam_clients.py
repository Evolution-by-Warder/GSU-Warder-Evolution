import importlib.util
from pathlib import Path
import types
import unittest
from unittest.mock import MagicMock, patch
from receiver_stubs import load

ROOT = Path(__file__).resolve().parents[1] / 'src/GlassSysUtil'
spec = importlib.util.spec_from_file_location('clients_parser_test', ROOT / 'oscam_clients.py')
clients = importlib.util.module_from_spec(spec); spec.loader.exec_module(clients)

# Schema/column classes from OpenVisionE2/oscam webif/api.xml and userconfig templates.
STATUS = '''<oscam><status>
<client type="s" name="root" protocol="server"/>
<client type="h" name="root" protocol="http"/>
<client type="r" name="reader" protocol="internal"/>
<client type="p" name="server" protocol="cs378x"/>
<client type="c" name="Gigablue" protocol="dvbapi" thid="0x10">
 <request caid="0624" provid="000000" srvid="3399" ecmtime="492" answered="server">JOJ PLUS HD [M7 Group]</request>
 <times login="2026-10-25" online="4122" idle="1"/>
 <connection ip="camd.socket" port="0">OK</connection>
</client></status></oscam>'''
USERS = '''<oscam><users><user name="Gigablue" status="online" ip="camd.socket" protocol="dvbapi">
<stats><cwok>123</cwok><cwnok>2</cwnok><cwignore>0</cwignore><cwtimeout>1</cwtimeout>
<cwcache>8</cwcache><cwtun>0</cwtun><cwlastresptime>490</cwlastresptime>
<emmok>3</emmok><emmnok>0</emmnok><timeonchannel>62</timeonchannel></stats>
</user><user name="Offline" status="offline" ip="" protocol=""><stats><cwok>0</cwok></stats></user>
</users></oscam>'''
HTML_USERS = '''<table><TR CLASS="online" id="user1" nopoll="">
<TD CLASS="usercol0"><A class="switchuser" data-next-action="disable" data-user-name="Gigablue" HREF="#">switch</A></TD>
<TD TITLE="Gigablue" data-sort-value="Gigablue" CLASS="usercol1"><A HREF="user_edit.html?user=Gigablue">Gigablue</A><SPAN CLASS="span_notifier">2</SPAN></TD>
<TD CLASS="usercol2">online<BR>camd.socket</TD><TD CLASS="usercol4">dvbapi</TD>
<TD CLASS="usercol5 groups"><DIV CLASS="groups">1,2</DIV></TD>
<TD CLASS="usercol3">00:00:01<BR>00:01:02</TD><TD CLASS="usercol6">JOJ PLUS HD</TD>
<TD CLASS="usercol7">492 ms</TD><TD CLASS="usercol9">123</TD><TD CLASS="usercol10">2</TD>
<TD CLASS="usercol11">0</TD><TD CLASS="usercol12">1</TD><TD CLASS="usercol14">8</TD>
<TD CLASS="usercol15">0</TD><TD CLASS="usercol17">3</TD><TD CLASS="usercol18">0</TD>
<TD CLASS="usercol13 hidden"><SPAN>10</SPAN> / <SPAN>9</SPAN> / <SPAN>1</SPAN> / <SPAN>0</SPAN></TD>
</TR></table>'''
HTML_STATUS = '''<table><TR ID="0x10" CLASS="c">
<TD CLASS="statuscol4"><A HREF="user_edit.html?user=Gigablue">Gigablue</A></TD>
<TD CLASS="statuscol7">camd.socket</TD><TD CLASS="statuscol9">dvbapi</TD>
<TD CLASS="statuscol13"><IMG ALT="JOJ PLUS HD"></TD>
<TD CLASS="statuscol15" TITLE="Online: 4122&#013;IDLE: 1">date</TD>
<TD CLASS="statuscol16">OK</TD></TR></table>'''


class ClientParserTests(unittest.TestCase):
    def test_status_keeps_real_named_client_and_excludes_readers_proxies_and_webif(self):
        rows = clients.parse_status(STATUS.splitlines())
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['name'], 'Gigablue')
        self.assertEqual(rows[0]['protocol'], 'dvbapi')
        self.assertEqual(rows[0]['address'], 'camd.socket')
        self.assertEqual(rows[0]['idle'], '0:00:01')
        self.assertEqual(rows[0]['status'], 'OK')

    def test_merge_adds_account_stats_keeps_live_ecm_and_offline_accounts(self):
        rows = clients.merge(clients.parse_status(STATUS), clients.parse_users(USERS))
        self.assertEqual([row['name'] for row in rows], ['Gigablue', 'Offline'])
        self.assertEqual(rows[0]['stats']['cwok'], '123')
        self.assertEqual(rows[0]['stats']['cwlastresptime'], '492')
        self.assertEqual(rows[0]['channel_time'], '0:01:02')
        self.assertTrue(rows[0]['manageable'])
        self.assertEqual(rows[1]['stats']['cwok'], '0')
        self.assertEqual(rows[1]['stats']['emmok'], '')

    def test_multiple_sessions_of_same_account_are_not_collapsed_or_renamed(self):
        first = clients.parse_status(STATUS)[0]
        second = dict(first, key='client:0x11', channel='Other channel')
        rows = clients.merge([first, second], clients.parse_users(USERS))
        self.assertEqual([r['key'] for r in rows], ['client:0x10', 'client:0x11', 'user:Offline'])
        self.assertEqual(rows[1]['channel'], 'Other channel')

    def test_unicode_special_characters_and_other_receivers_are_from_server(self):
        value = STATUS.replace('Gigablue', 'Vývoj &amp; Test*VU+')
        rows = clients.merge(clients.parse_status(value), [])
        self.assertEqual(rows[0]['name'], 'Vývoj & Test*VU+')
        self.assertFalse(rows[0]['manageable'])
        self.assertEqual(rows[0]['stats']['cwlastresptime'], '492')

    def test_modern_html_is_independent_of_whitespace_order_case_and_notifier_count(self):
        for value in (HTML_USERS, HTML_USERS.replace('TD', 'td').replace('CLASS=', 'class=').replace('\n', '')):
            row = clients.parse_users_html(value)[0]
            self.assertEqual(row['name'], 'Gigablue')
            self.assertEqual(row['stats']['cwok'], '123')
            self.assertEqual(row['stats']['cwcycle'], '10 / 9 / 1 / 0')
            self.assertEqual(row['channel_time'], '00:01:02')
            self.assertEqual(row['address'], 'camd.socket')

    def test_html_status_fallback_reads_clients_only(self):
        value = HTML_STATUS + HTML_STATUS.replace('CLASS="c"', 'CLASS="p"')
        rows = clients.parse_status_html(value)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['channel'], 'JOJ PLUS HD')
        self.assertEqual(rows[0]['idle'], '0:00:01')

    def test_bounded_fallback_uses_only_read_endpoints(self):
        calls = []
        def fetch(url, user, password):
            calls.append(url)
            if 'oscamapi' in url:
                return None
            return HTML_USERS if 'userconfig' in url else HTML_STATUS
        rows = clients.fetch_clients('http://127.0.0.1:8884', 'user', 'secret', fetch)
        self.assertEqual(rows[0]['name'], 'Gigablue')
        self.assertEqual(rows[0]['stats']['cwok'], '123')
        self.assertEqual(len(calls), 4)
        self.assertFalse(any('action=' in url for url in calls))

    def test_stats_failure_keeps_status_without_fabricating_counters_or_controls(self):
        fetch = lambda url, *unused: STATUS if 'part=status' in url else None
        row = clients.fetch_clients('http://box/', '', '', fetch)[0]
        self.assertEqual(row['name'], 'Gigablue')
        self.assertNotIn('cwok', row['stats'])
        self.assertFalse(row['manageable'])

    def test_valid_empty_status_is_not_confused_with_authentication_or_malformed_xml(self):
        self.assertEqual(clients.parse_status('<oscam><status/></oscam>'), [])
        for data in [None, '<html>Unauthorized</html>', '<oscam><status>', '<!DOCTYPE x><oscam><status/></oscam>']:
            with self.assertRaises(clients.ClientError):
                clients.parse_status(data)

    def test_state_change_url_encodes_account_and_requires_confirmed_result(self):
        name = 'Test & Vývoj'
        response = USERS.replace('Gigablue', 'Test &amp; Vývoj').replace('status="online"', 'status="disabled"')
        fetch = MagicMock(return_value=response)
        self.assertTrue(clients.set_enabled('http://box/', 'user', 'secret', fetch, name, True))
        query = clients.parse_qs(clients.urlsplit(fetch.call_args.args[0]).query)
        self.assertEqual(query['user'], [name]); self.assertEqual(query['action'], ['disable'])
        fetch.return_value = USERS.replace('Gigablue', 'Test &amp; Vývoj')
        with self.assertRaises(clients.ClientError):
            clients.set_enabled('http://box/', 'user', 'secret', fetch, name, True)


class ClientScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin = load(ROOT)
        from Plugins.Extensions.GlassSysUtil import oscam_clients_ui
        cls.ui = oscam_clients_ui

    def setUp(self):
        self.timer = MagicMock()
        with patch.object(self.plugin, 'eTimer', return_value=self.timer):
            self.screen = self.plugin.oscam_Users(MagicMock(), 'http://127.0.0.1:8884/', 'test', 'secret')
        self.records = clients.merge(clients.parse_status(STATUS), clients.parse_users(USERS))
        box = types.SimpleNamespace(TYPE_INFO=0, TYPE_ERROR=1, TYPE_YESNO=2)
        mock = patch.object(self.plugin, 'MessageBox', box); mock.start(); self.addCleanup(mock.stop)

    def test_requests_are_deferred_and_duplicate_timer_requests_are_ignored(self):
        pending = MagicMock()
        with patch.object(self.ui, 'deferToThread', return_value=pending) as worker, patch.object(self.plugin, 'getUrlData') as fetch:
            self.screen.oscamUsers(); self.screen.oscamUsers()
            worker.assert_called_once(); fetch.assert_not_called()
        pending.addCallback.call_args.args[0](self.records)
        self.assertEqual(self.screen.list[0][0], 'client:0x10')
        self.assertIn('dvbapi', self.screen['status_values_0'].text)
        self.assertIn('JOJ PLUS HD', self.screen['status_values_0'].text)
        self.assertEqual(self.screen['status_values_1'].text, '123\n2\n0\n1\n—')
        self.assertEqual(self.screen['status_values_2'].text, '8\n0\n492 ms\n3\n0')
        self.timer.start.assert_called_with(8000, True)

    def test_refresh_preserves_selected_client_when_rows_reorder(self):
        self.ui.render(self.screen, vars(self.plugin), self.records)
        self.screen['list'].moveToIndex(1)
        self.ui.render(self.screen, vars(self.plugin), list(reversed(self.records)))
        self.assertEqual(self.screen['list'].getCurrent()[0], 'user:Offline')
        self.assertEqual(self.screen['status_values_1'].text, '0\n—\n—\n—\n—')

    def test_empty_response_clears_previous_details_and_blue_action(self):
        self.ui.render(self.screen, vars(self.plugin), self.records)
        self.ui.render(self.screen, vars(self.plugin), [])
        self.assertEqual(self.screen.list[0][0], '*')
        self.assertEqual(self.screen['status_values_0'].text, '\n'.join(['—'] * 5))
        self.assertEqual(self.screen['blue_button'].text, '')

    def test_failure_clears_stale_counters_leaves_screen_open_and_retries(self):
        self.ui.render(self.screen, vars(self.plugin), self.records)
        pending = MagicMock()
        with patch.object(self.ui, 'deferToThread', return_value=pending):
            self.screen.oscamUsers()
        pending.addErrback.call_args.args[0](types.SimpleNamespace(value=OSError('offline')))
        self.assertFalse(self.screen.clientsClosed)
        self.assertEqual(self.screen.clientRecords, {})
        self.assertEqual(self.screen['status_values_1'].text, '\n'.join(['—'] * 5))
        self.timer.start.assert_called_with(8000, True)

    def test_close_stops_timer_and_late_response_does_not_touch_widgets(self):
        pending = MagicMock()
        with patch.object(self.ui, 'deferToThread', return_value=pending):
            self.screen.oscamUsers()
        self.screen.exit()
        self.assertIsNone(self.screen.refreshTimer)
        with patch.object(self.ui, 'render') as render:
            pending.addCallback.call_args.args[0](self.records)
        render.assert_not_called()
        self.assertTrue(self.screen.clientsClosed)

    def test_blue_action_requires_confirmation_and_cancel_sends_no_command(self):
        self.ui.render(self.screen, vars(self.plugin), self.records)
        with patch.object(self.ui, 'deferToThread') as worker:
            self.screen.chngState()
            request = self.screen.session.openWithCallback.call_args
            self.assertFalse(request.kwargs['default'])
            self.assertIn('Gigablue', request.args[2])
            request.args[0](False)
            worker.assert_not_called()
        self.assertFalse(self.screen.clientsConfirming)

    def test_confirmed_action_uses_captured_account_and_refreshes_after_verified_success(self):
        self.ui.render(self.screen, vars(self.plugin), self.records)
        self.screen.chngState()
        callback = self.screen.session.openWithCallback.call_args.args[0]
        self.screen['list'].moveToIndex(1)
        pending = MagicMock()
        with patch.object(self.ui, 'deferToThread', return_value=pending) as worker:
            callback(True)
        self.assertEqual(worker.call_args.args[-2:], ('Gigablue', True))
        with patch.object(self.ui, 'request') as refresh:
            pending.addCallback.call_args.args[0](True)
        refresh.assert_called_once()

    def test_client_without_account_stats_has_no_enable_disable_action(self):
        self.ui.render(self.screen, vars(self.plugin), clients.merge(clients.parse_status(STATUS), []))
        self.assertEqual(self.screen['blue_button'].text, '')
        self.screen.chngState()
        self.screen.session.openWithCallback.assert_not_called()

    def test_html_fallback_ecm_time_keeps_one_millisecond_unit(self):
        records = clients.merge(clients.parse_status_html(HTML_STATUS), clients.parse_users_html(HTML_USERS))
        self.ui.render(self.screen, vars(self.plugin), records)
        self.assertIn('492 ms', self.screen['status_values_2'].text)
        self.assertNotIn('ms ms', self.screen['status_values_2'].text)

    def test_actual_authenticated_http_fetch_reads_both_api_endpoints(self):
        import base64
        from http.server import BaseHTTPRequestHandler, HTTPServer
        import threading
        paths = []
        expected = 'Basic ' + base64.b64encode(b'test:secret').decode()
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.headers.get('Authorization') != expected:
                    self.send_response(401)
                    self.send_header('WWW-Authenticate', 'Basic realm="OSCam"')
                    self.end_headers()
                    return
                paths.append(self.path)
                data = STATUS if self.path.endswith('part=status') else USERS
                self.send_response(200); self.end_headers(); self.wfile.write(data.encode())
            def log_message(self, *args):
                pass
        server = HTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            rows = clients.fetch_clients('http://127.0.0.1:%d/' % server.server_port,
                                        'test', 'secret', self.plugin.getUrlData)
        finally:
            server.shutdown(); server.server_close(); thread.join(timeout=2)
        self.assertEqual(rows[0]['name'], 'Gigablue')
        self.assertEqual(rows[0]['stats']['cwok'], '123')
        self.assertEqual(paths, ['/oscamapi.html?part=status', '/oscamapi.html?part=userstats'])

