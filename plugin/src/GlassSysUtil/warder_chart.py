"""On-screen live measurements. Native calls stay on the GUI thread."""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Sources.CanvasSource import CanvasSource
from twisted.internet.threads import deferToThread
from .i18n import for_api
from .warder_dashboard import dimensions, skin
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


def draw(canvas, samples, key, width, height, bound=None):
    canvas.clear()
    canvas.fill(0, 0, width, height, 0x102136)
    for fraction in (0.25, 0.5, 0.75):
        canvas.fill(0, round(fraction*height), width, 1, 0x314b65)
    if samples:
        points = [(stamp, values.get(key)) for stamp, values in samples if values.get(key) is not None]
        floor = min([0] + [v for _, v in points])
        ceiling = bound or max([1] + [v for _, v in points])
        for stamp, value in points:
            x = round((stamp-samples[-1][0]+60) * (width-1)/60)
            bar = max(1, min(height, round((value-floor)/(ceiling-floor)*(height-1))))
            canvas.fill(max(0, min(width-1, x)), height-bar,
                        max(1, min(width-max(0, x), width//80)), bar, 0x34cfce)
    canvas.flush()


class LiveChart(Screen):
    def __init__(self, session, api, signal=False):
        self.width, self.height = dimensions(api)
        self.skin = skin(self.width, self.height, 'chart')
        Screen.__init__(self, session)
        self.api, self.signal = api, signal
        self.source = SignalMonitor(session.nav) if signal else Sampler()
        self.metrics = SIGNAL if signal else SYSTEM
        self.index = 0
        self.interval = 2
        self.closed = self.paused = self.pending = False
        self['history'] = CanvasSource()
        for name, key in [('heading', 'Signal history' if signal else 'Live monitoring'),
                          ('metric', ''), ('details', ''), ('red', 'Back'), ('green', 'Pause'),
                          ('yellow', 'Interval'), ('blue', 'Export CSV' if signal else 'Details')]:
            self[name] = Label(self.tr(key))
        self.timer = api['eTimer']()
        sig = getattr(self.timer, 'timeout', None)
        if hasattr(sig, 'connect'):
            self.connection = sig.connect(self.tick)
        elif hasattr(sig, 'get'):
            sig.get().append(self.tick)
        else:
            self.timer.callback.append(self.tick)
        self['actions'] = ActionMap(['DirectionActions', 'ColorActions', 'SetupActions'],
            {'left': lambda: self.move(-1), 'right': lambda: self.move(1),
             'up': lambda: self.move(-1), 'down': lambda: self.move(1),
             'green': self.pause, 'ok': self.pause, 'yellow': self.change_interval,
             'blue': self.export_or_next, 'red': self.close, 'cancel': self.close}, -2)
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
        key, label, unit = self.metrics[self.index]
        samples = self.source.history.snapshot()
        current = samples[-1][1].get(key) if samples else None
        self['metric'].setText('‹  %s    %s %s  ›' % (self.tr(label), display(current, key), unit))
        low, high, mean = statistics(samples, key)
        stats = '%s  %s     %s  %s     %s  %s' % (self.tr('Minimum'), display(low, key),
                   self.tr('Maximum'), display(high, key), self.tr('Average'), display(mean, key))
        if self.signal:
            stats += '\n%s  %d' % (self.tr('Lock losses'), lock_losses(samples))
        self['details'].setText(stats)
        self['yellow'].setText('%s · %d s' % (self.tr('Interval'), self.interval))
        draw(self['history'], samples, key, round(1730*self.width/1920), round(330*self.height/1080),
             100 if unit == '%' else 1 if key == 'lock' else None)

    def pause(self):
        self.paused = not self.paused
        self.timer.stop()
        self['green'].setText(self.tr('Start' if self.paused else 'Pause'))
        if not self.paused:
            if not self.signal and not self.pending:
                self.source.reset()
            self.tick()

    def move(self, amount):
        self.index = (self.index+amount) % len(self.metrics)
        self.render()

    def change_interval(self):
        choices = (1, 2, 5)
        self.interval = choices[(choices.index(self.interval)+1) % len(choices)]
        self.render()
        if not self.closed and not self.paused and not self.pending:
            self.timer.start(self.interval*1000, True)

    def export_or_next(self):
        if not self.signal:
            self.move(1)
            return
        from Screens.MessageBox import MessageBox
        try:
            message = export(self.source.history.snapshot())
        except OSError:
            message = self.tr('Unavailable')
        self.session.open(MessageBox, message, type=MessageBox.TYPE_INFO)

    def cleanup(self):
        self.closed = True
        self.timer.stop()
