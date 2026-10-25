"""OSCam client status and account statistics, independent of HTML formatting."""
from html.parser import HTMLParser
import re
from urllib.parse import urlencode, unquote, urlsplit, parse_qs
from xml.etree import ElementTree as ET

EMPTY = '—'
COUNTERS = ('cwok', 'cwnok', 'cwignore', 'cwtimeout', 'cwcycle', 'cwcache', 'cwtun', 'cwlastresptime', 'emmok', 'emmnok')


class ClientError(ValueError):
    pass


def text(value):
    return ' '.join(str(value or '').split())


def duration(value):
    value = text(value)
    if not value.isdigit():
        return value or EMPTY
    seconds = int(value)
    return '%d:%02d:%02d' % (seconds // 3600, seconds // 60 % 60, seconds % 60)


def xml(data, section):
    if data is None:
        raise ClientError('No response from OSCam.')
    raw = '\n'.join(data) if isinstance(data, list) else data
    if '<!DOCTYPE' in raw.upper() or '<!ENTITY' in raw.upper():
        raise ClientError('Unsupported XML declaration.')
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        raise ClientError('OSCam did not return valid XML.') from None
    element = root if root.tag == section else root.find(section)
    if element is None:
        raise ClientError('OSCam response has no ' + section + ' section.')
    return element


def parse_status(data):
    rows = []
    for index, node in enumerate(xml(data, 'status').findall('client')):
        if node.get('type', '').lower() != 'c':
            continue
        name = text(node.get('name'))
        if not name:
            continue
        request, times, connection = node.find('request'), node.find('times'), node.find('connection')
        rows.append({'key': 'client:' + (node.get('thid') or str(index)), 'name': name,
            'protocol': text(node.get('protocol')), 'channel': text(request.text) if request is not None else '',
            'address': text(connection.get('ip')) if connection is not None else '',
            'idle': duration(times.get('idle')) if times is not None else EMPTY,
            'status': text(connection.text) if connection is not None else 'connected',
            'ecmtime': text(request.get('ecmtime')) if request is not None else '', 'connected': True})
    return rows


def parse_users(data):
    users = []
    for node in xml(data, 'users').findall('user'):
        name = text(node.get('name'))
        if not name:
            continue
        stats = {key: text(node.findtext('stats/' + key)) for key in COUNTERS}
        users.append({'name': name, 'status': text(node.get('status')), 'address': text(node.get('ip')),
            'protocol': text(node.get('protocol')), 'stats': stats,
            'channel_time': duration(node.findtext('stats/timeonchannel')), 'manageable': True})
    return users


class Table(HTMLParser):
    """Collect named column classes, with br boundaries and nested tags intact."""
    def __init__(self, prefix):
        super().__init__(convert_charrefs=True)
        self.prefix, self.rows, self.row, self.cell = prefix, [], None, None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'tr':
            self.row = {'cells': {}, 'attrs': {}, 'name': '', 'class': attrs.get('class', ''), 'key': attrs.get('id', '')}
        if self.row is None:
            return
        if tag == 'td':
            self.cell = next((c for c in attrs.get('class', '').split() if re.fullmatch(self.prefix + r'\d+', c)), None)
            if self.cell:
                self.row['cells'][self.cell] = []
                self.row['attrs'][self.cell] = attrs
        if not self.cell:
            return
        if tag == 'br':
            self.row['cells'][self.cell].append('\n')
        if self.cell == 'usercol0' and attrs.get('data-user-name'):
            self.row['name'] = unquote(attrs['data-user-name'])
        if tag == 'a' and self.cell in ('usercol1', 'statuscol4'):
            name = parse_qs(urlsplit(attrs.get('href', '')).query).get('user', [''])[0]
            if name:
                self.row['name'] = name
        if tag == 'img' and self.cell == 'statuscol13':
            self.row['cells'][self.cell].append(attrs.get('alt') or attrs.get('title', ''))

    def handle_endtag(self, tag):
        if tag == 'td':
            self.cell = None
        elif tag == 'tr':
            if self.row and self.row['cells']:
                self.rows.append(self.row)
            self.row, self.cell = None, None

    def handle_data(self, data):
        if self.row is not None and self.cell:
            self.row['cells'][self.cell].append(data)


def table(data, prefix):
    if data is None:
        raise ClientError('No response from OSCam.')
    raw = '\n'.join(data) if isinstance(data, list) else data
    parser = Table(prefix)
    parser.feed(raw)
    # Distinguish a valid empty page from an authentication/error response.
    if not parser.rows and not re.search(prefix + r'\d+', raw, re.I):
        raise ClientError('OSCam returned an unrecognized table.')
    return parser.rows


def parse_users_html(data):
    result = []
    for row in table(data, 'usercol'):
        def value(n):
            return text(''.join(row['cells'].get('usercol' + str(n), [])))
        name = row['attrs'].get('usercol1', {}).get('data-sort-value') or row['name'] or value(1)
        if not name or 'usercol1' not in row['cells']:
            continue
        status_ip = ''.join(row['cells'].get('usercol2', [])).split('\n')
        idle_channel = ''.join(row['cells'].get('usercol3', [])).split('\n')
        stats = dict(zip(COUNTERS, [value(n) for n in (9, 10, 11, 12, 13, 14, 15, 7, 17, 18)]))
        result.append({'name': text(name), 'status': text(status_ip[0]) or row['class'],
            'address': text(status_ip[-1]) if len(status_ip) > 1 else '', 'protocol': value(4),
            'channel': value(6), 'idle': duration(idle_channel[0]),
            'channel_time': duration(idle_channel[-1]) if len(idle_channel) > 1 else EMPTY,
            'stats': stats, 'manageable': True})
    return result


def parse_status_html(data):
    rows = []
    for index, row in enumerate(table(data, 'statuscol')):
        def value(n):
            return text(''.join(row['cells'].get('statuscol' + str(n), [])))
        if 'c' not in row['class'].lower().split() and value(2).lower() != 'c':
            continue
        name = row['name'] or value(4)
        if not name:
            continue
        title = row['attrs'].get('statuscol15', {}).get('title', '')
        idle = re.search(r'idle:\s*(\d+)', title, re.I)
        rows.append({'key': 'client:' + (row['key'] or str(index)), 'name': name, 'address': value(7),
            'protocol': value(9), 'channel': value(13), 'status': value(16),
            'idle': duration(idle[1]) if idle else EMPTY, 'connected': True})
    return rows


def merge(clients, users):
    accounts = {user['name']: user for user in users}
    result, seen = [], set()
    for client in clients:
        account = accounts.get(client['name'], {})
        record = dict(account)
        record.update({k: v for k, v in client.items() if v not in ('', EMPTY)})
        # Disabled is an account setting, not the connection status string.
        record['disabled'] = 'disabled' in account.get('status', '').lower()
        record['manageable'] = bool(account.get('manageable'))
        record['stats'] = dict(account.get('stats', {}))
        if client.get('ecmtime'):
            record['stats']['cwlastresptime'] = client['ecmtime']
        result.append(record); seen.add(client['name'])
    for user in users:
        if user['name'] not in seen:
            record = dict(user, key='user:' + user['name'], connected=False,
                          disabled='disabled' in user.get('status', '').lower())
            result.append(record)
    return result


def fetch_clients(base, login, password, fetch):
    base = base.rstrip('/') + '/'
    try:
        clients = parse_status(fetch(base + 'oscamapi.html?part=status', login, password))
    except ClientError:
        clients = parse_status_html(fetch(base, login, password))
    try:
        users = parse_users(fetch(base + 'oscamapi.html?part=userstats', login, password))
    except ClientError:
        try:
            users = parse_users_html(fetch(base + 'userconfig.html', login, password))
        except ClientError:
            users = []  # Live status remains useful without account permissions/API.
    return merge(clients, users)


def set_enabled(base, login, password, fetch, name, disabled):
    query = urlencode({'part': 'userstats', 'user': name, 'action': 'disable' if disabled else 'enable'})
    users = parse_users(fetch(base.rstrip('/') + '/oscamapi.html?' + query, login, password))
    account = next((user for user in users if user['name'] == name), None)
    if account is None or ('disabled' in account['status'].lower()) != disabled:
        raise ClientError('OSCam did not confirm the requested account state.')
    return True
