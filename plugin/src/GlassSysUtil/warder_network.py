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
             tr('DNS configuration')+': '+(', '.join(report['dns']) or tr('Not exposed')),'',
             tr('This is a read-only check. Internet access, disk integrity and CAM decoding are not tested.')]
    return '\n'.join(rows)
