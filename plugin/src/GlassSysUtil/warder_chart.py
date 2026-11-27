"""On-screen live measurements. Native calls stay on the GUI thread."""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Sources.CanvasSource import CanvasSource
from twisted.internet.threads import deferToThread
from .i18n import for_api
from .warder_dashboard import dimensions, skin, install_header
from .warder_screen import Screen
from .warder_live import Sampler, statistics
from .warder_signal import SignalMonitor, export, lock_losses

SYSTEM = (('cpu', 'CPU', '%'), ('ram', 'RAM', '%'), ('swap', 'Swap', '%'),
          ('temp', 'Temperature', '°C'), ('rx', 'RX', 'KiB/s'), ('tx', 'TX', 'KiB/s'))
SIGNAL = (('snr', 'SNR', '%'), ('agc', 'AGC', '%'), ('db', 'SNR', 'dB'),
          ('ber', 'BER', ''), ('lock', 'LOCK', ''))


def display(value, key):
    if value is None:
        return '—'
    if key in ('rx', 'tx'):
        return '%.1f' % (value/1024)
    return str(int(value)) if key in ('lock', 'ber') else '%.1f' % value


def chart_scale(samples,key,bound=None):
    values=[v.get(key) for _,v in samples if v.get(key) is not None]
    return min([0]+values), bound if bound is not None else max([1]+values)


def draw(canvas, samples, key, width, height, bound=None):
    canvas.clear()
    canvas.fill(0, 0, width, height, 0x102136)
    for fraction in (0.25, 0.5, 0.75):
        canvas.fill(0, round(fraction*height), width, 1, 0x314b65)
    if samples:
        points = [(stamp, values.get(key)) for stamp, values in samples if values.get(key) is not None]
        floor,ceiling=chart_scale(samples,key,bound)
        for stamp, value in points:
            x = round((stamp-samples[-1][0]+60) * (width-1)/60)
            bar = max(1, min(height, round((value-floor)/(ceiling-floor)*(height-1))))
            canvas.fill(max(0, min(width-1, x)), height-bar,
                        max(1, min(width-max(0, x), width//80)), bar, 0x34cfce)
    canvas.flush()


def draw_trend(canvas,samples,key,width,height,bound=None,interval=2):
    """Small native plots, real timestamps, no interpolated missing observations."""
    canvas.clear()
    canvas.fill(0,0,width,height,0x102136)
    for fraction in (0.25,0.5,0.75):
        canvas.fill(0,min(height-1,round(fraction*height)),width,1,0x314b65)
    floor,ceiling=chart_scale(samples,key,bound)
    previous=None
    latest=samples[-1][0] if samples else 0
    line=getattr(canvas,'line',None)
    for stamp,values in samples:
        value=values.get(key)
        if value is None:
            previous=None
            continue
        x=max(0,min(width-1,round((stamp-latest+60)*(width-1)/60)))
        y=max(0,min(height-1,height-1-round((value-floor)/(ceiling-floor)*(height-1))))
        if previous and stamp-previous[0]<=max(2,interval*2.5) and callable(line):
            line(previous[1],previous[2],x,y,0x34cfce)
        canvas.fill(max(0,x-1),max(0,y-1),min(3,width-max(0,x-1)),min(3,height-max(0,y-1)),0x34cfce)
        previous=(stamp,x,y)
    canvas.flush()


class LiveChart(Screen):
    def __init__(self, session, api, signal=False):
        self.width, self.height = dimensions(api)
        self.skin = skin(self.width, self.height, 'signal-multichart' if signal else 'multichart')
        Screen.__init__(self, session)
        self.api, self.signal = api, signal
        install_header(self,api)
        self.source = SignalMonitor(session.nav) if signal else Sampler()
        self.metrics = SIGNAL if signal else SYSTEM
        self.interval = 2
        self.closed = self.paused = self.pending = False
        for name, key in [('heading', 'Signal history' if signal else 'Live monitoring'),
                          ('red', 'Back'), ('green', 'Pause'), ('yellow', 'Interval'),
                          ('blue', 'Export CSV' if signal else '')]:
            self[name] = Label(self.tr(key))
        self['window']=Label('−60 s → 0 s')
        for i,(key,caption,unit) in enumerate(self.metrics):
            self['plot%d'%i]=CanvasSource()
            self['metric_name%d'%i]=Label(self.tr(caption)+(' · '+unit if key in ('snr','db') else ''))
            self['metric_value%d'%i]=Label('— '+unit if unit else '—')
            self['plot_top%d'%i]=Label('—')
            self['plot_bottom%d'%i]=Label('—')
            for k,name in enumerate(('Minimum','Maximum','Average')):
                self['stat_name%d_%d'%(i,k)]=Label(self.tr(name))
                self['stat_value%d_%d'%(i,k)]=Label('—')
        if signal:
            self['signal_summary_title']=Label(self.tr('Lock losses'))
            self['signal_loss_count']=Label('—')
            self['signal_lock_state']=Label('—')
            self['signal_summary_note']=Label('—')
        self.timer = api['eTimer']()
        sig = getattr(self.timer, 'timeout', None)
        if hasattr(sig, 'connect'):
            self.connection = sig.connect(self.tick)
        elif hasattr(sig, 'get'):
            sig.get().append(self.tick)
        else:
            self.timer.callback.append(self.tick)
        self['actions'] = ActionMap(['DirectionActions', 'ColorActions', 'SetupActions'],
            {'green': self.pause, 'ok': self.pause, 'yellow': self.change_interval,
             'blue': self.export_or_next, 'red': self.close, 'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.render)
        self.onLayoutFinish.append(self.tick)
        self.onClose.append(self.cleanup)

    def tr(self, value):
        return for_api(self.api, value)

    def tick(self):
        if self.closed or self.paused or self.pending:
            return
        self.pending = True
        if self.signal:
            try:
                self.source.sample()
            except (AttributeError, RuntimeError, OSError, TypeError):
                self.source.history.append({})
            self.complete(None)
        else:
            deferToThread(self.source.sample).addCallbacks(self.complete, self.failed)

    def failed(self, failure):
        if not self.closed:
            self.source.history.append({})
        self.complete(None)

    def complete(self, unused):
        self.pending = False
        if self.closed or self.paused:
            return
        self.render()
        self.timer.start(self.interval*1000, True)

    def render(self):
        # A worker owns the system sampler until the deferred has fired.
        if self.pending or self.closed:
            return
        samples = self.source.history.snapshot()
        self['yellow'].setText('%s · %d s' % (self.tr('Interval'),self.interval))
        self.render_all(samples)

    def render_all(self,samples):
        for i,(key,caption,unit) in enumerate(self.metrics):
            current=samples[-1][1].get(key) if samples else None
            self['metric_value%d'%i].setText((display(current,key)+' '+unit).rstrip())
            bound=100 if unit=='%' else 1 if key=='lock' else None
            low_axis,high_axis=chart_scale(samples,key,bound)
            self['plot_top%d'%i].setText(display(high_axis,key))
            self['plot_bottom%d'%i].setText(display(low_axis,key))
            for k,value in enumerate(statistics(samples,key)):
                # An average of binary lock or integer errors is not necessarily integer.
                shown='%.1f'%value if k==2 and key in ('lock','ber') and value is not None else display(value,key)
                self['stat_value%d_%d'%(i,k)].setText(shown)
            draw_trend(self['plot%d'%i],samples,key,round(440*self.width/1920),
                       round(140*self.height/1080),bound,self.interval)
        if self.signal:
            valid=any(v.get('lock') is not None for _,v in samples)
            latest=samples[-1][1].get('lock') if samples else None
            losses=lock_losses(samples)
            self['signal_loss_count'].setText(str(losses) if valid else '—')
            self['signal_lock_state'].setText('LOCK   '+display(latest,'lock'))
            if latest==0:note=self.tr('No signal lock')
            elif losses:note=self.tr('Unstable reception')
            else:note='—'
            self['signal_summary_note'].setText(note)

    def pause(self):
        self.paused = not self.paused
        self.timer.stop()
        self['green'].setText(self.tr('Start' if self.paused else 'Pause'))
        if not self.paused:
            if not self.signal and not self.pending:
                self.source.reset()
            self.tick()

    def change_interval(self):
        choices = (1, 2, 5)
        self.interval = choices[(choices.index(self.interval)+1) % len(choices)]
        self.render()
        if not self.closed and not self.paused and not self.pending:
            self.timer.start(self.interval*1000, True)

    def export_or_next(self):
        if not self.signal:return
        from .warder_dialog import show_info
        try:
            message = export(self.source.history.snapshot())
        except OSError:
            message = self.tr('Unavailable')
        show_info(self.session,self.api,message,self.tr('Export CSV'))

    def cleanup(self):
        self.closed = True
        self.timer.stop()
