"""Small non-retuning signal overlay with an opt-in, bounded PulseAudio tone."""
import math
import shutil
import struct
import subprocess
from threading import Event, Lock
from xml.etree import ElementTree as ET
from Components.Label import Label
from Components.ActionMap import ActionMap
from twisted.internet.threads import deferToThread
from .i18n import for_api
from .warder_screen import Screen
from .warder_dashboard import dimensions
from .warder_signal import SignalMonitor


def mini_skin(w, h):
    sx, sy = w/1920, h/1080
    root = ET.Element('screen', name='GSUQuickSignal', position='%d,%d'%(round(50*sx),round(65*sy)),
                      size='%d,%d'%(round(775*sx),round(236*sy)), flags='wfNoBorder', backgroundColor='#00102136')
    for name, x, y, width, height, size, color in (
            ('title',25,13,725,51,32,'#0034cfce'), ('level',25,68,725,84,43,'#00ffffff'),
            ('audio',25,158,725,66,26,'#0045b9ff')):
        ET.SubElement(root, 'widget', name=name, position='%d,%d'%(round(x*sx),round(y*sy)),
                      size='%d,%d'%(round(width*sx),round(height*sy)), font='Regular;%d'%round(size*sy),
                      foregroundColor=color, backgroundColor='#00102136', valign='center')
    return ET.tostring(root,encoding='unicode')


class Tone:
    def __init__(self):
        self.command = shutil.which('paplay')
        self.gate = Lock()
        self.stop = Event()
        self.process = None

    def play(self, level):
        if not self.command or self.stop.is_set() or not self.gate.acquire(False):
            return
        try:
            if self.stop.is_set():
                return
            hz = 330+round(6*max(0,min(100,level)))
            pcm = b''.join(struct.pack('<h',round(1800*math.sin(2*math.pi*hz*i/8000)))
                           for i in range(640))
            self.process = subprocess.Popen([self.command,'--raw','--rate=8000','--format=s16le','--channels=1'],
                                            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            if self.stop.is_set():
                self.process.kill()
            try:
                self.process.communicate(pcm,timeout=0.8)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.communicate()
            return self.process.returncode == 0
        except OSError:
            return False
        finally:
            self.process = None
            self.gate.release()

    def close(self):
        self.stop.set()
        task = self.process
        if task is not None:
            try:
                task.terminate()
            except OSError:
                pass


class QuickSignal(Screen):
    def __init__(self, session, api):
        self.skin = mini_skin(*dimensions(api))
        Screen.__init__(self,session)
        self.api = api
        self.source = SignalMonitor(session.nav)
        self.tone = Tone()
        self.sound = self.closed = self.busy = False
        self['title'] = Label(for_api(api,'Signal'))
        self['level'] = Label('—')
        self['audio'] = Label('')
        self['actions'] = ActionMap(['ColorActions','SetupActions'],{'blue':self.toggle,
             'ok':self.close,'red':self.close,'cancel':self.close},-2)
        self.timer = api['eTimer']()
        sig = getattr(self.timer,'timeout',None)
        if hasattr(sig,'connect'):
            self.connection = sig.connect(self.tick)
        elif hasattr(sig,'get'):
            sig.get().append(self.tick)
        else:
            self.timer.callback.append(self.tick)
        self.onLayoutFinish.append(self.tick)
        self.onClose.append(self.cleanup)

    def toggle(self):
        self.sound = bool(self.tone.command) and not self.sound
        self.audio_label()

    def audio_label(self):
        key = ('yes' if self.sound else 'no') if self.tone.command else 'Unavailable'
        self['audio'].setText(for_api(self.api,'Audio:')+' '+for_api(self.api,key))

    def tick(self):
        if self.closed:
            return
        self.audio_label()
        try:
            v = self.source.sample()
        except (AttributeError,RuntimeError,OSError,TypeError):
            v = {}
        snr, db, lock = v.get('snr'), v.get('db'), v.get('lock')
        self['level'].setText('SNR   %s    %s    LOCK   %s' % ('—' if snr is None else '%.0f %%' % snr,
                              '—' if db is None else '%.1f dB' % db, '—' if lock is None else str(lock)))
        if self.sound and not self.busy and snr is not None and lock == 1:
            self.busy = True
            deferToThread(self.tone.play,snr).addBoth(self.finished)
        self.timer.start(1000,True)

    def finished(self,success):
        self.busy = False
        if not self.closed and success is False:
            self.sound = False
            self.audio_label()

    def cleanup(self):
        self.closed = True
        self.timer.stop()
        self.tone.close()
