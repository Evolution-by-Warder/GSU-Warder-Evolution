"""Selected Warder w19 diagnostics, adapted to isolated read-only collection."""
import argparse
import io
import json
import os
from pathlib import Path
import platform
import re
import shutil
import socket
import stat
import struct
import subprocess
import tarfile
import tempfile
import time

MAX_REPORT=1024*1024
LOG_LIMIT=32768


def read(path,limit=16384,private_log=False):
    flags=os.O_RDONLY|os.O_NONBLOCK
    if private_log:flags|=os.O_NOFOLLOW
    try:
        fd=os.open(path,flags)
        try:
            info=os.fstat(fd)
            if not stat.S_ISREG(info.st_mode):return ''
            if private_log and info.st_size>limit:os.lseek(fd,-limit,os.SEEK_END)
            raw=os.read(fd,limit)
            return '' if b'\0' in raw else raw.decode('utf-8','replace').strip()
        finally:os.close(fd)
    except OSError:return ''


def names(path,limit=256):
    try:return sorted(os.listdir(path))[:limit]
    except OSError:return []


def unescape_mount(value):
    return re.sub(r'\\([0-7]{3})',lambda match:chr(int(match[1],8)),value)


class Probe:
    def __init__(self,root='/',usage=shutil.disk_usage):
        self.root=Path(root);self.usage=usage

    def path(self,path):return self.root/path.lstrip('/')
    def text(self,path,limit=16384):return read(self.path(path),limit)
    def entries(self,path,limit=256):return names(self.path(path),limit)

    def collect(self):
        memory={}
        for line in self.text('/proc/meminfo').splitlines():
            key,separator,value=line.partition(':')
            parts=value.split()
            if separator and parts and parts[0].isdigit():memory[key]=int(parts[0])
        processes=[]
        for pid in self.entries('/proc',8192):
            if not pid.isdigit():continue
            name=self.text('/proc/'+pid+'/comm',128)
            state=next((line.split(':',1)[1].strip().split()[0] for line in self.text('/proc/'+pid+'/status',4096).splitlines() if line.startswith('State:') and line.split(':',1)[1].strip()),'?')
            if name and state not in ('Z','X','x'):
                processes.append({'pid':int(pid),'name':name,'state':state})
        disks=[];network_mounts=0;seen=set()
        for line in self.text('/proc/mounts',65536).splitlines():
            parts=line.split()
            if len(parts)<4:continue
            device,target,kind,options=parts[:4];target=unescape_mount(target)
            if kind in ('nfs','nfs4','cifs','smbfs'):network_mounts+=1;continue
            if (not device.startswith('/dev/') and target!='/') or target in seen:continue
            if kind in ('squashfs','cramfs','iso9660'):continue
            seen.add(target)
            record={'mount':target,'filesystem':kind,'readonly':'ro' in options.split(',')}
            try:
                usage=self.usage(self.path(target))
                record.update(total=usage.total,free=usage.free)
            except OSError:record['unavailable']=True
            disks.append(record)
        interfaces=[{'name':name,'state':self.text('/sys/class/net/'+name+'/operstate',32) or 'unknown'} for name in self.entries('/sys/class/net') if name!='lo']
        gateway=''
        for line in self.text('/proc/net/route').splitlines()[1:]:
            fields=line.split()
            try:
                if len(fields)>3 and fields[1]=='00000000' and int(fields[3],16)&2:
                    gateway=socket.inet_ntoa(struct.pack('<I',int(fields[2],16)));break
            except (ValueError,struct.error):continue
        dns=[fields[1] for line in self.text('/etc/resolv.conf').splitlines() if len(fields:=line.split())>=2 and fields[0]=='nameserver']
        sensors=[]
        for zone in self.entries('/sys/class/thermal'):
            if zone.startswith('thermal_zone'):sensors.append(('/sys/class/thermal/'+zone+'/temp','/sys/class/thermal/'+zone+'/type'))
        for monitor in self.entries('/sys/class/hwmon'):
            base='/sys/class/hwmon/'+monitor
            for name in self.entries(base):
                if name.startswith('temp') and name.endswith('_input'):sensors.append((base+'/'+name,base+'/'+name[:-6]+'_label'))
        sensors.extend([('/proc/stb/sensors/temp0/value',''),('/proc/stb/fp/temp_sensor','')])
        temperatures=[];seen=set()
        for path,label in sensors[:128]:
            try:
                value=float(self.text(path,64))
                if abs(value)>=1000:value/=1000
                real=str(self.path(path).resolve())
                if not -20<=value<=150 or real in seen:continue
                seen.add(real);temperatures.append({'label':self.text(label,128) if label else path,'celsius':value})
            except (ValueError,OSError,RuntimeError):continue
        settings={}
        for line in self.text('/etc/enigma2/settings',1024*1024).splitlines():
            key,separator,value=line.partition('=')
            if separator and key in ('config.plugins.GlassSysUtil.par48','config.plugins.GlassSysUtil.par50','config.plugins.GlassSysUtil.par57','config.plugins.GlassSysUtil.par58'):
                if re.fullmatch(r'True|False|\d{1,6}',value):settings[key.rsplit('.',1)[1]]=value
        settings.setdefault('par50','True')
        guard=None
        try:
            value=json.loads(self.text('/run/gsu-softcam-session.json',4096)).get('enabled')
            if type(value) is bool:guard=value
        except (ValueError,TypeError,AttributeError):pass
        image={}
        for line in self.text('/usr/lib/enigma.info').splitlines():
            key,separator,value=line.partition('=')
            if separator and key.strip() in ('distro','oe','architecture','imageversion','machinebuild','boxtype','brand','model'):
                image[key.strip()]=value.strip().strip("'\"")[:256]
        native_selected=''
        try:native_selected=os.path.basename(os.readlink(self.path('/etc/init.d/softcam')))
        except OSError:pass
        return {'schema':1,'generated':time.strftime('%Y-%m-%d %H:%M:%S %z'),
                'version':read(Path(__file__).with_name('version'),128),
                'system':{'python':platform.python_version(),'machine':platform.machine(),'kernel':platform.release(),'image':image},
                'memory':memory,'disks':disks,'interfaces':interfaces,'gateway':gateway,'dns':dns,
                'temperatures':temperatures,'network_mounts':network_mounts,
                'tuners':self.text('/proc/bus/nim_sockets',8192),'dvb_interfaces':self.entries('/sys/class/dvb'),
                'processes':processes,'selected_cam':native_selected,'gsu_settings':settings,'autocheck_guard_enabled':guard}


def summary(report,translate=lambda value:value):
    tr=translate;rows=[tr('System health check'),'']
    def row(state,label,value):rows.append('[%s] %s: %s' % (tr(state),tr(label),value))
    memory=report['memory'];total=memory.get('MemTotal',0);available=memory.get('MemAvailable')
    if total and available is not None:
        percent=available*100/total;row('OK' if percent>=15 else 'Warning','Available memory','%.1f%% (%s MiB)' % (percent,available//1024))
    else:row('Info','Available memory',tr('Not exposed'))
    if not report['disks']:row('Info','Storage',tr('Not exposed'))
    for disk in report['disks']:
        total=disk.get('total',0)
        if not total:row('Info','Storage',disk['mount']+' — '+tr('Unavailable'));continue
        percent=disk['free']*100/total
        detail='%s — %.1f%% (%s MiB) %s' % (disk['mount'],percent,disk['free']//1048576,tr('free'))
        if disk['readonly']:detail+='; '+tr('read-only')
        row('Warning' if percent<5 or disk['readonly'] else 'OK','Storage',detail)
    up=[item['name'] for item in report['interfaces'] if item['state']=='up']
    down=bool(report['interfaces']) and all(item['state'] in ('down','lowerlayerdown','notpresent') for item in report['interfaces'])
    row('OK' if up else 'Warning' if down else 'Info','Network link',', '.join(up) or tr('No active link detected'))
    row('Info','Default gateway',report['gateway'] or tr('Not exposed'))
    row('OK' if report['dns'] else 'Info','DNS configuration',', '.join(report['dns']) or tr('Not exposed'))
    running=any(item['name']=='enigma2' for item in report['processes'])
    row('OK' if running else 'Warning','Enigma2',tr('Running' if running else 'Not detected'))
    cams=sorted({item['name'] for item in report['processes'] if item['name'].lower().startswith(('oscam','ncam','cccam','doscam','mgcamd','wicardd','gbox','mbox'))})
    row('Info','CAM',', '.join(cams) or tr('No known CAM process detected'))
    if report['temperatures']:
        hottest=max(item['celsius'] for item in report['temperatures'])
        row('Info','Temperature','%.1f °C' % hottest)
    else:row('Info','Temperature',tr('Not exposed'))
    row('Info','Network mounts',str(report['network_mounts']))
    row('Info','Tuner interfaces',tr('Detected' if report['tuners'] or report['dvb_interfaces'] else 'Not exposed'))
    rows+=['',tr('This is a read-only check. Internet access, disk integrity and CAM decoding are not tested.')]
    return '\n'.join(rows)


def redact(value):
    value=re.sub(r'(?i)([a-z][a-z0-9+.-]*://)[^\s/@]+@',r'\1<redacted>@',value)
    value=re.sub(r'(?i)(--(?:password|passwd|token|guard)(?:=|\s+))\S+',r'\1<redacted>',value)
    pattern=r'(?i)\b(?:password|passwd|pwd|httpuser|httppwd|username|user|token|authorization|cookie|rsakey|boxkey|deskey|secret|serial(?:_number)?|uuid|machine-id|cw)\s*[:=]'
    value='\n'.join(re.sub(pattern+r'.*',lambda m:m[0].split(':',1)[0].split('=',1)[0]+': <redacted>',line) for line in value.splitlines())
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]','',value)


def write_bundle(report,directory='/tmp',logs=None):
    if logs is None:logs={'softcam-autostart.log':'/tmp/gsu-softcam-autostart.log','bitrate.log':'/tmp/gsu-bitrate.log'}
    def sanitized(value):
        if isinstance(value,dict):return {key:sanitized(item) for key,item in value.items()}
        if isinstance(value,list):return [sanitized(item) for item in value]
        return redact(value) if isinstance(value,str) else value
    entries={'README.txt':'GSU Warder diagnostics\nRead-only snapshot; no account/configuration files or full crash logs.\nLAN gateway/DNS, interface names and process names are included.\n',
             'health.txt':summary(report),'report.json':json.dumps(sanitized(report),ensure_ascii=False,indent=2)}
    for name,path in logs.items():
        if not re.fullmatch(r'[a-z0-9-]+\.log',name):raise ValueError('Invalid diagnostic log name')
        content=read(path,LOG_LIMIT,private_log=True)
        if content:entries[name]=content
    entries={name:(content if name=='report.json' else redact(content)).encode('utf-8') for name,content in entries.items()}
    if sum(map(len,entries.values()))>MAX_REPORT:raise ValueError('Diagnostic report is too large')
    fd,path=tempfile.mkstemp(prefix='gsu-diagnostics-'+time.strftime('%Y%m%d-%H%M%S')+'-',suffix='.tar.gz',dir=directory)
    try:
        with os.fdopen(fd,'wb') as stream,tarfile.open(fileobj=stream,mode='w:gz') as archive:
            for name,content in entries.items():
                member=tarfile.TarInfo(name);member.size=len(content);member.mode=0o600
                archive.addfile(member,io.BytesIO(content))
        return {'path':path,'bytes':os.path.getsize(path)}
    except BaseException:
        Path(path).unlink(missing_ok=True);raise


def run_task(kind,runner=subprocess.run):
    if kind not in ('health','bundle'):raise ValueError('Unknown tool')
    result=runner([shutil.which('python3') or '/usr/bin/python3',str(Path(__file__)),'--collect'],
                  stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=20,check=False)
    if result.returncode:raise OSError('Diagnostic collection failed')
    if len(result.stdout.encode('utf-8'))>MAX_REPORT:raise ValueError('Diagnostic report is too large')
    report=json.loads(result.stdout)
    if not isinstance(report,dict) or report.get('schema')!=1:raise ValueError('Invalid diagnostic report')
    return report if kind=='health' else write_bundle(report)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--collect',action='store_true',required=True);parser.parse_args()
    print(json.dumps(Probe().collect(),ensure_ascii=False))
