"""Read-only catalogue of the five official project feeds. No installation API."""
import json
import re
import shutil
import subprocess
from urllib.error import URLError
from .plugin_update import _open, parse_release, FEED_URL, version_key

ORG = 'Evolution-by-Warder/'
RAW = 'https://raw.githubusercontent.com/' + ORG
RELEASES = 'https://github.com/' + ORG
# Display name, repository, canonical feed path, product identity, installed package, IPK prefix, tag prefix
PROJECTS = (
    ('FullHDGlass', 'FullHDGlass-Warder-Evolution', 'update-production.json', None,
     'enigma2-plugin-skins-fullhdglass-warder-evolution', 'enigma2-plugin-skins-fullhdglass', ''),
    ('PiconHub', 'PiconHub-Warder-Evolution', 'plugin/update/stable.json', 'PiconHub Warder Evolution',
     'enigma2-plugin-extensions-piconhub-warder-evolution', 'enigma2-plugin-extensions-piconhub', 'v'),
    ('Warder Radio', 'Radio-Warder-Evolution', 'update/v2/stable.json', 'Warder Radio',
     'enigma2-plugin-extensions-radio-warder-evolution', 'enigma2-plugin-extensions-radio-warder-evolution', 'warder-radio-v'),
    ('YouTube', 'YouTube-Warder-Evolution', 'update/stable.json', 'YouTube Warder Evolution',
     'enigma2-plugin-extensions-youtube-warder-evolution', 'enigma2-plugin-extensions-youtube-warder-evolution', 'youtube-warder-v'),
    ('GSU', 'GSU-Warder-Evolution', 'plugin/update/stable-modern.json', 'Glass System Utility Warder Evolution',
     'enigma2-plugin-extensions-gsu-warder-evolution', 'enigma2-plugin-extensions-gsu', 'v'),
)


def release(project, raw, language):
    name, repo, path, identity, package, prefix, tag_prefix = project
    if len(raw) > 65536:
        raise ValueError('manifest size')
    doc = json.loads(raw)
    if name == 'GSU':
        item = parse_release(raw, '13.41-r6', 'stable-modern')
        return (item.version, item.notes_i18n.get(language) or item.notes) if item else None
    if identity:
        if doc.get('schema') != 1 or doc.get('channel') != 'stable' or doc.get('product') != identity:
            raise ValueError('feed identity')
        item = doc['release']
        if item is None:
            return None
    else:
        item = doc
    version = item['version']
    if not re.fullmatch(r'\d+(?:\.\d+){2,3}', version) or not re.fullmatch(r'[0-9a-f]{64}', item['sha256']):
        raise ValueError('release identity')
    filename = prefix+'_'+version+'_all.ipk'
    if identity:
        tag = tag_prefix+version
        expected = RELEASES+repo+'/releases/download/'+tag+'/'+filename
        if item['url'] != expected or item['tag'] != tag or type(item['bytes']) != int or not 0 < item['bytes'] <= 128*1024*1024:
            raise ValueError('unexpected package')
        notes = item.get('notes_i18n', {}).get(language) or item.get('notes', '')
    else:
        if item['package_url'] != RAW+repo+'/main/packages/'+filename:
            raise ValueError('unexpected skin package')
        notes = item.get('changelog_i18n', {}).get(language) or item.get('changelog', '')
    if not isinstance(notes, str) or len(notes) > 8192:
        raise ValueError('invalid notes')
    return version, notes


def installed(package, runner=subprocess.run):
    command = ['opkg', 'status', package] if shutil.which('opkg') else ['dpkg-query', '-s', package]
    try:
        result = runner(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=3, text=True)
    except (OSError, subprocess.TimeoutExpired):
        return None
    for paragraph in result.stdout.split('\n\n'):
        fields = dict(line.split(': ', 1) for line in paragraph.splitlines() if ': ' in line and not line.startswith(' '))
        if fields.get('Package') == package and fields.get('Status') in ('install ok installed','install user installed','hold ok installed'):
            value = fields.get('Version', '')
            if re.fullmatch(r'[0-9][0-9a-z.+:~-]{0,63}', value):
                return value
    return None


def status_label(name, current, available):
    if not current or not available:
        return 'Unavailable'
    clean = re.sub(r'^(?:\d+:)', '', current)
    if name == 'GSU':
        installed_key, remote = version_key(clean), version_key(available)
    else:
        match = re.fullmatch(r'(\d+(?:\.\d+){2,3})(?:-(?:r)?\d+)?', clean)
        if not match:
            return 'Unavailable'
        installed_key = tuple(map(int,match[1].split('.')))
        remote = tuple(map(int,available.split('.')))
    return 'Update' if installed_key < remote else 'Ready'


def read_feed(url, opener):
    with opener(url, timeout=3) as response:
        if response.geturl() != url:
            raise ValueError('unexpected redirect')
        raw = response.read(65537)
    if len(raw)>65536:
        raise ValueError('manifest size')
    return raw


def report(tr, language, cancelled, opener=_open, projects=None, compact=False, presentation=None):
    from .warder_package_status import database, dependency_state
    records, manager = database()
    lines = []
    table = []
    for project in PROJECTS if projects is None else projects:
        if cancelled.is_set():
            break
        name, repo, path = project[:3]
        record = records.get(project[4], {})
        current = record.get('Version') or installed(project[4])
        try:
            url = RAW+repo+'/main/'+path
            item = release(project, read_feed(url,opener), language)
            if name == 'GSU' and item is None and not cancelled.is_set():
                bridge = parse_release(read_feed(FEED_URL,opener), '0.0-r0')
                if bridge and bridge.version == '13.41-r6':
                    item = bridge.version, bridge.notes_i18n.get(language) or bridge.notes
            available = item[0] if item else tr('None')
        except (ValueError, TypeError, KeyError, AttributeError, OSError, URLError):
            item, available = None, tr('Unavailable')
        if cancelled.is_set():return ''
        status=tr('Unavailable')
        if item and current:
            try:status=tr(status_label(name,current,item[0]))
            except ValueError:pass
        table.append((name,current or '—',available,status))
        if presentation=='table':continue
        first=['%s    %s' % (tr('Installed version'),current or '—'),
               '%s    %s' % (tr('Stable version'),available)]
        if item and current:first.append(status)
        lines.extend((name, '', *first))
        if record and not compact:
            lines.append('')
            lines.append(tr('Package dependencies')+'   '+tr(dependency_state(project[4],records,manager)))
            lines.append(tr('Architecture')+'   '+record.get('Architecture','—'))
        if presentation=='panels':
            if cancelled.is_set():return ''
            if not (item and current):lines.extend(('',tr('Status')+'   '+status))
            return ('\n'.join(lines[2:]),item[1] if item and item[1] else '—')
        if item and item[1] and not compact:
            lines.extend(('',item[1]))
        lines.append('')
    if cancelled.is_set():return ''
    if presentation=='table':return table
    return '\n'.join(lines)


ENTRY_DIRS = {'FullHDGlass':'setupGlass17', 'PiconHub':'WarderPiconHub','Warder Radio':'WarderRadio',
              'YouTube':'WarderYouTube','GSU':'GlassSysUtil'}


def entrypoint(name):
    """Open only an already registered official product from its installed directory."""
    from pathlib import Path
    from Components.PluginComponent import plugins
    from Plugins.Plugin import PluginDescriptor
    from Tools.Directories import resolveFilename, SCOPE_PLUGINS
    base = Path(resolveFilename(SCOPE_PLUGINS,'Extensions')) / ENTRY_DIRS[name]
    for descriptor in plugins.getPlugins(PluginDescriptor.WHERE_PLUGINMENU):
        path = getattr(descriptor,'path',None)
        if path and Path(path) == base and callable(descriptor):
            return descriptor
    return None
