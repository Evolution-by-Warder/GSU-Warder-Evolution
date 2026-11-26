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


def smart(device, runner=subprocess.run):
    # Never wake a sleeping disk, start a self-test or change device settings.
    if not shutil.which('smartctl'):
        return None
    match = re.fullmatch(r'(/dev/sd[a-z]+)\d*|(/dev/nvme\d+n\d+)(?:p\d+)?', device)
    if not match:
        return None
    disk = match.group(1) or match.group(2)
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
    return (health.group(1).upper() if health else None, int(temperature.group(1)) if temperature else None)


def category_snapshot(probe=None,cancelled=None):
    p=probe or Probe()
    values=usage_categories(p,mounts(p),cancelled=cancelled)
    return [(name,*values.get(name,(0,False))) for name,_ in CATEGORIES]


def category_size(size,complete):
    if not size and not complete:return '—'
    # Small real lower bounds must not round to a misleading 0.0 MiB.
    value=('%d KiB'%max(1,size//1024)) if 0<size<104857 else '%.1f MiB'%(size/1048576)
    return ('' if complete else '≥ ')+value


def report(tr, detail=False, probe=None):
    p = probe or Probe()
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
        rows.append('')
        options = []
        smart_cache = {}
        for path, dev, fs, ro, usage in disks(p, table):
            rows.append('%s   ·   %s%s' % (path, fs, ' · '+tr('read-only') if ro else ''))
            if usage and usage.total>0:
                rows.append('    %s %.1f GiB    ·    %s %.1f GiB    ·    %s %.0f %%' % (tr('Total:'),usage.total/1073741824,tr('Free:'),usage.free/1073741824,tr('Used(%):'),100*(usage.total-usage.free)/usage.total))
            else:rows.append('    '+tr('Unavailable'))
            if (path.startswith('/media/') or path.startswith('/mnt/')) and not ro and usage and usage.free > 0:
                options.append((usage.free, path))
            if dev not in smart_cache and len(smart_cache) < 4:
                smart_cache[dev] = smart(dev)
            health = smart_cache.get(dev)
            if health and any(x is not None for x in health):
                rows.append('    SMART   %s   %s' % (health[0] or '—', '—' if health[1] is None else '%d °C' % health[1]))
            rows.append('')
        if options:
            rows.extend(('', tr('Picon storage')+'   '+max(options)[1]))
    return '\n'.join(rows) or tr('Unavailable')
