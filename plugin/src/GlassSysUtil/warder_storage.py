"""Bounded read-only storage inspection. Do not traverse other mounts or symlinks."""
import os
import re
import stat
import time
import subprocess
import shutil
from .warder_tools import Probe, unescape_mount
from .warder_telemetry import memory_values

REMOTE = {'nfs', 'nfs4', 'cifs', 'smbfs', 'sshfs', 'fuse.sshfs', 'autofs', '9p', 'ceph'}
CATEGORIES = (
    ('Picons', ('/usr/share/enigma2/picon', '/usr/share/enigma2/XPicons/picon',
                '/usr/share/enigma2/ZZPicons/picon', '/data/picon', '/picon')),
    ('Skins', ('/usr/share/enigma2',)),
    ('Plugins', ('/usr/lib/enigma2/python/Plugins',)),
    ('EPG', ('/etc/enigma2/epg.dat',)),
    ('Cache', ('/var/cache',)),
    ('Logs', ('/var/log', '/home/root/logs')),
)


def mounts(p):
    result = []
    for line in p.text('/proc/mounts', 131072).splitlines():
        fields = line.split()
        if len(fields) < 4:
            continue
        device, target, kind, options = fields[:4]
        target = unescape_mount(target)
        result.append((device, target, kind, 'ro' in options.split(',')))
    return result


def disks(p, table):
    rows = []
    for device, target, kind, readonly in table:
        if kind in REMOTE or (target != '/' and not device.startswith('/dev/')):
            continue
        try:
            usage = p.usage(p.path(target))
        except OSError:
            usage = None
        rows.append((target, device, kind, readonly, usage))
    return rows


def configured_picons(p, local):
    """Only read the four PiconHub path settings; never expose other settings."""
    profiles={}
    for line in p.text('/etc/enigma2/settings',1024*1024).splitlines():
        match=re.fullmatch(r'config\.plugins\.chocholousekpicons\.([0-3])\.(picon_folder|picon_folder_user)=(.*)',line)
        if match:profiles.setdefault(match[1],{})[match[2]]=match[3]
    roots=[]
    for profile in profiles.values():
        value=profile.get('picon_folder','')
        if value=='user_defined':value=profile.get('picon_folder_user','')
        if not value.startswith('/') or any(ord(c)<32 for c in value) or len(value)>512:continue
        value=value.rstrip('/')
        if os.path.normpath(value)!=value:continue
        # Refuse arbitrary system folders and whole disks. Dedicated picon
        # directories under known local mounts or Enigma2 data are allowed.
        if any(value.startswith(base.rstrip('/')+'/') for base in (*local,'/usr/share/enigma2','/data')):
            roots.append(value)
        elif value=='/picon':roots.append(value)
    return tuple(dict.fromkeys(roots))


def usage_categories(p, table, budget=100000, seconds=3, clock=time.monotonic, cancelled=None):
    """Independent bounded budgets: a large picon tree cannot starve later categories."""
    boundaries = {target for _, target, _, _ in table if target != '/'}
    local = [target for device, target, kind, _ in table
             if device.startswith('/dev/') and (target.startswith('/media/') or target.startswith('/mnt/')) and kind not in REMOTE]
    roots = {label: list(paths) for label, paths in CATEGORIES}
    for target in local:
        for label, suffix in [('Picons','picon'),('Picons','XPicons/picon'),('Picons','ZZPicons/picon'),
                              ('EPG','epg.dat'),('Logs','logs')]:
            roots[label].append(target.rstrip('/')+'/'+suffix)
    custom=set(configured_picons(p,local))
    roots['Picons'].extend(sorted(custom))
    picon_roots=set(roots['Picons'])
    totals,seen={},set()
    def stopped():
        return cancelled is not None and cancelled.is_set()
    for label,paths in roots.items():
        deadline=clock()+seconds
        size,visited,complete=0,0,True
        directories=set()
        for path in dict.fromkeys(paths):
            if stopped() or visited>=budget or clock()>=deadline:
                complete=False;break
            raw=p.path(path)
            if any(parent.is_symlink() for parent in (raw,*raw.parents)):
                if path in custom:complete=False
                continue
            if any(path==mount or path.startswith(mount+'/') for _,mount,fs,_ in table if fs in REMOTE):
                if path in custom:complete=False
                continue
            # Iterators are bounded in depth and closed on cancellation. This
            # avoids allocating a list with tens of thousands of directory entries.
            def walk(node,depth=0):
                nonlocal visited,complete,size
                if stopped() or visited>=budget or clock()>=deadline:
                    complete=False;return False
                visited+=1
                relative='/'+str(node.relative_to(p.root))
                if label!='Picons' and relative in picon_roots:return True
                try:
                    info=node.lstat()
                    key=(info.st_dev,info.st_ino)
                    if key in seen or stat.S_ISLNK(info.st_mode):return True
                    if stat.S_ISREG(info.st_mode):
                        # Custom profile directories may contain other files.
                        if path not in custom or node.suffix.lower()=='.png':
                            seen.add(key);size+=info.st_blocks*512
                    elif stat.S_ISDIR(info.st_mode):
                        if depth>=48:complete=False;return True
                        # Directory identity is tracked within a category only:
                        # a partial scan must not hide unrelated later roots.
                        if key in directories:return True
                        directories.add(key)
                        with os.scandir(node) as children:
                            for child in children:
                                if stopped() or visited>=budget or clock()>=deadline:
                                    complete=False;return False
                                target=node/child.name
                                if '/'+str(target.relative_to(p.root)) in boundaries:continue
                                if not walk(target,depth+1):return False
                except FileNotFoundError:
                    if path in custom and depth==0:complete=False
                except OSError:complete=False
                return True
            if not walk(raw):break
        totals[label]=size,complete
    return totals


def smart_device(device):
    match=re.fullmatch(r'(/dev/sd[a-z]+)\d*|(/dev/nvme\d+n\d+)(?:p\d+)?',device)
    return (match.group(1) or match.group(2)) if match else None


def smart(device, runner=subprocess.run, detailed=False):
    # Never wake a sleeping disk, start a self-test or change device settings.
    if not shutil.which('smartctl'):
        return None
    disk=smart_device(device)
    if not disk:return None
    try:
        result = runner(['smartctl', '-n', 'standby', '-H', '-A', disk], env={'LC_ALL':'C','PATH':os.defpath+':/usr/sbin:/sbin'},
                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=3, text=True)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode & 7:
        return None
    health = re.search(r'(?:test result|Health Status):\s*(PASSED|OK|FAILED)\b', result.stdout, re.I)
    temperature = re.search(r'^Temperature:\s+(-?\d+)\s+Celsius', result.stdout, re.M)
    if not temperature:
        temperature = re.search(r'^\s*(?:190|194)\s+\S+\s+(?:\S+\s+){7}(-?\d+)\b', result.stdout, re.M)
    status=(health.group(1).upper() if health else None,int(temperature.group(1)) if temperature else None)
    if not detailed:return status
    # Whitelist numeric SMART counters. Do not expose serials, WWNs, raw
    # vendor strings or unrelated command output; unavailable stays unknown.
    attrs={}
    for line in result.stdout.splitlines():
        fields=line.split()
        if len(fields)>=10 and fields[0] in ('5','9','12','187','188','197','198','199'):
            if re.fullmatch(r'[A-Za-z0-9_-]{1,60}',fields[1]) and fields[9].isdigit():
                attrs[fields[1]]=int(fields[9])
        elif ':' in line:
            key,raw=line.split(':',1)
            if key.strip() in ('Power On Hours','Power Cycles','Percentage Used','Media and Data Integrity Errors',
                               'Unsafe Shutdowns','Available Spare','Critical Warning'):
                value=raw.strip().replace(',','')
                if re.fullmatch(r'\d+%?',value):attrs[key.strip()]=int(value.rstrip('%'))
    return (*status,attrs)


def category_snapshot(probe=None,cancelled=None):
    p=probe or Probe()
    values=usage_categories(p,mounts(p),cancelled=cancelled)
    return [(name,*values.get(name,(0,False))) for name,_ in CATEGORIES]


def category_size(size,complete):
    if not size and not complete:return '—'
    # Small real lower bounds must not round to a misleading 0.0 MiB.
    value=('%d KiB'%max(1,size//1024)) if 0<size<104857 else '%.1f MiB'%(size/1048576)
    return ('' if complete else '≥ ')+value


def report(tr, detail=False, probe=None, panels=False, cancelled=None):
    p = probe or Probe()
    if cancelled is not None and cancelled.is_set():return ''
    table = mounts(p)
    rows = []
    if detail:
        for label, (size, complete) in usage_categories(p, table).items():
            rows.append('%s   %s%s' % (tr(label), category_size(size,complete), '' if complete else ' · '+tr('Partial result')))
    else:
        mem = memory_values(p.text('/proc/meminfo', 16384))
        for label, key in [('RAM', 'ram_available'), ('Swap', 'swap_free')]:
            value = mem[key]
            total=mem['ram_total' if key=='ram_available' else 'swap_total']
            rows.append(tr(label))
            rows.append('    %s %.1f MiB    ·    %s %.1f MiB' % (tr('Total:'),total/1048576,tr('Free:'),value/1048576) if total is not None and value is not None else '    —')
        memory_rows=rows[:]
        rows=[]
        options = []
        smart_cache = {}
        for path, dev, fs, ro, usage in disks(p, table):
            if cancelled is not None and cancelled.is_set():return ''
            rows.append('%s   ·   %s%s' % (path, fs, ' · '+tr('read-only') if ro else ''))
            if usage and usage.total>0:
                rows.append('    %s %.1f GiB    ·    %s %.1f GiB    ·    %s %.0f %%' % (tr('Total:'),usage.total/1073741824,tr('Free:'),usage.free/1073741824,tr('Used(%):'),100*(usage.total-usage.free)/usage.total))
            else:rows.append('    '+tr('Unavailable'))
            if (path.startswith('/media/') or path.startswith('/mnt/')) and not ro and usage and usage.free > 0:
                options.append((usage.free, path))
            disk=smart_device(dev)
            if disk and disk not in smart_cache and len(smart_cache)<4:
                smart_cache[disk]=smart(disk,detailed=True)
            health=smart_cache.get(disk)
            if health:
                rows.append('    SMART   %s   %s'%(health[0] or '—','—' if health[1] is None else '%d °C'%health[1]))
                for key,value in health[2].items():
                    rows.append('      %s   %d'%(key,value))
            elif disk:rows.append('    SMART   —')
            rows.append('')
        if options:
            rows.extend(('', tr('Picon storage')+'   '+max(options)[1]))
        disk_rows=rows
        if cancelled is not None and cancelled.is_set():return ''
        paths=['',tr('Saved storage paths')]
        for label,path in configured_storage_paths(p):
            paths.append('    '+tr(label)+'   '+(path or '—'))
        if cancelled is not None and cancelled.is_set():return ''
        if panels:return ('\n'.join(memory_rows+paths).strip(),'\n'.join(disk_rows).strip() or tr('Unavailable'))
        rows=memory_rows+['']+disk_rows+paths
    return '\n'.join(rows) or tr('Unavailable')


def memory_report(tr,cancelled,probe=None):
    """Detailed kernel memory fields are not a mutually exclusive pie chart."""
    from .warder_telemetry import memory_fields
    p=probe or Probe()
    values=memory_fields(p.text('/proc/meminfo',16384))
    rows=[]
    for key in ('MemTotal','MemAvailable','MemFree','Buffers','Cached','SReclaimable',
                'Shmem','Slab','AnonPages','Dirty','Writeback','SwapTotal','SwapFree'):
        if cancelled.is_set():return ''
        value=values.get(key)
        rows.append('%s   %s'%(key,'—' if value is None else '%.1f MiB'%(value/1048576)))
    raw=p.text('/proc/sys/vm/swappiness',32)
    rows.extend(('','swappiness   '+(raw if raw.isdigit() and 0<=int(raw)<=200 else '—')))
    return '\n'.join(rows)


def disk_counters(p):
    """Use whole block devices only; sector units in Linux diskstats are 512 B."""
    result={}
    for line in p.text('/proc/diskstats',65536).splitlines():
        f=line.split()
        if len(f)<14 or not re.fullmatch(r'(?:sd[a-z]+|hd[a-z]+|vd[a-z]+|mmcblk\d+|nvme\d+n\d+)',f[2]):continue
        try:values=tuple(int(f[i]) for i in (3,5,7,9))
        except ValueError:continue
        if min(values)>=0:result[f[2]]=values
    return result


def disk_activity(tr,cancelled,probe=None,clock=time.monotonic):
    """Short, passive sampling. No disk benchmark, file writes or wake-up."""
    p=probe or Probe()
    before=disk_counters(p);start=clock()
    if cancelled.wait(1):return ''
    after=disk_counters(p);elapsed=clock()-start
    rows=[]
    for name in sorted(before.keys()|after.keys()):
        if cancelled.is_set():return ''
        rows.append(name)
        old,new=before.get(name),after.get(name)
        delta=tuple(b-a for a,b in zip(old,new)) if old and new else ()
        if elapsed<=0 or not delta or min(delta)<0:
            rows.append('R —   ·   W —')
        else:
            rows.extend(('R   %.1f KiB/s   ·   %.1f IOPS'%(delta[1]/2/elapsed,delta[0]/elapsed),
                         'W   %.1f KiB/s   ·   %.1f IOPS'%(delta[3]/2/elapsed,delta[2]/elapsed)))
        rows.append('')
    return '\n'.join(rows).strip() or tr('Unavailable')


def configured_storage_paths(p):
    """Saved native path settings only; never resolve, stat or open the paths."""
    keys=('config.misc.epgcache_filename','config.misc.epgcachepath',
          'config.timeshift.path','config.usage.timeshift_path',
          'config.usage.default_path','config.usage.timer_path','config.usage.instantrec_path')
    values={}
    for line in p.text('/etc/enigma2/settings',1024*1024).splitlines():
        key,sep,value=line.partition('=')
        if not sep or key not in keys:continue
        if value in ('<default>','<current>','<timer>'):
            values[key]=value
        elif (value.startswith('/') and len(value)<=512 and value.isprintable()
              and not value.startswith('//') and '://' not in value
              and os.path.normpath(value)==value.rstrip('/')):
            values[key]=value
    return (
        ('EPG',values.get(keys[0]) or values.get(keys[1])),
        ('Timeshift',values.get(keys[2]) or values.get(keys[3])),
        ('Recordings',values.get(keys[4])),
        ('Timer recordings',values.get(keys[5])),
        ('Instant recordings',values.get(keys[6])),
    )


# Explicit, local-only top files analysis; sizes are logical file lengths.
LOCAL_FILE_SYSTEMS=frozenset(('ext2','ext3','ext4','xfs','btrfs','f2fs','vfat','exfat','ntfs','ntfs3','jffs2','ubifs','overlay','rootfs','squashfs','cramfs'))

def largest_files(p, table, cancelled, budget=15000, seconds=2, limit=20, clock=time.monotonic):
    """Bounded scan of dedicated folders. Never traverse a separate mount or link."""
    import heapq
    if cancelled.is_set():
        return [],False
    mountmap={target:(device,kind) for device,target,kind,_ in table}
    if '/' not in mountmap or mountmap['/'][1] not in LOCAL_FILE_SYSTEMS:
        return [],False
    local=[target for target,(device,kind) in mountmap.items()
           if device.startswith('/dev/') and kind in LOCAL_FILE_SYSTEMS
           and target.startswith(('/media/','/mnt/'))]
    roots=[]
    for target in sorted(local):
        roots.extend(target.rstrip('/')+'/'+suffix for suffix in ('movie','timeshift','picon','XPicons/picon','ZZPicons/picon','logs'))
    roots.extend(path for _,paths in CATEGORIES for path in paths)
    roots.extend(configured_picons(p,local))
    # Longest mount prefix determines ownership, including nested remote/bind mounts.
    def owner(path):
        return max((m for m in mountmap if m=='/' or path==m or path.startswith(m.rstrip('/')+'/')),key=len)
    def permitted(path):
        m=owner(path)
        return m=='/' or m in local
    deadline=clock()+seconds
    visited=0
    complete=True
    seen=set()
    heap=[]
    def stopped():
        return cancelled.is_set() or visited>=budget or clock()>=deadline
    def walk(node,relative,device,depth=0):
        nonlocal visited,complete
        if stopped():
            complete=False
            return False
        visited+=1
        try:
            info=node.lstat()
            if info.st_dev!=device or stat.S_ISLNK(info.st_mode):
                return True
            key=(info.st_dev,info.st_ino)
            if key in seen:
                return True
            if stat.S_ISREG(info.st_mode):
                seen.add(key)
                if relative.isprintable() and info.st_size>0:
                    item=(info.st_size,relative)
                    if len(heap)<limit:heapq.heappush(heap,item)
                    elif item>heap[0]:heapq.heapreplace(heap,item)
            elif stat.S_ISDIR(info.st_mode):
                seen.add(key)
                if depth>=32:
                    complete=False
                    return True
                with os.scandir(node) as children:
                    for child in children:
                        if stopped():
                            complete=False
                            return False
                        target=relative.rstrip('/')+'/'+child.name
                        if target in mountmap:continue
                        if not walk(node/child.name,target,device,depth+1):return False
        except FileNotFoundError:
            pass
        except OSError:
            complete=False
        return True
    if limit<=0:return [],False
    for path in dict.fromkeys(roots):
        if stopped():
            complete=False
            break
        if not permitted(path) or path in mountmap:continue
        node=p.path(path)
        try:
            # Inspect ancestors top-down. Do not stat through a symlink.
            chain=list(reversed(node.parents))
            if any(parent.is_symlink() for parent in chain+[node]):continue
            info=node.lstat()
            if info.st_dev!=p.path(owner(path)).lstat().st_dev:continue
        except FileNotFoundError:continue
        except OSError:
            complete=False
            continue
        if not walk(node,path,info.st_dev):break
    return sorted(heap,reverse=True),complete and not cancelled.is_set()


def largest_report(tr,cancelled,probe=None):
    p=probe or Probe()
    rows,complete=largest_files(p,mounts(p),cancelled)
    if cancelled.is_set():return ''
    lines=[tr('Selected local folders only')]
    if not complete:lines.append(tr('Partial result'))
    if not rows:lines.append(tr('Files')+'   '+('0' if complete else '—'))
    for size,path in rows:
        value='%.2f GiB'%(size/1073741824) if size>=1073741824 else '%.1f MiB'%(size/1048576) if size>=1048576 else '%d KiB'%max(1,(size+1023)//1024)
        lines.extend(('',value,path))
    return '\n'.join(lines)
