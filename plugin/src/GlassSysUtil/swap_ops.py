"""Worker-only swap file operations. Never remove block devices or overwrite files."""
import contextlib
import fcntl
import os
import re
import stat
import subprocess
import tempfile


SIZES = (32, 64, 128, 256, 512, 1024, 2048, 4096)


def unescape(value):
    return re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1], 8)), value)


def escape(value):
    return value.replace('\\', '\\134').replace(' ', '\\040').replace('\t', '\\011')


def swaps(path='/proc/swaps'):
    rows = []
    with open(path) as stream:
        for line in stream:
            fields = line.split()
            if len(fields) == 5 and fields[1] in ('file', 'partition'):
                rows.append((unescape(fields[0]), fields[1], int(fields[2]), int(fields[3]), int(fields[4])))
    return rows


def places(path='/proc/mounts'):
    result = []
    with open(path) as stream:
        for line in stream:
            fields = line.split()
            if len(fields) < 4:
                continue
            source, target, kind, options = fields[:4]
            target = unescape(target)
            if (source.startswith('/dev/') and kind in ('ext2', 'ext3', 'ext4', 'xfs')
                    and 'rw' in options.split(',') and target.startswith('/media/')
                    and os.path.realpath(target) == target and os.path.isdir(target)):
                if target not in result:
                    result.append(target)
    return sorted(result)


class SwapError(OSError):
    pass


class SwapStore:
    def __init__(self, fstab='/etc/fstab', swaps_path='/proc/swaps', mounts='/proc/mounts', lock='/run/gsu-swap.lock'):
        self.fstab, self.swaps_path, self.mounts, self.lock = fstab, swaps_path, mounts, lock

    @contextlib.contextmanager
    def locked(self):
        fd = os.open(self.lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield
        finally:
            os.close(fd)

    def run(self, *args):
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, timeout=45, check=False)
        if result.returncode:
            raise SwapError('%s: %s' % (args[0], result.stdout.strip()[-1500:]))

    def active(self, path):
        return any(row[0] == path for row in swaps(self.swaps_path))

    def mounted(self, path):
        path = os.path.abspath(path)
        if os.path.realpath(path) != path:
            raise SwapError('Symbolic links are not supported for swap files.')
        if path not in places(self.mounts):
            raise SwapError('Choose a mounted writable local ext2/ext3/ext4/XFS disk under /media.')
        return path

    def fstab_snapshot(self):
        try:
            fd = os.open(self.fstab, os.O_RDONLY | os.O_NOFOLLOW)
        except FileNotFoundError:
            return b'', None
        with os.fdopen(fd, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode):
                raise SwapError('fstab is not a regular file.')
            return stream.read(), info

    def fstab_write(self, old, new, info):
        if self.fstab_snapshot()[0] != old:
            raise SwapError('fstab changed during the operation; please try again.')
        fd, temporary = tempfile.mkstemp(prefix='.gsu-fstab-', dir=os.path.dirname(self.fstab))
        try:
            with os.fdopen(fd, 'wb') as stream:
                os.fchmod(stream.fileno(), stat.S_IMODE(info.st_mode) if info else 0o644)
                if info and os.geteuid() == 0:
                    os.fchown(stream.fileno(), info.st_uid, info.st_gid)
                stream.write(new)
                stream.flush()
                os.fsync(stream.fileno())
            if self.fstab_snapshot()[0] != old:
                raise SwapError('fstab changed during the operation; please try again.')
            os.replace(temporary, self.fstab)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @staticmethod
    def without_entry(data, path):
        result = []
        for line in data.splitlines(keepends=True):
            fields = line.decode('utf-8', 'surrogateescape').split()
            if fields and not fields[0].startswith('#') and len(fields) >= 3:
                if unescape(fields[0]) == path and fields[2] == 'swap':
                    continue
            result.append(line)
        return b''.join(result)

    def create(self, directory, size, name):
        if type(size) is not int or size not in SIZES:
            raise SwapError('Invalid swap size.')
        if not re.fullmatch(r'[\w-]{1,64}', name, flags=re.ASCII):
            raise SwapError('Use a name of 1–64 letters, digits, underscores or hyphens.')
        with self.locked():
            directory = self.mounted(directory)
            path = os.path.join(directory, 'swapfile_' + name)
            if os.path.lexists(path):
                raise SwapError('The selected file already exists.')
            disk = os.statvfs(directory)
            if disk.f_bavail * disk.f_frsize < (size + 16) * 1024 * 1024:
                raise SwapError('Not enough free disk space (16 MB reserve required).')
            old, info = self.fstab_snapshot()
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            identity = os.fstat(fd)
            try:
                with os.fdopen(fd, 'wb') as stream:
                    block = b'\0' * (1024 * 1024)
                    for _ in range(size):
                        stream.write(block)
                    stream.flush()
                    os.fsync(stream.fileno())
                self.mounted(directory)
                self.run('mkswap', path)
                self.run('swapon', path)
                if not self.active(path):
                    raise SwapError('The new swap file did not become active.')
                new = self.without_entry(old, path)
                if new and not new.endswith(b'\n'):
                    new += b'\n'
                new += (escape(path) + ' none swap defaults 0 0\n').encode()
                self.fstab_write(old, new, info)
            except Exception:
                if self.active(path):
                    try:
                        self.run('swapoff', path)
                    except Exception as error:
                        raise SwapError('Rollback could not stop the new swap; file preserved: %s (%s)' % (path, error))
                current = os.lstat(path)
                if (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino) and not self.active(path):
                    os.unlink(path)
                raise
            return path

    def delete(self, path):
        with self.locked():
            rows = swaps(self.swaps_path)
            row = next((r for r in rows if r[0] == path), None)
            if not row or row[1] != 'file':
                raise SwapError('Only active swap files can be deleted; swap partitions are preserved.')
            self.mounted(os.path.dirname(path))
            before = os.lstat(path)
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
                raise SwapError('Only regular swap files without links can be deleted.')
            old, info = self.fstab_snapshot()
            self.run('swapoff', path)
            if self.active(path):
                raise SwapError('Swap is still active; the file was preserved.')
            new = self.without_entry(old, path)
            updated = False
            try:
                current = os.lstat(path)
                if (current.st_dev, current.st_ino) != (before.st_dev, before.st_ino):
                    raise SwapError('The swap file changed during the operation.')
                self.fstab_write(old, new, info)
                updated = True
                os.unlink(path)
            except Exception as error:
                rollback = []
                if updated:
                    try:
                        self.fstab_write(new, old, info)
                    except Exception as failure:
                        rollback.append(str(failure))
                if os.path.exists(path):
                    try:
                        current = os.lstat(path)
                        if (current.st_dev, current.st_ino) == (before.st_dev, before.st_ino):
                            self.run('swapon', path)
                    except Exception as failure:
                        rollback.append(str(failure))
                raise SwapError(str(error) + ('; rollback: ' + '; '.join(rollback) if rollback else ''))
            return path
