import ast
import hashlib
import json
import pathlib
import tempfile
import types
import unittest
from unittest.mock import patch
from receiver_stubs import load

BASE=pathlib.Path(__file__).resolve().parents[1]
ROOT=BASE/'src/GlassSysUtil'
SOURCE=ROOT/'plugin.py'


class OriginalPortTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.plugin=load(ROOT)

    def test_every_original_class_function_and_signature_is_retained(self):
        tree=ast.parse(SOURCE.read_text());actual={}
        def walk(nodes,prefix=''):
            for node in nodes:
                if isinstance(node,(ast.ClassDef,ast.FunctionDef)):
                    name=prefix+node.name
                    actual[name]=len(node.args.args)+len(node.args.posonlyargs) if isinstance(node,ast.FunctionDef) else 0
                    walk(node.body,name+'.')
                else:
                    walk(list(ast.iter_child_nodes(node)),prefix)
        walk(tree.body)
        manifest=json.loads((BASE/'original-inventory.json').read_text())
        for item in manifest['objects']:
            if '<' not in item['name'] and item['name'] != 'generatePS.chck':
                self.assertTrue(item['name'] in actual,item['name'])
                self.assertEqual(actual[item['name']],item['args'],item['name'])
        self.assertEqual(sum(isinstance(n,ast.ClassDef) for n in ast.walk(tree)),62)

    def test_main_menu_keeps_all_sixteen_original_entries_and_real_contexts(self):
        module=self.plugin
        screen=module.SysUtilMngMain(types.SimpleNamespace())
        self.assertEqual(len(screen.menuListAll),16)
        self.assertEqual(screen['actions'].contexts,['SetupActions','ColorActions','GlobalActions','WizardActions','MenuActions'])
        screen.updatemenulist()
        self.assertEqual(len(screen['list'].list),16)

    def test_oscam_detects_openatv_binary_outside_legacy_directory(self):
        module=self.plugin
        with patch.object(module.os,'listdir',return_value=['3013']),patch('builtins.open',unittest.mock.mock_open(read_data='oscam-stable\n')):
            self.assertTrue(module.oscamRunning())
            self.assertFalse(module.oscamRunning(True))

    def test_oscam_version_file_discovers_real_config_and_auth_stays_local(self):
        module=self.plugin
        files={'/etc/remote_servers.cfg':'O: Local 127.0.0.1:8888\n','/tmp/.oscam/oscam.version':'ConfigDir: /etc/tuxbox/config/oscam-stable/\n','/etc/tuxbox/config/oscam-stable/oscam.conf':'[webif]\nhttpport = 8888\nhttpuser = local\nhttppwd = sample-secret\n'}
        import io
        def read(path,*a,**kw):
            if str(path) not in files:raise FileNotFoundError(path)
            return io.StringIO(files[str(path)])
        with patch('builtins.open',side_effect=read):
            item,url,user,password=module.readOscamCfg()
        self.assertEqual(url,'http://127.0.0.1:8888/')
        self.assertEqual((user,password),('local','sample-secret'))

    def test_url_fetch_is_utf8_bounded_and_does_not_replace_global_opener(self):
        module=self.plugin
        from unittest.mock import MagicMock
        response=MagicMock();response.__enter__.return_value=response
        response.read.return_value='žlté\nOK'.encode()
        opener=MagicMock();opener.open.return_value=response
        with patch.object(module.urllibXX2,'build_opener',return_value=opener),patch.object(module.urllibXX2,'install_opener') as install:
            self.assertEqual(module.getUrlData('http://127.0.0.1:8888/'),['žlté','OK'])
            install.assert_not_called()
            self.assertEqual(opener.open.call_args.kwargs['timeout'],4)

    def test_original_skin_definitions_are_preserved_except_unique_converter_name(self):
        for name,digest in json.loads((BASE/'skins-original.json').read_text()).items():
            raw=(ROOT/name).read_bytes().replace(b'GSUAgcConv',b'AgcConv')
            self.assertEqual(hashlib.sha256(raw).hexdigest(),digest,name)

    def test_no_obsolete_bytecode_or_library_abi_copy(self):
        for path in ROOT.rglob('*'):
            if '__pycache__' not in path.parts:
                self.assertNotIn(path.suffix,('.pyo','.pyc'))
                self.assertFalse(path.name.startswith(('plugin.py3','plugin.py2')))
        with patch.object(self.plugin,'system') as system:
            self.assertFalse(self.plugin.cpLibCr());system.assert_not_called()

    def test_corrected_constant_collections_are_real_values(self):
        source=SOURCE.read_text()
        self.assertTrue('ActionMap([63, 64' not in source)
        self.assertTrue('for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]' not in source)
        self.assertTrue('[_[1] for l in' not in source)


if __name__=='__main__':unittest.main()
