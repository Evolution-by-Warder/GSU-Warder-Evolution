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

    def test_system_panels_and_cpu_refresh_work_with_both_timer_apis(self):
        from unittest.mock import MagicMock
        module=self.plugin
        for modern in (False, True):
            with self.subTest(modern=modern):
                callbacks=[]
                signal=types.SimpleNamespace(get=lambda:callbacks)
                if modern:
                    signal.connect=lambda cb:callbacks.append(cb)
                timer=MagicMock();timer.timeout=signal
                with patch.object(module,'eTimer',return_value=timer) as factory:
                    screen=module.GlassSysInfoBrowser(types.SimpleNamespace())
                    for name in ('getMemInfo','getSpaceInfo','getServicesInfo'):
                        setattr(screen,name,MagicMock())
                    screen.getTempSensorsInfo=MagicMock(return_value='CPU Temp.: 65 C')
                    screen.getProccess=MagicMock(return_value='3013 oscam-stable\n')
                    screen.getDmesg=MagicMock(return_value='Linux receiver kernel\n')
                    screen.LetsgoParty()
                    self.assertEqual(screen['ProccessInfo'].text,'3013 oscam-stable\n')
                    self.assertEqual(screen['DmesgInfo'].text,'Linux receiver kernel\n')
                    timer.start.assert_called_with(200)
                    self.assertEqual(callbacks,[screen.getCPUInfo])
                    screen.getProccess.return_value='3017 oscam-stable\n'
                    screen.LetsgoParty()
                    self.assertEqual(screen['ProccessInfo'].text,'3017 oscam-stable\n')
                    self.assertEqual(factory.call_count,1)
                    self.assertEqual(callbacks,[screen.getCPUInfo])
                    screen.exit()
                    timer.stop.assert_called_once()

    def test_system_screen_can_close_before_initial_refresh(self):
        screen=self.plugin.GlassSysInfoBrowser(types.SimpleNamespace())
        screen.exit()
        self.assertIsNone(screen.cpuTimer)

    def test_channel_initial_data_and_ecm_work_with_both_timer_apis(self):
        from unittest.mock import MagicMock
        from contextlib import ExitStack
        from xml.etree.ElementTree import ElementTree, fromstring
        module=self.plugin
        ref='1:0:19:13A5:C85:3:EB0000:0:0:0:'
        fields=('sVideoPID','sAudioPID','sPCRPID','sPMTPID','sTXTPID',
                'sTSID','sONID','sSID','sVideoWidth','sVideoHeight','sAspect',
                'sServiceref','sIsCrypted','sCAIDs','sProvider','sTransferBPS')
        constants=types.SimpleNamespace(**{k:k for k in fields},resIsString=-2)
        values={'sVideoPID':0x668,'sAudioPID':0x669,'sVideoWidth':1920,
                'sVideoHeight':1080,'sAspect':3,'sProvider':-2,'sTransferBPS':2048}
        info=types.SimpleNamespace(getInfo=lambda key:values.get(key,1),
            getInfoString=lambda key:ref if key=='sServiceref' else 'CANAL+ CZ',
            getInfoObject=lambda key:[0x668])
        frontend={'tuner_type':'DVB-S2','orbital_position':235,
                  'frequency':12207000,'symbol_rate':27500000}
        service=types.SimpleNamespace(info=lambda:info,audioTracks=lambda:None,
            frontendInfo=lambda:types.SimpleNamespace(getAll=lambda original:frontend))
        session=types.SimpleNamespace(nav=types.SimpleNamespace(getCurrentService=lambda:service))
        for modern in (False,True):
            with self.subTest(modern=modern),ExitStack() as stack:
                timers=[];callbacks=[]
                def make_timer():
                    slots=[];signal=types.SimpleNamespace(get=lambda:slots)
                    if modern:signal.connect=lambda cb:slots.append(cb)
                    timer=MagicMock();timer.timeout=signal
                    timers.append(timer);callbacks.append(slots)
                    return timer
                stack.enter_context(patch.object(module,'eTimer',side_effect=make_timer))
                stack.enter_context(patch.object(module,'iServiceInformation',constants))
                stack.enter_context(patch.object(module,'eServiceReference',lambda value:types.SimpleNamespace(toString=lambda:value)))
                stack.enter_context(patch.object(module,'ENA_TT',False))
                stack.enter_context(patch.object(module,'ConvertToHumanReadable',lambda data:{'system':'DVB-S2','modulation':'8PSK','polarization':'Horizontal','fec_inner':'3/4'}))
                stack.enter_context(patch.object(module,'parse',return_value=ElementTree(fromstring('<satellites><sat name="Astra č. 3" position="235"/></satellites>'))))
                lookup=stack.enter_context(patch.object(module,'resPicon',side_effect=lambda name,kind:kind+'/'+name+'.png'))
                screen=module.channelInfoCenter(session)
                for name in ('picchannel','picprov','picsat','piccode','piccam'):
                    screen[name].instance.setPixmapFromFile=MagicMock()
                screen.showPicCode=MagicMock()
                screen.startInfo()
                self.assertEqual(len(timers),2)
                self.assertEqual(callbacks,[[screen.startBitrate],[screen.readEcmInfo]])
                timers[0].start.assert_called_with(1000)
                timers[1].start.assert_called_with(100)
                self.assertEqual(screen['tp_ref'].text,ref.rstrip(':'))
                self.assertEqual(screen['tp_sat'].text,'Astra č. 3')
                self.assertIn('DVB-S2\n8PSK\n12207 MHz',screen['tp_values'].text)
                self.assertIn('0668\n0669',screen['tp_values'].text)
                self.assertIn('1920 x 1080',screen['tp_values'].text)
                screen['picchannel'].instance.setPixmapFromFile.assert_called_once()
                screen['picprov'].instance.setPixmapFromFile.assert_called_once()
                screen['picsat'].instance.setPixmapFromFile.assert_called_once()
                self.assertEqual(screen['stream_btr'].text,'2 kB/s')
                ecm=('OSCam ', 'OSCam\n', '', '0668\n', '000000\n', '000000\n', '0C0A\n', 'server\n', 'local\n', '0\n', '0\n', '0.117\n', 'Irdeto', '', '')
                stack.enter_context(patch.object(module,'ECMparser',return_value=ecm))
                callbacks[1][0]()
                self.assertIn('0668',screen['ecmValues'].text)
                screen.showPicCode.assert_called_with('Irdeto-fs8','OSCam-fs8')
                timers[1].start.assert_called_with(3000)
                screen.exit()
                timers[0].stop.assert_called_once()
                self.assertEqual(timers[1].stop.call_count,2)

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
