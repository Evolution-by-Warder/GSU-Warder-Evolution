"""Read-only, bounded system overview and on-demand detail collection."""
from .warder_tools import Probe
from .warder_telemetry import memory_values
from .warder_health import resource_check, health_summary
import subprocess

def overview(probe=None):
    p=probe or Probe()
    memory=memory_values(p.text('/proc/meminfo',16384))
    checks=[resource_check('RAM',memory['ram_total'],memory['ram_available'])]
    try:
        disk=p.usage(p.path('/'))
        checks.append(resource_check('Flash',disk.total,disk.free,warning=10,critical=5))
    except OSError:
        checks.append(resource_check('Flash',None,None))
    return {'memory':memory,'checks':checks,'health':health_summary(checks)}

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
