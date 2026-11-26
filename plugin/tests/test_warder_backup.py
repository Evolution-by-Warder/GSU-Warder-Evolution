from pathlib import Path
from types import SimpleNamespace
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch
import hashlib
import json
import unittest
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
load(ROOT)
from Plugins.Extensions.GlassSysUtil import warder_backup as b

class Item:
    def __init__(self,value,choices=None,limits=None):
        self.value=value
        self.saved_value=value
        if choices is not None:self.choices=choices
        if limits is not None:self.limits=limits
    def save(self):self.saved_value=self.value

class BackupTests(unittest.TestCase):
    def test_local_backup_roundtrip_and_rejects_tampering_and_secrets(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            p.path('/media/hdd').mkdir(parents=True)
            p.path('/media/net').mkdir(parents=True)
            table=[('/dev/root','/','ext4',False),('/dev/sda1','/media/hdd','ext4',False),('server:/share','/media/net','nfs',False)]
            config=SimpleNamespace(plugins=SimpleNamespace(warderyoutube=SimpleNamespace(
                api_key=Item('secret'),max_quality=Item('720',['720','1080']))))
            with patch.object(b,'mounts',return_value=table):
                self.assertEqual(b.destinations(p),[p.path(b.ROOT),p.path('/media/hdd/warder-backups')])
                data=b.snapshot(config,probe=p)
                self.assertEqual(data,{'YouTube':{'warderyoutube.max_quality':'720'}})
                path=b.save(b.destinations(p)[1],data,p)
                self.assertNotIn('secret',path.read_text())
                self.assertEqual(b.load(path,p)['projects'],data)
                self.assertEqual(b.inventory(path.parent,p),[path])
                doc=json.loads(path.read_bytes())
                doc['payload']['projects']['YouTube']['warderyoutube.api_key']='secret'
                doc['sha256']=hashlib.sha256(b.canonical(doc['payload'])).hexdigest()
                path.write_bytes(b.canonical(doc))
                with self.assertRaises(ValueError):b.load(path,p)
                with self.assertRaises(ValueError):b.save(p.path('/media/net/warder-backups'),data,p)

    def test_native_choices_and_restore_verified(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            item=Item('720',['720','1080'])
            config=SimpleNamespace(plugins=SimpleNamespace(warderyoutube=SimpleNamespace(max_quality=item)))
            config.pickle=lambda:'config.plugins.warderyoutube.max_quality='+item.saved_value+'\n'
            settings=p.path('/etc/enigma2/settings')
            configfile=SimpleNamespace(CONFIG_FILE=str(settings),save=lambda:settings.write_text(config.pickle()))
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                path=b.save(p.path(b.ROOT),{'YouTube':{'warderyoutube.max_quality':'1080'}},p)
                count,skipped,rollback=b.restore(config,configfile,path,probe=p)
                self.assertEqual(count,1)
                self.assertEqual(item.value,'1080')
                self.assertEqual(b.load(rollback,p)['projects']['YouTube']['warderyoutube.max_quality'],'720')
                wrong=b.save(p.path(b.ROOT),{'YouTube':{'warderyoutube.max_quality':'999'}},p)
                self.assertEqual(b.restore(config,configfile,wrong,probe=p)[:2],(0,{'YouTube':1}))
                self.assertEqual(item.value,'1080')

    def test_radio_only_allowlisted_settings_no_stream_urls(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            path=p.path(b.RADIO);path.parent.mkdir(parents=True)
            path.write_text(json.dumps({'schema':1,'show_main_menu':True,'screensaver_delay':20,
                'favourites':[{'url':'https://example.test/private?token=secret'}]}))
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                self.assertEqual(b.snapshot(SimpleNamespace(plugins=SimpleNamespace()),('Warder Radio',),p),
                    {'Warder Radio':{'show_main_menu':True,'screensaver_delay':20}})


    def test_backup_ui_uses_existing_warder_panels_and_never_writes_on_selection(self):
        from Plugins.Extensions.GlassSysUtil import warder_backup_ui as ui
        api=vars(load(ROOT))
        session=MagicMock()
        with patch.object(b,'destinations',return_value=[Path('/media/hdd/warder-backups')]),patch.object(b,'snapshot',return_value={'YouTube':{'warderyoutube.max_quality':'720'}}),patch.object(b,'save') as save,patch.object(b,'restore') as restore:
            menu=ui.BackupMenu(session,api)
            menu.refresh()
            self.assertEqual(len(menu['list'].l.list),5)
            self.assertIn('YouTube',menu['descriptions'].getText())
            menu.select()
            self.assertEqual(len(menu.selected),4)
            save.assert_not_called()
            restore.assert_not_called()
            session.openWithCallback.assert_not_called()


    def test_private_data_cannot_be_written_as_plaintext(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            data={'YouTube':{'warderyoutube.api_key':'test_key_123456'}}
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                with self.assertRaises(ValueError):b.save(p.path(b.ROOT),data,p)
                self.assertEqual(b.inventory(p.path(b.ROOT),p),[])

    @unittest.skipUnless(b.crypto.available(),'optional AES-GCM provider unavailable')
    def test_encrypted_roundtrip_wrong_password_tamper_and_rollback(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            state=p.path(b.RADIO)
            state.parent.mkdir()
            old=[{'name':'Old','url':'https://example.test/old?token=old_private'}]
            new=[{'name':'New','url':'https://example.test/new?token=new_private'}]
            state.write_text(json.dumps({'schema':1,'favourites':old,'custom':[],'history':['preserve']}))
            item=Item('old_key_123456')
            config=SimpleNamespace(plugins=SimpleNamespace(warderyoutube=SimpleNamespace(api_key=item)))
            config.pickle=lambda:'config.plugins.warderyoutube.api_key='+item.saved_value+'\n'
            settings=p.path('/etc/enigma2/settings')
            configfile=SimpleNamespace(CONFIG_FILE=str(settings),save=lambda:settings.write_text(config.pickle()))
            password='fixture-password-1234'
            data={'YouTube':{'warderyoutube.api_key':'new_key_123456'},'Warder Radio':{'favourites':new}}
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                path=b.save(p.path(b.ROOT),data,p,password)
                self.assertNotIn('new_private',path.read_text())
                self.assertNotIn('new_key_123456',path.read_text())
                self.assertEqual(b.load(path,p,password)['projects'],data)
                with self.assertRaises(ValueError):b.load(path,p)
                with self.assertRaises(ValueError):b.load(path,p,'incorrect-password')
                count,skipped,rollback=b.restore(config,configfile,path,probe=p,password=password)
                self.assertEqual(count,2)
                self.assertEqual(item.value,'new_key_123456')
                restored=json.loads(state.read_text())
                self.assertEqual(restored['favourites'],new)
                self.assertEqual(restored['history'],['preserve'])
                self.assertNotIn('old_private',rollback.read_text())
                self.assertEqual(b.load(rollback,p,password)['projects']['Warder Radio']['favourites'],old)
                envelope=json.loads(path.read_text())
                envelope['ciphertext']=('A' if envelope['ciphertext'][0]!='A' else 'B')+envelope['ciphertext'][1:]
                path.write_bytes(b.canonical(envelope))
                with self.assertRaises(ValueError):b.load(path,p,password)

    def test_private_radio_list_validation_is_all_or_nothing(self):
        self.assertTrue(b.station_list([{'name':'Station','url':'https://example.test/radio?token=local'}]))
        self.assertFalse(b.station_list([{'name':'Station','url':'https://user:pass@example.test/radio'}]))
        self.assertFalse(b.station_list([{'name':'Station','url':'file:///etc/passwd'}]))
        self.assertFalse(b.station_list([{'name':'Station','url':'https://example.test/radio','extra':'secret'}]))


    def test_password_keyboard_masks_and_clears_secret(self):
        from Plugins.Extensions.GlassSysUtil.warder_backup_password import BackupPassword
        api=vars(load(ROOT))
        view=BackupPassword(MagicMock(),api,'Password')
        view.render()
        secret='Password1234'
        for char in secret:view.append(char)
        self.assertNotIn(secret,''.join(view['password%d'%i].getText() for i in range(3)))
        self.assertEqual(view.secret,secret)
        view.accept()
        self.assertEqual(view.result,(secret,))
        self.assertEqual(view.secret,'')

    def test_private_creation_requires_two_matching_entries(self):
        from Plugins.Extensions.GlassSysUtil.warder_backup_ui import BackupMenu
        api=vars(load(ROOT))
        menu=BackupMenu(MagicMock(),api)
        with patch.object(menu,'ask_password') as ask,patch.object(menu,'create') as create:
            menu.mode_selected(('Private',True))
            first=ask.call_args.args[1]
            first('fixture-password-123')
            second=ask.call_args.args[1]
            second('different-password')
            create.assert_not_called()
            first('fixture-password-123')
            ask.call_args.args[1]('fixture-password-123')
            create.assert_called_once_with('fixture-password-123')

    def test_restore_rejects_changed_preview(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            config=SimpleNamespace(plugins=SimpleNamespace())
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                path=b.save(p.path(b.ROOT),{'YouTube':{'warderyoutube.max_quality':'720'}},p)
                self.assertEqual(b.file_kind(path,p),'standard')
                with self.assertRaisesRegex(ValueError,'changed after preview'):
                    b.restore(config,None,path,probe=p,expected_digest='0'*64)


    def test_picon_profiles_use_target_catalog_and_exclude_delete_mode(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            catalog=p.path(b.PICON_MENU)
            catalog.parent.mkdir(parents=True)
            catalog.write_text(json.dumps({'selectors':[{'selector':'192E'},{'selector':'DTT_ITALIA'},{'selector':'CANALPLUS_SK'}]}))
            profile=SimpleNamespace(warder_selectors=Item('192E DTT_ITALIA DAB CANALPLUS_SK'),
                sats=Item('19.2e'),resolution=Item('220x132',['220x132']),
                background=Item('white',['transparent','white','black']),
                method=Item('all',['all','all_inc','sync_tv']),warder_process=Item(True))
            config=SimpleNamespace(plugins=SimpleNamespace(chocholousekpicons=[profile]))
            data=b.snapshot(config,('PiconHub',),p)['PiconHub']
            prefix='chocholousekpicons.0.'
            self.assertEqual(data[prefix+'warder_selectors'],'192E DTT_ITALIA DAB CANALPLUS_SK')
            self.assertEqual(data[prefix+'sats'],'19.2e')
            self.assertEqual(data[prefix+'background'],'white')
            self.assertNotIn(prefix+'method',data)
            self.assertNotIn(prefix+'warder_process',data)
            payload={'schema':1,'created':'2026-11-26','projects':{'PiconHub':{prefix+'warder_selectors':'192E UNKNOWN'}}}
            changes,radio,skipped,_=b.plan(config,payload,probe=p)
            self.assertEqual(changes,[])
            self.assertEqual(skipped,{'PiconHub':1})
            self.assertFalse(b.selectors_valid('192E IPTV-TEST'))
            payload['projects']['PiconHub']={prefix+'method':'all'}
            with self.assertRaises(ValueError):b.validate_payload(payload)

    def test_skin_visual_settings_and_gsu_osd_preferences(self):
        skin=SimpleNamespace(par45=Item('#006cbcf0'),par145=Item('0',['0','1']),
            par214=Item('AutoColors',['AutoColors','#ffffff']),descriptionScrollSpeed=Item('36',['10','36']),
            par80=Item('private-host'),par125=Item('/media/hdd',['/media/hdd']))
        gsu=SimpleNamespace(par4=Item(500,limits=[(1,2000)]),par60=Item(True),diagnosticAlerts=Item(False),
                            par10=Item('private-password'))
        config=SimpleNamespace(plugins=SimpleNamespace(setupGlass17=skin,GlassSysUtil=gsu))
        result=b.snapshot(config,('FullHDGlass','GSU'))
        self.assertEqual(set(result['FullHDGlass']),{'setupGlass17.par45','setupGlass17.par145',
                        'setupGlass17.par214','setupGlass17.descriptionScrollSpeed'})
        self.assertEqual(set(result['GSU']),{'GlassSysUtil.par4','GlassSysUtil.par60','GlassSysUtil.diagnosticAlerts'})
        self.assertNotIn('private',str(result))


    def test_restore_outcome_reports_disjoint_counts_and_no_secrets(self):
        payload={'projects':{'YouTube':{'a':'secret1','b':'secret2','c':'secret3'},
                             'Warder Radio':{'a':'secret4'},'GSU':{'a':True}}}
        summary=b.outcome(payload,('YouTube','Warder Radio'),
                          [('YouTube','a',None,'secret1')],{'a':'secret4'},{'YouTube':1})
        self.assertEqual(summary,{'YouTube':(1,1,1,0),'Warder Radio':(1,0,0,0),'GSU':(0,0,0,1)})
        from Plugins.Extensions.GlassSysUtil.warder_backup_ui import summary_lines,archive_title
        text='\n'.join(summary_lines(str,summary,completed=True))
        self.assertIn('Restored: 2',text)
        self.assertIn('Unchanged: 1',text)
        self.assertIn('Incompatible: 1',text)
        self.assertIn('Not selected: 1',text)
        self.assertNotIn('secret',text)
        self.assertEqual(archive_title(Path('warder-backup-20261126-151200-abcdefgh.json')),
                         '26.11.2026  15:12:00  ·  abcdefgh')

    def test_restore_details_report_actual_noop_and_incompatible(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            config=SimpleNamespace(plugins=SimpleNamespace(warderyoutube=SimpleNamespace(
                max_quality=Item('720',['720','1080']),player_mode=Item('auto',['auto','gst']))))
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                path=b.save(p.path(b.ROOT),{'YouTube':{'warderyoutube.max_quality':'720',
                    'warderyoutube.player_mode':'unsupported'},'GSU':{'GlassSysUtil.par0':True}},p)
                count,skipped,rollback,summary=b.restore(config,None,path,('YouTube',),p,details=True)
                self.assertEqual(count,0)
                self.assertIsNone(rollback)
                self.assertEqual(summary,{'YouTube':(0,1,1,0),'GSU':(0,0,0,1)})


    def test_fresh_radio_install_restores_without_existing_state(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            plugin=p.path(b.RADIO_PLUGIN)
            plugin.parent.mkdir(parents=True)
            plugin.write_text('# installed fixture')
            config=SimpleNamespace(plugins=SimpleNamespace())
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                path=b.save(p.path(b.ROOT),{'Warder Radio':{'screensaver_delay':20,'show_main_menu':True}},p)
                count,skipped,rollback=b.restore(config,None,path,probe=p)
                self.assertEqual(count,2)
                self.assertEqual(json.loads(p.path(b.RADIO).read_text()),
                                 {'schema':1,'screensaver_delay':20,'show_main_menu':True})
                self.assertEqual(b.load(rollback,p)['projects']['Warder Radio'],
                                 {'screensaver_delay':0,'show_main_menu':False})

    def test_local_recovery_copy_precedes_native_write_and_survives_usb_loss(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            p.path('/media/usb').mkdir(parents=True)
            table=[('/dev/root','/','ext4',False),('/dev/sda1','/media/usb','vfat',False)]
            item=Item('720',['720','1080'])
            config=SimpleNamespace(plugins=SimpleNamespace(warderyoutube=SimpleNamespace(max_quality=item)))
            config.pickle=lambda:'config.plugins.warderyoutube.max_quality='+item.saved_value+'\n'
            settings=p.path('/etc/enigma2/settings')
            def fail_first_save():
                self.assertTrue(b.inventory(p.path(b.ROOT),p))
                if item.value=='1080':
                    table.pop()
                    raise OSError('simulated write failure')
                settings.write_text(config.pickle())
            configfile=SimpleNamespace(CONFIG_FILE=str(settings),save=fail_first_save)
            with patch.object(b,'mounts',side_effect=lambda probe:list(table)):
                path=b.save(p.path('/media/usb/warder-backups'),{'YouTube':{'warderyoutube.max_quality':'1080'}},p)
                with self.assertRaises(b.RestoreFailure) as error:b.restore(config,configfile,path,probe=p)
                self.assertTrue(error.exception.recovered)
                self.assertEqual(error.exception.rollback.parent,p.path(b.ROOT))
                self.assertEqual(item.value,'720')
                self.assertEqual(b.load(error.exception.rollback,p)['projects']['YouTube']['warderyoutube.max_quality'],'720')

    def test_unmounted_destination_aborts_without_publishing_backup(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            p.path('/media/usb').mkdir(parents=True)
            table=[('/dev/root','/','ext4',False),('/dev/sda1','/media/usb','vfat',False)]
            real_fsync=b.os.fsync
            def disconnect(fd):
                real_fsync(fd)
                if len(table)>1:table.pop()
            with patch.object(b,'mounts',side_effect=lambda probe:list(table)),patch.object(b.os,'fsync',side_effect=disconnect):
                with self.assertRaises((OSError,ValueError)):
                    b.save(p.path('/media/usb/warder-backups'),{'GSU':{'GlassSysUtil.par0':True}},p)
                self.assertEqual(list(p.path('/media/usb/warder-backups').iterdir()),[])

    def test_generated_backup_filename_matches_inventory_pattern(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                path=b.save(p.path(b.ROOT),{'GSU':{'GlassSysUtil.par0':True}},p)
                self.assertRegex(path.name,b.NAME)
                self.assertNotIn('--',path.name)
                self.assertEqual(b.inventory(path.parent,p),[path])


    def test_staged_restore_aborts_if_target_changed_before_write(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            item=Item('720',['360','720','1080'])
            config=SimpleNamespace(plugins=SimpleNamespace(warderyoutube=SimpleNamespace(max_quality=item)))
            configfile=MagicMock()
            payload={'schema':1,'created':'2026-11-26','projects':{'YouTube':{'warderyoutube.max_quality':'1080'}}}
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                prepared=b.prepare_restore(config,payload,probe=p)
                self.assertEqual(item.value,'720')
                self.assertEqual(b.inventory(p.path(b.ROOT),p),[])
                with self.assertRaisesRegex(ValueError,'Recovery backup unavailable'):
                    b.apply_prepared(config,configfile,prepared,None,p)
                rollback=b.save_recovery(prepared['previous'],p)
                item.value='360'
                with self.assertRaisesRegex(ValueError,'Settings changed before restore'):
                    b.apply_prepared(config,configfile,prepared,rollback,p)
                self.assertEqual(item.value,'360')
                configfile.save.assert_not_called()
                self.assertEqual(b.load(rollback,p)['projects']['YouTube']['warderyoutube.max_quality'],'720')

    def test_staged_restore_preserves_native_saved_value_race(self):
        with TemporaryDirectory() as folder:
            p=b.Probe(folder)
            p.path('/etc/enigma2').mkdir(parents=True)
            item=Item('720',['720','1080'])
            config=SimpleNamespace(plugins=SimpleNamespace(warderyoutube=SimpleNamespace(max_quality=item)))
            payload={'schema':1,'created':'2026-11-26','projects':{'YouTube':{'warderyoutube.max_quality':'1080'}}}
            with patch.object(b,'mounts',return_value=[('/dev/root','/','ext4',False)]):
                prepared=b.prepare_restore(config,payload,probe=p)
                rollback=b.save_recovery(prepared['previous'],p)
                item.saved_value=None
                with self.assertRaisesRegex(ValueError,'Settings changed before restore'):
                    b.apply_prepared(config,MagicMock(),prepared,rollback,p)
                self.assertEqual(item.value,'720')


    def test_password_keyboard_has_exactly_one_cell_cursor(self):
        from Plugins.Extensions.GlassSysUtil.warder_backup_password import BackupPassword,KEYS,SHIFT_KEYS,password_skin,ROW_HEIGHT
        from Plugins.Extensions.GlassSysUtil import warder_main as view_style
        from xml.etree import ElementTree as ET
        api=vars(load(ROOT))
        view=BackupPassword(MagicMock(),api,'Password')
        view.prepare_keyboard()
        def check(row,column,keys):
            rows=view['list'].l.list
            active=[(i,j) for i,line in enumerate(rows) for j,cell in enumerate(line[1:])
                    if cell['backcolor']==int(view_style.SELECTION[1:],16)]
            self.assertEqual(active,[(row,column)])
            self.assertEqual([tuple(' ' if cell['text']=='␣' else cell['text'] for cell in line[1:]) for line in rows],list(keys))
            self.assertEqual(view['list'].getCurrentIndex(),0)
        self.assertEqual(''.join(KEYS[1]),'qwertyuiop')
        self.assertTrue(all(len(row)==10 for row in KEYS+SHIFT_KEYS))
        self.assertEqual({c for row in KEYS+SHIFT_KEYS for c in row if c!='Aa'},{chr(i) for i in range(32,127)})
        check(1,0,KEYS)
        view.horizontal(1)
        check(1,1,KEYS)
        view.add()
        self.assertEqual(view.secret,'w')
        view.toggle_shift()
        check(1,1,SHIFT_KEYS)
        view.add()
        self.assertEqual(view.secret,'wW')
        view.vertical(-2)
        check(5,1,SHIFT_KEYS)
        view.horizontal(-2)
        check(5,9,SHIFT_KEYS)
        view.add()
        self.assertEqual(view.secret,'wW ')
        view.horizontal(-1)
        view.add()
        check(5,8,KEYS)
        self.assertEqual(view.secret,'wW ')
        for w,h in ((1280,720),(1920,1080),(2560,1440),(3840,2160)):
            root=ET.fromstring(password_skin(w,h))
            keyboard=root.find("widget[@name='list']")
            self.assertEqual(keyboard.get('backgroundColor'),keyboard.get('backgroundColorSelected'))
            self.assertEqual(keyboard.get('scrollbarMode'),'showNever')
            x,y=map(int,keyboard.get('position').split(','))
            kw,kh=map(int,keyboard.get('size').split(','))
            self.assertLessEqual(x+kw,w)
            self.assertLessEqual(y+kh,h)
            self.assertGreaterEqual(kh,6*round(ROW_HEIGHT*h/1080))

    def test_password_visibility_is_explicit_and_resets_on_hide_and_close(self):
        from Plugins.Extensions.GlassSysUtil.warder_backup_password import BackupPassword
        api=vars(load(ROOT))
        view=BackupPassword(MagicMock(),api,'Password')
        def displayed():
            return ''.join(view['password%d'%i].getText() for i in range(3))
        secret='TestPassword123!'+('W'*112)
        for char in secret:view.append(char)
        self.assertEqual(displayed(),'•'*len(secret))
        view.toggle_visibility()
        self.assertEqual(displayed(),secret)
        self.assertEqual(view['blue'].getText(),view.tr('Hide password'))
        view.hide_password()
        self.assertEqual(displayed(),'•'*len(secret))
        view.toggle_visibility()
        view.cancel()
        self.assertEqual(view.secret,'')
        self.assertFalse(view.revealed)
        self.assertNotIn(secret,displayed())
        self.assertEqual(view.result,(None,))
