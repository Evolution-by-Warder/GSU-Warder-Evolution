"""Use the current native service and the image's own registered setup entries."""
from time import time


def read_frontend(service):
    try:
        frontend = service and service.frontendInfo()
        data = frontend and frontend.getAll(True)
        return data if isinstance(data, dict) else {}
    except (AttributeError, TypeError, RuntimeError):
        return {}


def slots():
    from Components.NimManager import nimmanager
    return [(slot.getSlotName(), slot.slot) for slot in getattr(nimmanager,'nim_slots',())
            if type(getattr(slot,'slot',None)) is int]


def details(session, api, tr, slot_number=None):
    from Components.NimManager import nimmanager
    nav = session.nav
    service = nav.getCurrentService()
    data = read_frontend(service)
    current_slot = data.get('tuner_number')
    show_current = slot_number is None or slot_number==current_slot
    if not show_current:
        data = {}
    try:
        human = api['ConvertToHumanReadable'](dict(data)) if data else {}
    except (KeyError, TypeError, ValueError, AttributeError):
        human = {}
    rows = []
    for key, caption in [('system','System:'), ('tuner_type','Type'), ('frequency','Frequency:'),
                         ('polarization','Polarisation:'), ('modulation','Modulation:'), ('fec_inner','FEC'),
                         ('symbol_rate','Symbol Rate:'), ('orbital_position','Satellite:'),
                         ('bandwidth','BW'), ('code_rate_hp','FEC HP'), ('code_rate_lp','FEC LP'),
                         ('transmission_mode','FFT'), ('guard_interval','GI'), ('hierarchy_information','α'),
                         ('inversion','I/Q'), ('rolloff','Roll-off'), ('pilot','Pilot'),
                         ('is_id','MIS'), ('pls_mode','PLS'), ('pls_code','PLS code'),
                         ('t2mi_plp_id','T2-MI PLP'), ('t2mi_pid','T2-MI PID'), ('plp_id','PLP')]:
        if key in data and data[key] not in (None, -1):
            rows.append('%s   %s' % (tr(caption), human[key] if human.get(key) is not None else data[key]))
    try:
        recordings = nav.getRecordings()
        count = len(recordings)
        occupied = {read_frontend(r).get('tuner_number') for r in recordings}
    except (AttributeError, RuntimeError, TypeError):
        occupied, count = set(), None
    rows.extend(('', tr('Recordings')+'   '+('—' if count is None else str(count))))
    for slot in getattr(nimmanager, 'nim_slots', []):
        number = getattr(slot, 'slot', None)
        if type(number) is not int or (slot_number is not None and slot_number!=number):
            continue
        state = []
        if number == data.get('tuner_number'):
            state.append(tr('Active'))
        if number in occupied:
            state.append(tr('Recordings'))
        fbc = getattr(slot, 'isFBC', None) or getattr(slot, 'isFBCTuner', None)
        if callable(fbc) and fbc():
            state.append('FBC')
        for method,label in (('isFBCRoot','FBC root'),('isFBCLink','FBC link')):
            flag=getattr(slot,method,None)
            if callable(flag) and flag():
                state.append(tr(label))
        rows.append('%s    %s' % (slot.getSlotName(), ' · '.join(state) or '—'))
        if slot_number is not None:
            description=getattr(slot,'getFriendlyFullDescription',None)
            if callable(description):
                rows.append(str(description()))
            types=getattr(slot,'getTunerTypesEnabled',None)
            if callable(types):
                values=types()
                if isinstance(values,(list,tuple,set)):
                    rows.append(' / '.join(str(v) for v in values))
    if service and show_current:
        info = service.info()
        enum = api['iServiceInformation']
        for name, label in [('sVideoPID','Video PID'), ('sAudioPID','Audio PID'), ('sPCRPID','PCR PID'),
                            ('sVideoWidth','W'), ('sVideoHeight','H'), ('sGamma','HDR')]:
            key = getattr(enum, name, None)
            if key is not None and info:
                value = info.getInfo(key)
                if type(value) is int and value >= 0:
                    if name == 'sGamma':
                        value = {0:'SDR', 1:'HDR', 2:'HDR10', 3:'HLG'}.get(value, value)
                    rows.append('%s   %s' % (label, value))
        tracks = getattr(service,'audioTracks',lambda:None)()
        if tracks and 0 <= tracks.getCurrentTrack() < tracks.getNumberOfTracks():
            audio = tracks.getTrackInfo(tracks.getCurrentTrack())
            rows.append('Audio   '+str(audio.getDescription())+'   '+str(audio.getLanguage()))
    from .warder_tools import Probe
    if not show_current:
        return '\n'.join(rows).strip() or tr('Unavailable')
    p = Probe()
    for label, path in [('HDMI', '/proc/stb/video/videomode'), ('HDMI · OUT', '/proc/stb/hdmi/output'),
                        ('HDMI · HDR', '/proc/stb/video/hdmi_hdrtype'), ('HDMI · PCM', '/proc/stb/audio/multichannel_pcm')]:
        value = p.text(path, 96)
        if value and value.isprintable():
            rows.append(label+'   '+value)
    return '\n'.join(rows).strip() or tr('Unavailable')


def recording_safe(nav, now=time):
    try:
        service = nav.getCurrentService()
        timeshift = service and service.timeshift()
        if timeshift and (timeshift.isTimeshiftActive() or timeshift.isTimeshiftEnabled()):
            return False
        if nav.getRecordings():
            return False
        count = getattr(nav, 'getAnyRecordingsCount', None)
        if count and count():
            return False
        upcoming = nav.RecordTimer.getNextRecordingTime()
        return type(upcoming) in (float, int) and (upcoming in (-1, 0) or upcoming-now() >= 360)
    except (RuntimeError, AttributeError, TypeError):
        return False


def native_tools(tr):
    from Components.PluginComponent import plugins
    # Only expose image-registered entry points that the installed tuner supports.
    allowed = {'satfinder', 'positioner_setup', 'blindscan'}
    options = []
    for item in plugins.getPluginsForMenu('scan'):
        if len(item) >= 3 and item[2] in allowed and callable(item[1]):
            options.append((item[0], item[1]))
    try:
        from Screens.ScanSetup import ScanSetup
        from enigma import eComponentScan
        if hasattr(ScanSetup,'startScan') and hasattr(eComponentScan,'scanRemoveServices'):
            options.append((tr('Manual scan'), manual_scan))
    except ImportError:
        pass
    return options


def choose_native(session, tr):
    from Screens.ChoiceBox import ChoiceBox
    from Screens.MessageBox import MessageBox
    def info(msg):
        session.open(MessageBox, tr(msg), type=MessageBox.TYPE_INFO)
    if not recording_safe(session.nav):
        return info('Tuner in use')
    try:
        options = native_tools(tr)
    except (ImportError, AttributeError, RuntimeError):
        options = []
    if not options:
        return info('Unavailable')
    def selected(item):
        if not item:
            return
        def confirmed(answer):
            if answer is not True:
                return
            if not recording_safe(session.nav):
                return info('Tuner in use')
            from twisted.internet.threads import deferToThread
            from Tools.Directories import resolveFilename, SCOPE_CONFIG
            from .warder_scan_backup import create
            owner = session.current_dialog
            def offer(folder):
                if session.current_dialog is not owner:
                    return
                def launch(accepted):
                    if accepted is True:
                        if recording_safe(session.nav):
                            item[1](session)
                        else:
                            info('Tuner in use')
                message = tr('Verified channel backup')+'\n'+folder+'\n\n'+tr('Open tuner setup? Live TV may stop.')
                session.openWithCallback(launch,MessageBox,message,type=MessageBox.TYPE_YESNO,default=False)
            def failed(_failure):
                if session.current_dialog is owner:
                    info('Recording or channel-list protection stopped the scan.')
            deferToThread(create,resolveFilename(SCOPE_CONFIG)).addCallbacks(offer,failed)
        session.openWithCallback(confirmed, MessageBox, tr('Open tuner setup? Live TV may stop.'), type=MessageBox.TYPE_YESNO, default=False)
    session.openWithCallback(selected, ChoiceBox, title=tr('Tuner setup'), list=options)


def manual_scan(session):
    from Screens.ScanSetup import ScanSetup
    from Screens.MessageBox import MessageBox
    from enigma import eComponentScan
    from .plugin import _

    class AdditiveScan(ScanSetup):
        def startScan(self, tlist, flags, feid, *args, **kwargs):
            if not recording_safe(self.session.nav) or flags & eComponentScan.scanRemoveServices:
                self.session.open(MessageBox, _('Recording or channel-list protection stopped the scan.'), type=MessageBox.TYPE_INFO)
                return
            return super().startScan(tlist, flags, feid, *args, **kwargs)

    if recording_safe(session.nav):
        session.open(AdditiveScan)
