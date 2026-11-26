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
