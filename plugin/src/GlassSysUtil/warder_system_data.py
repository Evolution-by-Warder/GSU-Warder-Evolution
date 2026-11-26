"""Read-only, bounded system overview and on-demand detail collection."""
from .warder_tools import Probe
from .warder_telemetry import memory_values
from .warder_health import resource_check, health_summary
import subprocess

def overview(probe=None):
    p=probe or Probe()
    memory=memory_values(p.text('/proc/meminfo',16384))
    checks=[resource_check('RAM',memory['ram_total'],memory['ram_available'])]
    disk=None
    try:
        disk=p.usage(p.path('/'))
        checks.append(resource_check('Flash',disk.total,disk.free,warning=10,critical=5))
    except OSError:
        checks.append(resource_check('Flash',None,None))
    return {'memory':memory,'checks':checks,'health':health_summary(checks),'flash_usage':disk}

def processes(probe=None):
    p=probe or Probe()
    rows=[]
    for pid in p.entries('/proc',8192):
        if not pid.isdigit():continue
        name=p.text('/proc/'+pid+'/comm',128)
        if not name:continue
        status=p.text('/proc/'+pid+'/status',8192)
        state='?';rss=None
        for line in status.splitlines():
            key,sep,value=line.partition(':')
            fields=value.split()
            if not sep or not fields:continue
            if key=='State':state=fields[0]
            elif key=='VmRSS' and len(fields)==2 and fields[1]=='kB' and fields[0].isdigit():
                rss=int(fields[0])
        # Do not read command lines or environment variables.
        rows.append((int(pid),name.replace('\n',' ').replace('\r',' '),state,rss))
    return sorted(rows,key=lambda row:(-(row[3] or 0),row[0]))

def system_log(runner=subprocess.run):
    """Local display only; never included in diagnostic export."""
    result=runner(['dmesg'],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                  timeout=5,check=False)
    if result.returncode!=0:return None
    return result.stdout[-65536:].decode('utf-8','replace').replace('\x00','')

def detail_text(kind, tr):
    if kind=='processes':
        rows=processes()
        if not rows:return tr('Unavailable')
        return 'PID   '+tr('Process Info')+'   RSS (KiB)\n\n'+'\n'.join(
            '%s   %s   %s   %s'%(pid,name,state,rss if rss is not None else '—')
            for pid,name,state,rss in rows)
    if kind=='log':
        try:return system_log() or tr('Unavailable')
        except (OSError,subprocess.TimeoutExpired):return tr('Unavailable')
    raise ValueError('unknown system detail')


def process_ticks(p, pid):
    value = p.text('/proc/%d/stat' % pid, 4096)
    # comm is enclosed in parentheses and can itself contain a closing parenthesis.
    _, sep, tail = value.rpartition(')')
    fields = tail.split()
    try:
        if sep and len(fields) >= 20:
            return int(fields[19]), int(fields[11])+int(fields[12])
    except ValueError:
        pass
    return None


def cpu_processes(tr, cancel, p=None):
    import os
    from time import monotonic
    p = p or Probe()
    rows = processes(p)
    before = {pid: process_ticks(p, pid) for pid, _, _, _ in rows}
    started = monotonic()
    if cancel.wait(0.5):
        return ''
    hz = os.sysconf('SC_CLK_TCK')
    delta = (monotonic()-started)*hz
    measured = []
    for pid, name, state, rss in rows:
        old, new = before[pid], process_ticks(p, pid)
        if old and new and old[0] == new[0] and new[1] >= old[1] and delta > 0:
            measured.append((100*(new[1]-old[1])/delta, pid, name, rss))
    return 'CPU (%)    PID    RSS (KiB)\n\n'+'\n'.join(
        '%5.1f    %d    %s    %s' % (cpu, pid, rss if rss is not None else '—', name)
        for cpu, pid, name, rss in sorted(measured, key=lambda r: (-r[0], r[1]))) if measured else tr('Unavailable')


def process_table(cancel, cpu_order=False, p=None):
    """Return measured columns; keep processes with unavailable CPU measurements."""
    import os
    from time import monotonic
    p=p or Probe()
    rows=processes(p)
    before={pid:process_ticks(p,pid) for pid,_,_,_ in rows}
    started=monotonic()
    if cancel.wait(0.5):return []
    try:elapsed=(monotonic()-started)*os.sysconf('SC_CLK_TCK')
    except (OSError,ValueError,TypeError):elapsed=0
    result=[]
    for pid,name,state,rss in rows:
        old,new=before[pid],process_ticks(p,pid)
        cpu=None
        if old and new and old[0]==new[0] and new[1]>=old[1] and elapsed>0:
            cpu=100*(new[1]-old[1])/elapsed
        result.append((pid,name,state,rss,cpu))
    column=4 if cpu_order else 3
    return sorted(result,key=lambda row:(row[column] is None,-(row[column] or 0),row[0]))


def dashboard(cancel, p=None):
    from .warder_live import Sampler
    from .warder_storage import mounts, disks
    p = p or Probe()
    report = overview(p)
    sampler = Sampler(p)
    sampler.sample()
    if cancel.wait(0.25):
        return None
    live = sampler.sample()
    local = disks(p, mounts(p))
    selected = [(path,usage,device) for path, device, _, _, usage in local if path != '/' and usage and (path.startswith('/media/') or path.startswith('/mnt/'))]
    best=max(selected,key=lambda item:item[1].free,default=None)
    flash = report['checks'][1]['available_percent']
    # List separate mount capacities. Bind mounts can otherwise double-count the same device.
    return {'health':report['health'], 'basis':report['memory']['ram_basis'],
            'disk_mount':best[0] if best else None,
            'temperature_source':sampler.temperature_source,
            'memory':report['memory'],'flash_usage':report['flash_usage'],
            'disk_usage':best[1] if best else None,'disk_device':best[2] if best else None,
            'values':(live['cpu'], live['ram'], live['swap'], flash,
                      best[1].free if best else None, live['temp'])}


PROTOCOLS=('FTP','Telnet','VPN','Samba','NFS')


def observed_services(p):
    """Local daemon observations, not a connectivity or authentication test."""
    names=set()
    for pid in p.entries('/proc',8192):
        if pid.isdigit():
            name=p.text('/proc/'+pid+'/comm',128).strip().lower()
            if name:names.add(name)
    patterns=(('vsftpd','proftpd','pure-ftpd','ftpd'),('telnetd','in.telnetd'),
              ('openvpn','wireguard','wg-quick'),('smbd','nmbd'),('nfsd','rpc.mountd','mountd'))
    return tuple(any(n in names for n in group) if names else None for group in patterns)


def information(cancel, p=None):
    from .warder_storage import smart
    p=p or Probe()
    result=dashboard(cancel,p)
    if result is None or cancel.is_set():return None
    result['services']=observed_services(p)
    result['disk_temperature']=None
    if result['disk_device'] and not cancel.is_set():
        status=smart(result['disk_device'])
        if status:result['disk_temperature']=status[1]
    return None if cancel.is_set() else result
