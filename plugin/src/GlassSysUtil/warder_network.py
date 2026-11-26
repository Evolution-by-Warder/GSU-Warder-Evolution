"""Local, read-only network overview; no probes or private configuration export."""
from pathlib import Path
from ipaddress import ip_address
import re
from .warder_tools import Probe

def collect(probe=None):
    p=probe or Probe()
    rows=[]
    for name in p.entries('/sys/class/net',64):
        if name=='lo' or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,32}',name):
            continue
        base='/sys/class/net/'+name
        state=p.text(base+'/operstate',32)
        speed=p.text(base+'/speed',32)
        rows.append(dict(name=name,state=state if state in ('up','down','unknown','dormant','lowerlayerdown','notpresent','testing') else 'unknown',
                         speed=int(speed) if speed.isdigit() and 0<int(speed)<=10000000 else None))
    gateways=[]
    for line in p.text('/proc/net/route',32768).splitlines()[1:]:
        fields=line.split()
        try:
            if len(fields)>=8 and fields[1]=='00000000' and fields[7]=='00000000' and int(fields[3],16)&2:
                address=ip_address(int.from_bytes(bytes.fromhex(fields[2]),'little'))
                gateways.append(str(address))
        except (ValueError,OverflowError):
            continue
    dns=[]
    for line in p.text('/etc/resolv.conf',16384).splitlines():
        fields=line.split()
        if len(fields)>=2 and fields[0]=='nameserver':
            try:dns.append(str(ip_address(fields[1])))
            except ValueError:pass
    return dict(interfaces=rows,gateways=list(dict.fromkeys(gateways)),dns=list(dict.fromkeys(dns)))

def summary(report,tr):
    rows=[]
    for item in report['interfaces']:
        speed=item['speed']
        rows.append(item['name']+' — '+tr({'up':'Running','down':'Unavailable'}.get(item['state'],'Not exposed'))+
                    (' · %s Mb/s'%speed if speed is not None else ''))
    rows += ['',tr('Default gateway')+': '+(', '.join(report['gateways']) or tr('Not exposed')),
             tr('DNS configuration')+': '+(', '.join(report['dns']) or tr('Not exposed'))]
    return '\n'.join(rows)


def local_addresses(name, probe):
    import socket
    import struct
    import fcntl
    result = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            raw = fcntl.ioctl(sock, 0x8915, struct.pack('256s', name.encode('ascii')[:15]))
            result.append(socket.inet_ntoa(raw[20:24]))
    except (OSError, ValueError):
        pass
    for line in probe.text('/proc/net/if_inet6', 8192).splitlines():
        fields = line.split()
        if len(fields) == 6 and fields[-1] == name:
            try:
                result.append(str(ip_address(bytes.fromhex(fields[0]))))
            except ValueError:
                pass
    return result


def ping(address, runner=None):
    import subprocess
    runner = runner or subprocess.run
    try:
        value = str(ip_address(address))
        res = runner(['ping', '-n', '-c', '3', '-W', '1', value], stdout=subprocess.PIPE,
                     stderr=subprocess.DEVNULL, timeout=5, text=True, env={'PATH':'/usr/sbin:/usr/bin:/sbin:/bin','LC_ALL':'C'})
    except (ValueError, OSError, subprocess.TimeoutExpired):
        return None
    loss = re.search(r'([\d.]+)%\s+packet loss', res.stdout)
    delay = re.search(r'(?:round-trip|rtt)[^=]*=\s*[\d.]+/([\d.]+)/', res.stdout)
    return (float(loss[1]), float(delay[1]) if delay else None) if loss else None


def diagnostics(tr, cancelled, probe=None, opener=None):
    from .plugin_update import MODERN_FEED_URL, _open, parse_release
    import time
    p = probe or Probe()
    data = collect(p)
    lines = []
    for row in data['interfaces']:
        addresses = local_addresses(row['name'], p)
        lines.append(row['name']+'   '+(', '.join(addresses) or '—'))
    gateway = next(iter(data['gateways']), None)
    response = ping(gateway) if gateway and not cancelled.is_set() else None
    lines.append(tr('Default gateway')+'   '+(gateway or '—'))
    if response:
        lines.append('%s   %.0f %%    ·    RTT   %s' % (tr('Packet loss'), response[0], '—' if response[1] is None else '%.1f ms'%response[1]))
    if cancelled.is_set():
        return ''
    start = time.monotonic()
    feed_online = False
    try:
        with (opener or _open)(MODERN_FEED_URL, timeout=4) as remote:
            if remote.geturl() != MODERN_FEED_URL:
                raise ValueError('redirect')
            payload = remote.read(65537)
            if len(payload) > 65536:
                raise ValueError('oversize')
            parse_release(payload, '13.41-r6', 'stable-modern')
        feed_online = True
        lines.append('GSU HTTPS   OK   %.0f ms' % ((time.monotonic()-start)*1000))
    except (OSError, ValueError):
        lines.append('GSU HTTPS   '+tr('Unavailable'))
    if cancelled.is_set():
        return ''
    official_site = 'https://warder-evolution.eu/'
    try:
        with (opener or _open)(official_site,timeout=4) as web:
            site_online = web.geturl()==official_site and bool(web.read(1))
    except (OSError,ValueError):
        site_online = False
    lines.append('warder-evolution.eu   '+('OK' if site_online else tr('Unavailable')))
    if feed_online or site_online:
        lines.append(tr('Internet reachable'))
    elif gateway and response and response[0] < 100:
        lines.append(tr('Gateway reachable; external checks failed'))
    elif data['interfaces'] and all(i['state']=='down' for i in data['interfaces']):
        lines.append(tr('No active link detected'))
    else:
        lines.append(tr('Not exposed'))
    table = p.text('/proc/mounts', 65536).splitlines()
    count = sum(1 for line in table if len(line.split()) > 2 and line.split()[2] in ('nfs','nfs4','cifs','smbfs','fuse.sshfs'))
    lines.append(tr('Network mounts')+'   '+str(count))
    return '\n'.join(lines)
