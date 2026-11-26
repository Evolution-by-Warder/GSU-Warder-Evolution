"""Private, byte-verified pre-scan copies of native channel databases and bouquets."""
import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
from pathlib import Path

CHANNEL_FILE = re.compile(r'(?:lamedb5?|bouquets\.(?:tv|radio)|(?:userbouquet|alternatives)\.[\w.-]+\.(?:tv|radio))\Z')
MAX_BYTES = 32 * 1024 * 1024
MAX_FILES = 1024


def copy_database(source, destination, limit):
    source_fd = os.open(source,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(source_fd,'rb') as reader:
        info = os.fstat(source_fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError('unsupported channel file')
        digest = hashlib.sha256()
        count = 0
        with destination.open('xb') as writer:
            while True:
                block = reader.read(65536)
                if not block:
                    break
                count += len(block)
                if count>limit:
                    raise ValueError('channel database changed during backup')
                writer.write(block)
                digest.update(block)
            writer.flush()
            os.fsync(writer.fileno())
        final = os.stat(source, follow_symlinks=False)
        if (final.st_ino,final.st_mtime_ns,final.st_size) != (info.st_ino,info.st_mtime_ns,count):
            raise ValueError('channel database changed during backup')
    check = hashlib.sha256()
    with destination.open('rb') as verify:
        for block in iter(lambda:verify.read(65536),b''):
            check.update(block)
    if check.digest()!=digest.digest():
        raise OSError('backup verification failed')
    return count,digest.hexdigest(),(info.st_dev,info.st_ino,info.st_size,info.st_mtime_ns)


def create(source, parent=None):
    source = Path(source)
    if parent is None:
        hdd = Path('/media/hdd')
        from .warder_storage import mounts,REMOTE
        from .warder_tools import Probe
        local = any(device.startswith('/dev/') and target==str(hdd) and fs not in REMOTE and not readonly
                    for device,target,fs,readonly in mounts(Probe()))
        parent = hdd if local and os.access(hdd,os.W_OK) else Path('/tmp')
    entries = []
    for path in source.iterdir():
        if CHANNEL_FILE.fullmatch(path.name):
            entries.append(path)
            if len(entries)>MAX_FILES:
                raise ValueError('too many channel lists')
    if not any(p.name in ('lamedb','lamedb5') for p in entries):
        raise ValueError('no native channel database')
    limit = min(MAX_BYTES,shutil.disk_usage(parent).free - 8*1024*1024)
    root = Path(tempfile.mkdtemp(prefix='gsu-channel-backup-',dir=parent))
    try:
        if root.stat().st_mode & 0o077:
            if Path(parent)==Path('/media/hdd'):
                root.rmdir()
                return create(source,Path('/tmp'))
            raise OSError('private backup directory unavailable')
        checks, identities = {}, {}
        for path in sorted(entries):
            size, checks[path.name], identities[path] = copy_database(path,root/path.name,limit)
            limit -= size
        if {p.name for p in entries} != {p.name for p in source.iterdir() if CHANNEL_FILE.fullmatch(p.name)}:
            raise ValueError('channel list changed during backup')
        for path,identity in identities.items():
            st=path.lstat()
            if (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns)!=identity:
                raise ValueError('channel files changed during snapshot')
        (root/'SHA256.json').write_text(json.dumps(checks,sort_keys=True,indent=2)+'\n',encoding='utf-8')
        return str(root)
    except Exception:
        if root.exists():
            shutil.rmtree(root)
        raise


def inventory(tr,cancelled,probe=None):
    """Read only existing private backup manifests; no rehash, restore or deletion."""
    from .warder_tools import Probe,read
    from .warder_storage import mounts,REMOTE
    from datetime import datetime
    p=probe or Probe()
    table=mounts(p)
    remote=tuple(target.rstrip('/')+'/' for _,target,fs,_ in table if fs in REMOTE)
    roots=['/tmp']
    if any(device.startswith('/dev/') and target=='/media/hdd' and fs not in REMOTE
           for device,target,fs,_ in table):
        roots.append('/media/hdd')
    candidates=[]
    for location in roots:
        if cancelled.is_set():return ''
        if any((location.rstrip('/')+'/').startswith(target) for target in remote):continue
        parent=p.path(location)
        if any(node.is_symlink() for node in (parent,*parent.parents)):continue
        for name in p.entries(location,512):
            if cancelled.is_set():return ''
            if not re.fullmatch(r'gsu-channel-backup-[A-Za-z0-9_-]{1,64}',name):continue
            path=parent/name
            try:
                info=path.lstat()
                if stat.S_ISDIR(info.st_mode) and not info.st_mode&0o077:
                    candidates.append((info.st_mtime,location,name,path))
            except OSError:continue
    rows=[]
    for stamp,location,name,path in sorted(candidates,key=lambda row:(-row[0],row[1],row[2]))[:12]:
        if cancelled.is_set():return ''
        # Do not follow a replaced directory or read channel lists (which may
        # contain private IPTV credentials). This is manifest metadata only.
        if path.is_symlink():continue
        raw=read(path/'SHA256.json',131072,private_log=True)
        try:
            manifest=json.loads(raw)
            valid=(isinstance(manifest,dict) and 1<=len(manifest)<=MAX_FILES
                   and any(k in manifest for k in ('lamedb','lamedb5'))
                   and all(CHANNEL_FILE.fullmatch(k) and isinstance(v,str) and
                           re.fullmatch(r'[0-9a-f]{64}',v) for k,v in manifest.items()))
        except (ValueError,TypeError,AttributeError):valid=False
        try:date=datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError,OverflowError,OSError):date='—'
        rows.extend((location+'/'+name,date,'SHA256.json   '+(str(len(manifest))+' · '+tr('Files') if valid else tr('Unavailable')),''))
    if len(candidates)>12:rows.append(tr('Partial result'))
    return '\n'.join(rows).strip() or tr('Unavailable')
