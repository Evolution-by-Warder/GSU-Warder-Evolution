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
                screen['ecmValues'].instance.setWrap=MagicMock()
                screen.startInfo()
                screen['ecmValues'].instance.setWrap.assert_called_once_with(0)
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

    def test_channel_caids_are_unique_and_ecm_keeps_eleven_rows(self):
        from unittest.mock import MagicMock
        module=self.plugin
        screen=module.channelInfoCenter(types.SimpleNamespace())
        info=types.SimpleNamespace(getInfoObject=lambda key:[0x624,0x181D,0x624,0x668,0x181D])
        with patch.object(module,'iServiceInformation',types.SimpleNamespace(sCAIDs=1)):
            self.assertEqual(screen.getCaidInfo(info),'0624  181D  0668')
        screen.runECMTimer1=MagicMock();screen.showPicCode=MagicMock()
        ecm=(' (2.26.09-11968-802)\n','OScam\n','','0668\n','000000\n','000000\n','0C0A\n','server\n','192.168.10.6\n','0\n','0\n','0.126\n','Irdeto','','')
        with patch.object(module,'ECMparser',return_value=ecm) as parser:
            screen.readEcmInfo()
            parser.assert_called_once_with(cl=24)
        rows=screen['ecmValues'].text.splitlines()
        self.assertEqual(len(rows),11)
        self.assertEqual(rows[0],'OScam (2.26.09-11968-802)')
        self.assertEqual(rows[1:4],['Irdeto','0668','000000'])
        self.assertEqual(rows[-1],'0.126')

    def test_standalone_ecm_full_revision_refresh_and_close_with_both_timer_apis(self):
        from unittest.mock import MagicMock
        from contextlib import ExitStack
        module=self.plugin
        info=types.SimpleNamespace(getInfo=lambda key:1)
        service=types.SimpleNamespace(info=lambda:info)
        session=types.SimpleNamespace(nav=types.SimpleNamespace(getCurrentService=lambda:service))
        for modern in (False,True):
            with self.subTest(modern=modern),ExitStack() as stack:
                callbacks=[]
                signal=types.SimpleNamespace(get=lambda:callbacks)
                if modern:signal.connect=lambda cb:callbacks.append(cb)
                timer=MagicMock();timer.timeout=signal
                stack.enter_context(patch.object(module,'eTimer',return_value=timer))
                stack.enter_context(patch.object(module,'iServiceInformation',types.SimpleNamespace(sIsCrypted=1)))
                stack.enter_context(patch.object(module,'findPicon',return_value='test-Irdeto.png'))
                ecm=(' (2.26.09-11968-802)\n','OScam\n','','0668\n','000000\n','000000\n','0C0A\n','server\n','local\n','0\n','0\n','0.126\n','Irdeto','test-cw0\n','test-cw1\n')
                next_ecm=ecm[:11]+('0.134\n',)+ecm[12:]
                parser=stack.enter_context(patch.object(module,'ECMparser',side_effect=[ecm,next_ecm]))
                screen=module.ECMInfo(session)
                screen['piccode'].instance.setPixmapFromFile=MagicMock()
                screen.startSearchInfo()
                parser.assert_called_once_with(cl=24)
                self.assertEqual(screen['ecmValues'].text.splitlines()[0],'OScam (2.26.09-11968-802)')
                self.assertEqual(len(screen['ecmValues'].text.splitlines()),13)
                self.assertEqual(screen['ecmValues'].text.splitlines()[-1],'0.126')
                self.assertEqual(callbacks,[screen.readEcmInfo])
                timer.start.assert_called_with(5000,True)
                callbacks[0]()
                self.assertEqual(screen['ecmValues'].text.splitlines()[-1],'0.134')
                self.assertEqual(parser.call_count,2)
                self.assertEqual(timer.start.call_count,2)
                screen['piccode'].instance.setPixmapFromFile.assert_called_with('test-Irdeto.png')
                screen.exit()
                self.assertEqual(timer.stop.call_count,3)
                self.assertIsNone(screen.runECMTimer)

    def test_retired_ftp_gate_never_connects_or_sends_credentials(self):
        module=self.plugin
        with patch.object(module.ftplib,'FTP') as ftp:
            message,server=module.chckFtp()
        ftp.assert_not_called()
        self.assertIsNone(server)
        self.assertIn('Downloads disabled',message)

    def test_cam_download_action_opens_native_catalogue_without_ftp(self):
        from unittest.mock import MagicMock
        module=self.plugin
        session=types.SimpleNamespace(open=MagicMock(),openWithCallback=MagicMock())
        screen=module.univCamMng(session);screen.enCommand=True
        with patch.object(module.ftplib,'FTP') as ftp:
            screen.moreCamSrv()
        ftp.assert_not_called()
        session.open.assert_not_called()
        session.openWithCallback.assert_called_once_with(screen.inicializeUCM,module.ftp_center,None)

    def test_cam_manager_lists_native_softcam_and_routes_buttons(self):
        from unittest.mock import MagicMock
        module=self.plugin
        adapter=MagicMock();adapter.selected.return_value='oscam-uni';adapter.running.return_value=True;adapter.available.return_value=['oscam-master','oscam-uni'];adapter.active_name.return_value='oscam-uni'
        with patch.object(module,'NativeSoftcam',return_value=adapter),patch.object(module,'listDir',return_value=[]):
            screen=module.univCamMng(types.SimpleNamespace())
            screen.CamSrvList()
        self.assertEqual(screen.numCam,2)
        self.assertEqual(screen.numSrv,0)
        self.assertEqual(screen.getCamName(),'oscam-uni')
        self.assertEqual(screen.Cam_list['oscam-uni'],'@native-softcam')
        self.assertEqual(screen.Cam_list['oscam-master'],'@native-softcam')
        self.assertEqual(screen['config'].list[0][1].value,'oscam-uni')
        self.assertEqual(screen['activCam'].text,'Active CAM: oscam-uni')
        screen.CamSrvMsg=MagicMock()
        self.assertTrue(screen.checkStatCam())
        screen.CamSrvMsg.assert_called_with('CAM Running')
        with patch.object(module,'_native_softcam_action',return_value=True) as action:
            screen.start();screen.stop()
            self.assertEqual([call.args[1] for call in action.call_args_list],['start','stop'])
        adapter.running.return_value=False;adapter.active_name.return_value=None
        with patch('builtins.open',side_effect=FileNotFoundError):
            self.assertEqual(screen.getCamName(),'None')
        self.assertTrue(screen.checkStatCam())
        screen.CamSrvMsg.assert_called_with('No Running CAM')

    def test_cam_manager_caids_are_unique_in_broadcast_order(self):
        module=self.plugin
        info=types.SimpleNamespace(getInfoObject=lambda key:[0x624,0x181D,0x668,0x624,0x181D,0x668])
        with patch.object(module,'iServiceInformation',types.SimpleNamespace(sCAIDs=1)):
            text=module.univCamMng.getCaidInfo(None,info)
        self.assertEqual(text,'Available CAIDs: 0624  181D  0668  ')
        empty=types.SimpleNamespace(getInfoObject=lambda key:None)
        with patch.object(module,'iServiceInformation',types.SimpleNamespace(sCAIDs=1)):
            self.assertEqual(module.univCamMng.getCaidInfo(None,empty),'No CA info available')

    def test_channel_bitrate_output_handles_partial_and_combined_reads(self):
        module=self.plugin
        screen=module.channelInfoCenter(types.SimpleNamespace())
        with patch('builtins.open',unittest.mock.mock_open()):
            screen.dataAvail(b'100 200 150 1')
            self.assertEqual(screen['bit_act'].text,'')
            screen.dataAvail(b'80\n 180  192 186 191\n')
            self.assertEqual(screen['bit_act'].text,'Act:\n180\n191')
            self.assertEqual(screen['bit_min'].text,'Min:\n100\n180')
            screen.dataAvail('warning: read retry\n200 300 250 280\n190 200 195 199\n210 310 260 290\n191 201 196 200\n')
            self.assertEqual(screen['bit_act'].text,'Act:\n290\n200')
            self.assertEqual(screen['bit_avg'].text,'Avg:\n260\n196')

    def test_channel_cam_width_leaves_room_for_full_revision_without_overlap(self):
        import xml.etree.ElementTree as ET
        screen=self.plugin.channelInfoCenter(types.SimpleNamespace())
        tree=ET.fromstring(screen.skin)
        values=tree.find("widget[@name='ecmValues']")
        self.assertEqual(values.get('size'),'340,345')
        x=int(values.get('position').split(',')[0])
        channel=tree.find("widget[@name='picchannel']")
        self.assertLess(x+340,int(channel.get('position').split(',')[0]))

    def test_cccam_menu_consumes_text_and_retains_all_original_choices(self):
        import io
        module=self.plugin
        data='CCcam WebInfo\nConnected clients: 1\nAvailable shares: 1\nAvailable providers: 1\ncard inserted\n| CAID | Provider |\n| 0668 | Local |\n'
        with patch.object(module,'_cccam_open',side_effect=lambda url:io.StringIO(data)):
            screen=module.cccamInfo(types.SimpleNamespace(),url='http://example.invalid:16001')
            screen.updatemenulist()
        self.assertEqual(len(screen['list'].list),8)
        self.assertTrue(all(screen.status.values()))

    def test_cccam_unreachable_configured_server_remains_visible(self):
        module=self.plugin
        with patch.object(module,'fileExists',return_value=True),patch('builtins.open',unittest.mock.mock_open(read_data='C: Office example.invalid:16001\n')),patch.object(module,'_cccam_open',side_effect=OSError('unavailable')):
            screen=module.cccamInfoChoiceServer(types.SimpleNamespace())
            screen.readCccamServers()
        self.assertEqual(len(screen['list'].list),1)
        self.assertFalse(screen.status[screen['list'].getCurrent()[0]])

    def test_oscam_reader_screen_uses_real_protocol_and_four_emm_counters(self):
        from test_oscam_readers import fixture
        from unittest.mock import MagicMock
        module=self.plugin;session=types.SimpleNamespace(open=MagicMock())
        screen=module.oscam_readers(session,'http://127.0.0.1:8888/','','')
        with patch.object(module,'getUrlData',return_value=fixture()):screen.oscamreaders()
        row=screen['list'].getCurrent()
        self.assertIn('cs378x',row[1]['text'])
        self.assertIn('online 192.168.10.6',row[1]['text'])
        self.assertEqual(screen['status_values_0'].text,'0 / 1 / 2 / 3\n4 / 5 / 6 / 7')
        self.assertEqual(screen['status_values_1'].text,'8 / 9 / 10 / 11\n12 / 13 / 14 / 15')
        self.assertEqual(row[0].split('*')[2],'cs378x')
        with patch.object(module.MessageBox,'TYPE_INFO',0,create=True):screen.entitlements()
        self.assertIs(session.open.call_args.args[0],module.MessageBox)

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

    def _cam_process_files(self, processes):
        import io
        files={}
        for pid,name,state in processes:
            files['/proc/%s/comm'%pid]=name+'\n'
            if state is not None:
                files['/proc/%s/status'%pid]='Name:\t%s\nState:\t%s\n'%(name,state)
        def read(path,*args,**kwargs):
            if str(path) not in files:raise FileNotFoundError(path)
            return io.StringIO(files[str(path)])
        return read

    def test_ecm_registers_in_extensions_menu_without_replacing_info_or_color_keys(self):
        class Descriptor:
            WHERE_PLUGINMENU=1;WHERE_SESSIONSTART=2;WHERE_EXTENSIONSMENU=3
            WHERE_MENU=4;WHERE_EVENTINFO=5
            def __init__(self,**kwargs):self.__dict__.update(kwargs)
        previous=self.plugin.config.plugins.GlassSysUtil.par40.value
        try:
            for enabled in (False,True):
                self.plugin.config.plugins.GlassSysUtil.par40.value=enabled
                with patch.object(self.plugin,'PluginDescriptor',Descriptor):
                    entries=self.plugin.Plugins('/test')
                found=[p for p in entries if getattr(p,'name',None)=='(GSU) ECM Info']
                self.assertFalse(any(p.where==Descriptor.WHERE_EVENTINFO for p in entries))
                self.assertEqual(len(found),1)
                self.assertEqual(found[0].where,Descriptor.WHERE_EXTENSIONSMENU)
                self.assertIs(found[0].fnc,self.plugin._open_ecm_info)
        finally:self.plugin.config.plugins.GlassSysUtil.par40.value=previous

    def test_retired_shortcut_option_is_skipped_and_never_requests_gui_restart(self):
        from unittest.mock import MagicMock
        screen=self.plugin.univCamMng(types.SimpleNamespace(openWithCallback=MagicMock()))
        self.assertNotIn(5,screen.aa)
        point=types.SimpleNamespace(x=lambda:500,y=lambda:100)
        for i in range(10):screen['txt%d'%i].instance=types.SimpleNamespace(position=lambda:point)
        screen['select_pict'].move=MagicMock()
        screen.idxAllFnc=0;visited=[]
        screen.numSrv=1  # This test retains all non-retired server actions.
        for _ in range(9):
            screen.selectFnc();visited.append(screen.idxAllFnc)
        self.assertEqual(visited,[1,2,3,4,6,7,8,9,0])
        screen.enCommand=True;screen.close=MagicMock()
        screen.exit()
        screen.close.assert_called_once_with()
        screen.session.openWithCallback.assert_not_called()

    def test_session_start_leaves_image_infobar_untouched_with_old_shortcut_flag(self):
        from unittest.mock import MagicMock
        import Screens.InfoBarGenerics as infobar
        old_init=infobar.InfoBarPlugins.__init__
        original=self.plugin.config.plugins.GlassSysUtil.par40.value
        self.plugin.config.plugins.GlassSysUtil.par40.value=True
        try:
            with patch.object(self.plugin,'autocams',types.SimpleNamespace(autoStartCheck=MagicMock())),patch.object(self.plugin,'OnScreenEcm',types.SimpleNamespace(startShowOSD=MagicMock())),patch.object(self.plugin,'autoInstallMng',types.SimpleNamespace(autoInstallStart=MagicMock())):
                self.plugin.sessionAutostart(0,session=object())
            self.assertIs(infobar.InfoBarPlugins.__init__,old_init)
        finally:self.plugin.config.plugins.GlassSysUtil.par40.value=original

    def test_native_info_menu_callback_opens_original_ecm_screen(self):
        from unittest.mock import MagicMock
        session=types.SimpleNamespace(open=MagicMock())
        self.plugin._open_ecm_info(session=session,servicelist=object(),event=object())
        session.open.assert_called_once_with(self.plugin.ECMInfo)

    def test_oscam_detects_openatv_binary_outside_legacy_directory(self):
        with patch.object(self.plugin.os,'listdir',return_value=['3013']),patch('builtins.open',self._cam_process_files([('3013','oscam-stable','S (sleeping)')])):
            self.assertTrue(self.plugin.oscamRunning())
            self.assertFalse(self.plugin.oscamRunning(True))

    def test_dead_oscam_and_osemu_do_not_block_updates(self):
        for name in ('oscam-master','osemu'):
            for state in ('Z (zombie)','X (dead)','x (dead)'):
                with self.subTest(name=name,state=state),patch.object(self.plugin.os,'listdir',return_value=['22044']),patch('builtins.open',self._cam_process_files([('22044',name,state)])):
                    self.assertFalse(self.plugin.oscamRunning(name=='osemu'))

    def test_live_cam_still_blocks_update_alongside_zombie(self):
        processes=[('22044','oscam-master','Z (zombie)'),('22042','oscam-master','S (sleeping)')]
        with patch.object(self.plugin.os,'listdir',return_value=['22044','22042']),patch('builtins.open',self._cam_process_files(processes)):
            self.assertTrue(self.plugin.oscamRunning())
        with patch.object(self.plugin.os,'listdir',return_value=['77']),patch('builtins.open',self._cam_process_files([('77','osemu','R (running)')])):
            self.assertTrue(self.plugin.oscamRunning(True))

    def test_cam_exiting_during_detection_is_tolerated(self):
        with patch.object(self.plugin.os,'listdir',return_value=['22044']),patch('builtins.open',self._cam_process_files([('22044','oscam-master',None)])):
            self.assertFalse(self.plugin.oscamRunning())

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
