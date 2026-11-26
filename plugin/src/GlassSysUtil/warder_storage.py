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
    ('Picons', ('/usr/share/enigma2/picon', '/picon')),
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


def usage_categories(p, table, budget=20000, seconds=3, clock=time.monotonic):
    deadline = clock()+seconds
    boundaries = {target for _, target, _, _ in table if target != '/'}
    local = [target for device, target, kind, _ in table
             if device.startswith('/dev/') and target.startswith('/media/') and kind not in REMOTE]
    roots = {label: list(paths) for label, paths in CATEGORIES}
    for target in local:
        for label, suffix in [('Picons', 'picon'), ('EPG', 'epg.dat'), ('Logs', 'logs')]:
            roots[label].append(target.rstrip('/')+'/'+suffix)
    totals, seen, visited = {}, set(), 0
    exhausted = False
    for label, paths in roots.items():
        size, complete = 0, not exhausted
        for path in paths:
            # Reject symlinked path components as well as a symlink at the root.
            raw = p.path(path)
            if any(parent.is_symlink() for parent in (raw, *raw.parents)):
                continue
            if any((path == mount or path.startswith(mount+'/')) for _, mount, fs, _ in table if fs in REMOTE):
                continue
            pending = [raw]
            while pending:
                if visited >= budget or clock() >= deadline:
                    complete, exhausted = False, True
                    break
                node = pending.pop()
                visited += 1
                try:
                    info = node.lstat()
                    key = (info.st_dev, info.st_ino)
                    if key in seen or stat.S_ISLNK(info.st_mode):
                        continue
                    seen.add(key)
                    if stat.S_ISREG(info.st_mode):
                        size += info.st_blocks * 512
                    elif stat.S_ISDIR(info.st_mode):
                        with os.scandir(node) as children:
                            for child in children:
                                if visited+len(pending) >= budget or clock() >= deadline:
                                    complete = False
                                    break
                                if ('/' + str(node.relative_to(p.root)/child.name)) not in boundaries:
                                    pending.append(node/child.name)
                except FileNotFoundError:
                    continue
                except OSError:
                    complete = False
            if exhausted:
                break
        totals[label] = size, complete
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


def category_snapshot(probe=None):
    p=probe or Probe()
    values=usage_categories(p,mounts(p))
    return [(name,*values.get(name,(0,False))) for name,_ in CATEGORIES]


def report(tr, detail=False, probe=None):
    p = probe or Probe()
    table = mounts(p)
    rows = []
    if detail:
        for label, (size, complete) in usage_categories(p, table).items():
            rows.append('%s   %.1f MiB%s' % (tr(label), size/1048576, '' if complete else ' · '+tr('Partial result')))
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
            if path.startswith('/media/') and not ro and usage and usage.free > 0:
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
