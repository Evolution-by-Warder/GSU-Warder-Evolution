"""Delayed startup and optional recovery; all CAM operations run in a worker."""
import json
import os
import shlex
import shutil
import stat
import time
import tempfile
from pathlib import Path

GUARD=Path('/run/gsu-softcam-session.json')
_ACTIVE=None
CHECK_INTERVAL=15
MAX_RETRY_INTERVAL=300


def autocheck_help(api):
    text='Checks the selected native CAM every 15 seconds and restores it if stopped unexpectedly. Manual GSU stop pauses recovery.'
    translated=api['_'](text)
    language=getattr(getattr(getattr(api.get('config'),'osd',None),'language',None),'value','')
    if translated==text and language.startswith('sk'):
        return 'Kontrola vybraného CAM-u každých 15 sekúnd a obnova pri výpadku. Ručné zastavenie v GSU pozastaví obnovu.'
    return translated


def publish_guard(token,enabled):
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',dir=GUARD.parent,prefix='.gsu-softcam-',delete=False) as stream:
            temporary=stream.name
            json.dump({'token':token,'enabled':bool(enabled)},stream)
        os.replace(temporary,GUARD)
    finally:
        if temporary and os.path.exists(temporary):os.unlink(temporary)


def guard_valid(token,periodic=False):
    try:
        state=json.loads(GUARD.read_text())
        return state['token']==token and (not periodic or state['enabled'] is True)
    except (OSError,ValueError,KeyError,TypeError):return False


def log_event(event):
    line='%.3f %s\n' % (time.monotonic(),event)
    print('[GSU autostart] '+line.rstrip(),flush=True)
    # Diagnostic output must never prevent CAM operation or follow a tmp symlink.
    try:
        fd=os.open('/tmp/gsu-softcam-autostart.log',os.O_WRONLY|os.O_CREAT|os.O_APPEND|os.O_NOFOLLOW|os.O_NONBLOCK,0o600)
        try:
            details=os.fstat(fd)
            if stat.S_ISREG(details.st_mode) and details.st_uid==os.geteuid():
                if details.st_size>32768:os.ftruncate(fd,0)
                os.write(fd,line.encode('utf-8'))
        finally:os.close(fd)
    except OSError:pass


def start_if_needed(native,expected,guard=None,periodic=False):
    if guard is not None and not guard_valid(guard,periodic):
        log_event('skipped: automatic request cancelled');return 0
    if native.selected()!=expected:
        log_event('skipped: selection changed');return 0
    active=native.active_name()
    if active:
        log_event('skipped: already running '+active);return 0
    # start_verified rechecks selection and other running native CAMs.
    log_event('starting '+expected)
    result=native.start_verified(expected)
    log_event('started '+expected)
    return result


class DelayedNativeStart:
    def __init__(self,native,timer_factory,container_factory,delay,enabled=lambda:False):
        self.native=native
        self.name=native.selected()
        self.enabled=enabled
        self.container_factory=container_factory
        self.timer=timer_factory()
        self.checkTimer=timer_factory()
        self.cancelled=False
        self.fired=False
        self.inflight=False
        self.busy=0
        self.failures=0
        self.failure_name=None
        self.paused=set()
        self.token=os.urandom(16).hex()
        self.guard_ready=False
        self.delay=max(1,min(30,int(delay)))
        try:self.connection=self.timer.timeout.connect(self.fire)
        except AttributeError:
            signal=self.timer.timeout
            (signal.get() if hasattr(signal,'get') else signal).append(self.fire)
        try:self.check_connection=self.checkTimer.timeout.connect(self.check)
        except AttributeError:
            signal=self.checkTimer.timeout
            (signal.get() if hasattr(signal,'get') else signal).append(self.check)

    def publish(self,new_token=False):
        if new_token:self.token=os.urandom(16).hex()
        try:
            publish_guard(self.token,self.enabled() and not self.cancelled)
            self.guard_ready=True
        except OSError as error:
            self.guard_ready=False
            log_event('automatic control unavailable: '+str(error))

    def configure(self):
        self.failures=0
        self.publish()
        log_event('autocheck '+('enabled interval=15s' if self.enabled() else 'disabled'))
        self.arm_check()

    def arm_check(self):
        self.checkTimer.stop()
        interval=min(MAX_RETRY_INTERVAL,CHECK_INTERVAL*2**self.failures)
        if self.fired and not self.cancelled and self.enabled():self.checkTimer.startLongTimer(interval)

    def schedule(self):
        if not self.name:return False
        self.publish()
        log_event('scheduled '+self.name+' delay='+str(self.delay)+'s')
        self.timer.startLongTimer(self.delay)
        return True

    def fire(self):
        self.timer.stop()
        if self.cancelled or self.fired:return
        self.fired=True
        self.spawn(self.name,False)

    def check(self):
        self.checkTimer.stop()
        if self.cancelled or not self.fired or not self.enabled():return
        name=self.native.selected()
        if not name:
            log_event('autocheck skipped: no selected CAM');self.arm_check();return
        self.spawn(name,True)

    def spawn(self,name,periodic):
        if self.cancelled:return
        if self.busy or self.inflight or name in self.paused:
            log_event('autocheck/start skipped: manual stop or command in progress')
            self.arm_check();return
        if not self.guard_ready:
            self.arm_check();return
        if name!=self.failure_name:
            self.failure_name=name
            self.failures=0
        self.inflight=True
        self.worker_reason='autocheck' if periodic else 'autostart'
        log_event(self.worker_reason+' checking '+name)
        try:
            self.container=self.container_factory()
            container=self.container
            request_token=self.token
            def completed(code):
                if self.container is container:self.finished(code,request_token)
            signal=self.container.appClosed
            try:self.finished_connection=signal.connect(completed)
            except AttributeError:(signal.get() if hasattr(signal,'get') else signal).append(completed)
            command=[shutil.which('python3') or '/usr/bin/python3',str(Path(__file__).with_name('native_softcam.py')),'--'+self.worker_reason,name,'--guard',self.token]
            result=self.container.execute(' '.join(shlex.quote(part) for part in command))
            if result:self.finished(result)
        except Exception as error:
            log_event('worker error: '+str(error))
            self.finished(-1)

    def finished(self,code,request_token=None):
        if not self.inflight:return
        self.inflight=False
        log_event('worker finished code='+str(code))
        if request_token is None or request_token==self.token:
            self.failures=min(5,self.failures+1) if code else 0
            if code:log_event('autocheck retry in=%ss failures=%s' % (min(MAX_RETRY_INTERVAL,CHECK_INTERVAL*2**self.failures),self.failures))
        self.arm_check()

    def cancel(self):
        self.cancelled=True
        self.timer.stop()
        self.checkTimer.stop()
        self.publish(new_token=True)

    def manual_begin(self,name,operation):
        self.failures=0
        was_paused=name in self.paused
        self.busy+=1
        if operation=='stop':self.paused.add(name)
        self.publish(new_token=True)
        return name,operation,was_paused

    def manual_end(self,ticket,success):
        name,operation,was_paused=ticket
        self.busy=max(0,self.busy-1)
        if (success and operation!='stop') or (not success and not was_paused):self.paused.discard(name)
        log_event('manual '+operation+' '+name+' '+('ok' if success else 'failed'))
        self.arm_check()


def manual_begin(name,operation):
    if _ACTIVE:return _ACTIVE,_ACTIVE.manual_begin(name,operation)


def manual_end(ticket,success):
    if ticket:ticket[0].manual_end(ticket[1],success)


def configure(owner):
    controller=getattr(owner,'nativeDelayedStart',None)
    if controller:
        controller.configure()
    else:
        # No live controller may authorize an automatic worker from an old session.
        try:publish_guard(os.urandom(16).hex(),False)
        except OSError as error:log_event('automatic control unavailable: '+str(error))
        log_event('autocheck unavailable: no session controller')


def begin(owner,api):
    global _ACTIVE
    from .native_softcam import NativeSoftcam
    previous=getattr(owner,'nativeDelayedStart',None)
    if previous:previous.cancel()
    if _ACTIVE is not None and _ACTIVE is not previous:_ACTIVE.cancel()
    _ACTIVE=None
    native=NativeSoftcam()
    settings=api['config'].plugins.GlassSysUtil
    owner.nativeDelayedStart=DelayedNativeStart(native,api['eTimer'],api['eConsoleAppContainer'],settings.par48.value,lambda:settings.par50.value)
    _ACTIVE=owner.nativeDelayedStart
    scheduled=owner.nativeDelayedStart.schedule()
    # Keep the controller for a native CAM selected later through the manager.
    # There is no boot request to delay when the session begins without one.
    if not scheduled:owner.nativeDelayedStart.fired=True
    owner.nativeDelayedStart.configure()
    if not scheduled:return False
    # Keep the independent mount checker, even when native CAM handling is used.
    if api['config'].plugins.GlassSysUtil.par57.value!='0':
        owner.cifsNfsTimer=api['eTimer']()
        try:owner.cifsNfsTimer_conn=owner.cifsNfsTimer.timeout.connect(owner.chckCifsNfs)
        except AttributeError:owner.cifsNfsTimer.timeout.get().append(owner.chckCifsNfs)
        owner.chckCifsNfs()
    return True
