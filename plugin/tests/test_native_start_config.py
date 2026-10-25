import importlib.util
import json
import os
from pathlib import Path
import shlex
import stat
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock,patch

ROOT=Path(__file__).resolve().parents[1]/'src/GlassSysUtil'
spec=importlib.util.spec_from_file_location('native_start_config_under_test',ROOT/'native_start_config.py')
config=importlib.util.module_from_spec(spec);spec.loader.exec_module(config)


class StartConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.init=self.root/'init';self.bin=self.root/'bin';self.store_dir=self.root/'settings'
        self.cfg=self.root/'config dir';self.tmp=self.root/'temporary'
        for p in (self.init,self.bin,self.cfg,self.tmp):p.mkdir()
        self.name='oscam-master';self.binary=self.bin/self.name;self.script=self.init/('softcam.'+self.name)
        self.capture=self.root/'captured.json'
        self.help='ConfigDir  : '+str(self.cfg)+'\n'+'\n'.join(d[0] for d in config.OPTIONS.values())+'\n--temp-dir <dir>\n . Default: '+str(self.tmp)+'\n'
        self.binary.write_text('#!'+sys.executable+'\nimport json,sys\nfrom pathlib import Path\nif "--help" in sys.argv:\n print('+repr(self.help)+')\nelse:\n Path('+repr(str(self.capture))+').write_text(json.dumps(sys.argv[1:]))\n')
        self.binary.chmod(0o755)
        self.original='#!/bin/sh\nCAM='+self.name+'\nDAEMON='+shlex.quote(str(self.binary))+'\nPIDFILE=/var/tmp/${CAM}.pid\ncase "$1" in\nstart)\n    $DAEMON --config-dir '+shlex.quote(str(self.cfg))+' --daemon --pidfile $PIDFILE --restart 2 --utf8 2 | cat\n    echo started\n    ;;\nstop) echo stopped;;\nesac\n'
        self.script.write_text(self.original);self.script.chmod(0o751)
        self.store=config.StartConfigStore(self.init,self.bin,self.store_dir)

    def test_snapshot_reads_actual_help_and_init_defaults_without_writes(self):
        snapshot=self.store.snapshot(self.name)
        self.assertEqual(snapshot['values']['config_dir'],str(self.cfg))
        self.assertEqual(snapshot['values']['temp_dir'],str(self.tmp))
        self.assertEqual(snapshot['values']['restart'],2)
        self.assertEqual(snapshot['values']['pending'],32)
        self.assertEqual(snapshot['pidfile'],'/var/tmp/oscam-master.pid')
        self.assertFalse(self.store_dir.exists());self.assertEqual(self.script.read_text(),self.original)

    def test_save_preserves_native_command_tail_and_original_backup(self):
        snapshot=self.store.snapshot(self.name);values=dict(snapshot['values'],debug=128)
        self.store.save(snapshot,values)
        adapted=self.script.read_text()
        self.assertIn('--launch oscam-master -- $DAEMON',adapted)
        self.assertIn('--daemon --pidfile $PIDFILE --restart 2 --utf8 2 | cat',adapted)
        self.assertEqual(stat.S_IMODE(self.script.stat().st_mode),0o751)
        self.assertEqual((self.store_dir/(self.name+'.init-backup')).read_text(),self.original)
        self.assertFalse(self.capture.exists()) # save never starts or restarts CAM
        second=self.store.snapshot(self.name);self.assertEqual(second['values']['debug'],128)
        values['debug']=0;self.store.save(second,values)
        self.assertEqual(self.script.read_text().count('# GSU OSCam startup adapter:'),1)
        self.assertEqual((self.store_dir/(self.name+'.init-backup')).read_text(),self.original)

    def test_launch_uses_argv_and_keeps_pid_daemon_and_unknown_options(self):
        snapshot=self.store.snapshot(self.name)
        special=self.root/'config; $(touch SHOULD_NOT_EXIST)';special.mkdir()
        self.store.save(snapshot,dict(snapshot['values'],config_dir=str(special),debug=128))
        defaults=['--config-dir',str(self.cfg),'--daemon','--pidfile','/var/tmp/oscam-master.pid','--restart','2','--utf8','2']
        with patch.object(config.os,'execv') as execute:self.store.launch(self.name,[str(self.binary)]+defaults)
        binary,args=execute.call_args.args
        self.assertEqual(binary,str(self.binary));self.assertEqual(args[0],str(self.binary))
        self.assertIn('--daemon',args);self.assertIn('/var/tmp/oscam-master.pid',args)
        self.assertEqual(args[args.index('--config-dir')+1],str(special))
        self.assertEqual(args.count('--restart'),1)
        self.assertEqual(args[args.index('--debug')+1],'128')
        self.assertEqual(args[args.index('--utf8')+1],'2')
        self.assertFalse((self.root/'SHOULD_NOT_EXIST').exists())

    def test_changed_script_or_invalid_values_never_overwrite_init(self):
        snapshot=self.store.snapshot(self.name)
        for invalid in [dict(snapshot['values'],pending=0),dict(snapshot['values'],restart=3),dict(snapshot['values'],config_dir='/missing-gsu-test-directory'),dict(snapshot['values'],debug='1; reboot')]:
            with self.assertRaises(ValueError):self.store.save(snapshot,invalid)
            self.assertEqual(self.script.read_text(),self.original)
            self.assertFalse(self.store_dir.exists())
        self.script.write_text(self.original+'# changed by package\n')
        with self.assertRaises(OSError):self.store.save(snapshot,snapshot['values'])
        self.assertTrue(self.script.read_text().endswith('# changed by package\n'))

    def test_script_write_failure_rolls_back_saved_options(self):
        snapshot=self.store.snapshot(self.name);original_write=config.atomic_write
        def write(path,data,mode=0o644):
            if path==self.script:raise OSError('read-only init directory')
            return original_write(path,data,mode)
        with patch.object(config,'atomic_write',side_effect=write):
            with self.assertRaises(OSError):self.store.save(snapshot,snapshot['values'])
        self.assertEqual(self.script.read_text(),self.original)
        self.assertFalse((self.store_dir/(self.name+'.json')).exists())

    def test_package_update_can_reapply_adapter_without_losing_new_native_arguments(self):
        snapshot=self.store.snapshot(self.name);self.store.save(snapshot,dict(snapshot['values'],debug=64))
        updated=self.original.replace('--restart 2','--restart 1')+'# updated package\n'
        self.script.write_text(updated)
        self.store.ensure_adapter(self.name)
        self.assertIn('--restart 1',self.script.read_text())
        self.assertTrue(self.script.read_text().endswith('# updated package\n'))
        self.assertEqual(self.store.snapshot(self.name)['values']['debug'],64)
        self.assertEqual(self.store._original(self.script.read_text(),self.name),updated)
        self.assertEqual((self.store_dir/(self.name+'.init-backup')).read_text(),self.original)

    def test_uninstall_restores_current_native_line_and_keeps_other_package_changes(self):
        snapshot=self.store.snapshot(self.name);self.store.save(snapshot,snapshot['values'])
        self.script.write_text(self.script.read_text()+'# unrelated admin edit\n')
        self.store.restore_all()
        self.assertEqual(self.script.read_text(),self.original+'# unrelated admin edit\n')
        self.assertTrue((self.store_dir/(self.name+'.json')).exists())
        self.store.restore_all() # safe to repeat
        self.assertEqual(self.script.read_text(),self.original+'# unrelated admin edit\n')

    def test_settings_are_per_cam_and_foreign_binary_is_rejected(self):
        snapshot=self.store.snapshot(self.name);self.store.save(snapshot,snapshot['values'])
        other='oscam-stable';(self.bin/other).symlink_to(self.binary)
        (self.init/('softcam.'+other)).write_text(self.original.replace(self.name,other));(self.init/('softcam.'+other)).chmod(0o755)
        self.assertFalse((self.store_dir/(other+'.json')).exists())
        with patch.object(config.os,'execv') as execute:
            with self.assertRaises(ValueError):self.store.launch(self.name,['/bin/echo','unexpected'])
        execute.assert_not_called()
        for name in ('../oscam','cccam',''):
            with self.assertRaises(ValueError):self.store.snapshot(name)

    def test_unsupported_script_and_help_fail_before_any_write(self):
        self.script.write_text('#!/bin/sh\nexec custom-launcher\n')
        with self.assertRaises(ValueError):self.store.snapshot(self.name)
        self.script.write_text(self.original)
        with patch.object(config.subprocess,'run',return_value=types.SimpleNamespace(stdout=b'unknown program')):
            with self.assertRaises(ValueError):self.store.snapshot(self.name)
        with patch.object(config.subprocess,'run',side_effect=subprocess.TimeoutExpired('help',5)):
            with self.assertRaises(subprocess.TimeoutExpired):self.store.snapshot(self.name)
        self.assertFalse(self.store_dir.exists())

    def test_real_shell_launch_uses_configured_values_and_keeps_paths_literal(self):
        # A harmless Python argv recorder replaces OSCam. The adapted native
        # shell script invokes the actual adapter, which execs this recorder.
        runner=self.root/'test-launcher.py'
        runner.write_text('import importlib.util,sys\nspec=importlib.util.spec_from_file_location("start",'+repr(str(ROOT/'native_start_config.py'))+')\nm=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)\ns=m.StartConfigStore('+repr(str(self.init))+','+repr(str(self.bin))+','+repr(str(self.store_dir))+')\ns.launch(sys.argv[2],sys.argv[4:])\n')
        with patch.object(config,'__file__',str(runner)):
            snapshot=self.store.snapshot(self.name)
            special=self.root/'cfg spaces; literal';special.mkdir()
            self.store.save(snapshot,dict(snapshot['values'],config_dir=str(special),debug=256))
        # Match the receiver interpreter path to this test host interpreter.
        self.script.write_text(self.script.read_text().replace('/usr/bin/python3',shlex.quote(sys.executable)))
        result=subprocess.run(['/bin/sh',str(self.script),'start'],capture_output=True,timeout=5)
        self.assertEqual(result.returncode,0,result.stderr)
        args=json.loads(self.capture.read_text())
        self.assertEqual(args[args.index('--config-dir')+1],str(special))
        self.assertEqual(args[args.index('--debug')+1],'256')
        self.assertEqual(args[args.index('--pidfile')+1],'/var/tmp/oscam-master.pid')
        self.assertIn('--daemon',args);self.assertIn('--utf8',args)


if __name__=='__main__':unittest.main()
