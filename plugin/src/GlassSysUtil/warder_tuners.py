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


def details(session, api, tr, slot_number=None, panels=False):
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
    if data:rows.append(tr('Transponder'))
    for key, caption in [('system','System:'), ('tuner_type','Type'), ('frequency','Frequency:'),
                         ('polarization','Polarisation:'), ('modulation','Modulation:'), ('fec_inner','FEC'),
                         ('symbol_rate','Symbol Rate:'), ('orbital_position','Satellite:'),
                         ('bandwidth','BW'), ('code_rate_hp','FEC HP'), ('code_rate_lp','FEC LP'),
                         ('transmission_mode','FFT'), ('guard_interval','GI'), ('hierarchy_information','α'),
                         ('inversion','I/Q'), ('rolloff','Roll-off'), ('pilot','Pilot'),
                         ('is_id','MIS'), ('pls_mode','PLS'), ('pls_code','PLS code'),
                         ('t2mi_plp_id','T2-MI PLP'), ('t2mi_pid','T2-MI PID'), ('plp_id','PLP')]:
        if key in data and data[key] not in (None, -1):
            rows.append('    %s   %s' % (tr(caption), human[key] if human.get(key) is not None else data[key]))
    try:
        recordings = nav.getRecordings()
        count = len(recordings)
        occupied = {read_frontend(r).get('tuner_number') for r in recordings}
    except (AttributeError, RuntimeError, TypeError):
        occupied, count = set(), None
    transponder=rows[1:] if data else []
    if panels:rows=[]
    elif rows:rows.append('')
    rows.extend((tr('Tuner interfaces'), '    '+tr('Recordings')+'   '+('—' if count is None else str(count))))
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
        rows.append('    %s    %s' % (slot.getSlotName(), ' · '.join(state) or '—'))
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
        rows.extend(('',tr('Channel Information')))
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
                    rows.append('    %s   %s' % (label, value))
        tracks = getattr(service,'audioTracks',lambda:None)()
        if tracks and 0 <= tracks.getCurrentTrack() < tracks.getNumberOfTracks():
            audio = tracks.getTrackInfo(tracks.getCurrentTrack())
            rows.append('    '+tr('Audio:')+'   '+str(audio.getDescription())+'   '+str(audio.getLanguage()))
    from .warder_tools import Probe
    if not show_current:
        if panels:return ('\n'.join(transponder).strip() or tr('Unavailable'),'\n'.join(rows[1:]).strip() or tr('Unavailable'))
        return '\n'.join(rows).strip() or tr('Unavailable')
    p = Probe()
    for label, path in [('HDMI', '/proc/stb/video/videomode'), ('HDMI · OUT', '/proc/stb/hdmi/output'),
                        ('HDMI · HDR', '/proc/stb/video/hdmi_hdrtype'), ('HDMI · PCM', '/proc/stb/audio/multichannel_pcm')]:
        value = p.text(path, 96)
        if value and value.isprintable():
            rows.append(label+'   '+value)
    if panels:return ('\n'.join(transponder).strip() or tr('Unavailable'),'\n'.join(rows[1:]).strip() or tr('Unavailable'))
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
            action=styled_satfinder(item[1]) if item[2]=='satfinder' else item[1]
            # Do not offer an unrecognized scanner as a measurement-only finder.
            if action is not None:options.append((item[0],action))
    try:
        from Screens.ScanSetup import ScanSetup
        from enigma import eComponentScan
        if hasattr(ScanSetup,'startScan') and hasattr(eComponentScan,'scanRemoveServices'):
            options.append((tr('Manual scan'), manual_scan))
    except ImportError:
        pass
    return options


def styled_satfinder(action):
    """Use the native frontend but expose a measurement-only finder in GSU."""
    from types import FunctionType
    if not isinstance(action,FunctionType):return None
    original=action.__globals__.get('Satfinder')
    if (not isinstance(original,type) or action.__name__!='SatfinderMain'
            or not callable(getattr(original,'keyGoScan',None))
            or not callable(getattr(original,'retune',None))):return None

    class WarderSatfinder(original):
        def __init__(self,session):
            super().__init__(session)
            from . import plugin
            from .warder_tuner_ui import install
            # Native fallback skins may still bind these components.
            for name in ('key_green','introduction'):
                if name in self:self[name].setText('')
            if not install(self,vars(plugin),True):
                self.skinName=['Satfinder']

        def retune(self,*args,**kwargs):
            # Native retune continues to own the selected frontend. Never
            # mix observations from two tuning attempts.
            header=getattr(self,'_diagnostic_header',None)
            if header is not None and hasattr(header,'reset_history'):header.reset_history()
            self._warder_measurement_id=None
            return super().retune(*args,**kwargs)

        def retuneSat(self,*args,**kwargs):
            # Only recognize a newly prepared native satellite tuple after a
            # completed tuning call. Do not infer parameters from live TV.
            previous=getattr(self,'transponder',None)
            result=super().retuneSat(*args,**kwargs)
            self._warder_measurement_id=None
            if (getattr(self,'initcomplete',False) is True
                    and getattr(self,'frontend',None) is not None
                    and getattr(self,'transponder',None) is not previous):
                from .warder_signal import satellite_identity
                self._warder_measurement_id=satellite_identity(self)
            return result

        def keyGoScan(self,*args,**kwargs):
            # The native OK/green handler otherwise releases the live frontend
            # BEFORE calling startScan. Prevent that path at its entry.
            return None

        def keyGo(self,*args,**kwargs):
            # Also guard inherited ScanSetup action bindings.
            return None

        def startScan(self,*args,**kwargs):
            # Last line of defense; the finder never launches a service scan.
            return None

    namespace=dict(action.__globals__,Satfinder=WarderSatfinder)
    wrapped=FunctionType(action.__code__,namespace,action.__name__,action.__defaults__,action.__closure__)
    wrapped.__kwdefaults__=action.__kwdefaults__
    return wrapped


def tuner_info(session,tr,message):
    from . import plugin
    from .warder_dialog import show_info
    return show_info(session,vars(plugin),tr(message),tr('Tuner setup'))


def open_native(session,tr,action):
    """Explicit menu selection opens the tool after a private verified backup."""
    def info(msg):
        return tuner_info(session,tr,msg)
    if not callable(action) or not recording_safe(session.nav):
        return info('Tuner in use')
    owner=session.current_dialog
    if getattr(owner,'_gsu_native_pending',False) is True:
        return
    owner._gsu_native_pending=True
    def clear():
        owner._gsu_native_pending=False
    from twisted.internet.threads import deferToThread
    from Tools.Directories import resolveFilename,SCOPE_CONFIG
    from .warder_scan_backup import create
    def launch(folder):
        clear()
        if session.current_dialog is not owner:
            return
        if not recording_safe(session.nav):
            return info('Tuner in use')
        owner._gsu_last_channel_backup=folder
        describe=getattr(owner,'describe',None)
        if callable(describe):describe()
        try:
            action(session)
        except (AttributeError,RuntimeError,TypeError,ImportError,OSError,ValueError):
            info('Unavailable')
    def failed(_failure):
        clear()
        if session.current_dialog is owner:
            info('Recording or channel-list protection stopped the scan.')
    try:
        deferToThread(create,resolveFilename(SCOPE_CONFIG)).addCallbacks(launch,failed)
    except (OSError,RuntimeError,TypeError,AttributeError):
        failed(None)


def choose_native(session, tr):
    """Compatibility route; skip a redundant selector if only one tool exists."""
    from . import plugin
    from .warder_dialog import choose
    def info(msg):
        return tuner_info(session,tr,msg)
    if not recording_safe(session.nav):
        return info('Tuner in use')
    try:
        options=native_tools(tr)
    except (ImportError,AttributeError,RuntimeError,TypeError):
        options=[]
    if not options:return info('Unavailable')
    if len(options)==1:return open_native(session,tr,options[0][1])
    def selected(item):
        if item in options:open_native(session,tr,item[1])
    choose(session,vars(plugin),selected,tr('Tuner setup'),options)

def manual_scan(session):
    from Screens.ScanSetup import ScanSetup
    from .plugin import _

    class WarderManualScan(ScanSetup):
        def __init__(self,session):
            super().__init__(session)
            # Enigma2's Screen constructor defaults to the actual subclass name.
            # Keep the native ScanSetup fallback on images with unfamiliar components.
            names=getattr(self,'skinName',None)
            names=names if isinstance(names,(list,tuple)) else [names]
            self.skinName=['ScanSetup']+[name for name in names
                if isinstance(name,str) and name not in ('ScanSetup','WarderManualScan')]
            from . import plugin
            from .warder_tuner_ui import install
            install(self,vars(plugin),False)

        def startScan(self, tlist, flags, feid, *args, **kwargs):
            # The user's native clear-before-scan selection is authoritative.
            # The verified backup was created before opening this tool.
            if not recording_safe(self.session.nav):
                tuner_info(self.session,_,'Tuner in use')
                return
            from .warder_tuner_ui import run_with_scan_progress
            return run_with_scan_progress(super().startScan,tlist,flags,feid,*args,**kwargs)

    if recording_safe(session.nav):
        session.open(WarderManualScan)
