"""Original client screen, with bounded requests outside the GUI thread."""
from twisted.internet.threads import deferToThread
from .oscam_clients import EMPTY, COUNTERS, fetch_clients, set_enabled

_SK = {
    'Loading clients...': 'Načítavam klientov...',
    'No clients or accounts found.': 'Nenašli sa žiadni klienti ani účty.',
    'Unable to load OSCam clients.': 'Nepodarilo sa načítať klientov OSCam-u.',
    'Account change failed.': 'Zmena stavu účtu zlyhala.',
}


def tr(api, value):
    result = api['_'](value)
    language = getattr(getattr(getattr(api['config'], 'osd', None), 'language', None), 'value', '')
    return _SK.get(value, result) if result == value and language.startswith('sk') else result


def initialize(screen):
    screen.clientsClosed = False
    screen.clientsBusy = False
    screen.clientsConfirming = False
    screen.clientRecords = {}
    screen.onClose.append(lambda: stop(screen))


def prepare(screen):
    # Newlines separate fields. Wrapping any field shifts all subsequent values.
    for index in range(3):
        for kind in ('labels', 'values'):
            widget = screen['status_' + kind + '_' + str(index)]
            if widget.instance is not None:
                widget.instance.setWrap(0)


def stop(screen):
    screen.clientsClosed = True
    if screen.refreshTimer is not None:
        screen.refreshTimer.stop()
        screen.refreshTimer = None


def close(screen):
    stop(screen)
    screen.close()


def schedule(screen):
    if not screen.clientsClosed and screen.refreshTimer is not None:
        screen.refreshTimer.start(8000, True)


def clear_details(screen):
    for index in range(3):
        screen['status_values_' + str(index)].setText('\n'.join([EMPTY] * 5))
    screen['blue_button'].setText('')


def message(screen, api, value):
    screen.clientRecords = {}
    screen.list = [['*', api['MultiContentEntryText'](pos=(api['fhd'](25), 0),
        size=(api['fhd'](900), api['fhd'](22)), font=0, text=value)]]
    screen['list'].l.setList(screen.list)
    clear_details(screen)


def render(screen, api, records):
    selected = screen['list'].getCurrent()
    old_key = selected[0] if selected else None
    screen.clientRecords = {record['key']: record for record in records}
    screen.list = []
    for record in records:
        color = 'blue' if record['disabled'] else 'green' if record.get('connected') else 'red'
        label = record['name']
        if record.get('protocol'):
            label += ' [' + record['protocol'] + ']'
        if record.get('status'):
            label += ' — ' + record['status']
        row = [record['key'], api['MultiContentEntryText'](pos=(api['fhd'](25), 0),
            size=(api['fhd'](900), api['fhd'](22)), font=0, text=label),
            api['MultiContentEntryPixmapAlphaTest'](pos=(0, api['fhd'](3)),
                size=(api['fhd'](15), api['fhd'](16)), png=api['LoadPixmap'](api['BP_ICO'] % color))]
        screen.list.append(row)
    if not records:
        message(screen, api, tr(api, 'No clients or accounts found.'))
        return
    screen['list'].l.setList(screen.list)
    index = next((i for i, row in enumerate(screen.list) if row[0] == old_key), 0)
    screen['list'].moveToIndex(index)
    details(screen, api)


def request(screen, api):
    if screen.clientsClosed or screen.clientsBusy or screen.clientsConfirming:
        return
    screen.refreshTimer.stop()
    screen.clientsBusy = True
    if not screen.list:
        message(screen, api, tr(api, 'Loading clients...'))
    def done(records):
        screen.clientsBusy = False
        if screen.clientsClosed:
            return
        screen.setTitlenew()
        render(screen, api, records)
        schedule(screen)
    def failed(failure):
        screen.clientsBusy = False
        if not screen.clientsClosed:
            # Never leave old counters on screen as if the refresh succeeded.
            message(screen, api, tr(api, 'Unable to load OSCam clients.'))
            schedule(screen)
        return None
    screen.clientsRequest = deferToThread(fetch_clients, screen.url, screen.login, screen.passwd, api['getUrlData'])
    screen.clientsRequest.addCallback(done)
    screen.clientsRequest.addErrback(failed)


def selected_record(screen):
    selected = screen['list'].getCurrent()
    return screen.clientRecords.get(selected[0]) if selected else None


def details(screen, api):
    record = selected_record(screen)
    if record is None:
        clear_details(screen)
        return
    values = [record.get(key) or EMPTY for key in ('address', 'protocol', 'channel', 'channel_time', 'idle')]
    # Keep the full negotiated-client description in the wide top list row.
    # The narrow detail column needs the actual protocol name only.
    values[1] = values[1].split(' (', 1)[0]
    stats = record.get('stats', {})
    counters = [stats.get(key) or EMPTY for key in COUNTERS]
    if counters[7] != EMPTY and not counters[7].lower().endswith('ms'):
        counters[7] += ' ms'
    screen['status_values_0'].setText('\n'.join(values))
    screen['status_values_1'].setText('\n'.join(counters[:5]))
    screen['status_values_2'].setText('\n'.join(counters[5:]))
    screen['blue_button'].setText(api['_']('Enable' if record['disabled'] else 'Disable') if record['manageable'] else '')


def change_state(screen, api):
    if screen.clientsClosed or screen.clientsBusy or screen.clientsConfirming:
        return
    record = selected_record(screen)
    if record is None or not record.get('manageable'):
        return
    name, disabled = record['name'], not record['disabled']
    screen.clientsConfirming = True
    screen.refreshTimer.stop()
    box = api['MessageBox']
    def confirmed(answer):
        screen.clientsConfirming = False
        if screen.clientsClosed:
            return
        if not answer:
            schedule(screen)
            return
        screen.clientsBusy = True
        def done(result):
            screen.clientsBusy = False
            if not screen.clientsClosed:
                request(screen, api)
        def failed(failure):
            screen.clientsBusy = False
            if not screen.clientsClosed:
                screen.session.open(box, tr(api, 'Account change failed.'), box.TYPE_ERROR)
                schedule(screen)
            return None
        screen.clientsRequest = deferToThread(set_enabled, screen.url, screen.login, screen.passwd,
                                             api['getUrlData'], name, disabled)
        screen.clientsRequest.addCallback(done)
        screen.clientsRequest.addErrback(failed)
    screen.session.openWithCallback(confirmed, box,
        api['_']('Disable' if disabled else 'Enable') + ': ' + name + '?', box.TYPE_YESNO, default=False)
