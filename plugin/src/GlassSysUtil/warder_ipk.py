"""Inspect local IPK metadata without extraction, maintainer scripts or installation."""
import gzip
import io
import os
import re
import stat
import tarfile
from pathlib import Path

LIMIT = 2*1024*1024
FIELDS = ('Package', 'Version', 'Architecture', 'Depends', 'Pre-Depends', 'Conflicts')
HOOKS = {'preinst','postinst','prerm','postrm'}


def inspect(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or not 8 <= info.st_size <= 128*1024*1024:
            raise ValueError('size or file type')
        if stream.read(8) != b'!<arch>\n':
            raise ValueError('unsupported container')
        control = None
        for _ in range(32):
            header = stream.read(60)
            if not header:
                break
            if len(header) != 60 or header[-2:] != b'`\n':
                raise ValueError('invalid header')
            name = header[:16].decode('ascii').rstrip(' /')
            size = int(header[48:58])
            if size < 0 or stream.tell()+size > info.st_size:
                raise ValueError('invalid length')
            if name in ('control.tar.gz','control.tar'):
                if control is not None or size > LIMIT:
                    raise ValueError('invalid control')
                raw = stream.read(size)
                if name.endswith('.gz'):
                    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as gz:
                        raw = gz.read(LIMIT+1)
                if len(raw) > LIMIT:
                    raise ValueError('control too large')
                control = raw
            else:
                stream.seek(size,1)
            stream.seek(size%2,1)
        else:
            raise ValueError('too many members')
    if control is None:
        raise ValueError('unsupported control')
    metadata, scripts = None, set()
    with tarfile.open(fileobj=io.BytesIO(control),mode='r:') as archive:
        for index, member in enumerate(archive):
            if index >= 128:
                raise ValueError('too many control members')
            name = member.name.removeprefix('./')
            if name == 'control':
                if not member.isfile() or member.size > 65536 or metadata is not None:
                    raise ValueError('invalid control')
                metadata = archive.extractfile(member).read().decode('utf-8')
            if name in HOOKS:
                scripts.add(name)
    if metadata is None:
        raise ValueError('missing metadata')
    fields = {}
    for line in metadata.splitlines():
        key, sep, value = line.partition(':')
        if sep and key in FIELDS:
            if key in fields or len(value) > 2048 or any(ord(c) < 32 for c in value):
                raise ValueError('invalid field')
            fields[key] = value.strip()
    if not all(fields.get(k) for k in FIELDS[:3]):
        raise ValueError('missing fields')
    return fields, sorted(scripts)


def review(tr, directory='/tmp'):
    # Show a bounded inventory in a worker. Never open links, sockets or devices.
    lines = []
    with os.scandir(directory) as files:
        for index, item in enumerate(files):
            if index >= 4096:
                lines.append(tr('Partial result'))
                break
            if not item.name.endswith('.ipk') or not item.is_file(follow_symlinks=False):
                continue
            lines.append(re.sub(r'[\x00-\x1f\x7f]', '?', item.name)[:160])
            try:
                fields, scripts = inspect(Path(directory)/item.name)
                lines.append('   '.join(fields[k] for k in FIELDS[:3]))
                lines.extend(k+'   '+fields[k] for k in FIELDS[3:] if fields.get(k))
                lines.append(tr('Scripts')+'   '+(', '.join(scripts) or '—'))
            except (ValueError, EOFError, OSError, tarfile.TarError):
                lines.append(tr('Unavailable'))
            lines.append('')
            if len(lines) >= 45:
                lines.append(tr('Partial result'))
                break
    return '\n'.join(lines) if lines else tr('No Files Found')
