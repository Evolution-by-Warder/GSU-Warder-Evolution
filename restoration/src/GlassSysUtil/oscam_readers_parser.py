"""Read reader-table fields by their WebIf column classes, not cell offsets."""
from html.parser import HTMLParser
from urllib.parse import parse_qs, unquote, urlsplit


class ReaderTable(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows = []
        self.row = None
        self.cell = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'tr':
            self.row = {'cells': {}, 'protocol': '', 'enabled': None, 'label': ''}
        if self.row is None:
            return
        if tag == 'td':
            self.cell = next((x for x in attrs.get('class', '').split() if x.startswith('readercol')), None)
            if self.cell:
                self.row['cells'].setdefault(self.cell, [])
            if self.cell == 'readercol1':
                self.row['label'] = attrs.get('data-sort-value', '')
        action = attrs.get('data-next-action', '')
        query = parse_qs(urlsplit(attrs.get('href', '')).query)
        action = action or query.get('action', [''])[0]
        if action in ('enable', 'disable'):
            self.row['enabled'] = action == 'disable'
            self.row['label'] = self.row['label'] or unquote(attrs.get('data-reader-name', '') or query.get('label', [''])[0])
        title = attrs.get('title', '')
        if self.cell == 'readercol2' and title.lower().startswith('protocol:'):
            self.row['protocol'] = title.split(':', 1)[1].strip()

    def handle_endtag(self, tag):
        if tag == 'td':
            self.cell = None
        elif tag == 'tr':
            if self.row and 'readercol1' in self.row['cells']:
                self.rows.append(self.row)
            self.row = None
            self.cell = None

    def handle_data(self, data):
        if self.row is not None and self.cell:
            self.row['cells'][self.cell].append(data)


def parse_readers(data):
    parser = ReaderTable()
    parser.feed('\n'.join(data))
    records = []
    for row in parser.rows:
        cells = {key: ' '.join(' '.join(value).split()) for key, value in row['cells'].items()}
        label = row['label'] or cells.get('readercol1', '')
        if not label or row['enabled'] is None:
            continue
        protocol = row['protocol']
        status = cells.get('readercol2', '')
        if not protocol and status.lower() in ('internal', 'mouse', 'pcsc', 'cs378x', 'camd35', 'cccam', 'newcamd', 'emu', 'serial', 'smartreader', 'radegast', 'pandora'):
            protocol, status = status, ''
        records.append({'label': label, 'protocol': protocol or '-', 'status': status,
                        'enabled': row['enabled'],
                        'counts': [cells.get('readercol%d' % col, '0 / 0 / 0 / 0') for col in (7, 8, 9, 10)]})
    return records
