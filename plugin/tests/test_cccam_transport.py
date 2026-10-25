import base64
import importlib.util
import pathlib
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import MagicMock, patch

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gsu_cccam_transport',ROOT/'src/GlassSysUtil/cccam_transport.py')
transport=importlib.util.module_from_spec(spec);spec.loader.exec_module(transport)


class TransportTests(unittest.TestCase):
    def test_real_local_http_auth_and_unicode_text(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                expected='Basic '+base64.b64encode(b'local:sample@pass').decode()
                if self.headers.get('Authorization') != expected:
                    self.send_response(401);self.send_header('WWW-Authenticate','Basic realm="WebInfo"');self.end_headers();return
                self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers()
                self.wfile.write('| Providers |\n| 0668 | Žltý provider |\n'.encode())
            def log_message(self,*args):pass
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            url='http://local:sample%%40pass@127.0.0.1:%d/providers' % server.server_port
            self.assertEqual(transport.open_text(url).readlines(),['| Providers |\n','| 0668 | Žltý provider |\n'])
        finally:
            server.shutdown();thread.join();server.server_close()

    def test_bound_and_no_global_opener_mutation(self):
        response=MagicMock();response.__enter__.return_value=response
        response.read.return_value=b'x'*33;response.headers.get_content_charset.return_value='utf-8'
        opener=MagicMock();opener.open.return_value=response
        with patch.object(transport,'LIMIT',32),patch.object(transport,'build_opener',return_value=opener):
            with self.assertRaises(OSError):transport.open_text('http://127.0.0.1:16001/providers')
            self.assertEqual(opener.open.call_args.kwargs['timeout'],4)
            response.read.assert_called_once_with(33)
