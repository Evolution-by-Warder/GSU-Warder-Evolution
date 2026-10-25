import hashlib
import importlib
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock,patch
from receiver_stubs import load

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src/GlassSysUtil'))
import plugin_update as update
sys.path.insert(0,str(ROOT/'tools'))
from build_ipk import archive
import publish_update


def ipk(version='13.40-r37',package=update.PACKAGE_ID):
    control=archive([('control',('Package: %s\nVersion: %s\nArchitecture: all\n' % (package,version)).encode(),0o644)])
    result=b'!<arch>\n'
    for name,data in [('debian-binary',b'2.0\n'),('control.tar.gz',control)]:
        result+=('%-16s%-12s%-6s%-6s%-8s%-10s`\n' % (name+'/',0,0,0,'100644',len(data))).encode()+data
        if len(data)%2:result+=b'\n'
    return result


class PluginUpdateTests(unittest.TestCase):
    def setUp(self):
        self.data=ipk()
        self.item={'version':'13.40-r37','tag':'v13.40-r37','url':'https://github.com/'+update.REPOSITORY+'/releases/download/v13.40-r37/'+update.PACKAGE_ID+'_13.40-r37_all.ipk','bytes':len(self.data),'sha256':hashlib.sha256(self.data).hexdigest(),'notes':'Changes'}
        self.document={'schema':1,'product':'Glass System Utility Warder Evolution','channel':'original-python314','release':self.item}

    def release(self):return update.parse_release(json.dumps(self.document),'13.40-r36')

    def test_only_new_restoration_release_is_offered(self):
        self.assertEqual(self.release().version,'13.40-r37')
        self.assertIsNone(update.parse_release(json.dumps(self.document),'13.40-r37'))
        self.assertIsNone(update.parse_release(json.dumps(self.document),'13.40-r100'))
        self.document['release']=None
        self.assertIsNone(self.release())

    def test_other_products_channels_versions_urls_and_invalid_metadata_rejected(self):
        for field,value in [('product','PiconHub Warder Evolution'),('channel','stable')]:
            document=dict(self.document);document[field]=value
            with self.subTest(field=field),self.assertRaises(update.UpdateError):update.parse_release(json.dumps(document),'13.40-r36')
        for field,value in [('version','13.38-w19'),('url','http://example.invalid/update.ipk'),('tag','v13.40-r38'),('sha256','abc'),('bytes',True),('bytes',update.MAX_IPK_BYTES+1)]:
            previous=self.item[field];self.item[field]=value
            with self.subTest(field=field),self.assertRaises(update.UpdateError):self.release()
            self.item[field]=previous

    def test_check_bounds_manifest_and_network_failure_propagates_to_ui(self):
        with self.assertRaises(update.UpdateError):update.check_release('13.40-r36',lambda url:io.BytesIO(b' '*65537))
        with self.assertRaises(OSError):update.check_release('13.40-r36',MagicMock(side_effect=OSError('offline')))

    def test_download_hash_size_and_package_identity_precede_install(self):
        release=self.release()
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/'update.ipk'
            update.download_release(release,target,lambda *a,**kw:io.BytesIO(self.data))
            update.validate_ipk(target,release)
            target.unlink()
            with self.assertRaises(update.UpdateError):update.download_release(release,target,lambda *a,**kw:io.BytesIO(self.data[:-1]))
            self.assertFalse(target.exists())
            with self.assertRaises(update.UpdateError):update.download_release(release,target,lambda *a,**kw:io.BytesIO(b'x'*len(self.data)))
            self.assertFalse(target.exists())
            target.write_bytes(ipk(package='wrong-product'))
            with self.assertRaises(update.UpdateError):update.validate_ipk(target,release)

    def test_install_uses_argv_without_force_and_cleans_download_on_failure(self):
        runner=MagicMock(return_value=types.SimpleNamespace(returncode=1,stdout='failed'))
        with self.assertRaises(update.UpdateError):update.install_release(self.release(),lambda *a,**kw:io.BytesIO(self.data),runner)
        command=runner.call_args.args[0]
        self.assertEqual(command[:2],['opkg','install'])
        self.assertEqual(len(command),3)
        self.assertFalse(Path(command[2]).exists())
        runner.reset_mock()
        with self.assertRaises(update.UpdateError):update.install_release(self.release(),lambda *a,**kw:io.BytesIO(b'broken'),runner)
        runner.assert_not_called()


class PublishUpdateTests(unittest.TestCase):
    def prepare(self,folder):
        root=Path(folder)/'plugin'
        compatibility=Path(folder)/'restoration/update/candidate.json'
        compatibility.parent.mkdir(parents=True)
        compatibility.write_text('original-feed')
        for name in ('src/GlassSysUtil','dist','update'):(root/name).mkdir(parents=True)
        (root/'src/GlassSysUtil/version').write_text('13.40-r37')
        (root/'update/release-request').write_text('13.40-r37')
        (root/'update/RELEASE-NOTES.md').write_text('Opravy')
        (root/'update/candidate.json').write_text('original-feed')
        (root/'dist'/('%s_13.40-r37_all.ipk' % update.PACKAGE_ID)).write_bytes(ipk())
        return root

    def test_wrong_branch_cannot_publish(self):
        with patch.dict('os.environ',{'GITHUB_REF':'refs/heads/warder-master-production'}),patch.object(publish_update,'run') as run:
            with self.assertRaises(RuntimeError):publish_update.publish()
            run.assert_not_called()

    def test_feed_advances_only_after_verifying_actual_published_bytes(self):
        for valid in (False,True):
            with self.subTest(valid=valid),tempfile.TemporaryDirectory() as folder:
                root=self.prepare(folder);commands=[]
                def run(*args):
                    commands.append(args)
                    if args[:2]==('gh','api'):return json.dumps([[{'tag_name':'v13.40-r37','draft':False,'prerelease':True}]])
                    if args[:3]==('gh','release','download'):
                        if not any(command[0]=='git' for command in commands):
                            self.assertEqual((root/'update/candidate.json').read_text(),'original-feed')
                        (Path(args[-1])/(update.PACKAGE_ID+'_13.40-r37_all.ipk')).write_bytes(ipk() if valid else b'wrong')
                    return ''
                with patch.object(publish_update,'BASE',root),patch.object(publish_update,'run',side_effect=run),patch.dict('os.environ',{'GITHUB_REF':'refs/heads/original-python314'}):
                    if valid:
                        publish_update.publish()
                        self.assertEqual(json.loads((root/'update/candidate.json').read_text())['release']['sha256'],hashlib.sha256(ipk()).hexdigest())
                        self.assertEqual((root.parent/'restoration/update/candidate.json').read_bytes(),(root/'update/candidate.json').read_bytes())
                        self.assertEqual(commands[-1],('git','push','origin','HEAD:original-python314'))
                        before=len(commands)
                        publish_update.publish()
                        self.assertFalse(any(command[0]=='git' for command in commands[before:]))
                    else:
                        with self.assertRaises(RuntimeError):publish_update.publish()
                        self.assertEqual((root/'update/candidate.json').read_text(),'original-feed')
                        self.assertEqual((root.parent/'restoration/update/candidate.json').read_text(),'original-feed')
                        self.assertFalse(any(command[0]=='git' for command in commands))


class PluginUpdateUITests(unittest.TestCase):
    def setUp(self):
        self.plugin=load(ROOT/'src/GlassSysUtil')
        self.ui=importlib.import_module('Plugins.Extensions.GlassSysUtil.plugin_update_ui')
        notice=types.SimpleNamespace(TYPE_INFO=0,TYPE_YESNO=1,TYPE_ERROR=2)
        mock=patch.object(self.ui,'MessageBox',notice);mock.start();self.addCleanup(mock.stop)
        self.session=MagicMock()
        self.screen=self.plugin.SysUtilMngMain(self.session)
        self.session.current_dialog=self.screen
        self.screen.readVersion=MagicMock(return_value='13.40-r36')
        self.screen['info'].setText=MagicMock()
        self.factory=MagicMock()
        self.check=MagicMock()
        self.api=vars(self.plugin)
        self.api['config'].osd.language.value='sk_SK'
        self.controller=self.ui.StartupUpdateCheck(self.screen,self.api,self.check,self.factory)
        self.release=types.SimpleNamespace(version='13.40-r37',notes='Opravy',notes_i18n={})

    def test_start_once_and_manual_request_reuses_inflight_check(self):
        self.controller.start();self.controller.start()
        self.assertFalse(self.controller.request(manual=True))
        self.factory.return_value.start.assert_called_once()
        self.check.assert_not_called()
        self.check.return_value=self.release
        self.controller.work();self.controller.poll()
        self.check.assert_called_once_with('13.40-r36')
        self.assertFalse(self.session.openWithCallback.call_args.kwargs['default'])

    def test_offer_waits_until_parent_active_and_closed_parent_cannot_install(self):
        self.controller.results.put((self.release,None))
        self.session.current_dialog=object()
        self.controller.poll();self.session.openWithCallback.assert_not_called()
        self.session.current_dialog=self.screen
        self.controller.poll();self.session.openWithCallback.assert_called_once()
        callback=self.session.openWithCallback.call_args.args[0]
        callback(False);self.session.open.assert_not_called()
        self.controller.stop();callback(True);self.session.open.assert_not_called()

    def test_automatic_failure_is_silent_and_manual_failure_visible(self):
        self.controller.results.put((None,'offline'));self.controller.poll()
        self.session.open.assert_not_called()
        self.controller.manual=True
        self.controller.results.put((None,'offline'));self.controller.poll()
        self.session.open.assert_called_once()

    def test_accepted_update_opens_installer_and_manual_current_is_reported(self):
        self.controller.answer(self.release,True)
        self.session.open.assert_called_once_with(self.ui.PluginInstallScreen,self.release,self.api)
        self.session.reset_mock();self.controller.manual=True
        self.controller.results.put((None,None));self.controller.poll()
        self.session.open.assert_called_once()

    def test_install_success_changes_existing_screen_then_restarts_after_three_seconds(self):
        timers=[MagicMock(),MagicMock()];api=dict(self.api);api['eTimer']=iter(timers).__next__
        install=MagicMock(return_value='13.40-r37');factory=MagicMock()
        screen=self.ui.PluginInstallScreen(self.session,self.release,api,install,factory)
        screen.start();screen.start();factory.return_value.start.assert_called_once()
        install.assert_not_called()
        screen.work();screen.poll()
        self.assertIn('3 sekundy',screen['status'].text)
        timers[1].start.assert_called_once_with(3000,True)
        self.session.open.assert_not_called();screen.finish();self.assertFalse(hasattr(screen,'result'))
        import enigma
        with patch.object(enigma,'quitMainloop') as quit:
            screen.restart();quit.assert_called_once_with(3)
            screen.cleanup();screen.restart();quit.assert_called_once()

    def test_install_failure_allows_back_without_restart(self):
        timers=[MagicMock(),MagicMock()];api=dict(self.api);api['eTimer']=iter(timers).__next__
        screen=self.ui.PluginInstallScreen(self.session,self.release,api,thread_factory=MagicMock())
        screen.results.put((None,'opkg failed'));screen.poll()
        self.assertIn('zlyhala',screen['status'].text)
        self.assertEqual(screen['red'].text,'Naspäť')
        timers[1].start.assert_not_called()
        screen.finish();self.assertEqual(screen.result,())


if __name__=='__main__':unittest.main()
