"""One delayed native CAM check per Enigma session; no GUI-thread start/stop."""
import os
import shlex
import shutil
import stat
import time
from pathlib import Path


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


def start_if_needed(native,expected):
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
    def __init__(self,native,timer_factory,container_factory,delay):
        self.name=native.selected()
        self.container_factory=container_factory
        self.timer=timer_factory()
        self.cancelled=False
        self.fired=False
        self.delay=max(1,min(30,int(delay)))
        try:self.connection=self.timer.timeout.connect(self.fire)
        except AttributeError:
            signal=self.timer.timeout
            (signal.get() if hasattr(signal,'get') else signal).append(self.fire)

    def schedule(self):
        if not self.name:return False
        log_event('scheduled '+self.name+' delay='+str(self.delay)+'s')
        self.timer.startLongTimer(self.delay)
        return True

    def fire(self):
        self.timer.stop()
        if self.cancelled or self.fired:return
        self.fired=True
        self.container=self.container_factory()
        signal=self.container.appClosed
        try:self.finished_connection=signal.connect(self.finished)
        except AttributeError:(signal.get() if hasattr(signal,'get') else signal).append(self.finished)
        command=[shutil.which('python3') or '/usr/bin/python3',str(Path(__file__).with_name('native_softcam.py')),'--autostart',self.name]
        try:
            result=self.container.execute(' '.join(shlex.quote(part) for part in command))
            if result:self.finished(result)
        except Exception as error:
            log_event('worker error: '+str(error))

    def finished(self,code):
        log_event('worker finished code='+str(code))

    def cancel(self):
        self.cancelled=True
        self.timer.stop()


def begin(owner,api):
    from .native_softcam import NativeSoftcam
    previous=getattr(owner,'nativeDelayedStart',None)
    if previous:previous.cancel()
    native=NativeSoftcam()
    if not native.selected():return False
    owner.nativeDelayedStart=DelayedNativeStart(native,api['eTimer'],api['eConsoleAppContainer'],api['config'].plugins.GlassSysUtil.par48.value)
    owner.nativeDelayedStart.schedule()
    # Keep the independent mount checker, even when native CAM handling is used.
    if api['config'].plugins.GlassSysUtil.par57.value!='0':
        owner.cifsNfsTimer=api['eTimer']()
        try:owner.cifsNfsTimer_conn=owner.cifsNfsTimer.timeout.connect(owner.chckCifsNfs)
        except AttributeError:owner.cifsNfsTimer.timeout.get().append(owner.chckCifsNfs)
        owner.chckCifsNfs()
    return True
