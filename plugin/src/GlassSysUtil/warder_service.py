"""On-demand service checks and an explicit allowlist for shareable reports."""
import json
import re
import shutil
import tempfile
from . import install_health
from .warder_system_data import overview
from .warder_tools import Probe, read

# Export only schema-defined numeric resource values. No strings from the receiver.
def forum_snapshot(probe=None):
    result = overview(probe or Probe())
    return {'schema': 1, 'available_percent': {
        item['name']: round(item['available_percent'], 1) if item['available_percent'] is not None else None
        for item in result['checks'] if item['name'] in ('RAM', 'Flash')}}


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
    except (OSError, ValueError, TypeError):
        result = tr('Warning')
    packages = [cmd for cmd in ('opkg', 'apt', 'dpkg-query') if shutil.which(cmd)]
    exceptions = crash_summary(p)
    messages = {'ModuleNotFoundError':'Check plugin dependencies', 'ImportError':'Check plugin dependencies',
                'MemoryError':'Review memory and storage', 'PermissionError':'Check file permissions',
                'FileNotFoundError':'Check installed files', 'AttributeError':'Check image compatibility',
                'TypeError':'Check image compatibility'}
    suggestions = [tr(messages[name]) for name in dict.fromkeys(exceptions) if name in messages]
    return '\n'.join(('GSU   '+result, tr('Package manager')+'   '+(', '.join(packages) or '—'),
                      tr('Crash logs')+'   '+(', '.join(exceptions) or '—'), *dict.fromkeys(suggestions)))
