"""Local, read-only network overview; no probes or private configuration export."""
from ipaddress import ip_address
import re
from .warder_tools import Probe, unescape_mount

REMOTE_FS=frozenset(('nfs','nfs4','cifs','smbfs','fuse.sshfs'))

def collect(probe=None, include_addresses=False):
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
    result=dict(interfaces=rows,gateways=list(dict.fromkeys(gateways)),dns=list(dict.fromkeys(dns)))
    if include_addresses:
        for item in rows:item['addresses']=local_addresses(item['name'],p)
        result['network_mounts']=len(network_mounts(p))
    return result

def summary(report,tr):
    rows=[]
    for item in report['interfaces']:
        speed=item['speed']
        rows.append(item['name']+' — '+tr({'up':'Running','down':'Unavailable'}.get(item['state'],'Not exposed'))+
                    (' · %s Mb/s'%speed if speed is not None else ''))
        if 'addresses' in item:rows.append('    IP   '+(', '.join(item['addresses']) or '—'))
        rows.append('')
    rows += ['',tr('Default gateway')+': '+(', '.join(report['gateways']) or tr('Not exposed')),
             tr('DNS configuration')+': '+(', '.join(report['dns']) or tr('Not exposed'))]
    if 'network_mounts' in report:rows.append(tr('Network mounts')+': '+str(report['network_mounts']))
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
    count = len(network_mounts(p))
    lines.append(tr('Network mounts')+'   '+str(count))
    return '\n'.join(lines)


def overview_panels(report,tr):
    """Split real measured network data into interface and connection panels."""
    left=[]
    for item in report['interfaces']:
        state=tr({'up':'Running','down':'Unavailable'}.get(item['state'],'Not exposed'))
        left.append(item['name']+'  ·  '+state)
        speed=item['speed']
        if speed is not None:
            left.append('    %s Mb/s'%speed)
        left.extend('    '+address for address in item.get('addresses',()))
        left.append('')
    right=[tr('Default gateway'),*('    '+v for v in report['gateways'] or ['—']),
           '',tr('DNS configuration'),*('    '+v for v in report['dns'] or ['—'])]
    if 'network_mounts' in report:
        right.extend(('',tr('Network mounts'),'    '+str(report['network_mounts'])))
    return ('\n'.join(left).strip() or tr('Unavailable'),'\n'.join(right))


def network_mounts(p):
    """List local mount points only: never stat remote storage or expose credentials."""
    rows=[]
    for line in p.text('/proc/mounts',65536).splitlines():
        fields=line.split()
        if len(fields)>=4 and fields[2] in REMOTE_FS:
            target=unescape_mount(fields[1])
            if target.startswith('/') and target.isprintable():
                rows.append((target,fields[2],'ro' in fields[3].split(',')))
    return rows


def interface_details(p,row):
    base='/sys/class/net/'+row['name']
    mac=p.text(base+'/address',32)
    duplex=p.text(base+'/duplex',16).lower()
    carrier=p.text(base+'/carrier',8)
    wifi=None
    for line in p.text('/proc/net/wireless',8192).splitlines():
        name,sep,body=line.partition(':')
        if not sep or name.strip()!=row['name']:continue
        fields=body.split()
        try:
            quality,level,noise=(float(v.rstrip('.')) for v in fields[1:4])
            if all(-1000<=v<=1000 for v in (quality,level,noise)):
                wifi=(quality,level,noise)
        except (ValueError,TypeError):pass
        break
    return (mac if re.fullmatch(r'(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}',mac) else None,
            duplex if duplex in ('full','half') else None,
            int(carrier) if carrier in ('0','1') else None,wifi)


def interface_statistics(p):
    result={}
    for line in p.text('/proc/net/dev',32768).splitlines():
        name,sep,body=line.rpartition(':')
        name=name.strip()
        if not sep or name=='lo' or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,32}',name):continue
        try:fields=tuple(int(v) for v in body.split())
        except ValueError:continue
        if len(fields)>=16 and min(fields)>=0:
            result[name]=(fields[:4],fields[8:12])
    return result


def listening_ports(p):
    """Observed local socket tables, never a remote port scan or service attribution."""
    result={}
    for protocol in ('tcp','tcp6','udp','udp6'):
        raw=p.text('/proc/net/'+protocol,65536)
        if not raw:
            result[protocol]=None
            continue
        ports=set()
        for line in raw.splitlines()[1:]:
            fields=line.split()
            if len(fields)<4 or fields[3]!=('0A' if protocol.startswith('tcp') else '07'):continue
            try:port=int(fields[1].rsplit(':',1)[1],16)
            except (ValueError,IndexError):continue
            if 0<port<=65535:ports.add(port)
        result[protocol]=sorted(ports)
    return result


def detail_report(kind,tr,cancelled,probe=None):
    p=probe or Probe()
    if cancelled.is_set():return ''
    rows=[]
    if kind=='network-interfaces':
        data=collect(p,include_addresses=True)
        for item in data['interfaces']:
            if cancelled.is_set():return ''
            mac,duplex,carrier,wifi=interface_details(p,item)
            rows.extend((item['name']+'  ·  '+tr({'up':'Running','down':'Unavailable'}.get(item['state'],'Not exposed')),
                         'IP   '+(', '.join(item['addresses']) or '—'),
                         'MAC   '+(mac or '—'),
                         'Mb/s   '+(str(item['speed']) if item['speed'] is not None else '—'),
                         'Duplex   '+(duplex or '—'),
                         'Link   '+(str(carrier) if carrier is not None else '—')))
            if wifi is not None:
                rows.append('Wi-Fi   LQ %.0f   RSSI %.0f   Noise %.0f'%wifi)
            rows.append('')
    elif kind=='network-statistics':
        for name,(rx,tx) in sorted(interface_statistics(p).items()):
            if cancelled.is_set():return ''
            rows.extend((name,'RX   %.2f MiB   ·   %s %d'%(rx[0]/1048576,tr('Packets'),rx[1]),
                         '     %s %d   ·   %s %d'%(tr('Errors'),rx[2],tr('Dropped packets'),rx[3]),
                         'TX   %.2f MiB   ·   %s %d'%(tx[0]/1048576,tr('Packets'),tx[1]),
                         '     %s %d   ·   %s %d'%(tr('Errors'),tx[2],tr('Dropped packets'),tx[3]),''))
    elif kind=='network-mounts':
        for target,fs,readonly in network_mounts(p):
            rows.append(target+'   ·   '+fs+('   ·   '+tr('read-only') if readonly else ''))
        # Empty means no known remote mounts; absence of proc table is unknown.
        if not rows and p.text('/proc/mounts',65536):
            rows.append(tr('Network mounts')+'   0')
    elif kind=='network-services':
        from .warder_system_data import observed_services,PROTOCOLS
        rows.extend(name+'   '+(tr('Running') if state is True else tr('Not detected') if state is False else '—')
                    for name,state in zip(PROTOCOLS,observed_services(p)))
        rows.extend(('',tr('Local ports')))
        for protocol,ports in listening_ports(p).items():
            rows.append(protocol.upper()+'   '+('—' if ports is None else ', '.join(map(str,ports)) or '0'))
    else:raise ValueError('unknown network report')
    return '\n'.join(rows).strip() or tr('Unavailable')
