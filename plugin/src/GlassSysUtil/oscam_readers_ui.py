"""Nonblocking reader-table refresh and confirmed, verified account actions."""
from urllib.parse import urlencode, quote
from twisted.internet.threads import deferToThread
from .oscam_readers_parser import parse_readers

_SK={
    'Loading readers...':'Načítavam čítačky...',
    'Unable to load OSCam readers.':'Nepodarilo sa načítať čítačky OSCam-u.',
    'Reader change failed.':'Zmena stavu čítačky zlyhala.',
}


def tr(api,value):
    result=api['_'](value)
    language=api['config'].osd.language.value
    return _SK.get(value,result) if result==value and language.startswith('sk') else result


def fetch(url,login,passwd,transport):
    data=transport(url+'readers.html',login,passwd)
    if not isinstance(data,list):raise ValueError('OSCam reader table is unavailable')
    return data


def set_enabled(url,login,passwd,transport,name,enabled):
    query=urlencode({'label':name,'action':'enable' if enabled else 'disable'})
    response=transport(url+'readers.html?'+query,login,passwd)
    if not isinstance(response,list):raise ValueError('OSCam reader action failed')
    # A separate read verifies the resulting state, not just a successful HTTP call.
    data=fetch(url,login,passwd,transport)
    records=[row for row in parse_readers(data) if row['label']==name]
    if len(records)!=1 or records[0]['enabled'] is not enabled:
        raise ValueError('OSCam reader state was not confirmed')
    return data


def initialize(screen):
    screen.readersClosed=False
    screen.readersBusy=False
    screen.readersConfirming=False
    screen.readerRecords={}
    screen.onClose.append(lambda:stop(screen))


def stop(screen):
    screen.readersClosed=True
    if screen.refreshTimer is not None:
        screen.refreshTimer.stop();screen.refreshTimer=None


def close(screen):
    stop(screen);screen.close()


def schedule(screen):
    if not screen.readersClosed and screen.refreshTimer is not None:
        screen.refreshTimer.start(8000,True)


def selected(screen):
    row=screen['list'].getCurrent()
    return screen.readerRecords.get(row[0]) if row else None


def message(screen,api,value):
    screen.readerRecords={}
    screen.list=[['*',api['MultiContentEntryText'](pos=(api['fhd'](25),0),size=(api['fhd'](850),api['fhd'](22)),font=0,text=value)]]
    screen['list'].l.setList(screen.list)
    for name in ('status_values_0','status_values_1','blue_button'):screen[name].setText('')


def render(screen,api,data):
    current=selected(screen)
    old_name=current['label'] if current else None
    screen.renderReaders(data)
    records=parse_readers(data)
    if records:
        screen.readerRecords={row[0]:record for row,record in zip(screen.list,records)}
    else:
        # Preserve the original class-less HTML renderer for old OSCam versions.
        screen.readerRecords={}
        for row in screen.list:
            parts=row[0].split('*')
            if len(parts)>7:
                screen.readerRecords[row[0]]={'label':parts[1],'protocol':parts[2],'enabled':parts[7]=='green'}
    index=next((i for i,row in enumerate(screen.list) if screen.readerRecords.get(row[0],{}).get('label')==old_name),0)
    if screen.list:screen['list'].moveToIndex(index)
    screen.reactivate()


def request(screen,api):
    if screen.readersClosed or screen.readersBusy or screen.readersConfirming:return
    screen.refreshTimer.stop();screen.readersBusy=True
    if not screen.list:message(screen,api,tr(api,'Loading readers...'))
    def done(data):
        screen.readersBusy=False
        if not screen.readersClosed:
            render(screen,api,data);schedule(screen)
    def failed(failure):
        screen.readersBusy=False
        if not screen.readersClosed:
            message(screen,api,tr(api,'Unable to load OSCam readers.'));schedule(screen)
        return None
    screen.readersRequest=deferToThread(fetch,screen.url,screen.login,screen.passwd,api['getUrlData'])
    screen.readersRequest.addCallback(done)
    screen.readersRequest.addErrback(failed)


def details(screen,api):
    if not selected(screen):
        for name in ('status_values_0','status_values_1','blue_button'):screen[name].setText('')
        return
    screen.renderReaderDetails()


def entitlements(screen,api):
    if screen.readersClosed or screen.readersBusy or screen.readersConfirming:return
    record=selected(screen)
    if record is None:return
    if any(value in record['protocol'] for value in ('newcamd','camd3','cs3')):
        screen.session.open(api['MessageBox'],api['_']('Protocol not allowed for entitlements'),api['MessageBox'].TYPE_INFO,4)
    else:
        screen.session.open(api['oscam_entitlements'],screen.url,quote(record['label'],safe=''),screen.login,screen.passwd)


def change_state(screen,api):
    if screen.readersClosed or screen.readersBusy or screen.readersConfirming:return
    record=selected(screen)
    if record is None:return
    name,enabled=record['label'],not record['enabled']
    screen.readersConfirming=True;screen.refreshTimer.stop()
    box=api['MessageBox']
    def confirmed(answer):
        screen.readersConfirming=False
        if screen.readersClosed:return
        if not answer:schedule(screen);return
        screen.readersBusy=True
        def done(data):
            screen.readersBusy=False
            if not screen.readersClosed:render(screen,api,data);schedule(screen)
        def failed(failure):
            screen.readersBusy=False
            if not screen.readersClosed:
                # Re-read after an uncertain action, rather than display stale state.
                message(screen,api,tr(api,'Reader change failed.'))
                screen.session.open(box,tr(api,'Reader change failed.'),box.TYPE_ERROR)
                schedule(screen)
            return None
        screen.readersRequest=deferToThread(set_enabled,screen.url,screen.login,screen.passwd,api['getUrlData'],name,enabled)
        screen.readersRequest.addCallback(done)
        screen.readersRequest.addErrback(failed)
    screen.session.openWithCallback(confirmed,box,api['_']('Enable' if enabled else 'Disable')+': '+name+'?',box.TYPE_YESNO,default=False)
