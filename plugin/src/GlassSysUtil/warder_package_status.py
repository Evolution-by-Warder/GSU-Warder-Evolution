"""Read the installed package database on demand. Never invoke a package transaction."""
import re
import subprocess
from pathlib import Path

DATABASES = ('/var/lib/opkg/status', '/usr/lib/opkg/status','/var/lib/dpkg/status')
NAME = re.compile(r'[a-z0-9][a-z0-9+.-]*\Z')
RELATION = re.compile(r'([a-z0-9][a-z0-9+.-]*)(?::(?:native|any))?(?:\s*\((<<|<=|=|>=|>>)\s*([^()\s]+)\))?\Z')
LIMIT = 16 * 1024 * 1024


def database(root=Path('/')):
    for location in DATABASES:
        path = root / location.lstrip('/')
        records = {}
        try:
            with path.open('rb') as stream:
                if path.stat().st_size > LIMIT:
                    continue
                fields = {}
                consumed = 0
                while True:
                    line = stream.readline(65536)
                    consumed += len(line)
                    if consumed > LIMIT or (len(line)==65536 and not line.endswith(b'\n')):
                        records.clear()
                        break
                    if line.strip():
                        key, sep, value = line.decode('utf-8','replace').partition(': ')
                        if sep and key in ('Package','Status','Version','Depends','Pre-Depends','Provides','Architecture'):
                            fields[key] = value.strip()
                        continue
                    state = fields.get('Status','').split()
                    if len(state)==3 and state[-1]=='installed' and state[1] in ('ok','user') and NAME.fullmatch(fields.get('Package','')):
                        records[fields['Package']] = fields
                    fields = {}
                    if not line:
                        break
        except OSError:
            continue
        if records:
            return records, 'dpkg' if '/dpkg/' in location else 'opkg'
    return {}, None


def compare_versions(manager,installed,operator,required):
    args = [manager, '--compare-versions' if manager=='dpkg' else 'compare-versions',
            installed, operator, required]
    try:
        status = subprocess.run(args,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=1).returncode
    except (OSError,subprocess.TimeoutExpired):
        return None
    return status==0 if status in (0,1) else None


def dependency_state(package, records, manager, compare=compare_versions):
    fields = records.get(package)
    if not fields or not manager:
        return 'Unavailable'
    provides = {row.strip().split(' ')[0] for entry in records.values()
                for row in entry.get('Provides','').split(',') if row.strip()}
    unknown = False
    remaining = 6
    for group in ','.join((fields.get('Pre-Depends',''),fields.get('Depends',''))).split(','):
        if not group.strip():
            continue
        candidates = []
        for alternative in group.split('|'):
            found = RELATION.fullmatch(alternative.strip())
            if not found:
                candidates.append(None)
                continue
            name, operator, version = found.groups()
            if name not in records:
                candidates.append((None if operator else True) if name in provides else False)
            elif not operator:
                candidates.append(True)
            elif remaining:
                remaining -= 1
                candidates.append(compare(manager,records[name].get('Version',''),operator,version))
            else:
                candidates.append(None)
        if True in candidates:
            continue
        if None in candidates:
            unknown = True
        else:
            return 'Check plugin dependencies'
    return 'Unavailable' if unknown else 'Ready'


def plugin_inventory(tr,cancelled,root=Path('/')):
    """Installed plugin packages only; no package transactions or feed requests."""
    records,manager=database(root)
    if not manager:return tr('Unavailable')
    selected=[(name,row) for name,row in sorted(records.items()) if name.startswith('enigma2-plugin-')]
    rows=[manager+'   ·   '+tr('Total:')+' '+str(len(selected)),'']
    for name,row in selected[:512]:
        if cancelled.is_set():return ''
        version=row.get('Version','—')
        architecture=row.get('Architecture','—')
        rows.extend((name,version+'   ·   '+architecture,''))
    if len(selected)>512:rows.append(tr('Partial result'))
    return '\n'.join(rows).strip()
