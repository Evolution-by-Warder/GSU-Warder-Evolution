import importlib.util
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import MagicMock, patch
from receiver_stubs import load

ROOT = Path(__file__).resolve().parents[1] / 'src/GlassSysUtil'
spec = importlib.util.spec_from_file_location('swap_ops_test', ROOT / 'swap_ops.py')
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)


class SwapOperationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.fstab = self.directory / 'fstab'
        self.fstab.write_text('# keep this\n/dev/root / ext4 defaults 0 1\n')
        self.proc = self.directory / 'swaps'
        self.proc.write_text('Filename Type Size Used Priority\n')
        self.store = ops.SwapStore(str(self.fstab), str(self.proc), lock=str(self.directory / 'lock'))
        self.store.mounted = lambda path: str(path)
        self.commands = []
        self.store.run = self.command

    def command(self, name, path):
        self.commands.append((name, path))
        if name == 'swapon':
            self.proc.write_text('Filename Type Size Used Priority\n%s file 32764 0 -2\n' % ops.escape(path))
        elif name == 'swapoff':
            self.proc.write_text('Filename Type Size Used Priority\n')

    def active_file(self, name='swapfile_test'):
        path = self.directory / name
        path.write_bytes(b'test')
        self.command('swapon', str(path))
        self.commands.clear()
        return path

    def test_create_allocates_private_file_verifies_active_and_appends_fstab(self):
        path = self.store.create(str(self.directory), 32, 'test')
        self.assertEqual(Path(path).stat().st_size, 32 * 1024 * 1024)
        self.assertEqual(Path(path).stat().st_mode & 0o777, 0o600)
        self.assertEqual([row[0] for row in self.commands], ['mkswap', 'swapon'])
        self.assertTrue(self.store.active(path))
        self.assertIn('# keep this\n', self.fstab.read_text())
        self.assertIn(path + ' none swap defaults 0 0\n', self.fstab.read_text())

    def test_existing_file_and_symlink_are_not_overwritten(self):
        path = self.directory / 'swapfile_test'
        path.write_bytes(b'original')
        for linked in (False, True):
            if linked:
                path.unlink(); path.symlink_to(self.fstab)
            with self.assertRaises(ops.SwapError):
                self.store.create(str(self.directory), 32, 'test')
        self.assertFalse(self.commands)
        self.assertTrue(self.fstab.read_text().startswith('# keep'))

    def test_invalid_size_name_and_low_space_do_not_create_files(self):
        for size, name in [(1, 'good'), (True, 'good'), (32, '../bad'), (32, 'bad;name'), (32, '')]:
            with self.assertRaises(ops.SwapError):
                self.store.create(str(self.directory), size, name)
        with patch.object(ops.os, 'statvfs', return_value=types.SimpleNamespace(f_bavail=1, f_frsize=4096)):
            with self.assertRaises(ops.SwapError):
                self.store.create(str(self.directory), 32, 'test')
        self.assertFalse((self.directory / 'swapfile_test').exists())

    def test_failed_mkswap_removes_only_new_file_and_preserves_fstab(self):
        before = self.fstab.read_bytes()
        self.store.run = MagicMock(side_effect=ops.SwapError('mkswap failed'))
        with self.assertRaisesRegex(ops.SwapError, 'mkswap failed'):
            self.store.create(str(self.directory), 32, 'test')
        self.assertFalse((self.directory / 'swapfile_test').exists())
        self.assertEqual(self.fstab.read_bytes(), before)

    def test_success_exit_without_active_swap_is_failure(self):
        self.store.run = MagicMock()
        with self.assertRaisesRegex(ops.SwapError, 'did not become active'):
            self.store.create(str(self.directory), 32, 'test')
        self.assertFalse((self.directory / 'swapfile_test').exists())

    def test_failed_fstab_update_rolls_back_new_active_swap(self):
        self.store.fstab_write = MagicMock(side_effect=OSError('read only'))
        with self.assertRaises(OSError):
            self.store.create(str(self.directory), 32, 'test')
        self.assertEqual([row[0] for row in self.commands], ['mkswap', 'swapon', 'swapoff'])
        self.assertFalse((self.directory / 'swapfile_test').exists())

    def test_failed_rollback_preserves_active_file(self):
        self.store.fstab_write = MagicMock(side_effect=OSError('read only'))
        def run(name, path):
            if name == 'swapoff':
                raise ops.SwapError('busy')
            self.command(name, path)
        self.store.run = run
        with self.assertRaisesRegex(ops.SwapError, 'file preserved'):
            self.store.create(str(self.directory), 32, 'test')
        self.assertTrue((self.directory / 'swapfile_test').exists())

    def test_partition_delete_is_rejected_before_any_command(self):
        self.proc.write_text('/dev/mmcblk0p12 partition 262140 0 -1\n')
        with self.assertRaisesRegex(ops.SwapError, 'partitions are preserved'):
            self.store.delete('/dev/mmcblk0p12')
        self.assertFalse(self.commands)

    def test_delete_updates_only_exact_swap_entry_preserves_comments_and_similar_names(self):
        path = self.active_file('swapfile_with space')
        data = ('# ' + str(path) + '\n' + ops.escape(str(path)) + ' none swap defaults 0 0\n' +
                ops.escape(str(path)) + '_other none swap defaults 0 0\n')
        self.fstab.write_text(data)
        self.store.delete(str(path))
        self.assertFalse(path.exists())
        self.assertIn('# ' + str(path), self.fstab.read_text())
        self.assertIn('_other none swap', self.fstab.read_text())
        self.assertEqual(self.commands, [('swapoff', str(path))])

    def test_failed_swapoff_does_not_unlink_or_edit_fstab(self):
        path = self.active_file()
        before = self.fstab.read_bytes()
        self.store.run = MagicMock(side_effect=ops.SwapError('busy'))
        with self.assertRaises(ops.SwapError):
            self.store.delete(str(path))
        self.assertTrue(path.exists())
        self.assertEqual(self.fstab.read_bytes(), before)

    def test_failed_delete_fstab_restores_active_swap_and_keeps_file(self):
        path = self.active_file()
        self.store.fstab_write = MagicMock(side_effect=OSError('read only'))
        with self.assertRaises(ops.SwapError):
            self.store.delete(str(path))
        self.assertTrue(path.exists())
        self.assertTrue(self.store.active(str(path)))

    def test_fstab_update_detects_external_change(self):
        before, info = self.store.fstab_snapshot()
        self.fstab.write_text('# changed externally\n')
        with self.assertRaisesRegex(ops.SwapError, 'changed during'):
            self.store.fstab_write(before, b'new', info)
        self.assertEqual(self.fstab.read_text(), '# changed externally\n')

    def test_failed_unlink_restores_fstab_and_reactivates_file(self):
        path = self.active_file()
        original = (str(path) + ' none swap defaults 0 0\n').encode()
        self.fstab.write_bytes(original)
        unlink = ops.os.unlink
        def fail_selected(target, *args, **kwargs):
            if str(target) == str(path):
                raise PermissionError('unlink denied')
            return unlink(target, *args, **kwargs)
        with patch.object(ops.os, 'unlink', side_effect=fail_selected):
            with self.assertRaisesRegex(ops.SwapError, 'unlink denied'):
                self.store.delete(str(path))
        self.assertTrue(path.exists())
        self.assertTrue(self.store.active(str(path)))
        self.assertEqual(self.fstab.read_bytes(), original)

    def test_worker_lock_rejects_overlapping_operation(self):
        with self.store.locked():
            with self.assertRaises(BlockingIOError):
                with self.store.locked():
                    self.fail('overlapping operation acquired the lock')

    def test_swapoff_success_code_without_stopping_keeps_file_and_fstab(self):
        path = self.active_file()
        original = self.fstab.read_bytes()
        self.store.run = MagicMock()
        with self.assertRaisesRegex(ops.SwapError, 'still active'):
            self.store.delete(str(path))
        self.assertTrue(path.exists())
        self.assertEqual(self.fstab.read_bytes(), original)

    def test_mount_discovery_supports_custom_media_mounts_but_excludes_network_root_readonly(self):
        mounts = self.directory / 'mounts'
        mounts.write_text('/dev/a / ext4 rw 0 0\n/dev/b /media/hdd ext4 rw 0 0\n'
            '/dev/c /media/My\\040USB ext4 rw 0 0\n/dev/d /media/ro ext4 ro 0 0\n'
            'server:/share /media/net nfs rw 0 0\n/dev/e /media/btrfs btrfs rw 0 0\n')
        with patch.object(ops.os.path, 'isdir', return_value=True):
            self.assertEqual(ops.places(str(mounts)), ['/media/My USB', '/media/hdd'])

    def test_subprocess_failure_and_timeout_propagate_without_shell(self):
        self.store.run = types.MethodType(ops.SwapStore.run, self.store)
        with patch.object(ops.subprocess, 'run', return_value=types.SimpleNamespace(returncode=1, stdout='unsupported filesystem')) as run:
            with self.assertRaisesRegex(ops.SwapError, 'unsupported filesystem'):
                self.store.run('swapon', '/media/hdd/file;name')
            self.assertEqual(run.call_args.args[0], ('swapon', '/media/hdd/file;name'))
            self.assertNotIn('shell', run.call_args.kwargs)
        with patch.object(ops.subprocess, 'run', side_effect=ops.subprocess.TimeoutExpired('swapon', 45)):
            with self.assertRaises(ops.subprocess.TimeoutExpired):
                self.store.run('swapon', '/media/hdd/file')


class SwapUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin = load(ROOT)
        from Plugins.Extensions.GlassSysUtil import swap_ui
        cls.ui = swap_ui

    def setUp(self):
        replacement = types.SimpleNamespace(TYPE_INFO=0, TYPE_ERROR=1, TYPE_YESNO=2)
        mock = patch.object(self.plugin, 'MessageBox', replacement)
        mock.start(); self.addCleanup(mock.stop)

    def test_create_is_deferred_busy_blocks_repeat_and_exit_then_success_closes_after_dialog(self):
        session = MagicMock()
        screen = self.plugin.SwapCreate(session)
        screen.list = [('size', types.SimpleNamespace(value='32')), ('disk', types.SimpleNamespace(value='/media/hdd')),
                       ('name', types.SimpleNamespace(value='test'))]
        pending = MagicMock()
        with patch.object(self.ui, 'deferToThread', return_value=pending) as thread:
            screen.SwapCreate(); screen.SwapCreate(); screen.exitSwap()
        self.assertEqual(thread.call_count, 1)
        self.assertTrue(screen._swap_busy)
        session.open.assert_not_called()
        pending.addCallback.call_args.args[0]('/media/hdd/swapfile_test')
        self.assertFalse(screen._swap_busy)
        session.openWithCallback.assert_called_once()

    def test_failure_keeps_editor_open_and_reports_error(self):
        session = MagicMock(); screen = self.plugin.SwapCreate(session)
        pending = MagicMock()
        with patch.object(self.ui, 'deferToThread', return_value=pending):
            self.ui.run(screen, vars(self.plugin), 'create', '/media/hdd', 32, 'test')
        pending.addErrback.call_args.args[0](types.SimpleNamespace(value=OSError('disk full')))
        self.assertFalse(screen._swap_busy)
        self.assertIn('disk full', session.open.call_args.args[1])
        session.openWithCallback.assert_not_called()

    def test_delete_confirmation_captures_path_and_partition_is_protected(self):
        session = MagicMock(); screen = self.plugin.swap_manager(session)
        screen['list'].getCurrent = lambda: ['/dev/mmcblk0p12']
        with patch.object(self.ui, 'swaps', return_value=[('/dev/mmcblk0p12', 'partition', 256, 0, -1)]):
            screen.swapDeleteQuestion()
        session.openWithCallback.assert_not_called()
        screen['list'].getCurrent = lambda: ['/media/hdd/swapfile']
        with patch.object(self.ui, 'swaps', return_value=[('/media/hdd/swapfile', 'file', 256, 0, -1)]):
            screen.swapDeleteQuestion()
        self.assertEqual(screen._swap_delete_path, '/media/hdd/swapfile')
        self.assertFalse(session.openWithCallback.call_args.kwargs['default'])
        with patch.object(self.ui, 'run') as run:
            screen['list'].getCurrent = lambda: ['/media/hdd/another']
            screen.swapDelete(True)
        self.assertEqual(run.call_args.args[-1], '/media/hdd/swapfile')

    def test_disk_discovery_is_deferred_and_late_callback_ignores_closed_screen(self):
        session = MagicMock(); screen = self.plugin.SwapCreate(session)
        pending = MagicMock()
        with patch.object(self.ui, 'deferToThread', return_value=pending) as thread:
            screen.SwapDefine()
        thread.assert_called_once_with(self.ui.places)
        screen._swap_closed = True
        pending.addCallback.call_args.args[0](['/media/hdd'])
        self.assertFalse(screen._swap_busy)
        session.open.assert_not_called()

    def test_disk_discovery_updates_real_selection_choices(self):
        screen = self.plugin.SwapCreate(MagicMock())
        pending = MagicMock()
        with patch.object(self.ui, 'deferToThread', return_value=pending):
            screen.SwapDefine()
        screen.list[1] = ('disk', MagicMock())
        screen['config'].invalidateCurrent = MagicMock()
        pending.addCallback.call_args.args[0](['/media/hdd', '/media/My USB'])
        screen.list[1][1].setChoices.assert_called_once_with(
            [self.plugin._('None'), '/media/hdd', '/media/My USB'], default=self.plugin._('None'))
        self.assertFalse(screen._swap_busy)

    def test_swap_list_keeps_decoded_path_for_delete_selection(self):
        screen = self.plugin.swap_manager(MagicMock())
        with patch.object(self.ui, 'swaps', return_value=[('/media/My USB/swapfile_test', 'file', 32764, 0, -2)]):
            screen.readSwapInfo()
        self.assertEqual(screen.list[0][0], '/media/My USB/swapfile_test')

