"""On-demand service checks and an explicit allowlist for shareable reports."""
import json
import re
import shutil
import tempfile
from . import install_health
from .warder_system_data import overview
from .warder_tools import Probe, read

# Each exported receiver value is a bounded number or an enumerated label.
def forum_snapshot(probe=None):
    import platform
    import sys
    from pathlib import Path
    p = probe or Probe()
    result = overview(p)
    memory = result.get('memory',{})
    arch = platform.machine().lower()
    arch = arch if arch in ('aarch64','armv7l','armv6l','mips','mipsel','mips64','mips64el','x86_64') else None
    version = read(Path(__file__).with_name('version'),64)
    values = {item['name']:round(item['available_percent'],1) if item['available_percent'] is not None else None
              for item in result['checks'] if item['name'] in ('RAM','Flash')}
    total, free = memory.get('swap_total'),memory.get('swap_free')
    if total and free is not None and 0<=free<=total:
        values['Swap'] = round(100*free/total,1)
    temperatures = p.temperatures(p.sensor_paths())
    return {'schema':2,'gsu':version if re.fullmatch(r'[0-9]+(?:\.[0-9]+){2}',version) else None,
            'python':list(sys.version_info[:2]),'architecture':arch,'available_percent':values,
            'temperature_c':max((s['celsius'] for s in temperatures),default=None),
            'crash_classes':crash_summary(p)}


def save_preview(preview, directory='/tmp'):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', prefix='gsu-forum-', suffix='.json',
                                     dir=directory, delete=False) as out:
        out.write(preview+'\n')
        return out.name


CRASH_ROOTS=('/home/root/logs','/media/hdd','/tmp')
CRASH_NAME=re.compile(r'(?:enigma2_crash|enigma2-crash)[\w.-]*\.log')
CRASH_SUGGESTIONS={'ModuleNotFoundError':'Check plugin dependencies', 'ImportError':'Check plugin dependencies',
                   'MemoryError':'Review memory and storage', 'PermissionError':'Check file permissions',
                   'FileNotFoundError':'Check installed files', 'AttributeError':'Check image compatibility',
                   'TypeError':'Check image compatibility'}


def crash_exception(text):
    # Only disclose exception classes from the Python built-in namespace.
    import builtins
    matches=re.findall(r'^([A-Za-z]+(?:Error|Exception))(?::|$)',text,re.M)
    name=matches[-1] if matches else None
    kind=getattr(builtins,name,None) if name else None
    return name if isinstance(kind,type) and issubclass(kind,Exception) else None


def crash_files(p):
    """Bounded candidates on local mounts; do not browse remote shares."""
    from .warder_storage import mounts,REMOTE
    remote=tuple(target.rstrip('/')+'/' for _,target,fs,_ in mounts(p) if fs in REMOTE)
    for root in CRASH_ROOTS:
        if any((root.rstrip('/')+'/').startswith(target) for target in remote):continue
        for name in p.entries(root,256):
            if CRASH_NAME.fullmatch(name):
                yield p.path(root)/name


def crash_summary(p):
    exceptions=[]
    for path in crash_files(p):
        name=crash_exception(read(path,32768,private_log=True))
        if name:exceptions.append(name)
        if len(exceptions)>=5:break
    return exceptions


def crash_inventory(cancelled,probe=None):
    """Bounded, most recent local regular crash files, shared by both views."""
    import stat
    p=probe or Probe()
    candidates=[]
    for path in crash_files(p):
        if cancelled.is_set():return []
        try:
            st=path.lstat()
            if stat.S_ISREG(st.st_mode):
                candidates.append((st.st_mtime,st.st_size,path,(st.st_dev,st.st_ino,st.st_mtime_ns,st.st_size)))
        except OSError:continue
    return sorted(candidates,key=lambda item:(-item[0],str(item[2])))[:10]


def crash_report(tr,cancelled,probe=None):
    """Local, bounded recent crash summaries. Raw log text is not exported."""
    from datetime import datetime
    rows=[]
    for timestamp,size,path,identity in crash_inventory(cancelled,probe):
        if cancelled.is_set():return ''
        name=crash_exception(read(path,32768,private_log=True))
        try:stamp=datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except (OverflowError,OSError,ValueError):stamp='—'
        rows.extend((path.name,stamp+'   ·   %.1f KiB'%(size/1024),name or '—'))
        if name in CRASH_SUGGESTIONS:rows.append(tr(CRASH_SUGGESTIONS[name]))
        rows.append('')
    return '\n'.join(rows).strip() or tr('Unavailable')


def health(tr, p=None):
    p = p or Probe()
    try:
        result = install_health.verify_files()
        integrity=tr('Ready')+' · '+result
    except (OSError, ValueError, TypeError):
        integrity=tr('Warning')+' · '+tr('Check installed files')
    packages = [cmd for cmd in ('opkg', 'apt', 'dpkg-query') if shutil.which(cmd)]
    from .warder_package_status import database, dependency_state
    records, manager = database(p.path('/'))
    dependencies = dependency_state(install_health.PACKAGE,records,manager)
    exceptions = crash_summary(p)
    suggestions = [tr(CRASH_SUGGESTIONS[name]) for name in dict.fromkeys(exceptions) if name in CRASH_SUGGESTIONS]
    return '\n\n'.join(('GSU   '+integrity, tr('Package manager')+'\n    '+(', '.join(packages) or '—'),
                      tr('Package dependencies')+'\n    '+tr(dependencies), tr('Crash logs')+'\n    '+(', '.join(exceptions) or '—'), *dict.fromkeys(suggestions)))


def format_preview(raw,tr):
    """Readable local preview of every field in the exact saved allowlisted JSON."""
    value=json.loads(raw)
    keys={'schema','gsu','python','architecture','available_percent','temperature_c','crash_classes'}
    if not isinstance(value,dict) or set(value)!=keys:
        return raw  # Never hide unknown fields from the person reviewing the export.
    def shown(v):
        return '—' if v is None else str(v)
    rows=['GSU    '+shown(value['gsu']),
          'Python    '+'.'.join(map(str,value['python'])),
          tr('Architecture')+'    '+shown(value['architecture']),
          'schema    '+shown(value['schema']),'',
          tr('Available memory')+' / Flash']
    for name,percent in value['available_percent'].items():
        rows.append('    %s    %s'%(tr(name),'—' if percent is None else '%.1f %%'%percent))
    rows.extend(('',tr('Temperature')+'    '+('—' if value['temperature_c'] is None else '%.1f °C'%value['temperature_c']),
                 '',tr('Crash logs'), '    '+(', '.join(value['crash_classes']) or '—')))
    return '\n'.join(rows)


def crash_detail(path,identity,tr,cancelled,probe=None):
    """Selected local crash tail only, recheck inventory and identity, redact secrets."""
    import os,stat
    from .warder_tools import redact
    p=probe or Probe()
    if cancelled.is_set():return ''
    if not any(candidate==path and current==identity for _,_,candidate,current in crash_inventory(cancelled,p)):
        return tr('Unavailable')
    try:
        fd=os.open(path,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
        try:
            st=os.fstat(fd)
            if not stat.S_ISREG(st.st_mode) or (st.st_dev,st.st_ino,st.st_mtime_ns,st.st_size)!=identity:
                return tr('Unavailable')
            limit=32768
            if st.st_size>limit:os.lseek(fd,-limit,os.SEEK_END)
            raw=os.read(fd,limit)
            final=os.fstat(fd)
            if (final.st_dev,final.st_ino,final.st_mtime_ns,final.st_size)!=identity or b'\x00' in raw:
                return tr('Unavailable')
        finally:os.close(fd)
    except OSError:return tr('Unavailable')
    if cancelled.is_set():return ''
    text=raw.decode('utf-8','replace')
    name=crash_exception(text)
    lines=[path.name]
    if name:lines.append(name)
    if name in CRASH_SUGGESTIONS:lines.append(tr(CRASH_SUGGESTIONS[name]))
    if st.st_size>limit:lines.append(tr('Partial result')+' · 32 KiB')
    lines.extend(('',redact(text)))
    return '\n'.join(lines)
