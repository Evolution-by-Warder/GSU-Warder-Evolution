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


def crash_summary(p):
    roots = ('/home/root/logs', '/media/hdd', '/tmp')
    # Only disclose exception classes from the Python built-in namespace.
    import builtins
    allowed = {k for k, v in vars(builtins).items() if isinstance(v, type) and issubclass(v, Exception)}
    exceptions = []
    for root in roots:
        for name in p.entries(root, 256):
            if not re.fullmatch(r'(?:enigma2_crash|enigma2-crash)[\w.-]*\.log', name):
                continue
            path = p.path(root) / name
            text = read(path, 32768, private_log=True)
            matches = re.findall(r'^([A-Za-z]+(?:Error|Exception))(?::|$)', text, re.M)
            exceptions.extend(cls for cls in matches[-1:] if cls in allowed)
            if len(exceptions) >= 5:
                return exceptions
    return exceptions


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
    messages = {'ModuleNotFoundError':'Check plugin dependencies', 'ImportError':'Check plugin dependencies',
                'MemoryError':'Review memory and storage', 'PermissionError':'Check file permissions',
                'FileNotFoundError':'Check installed files', 'AttributeError':'Check image compatibility',
                'TypeError':'Check image compatibility'}
    suggestions = [tr(messages[name]) for name in dict.fromkeys(exceptions) if name in messages]
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
