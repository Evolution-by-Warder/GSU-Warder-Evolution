"""Living-room overview: six measurements, one action to open live history."""
from threading import Event
from time import monotonic
from Components.ActionMap import ActionMap
from Components.Label import Label
from twisted.internet.threads import deferToThread
from .i18n import for_api
from .warder_dashboard import dimensions, skin, install_header
from .warder_screen import Screen
from .warder_system_data import dashboard

_last_notice = {}


class Overview(Screen):
    def __init__(self, session, api):
        self.skin = skin(*dimensions(api), 'overview')
        Screen.__init__(self, session)
        self.api = api
        install_header(self,api)
        self.cancelled = Event()
        self.pending = False
        for name, label in [('heading','System centre'), ('summary','Loading…'), ('red','Back'),
                            ('green','Live monitoring'), ('yellow','Refresh'), ('blue','Warning')]:
            self[name] = Label(self.tr(label))
        for i, title in enumerate(('CPU', 'RAM', 'Swap', 'Flash', 'HDD / SSD / USB', 'Temperature')):
            self['label%d'%i] = Label(self.tr(title))
            self['value%d'%i] = Label('—')
            if i<4:
                self['meter%d'%i]=api['ProgressBar']()
                self['meter%d'%i].hide()
            else:
                self['sub%d'%i]=Label('')
        self['actions'] = ActionMap(['ColorActions','SetupActions'],
              {'red':self.close,'cancel':self.close,'ok':self.live,'green':self.live,
               'yellow':self.refresh,'blue':self.toggle}, -2)
        self.onLayoutFinish.append(self.refresh)
        self.onClose.append(self.cancelled.set)

    def tr(self, key):
        return for_api(self.api, key)

    def live(self):
        from .warder_chart import LiveChart
        self.session.open(LiveChart, self.api)

    def alerts(self):
        return self.api['config'].plugins.GlassSysUtil.diagnosticAlerts

    def toggle(self):
        setting = self.alerts()
        setting.value = not setting.value
        setting.save()
        self.api['configfile'].save()
        self.show_setting()

    def show_setting(self):
        self['blue'].setText('%s · %s' % (self.tr('Warning'), self.tr('yes' if self.alerts().value else 'no')))

    def refresh(self):
        if self.pending or self.cancelled.is_set():
            return
        self.show_setting()
        self.pending = True
        deferToThread(dashboard, self.cancelled).addCallbacks(self.done, self.failed)

    def done(self, report):
        self.pending = False
        if self.cancelled.is_set() or report is None:
            return
        for i, value in enumerate(report['values']):
            if value is None:
                text = '—'
            elif i == 4:
                text = '%.1f GiB' % (value/1073741824)
            elif i == 5:
                text = '%.1f °C' % value
            else:
                text = '%.0f %%' % value
            self['value%d'%i].setText(text)
            if i<4:
                meter=self['meter%d'%i]
                if value is None:meter.hide()
                else:
                    meter.setValue(round(max(0,min(100,value))))
                    meter.show()
        self['label1'].setText('RAM · '+self.tr('Used(%):').rstrip(':'))
        self['label3'].setText('Flash · '+self.tr('free'))
        self['label4'].setText('HDD / SSD / USB · '+self.tr('free'))
        self['sub4'].setText(str(report.get('disk_mount') or ''))
        self['sub5'].setText(str(report.get('temperature_source') or ''))
        h = report['health']
        score = str(h['score'])+'/100' if h['score'] is not None else '—'
        message = '%s   %s     ·     %s   %d/%d (RAM / Flash)' % (self.tr('Resource score'),score,
                                                      self.tr('Measured checks'),*h['coverage'])
        if h['state'] in ('warning','critical'):
            advice = self.tr('Review memory and storage')
            message += '\n'+advice
            now = monotonic()
            if self.alerts().value and now-_last_notice.get(h['state'],float('-inf')) >= 1800:
                from Screens.MessageBox import MessageBox
                _last_notice[h['state']] = now
                self.session.open(MessageBox, advice, type=MessageBox.TYPE_INFO, timeout=6)
        self['summary'].setText(message)

    def failed(self, failure):
        self.pending = False
        if not self.cancelled.is_set():
            self['summary'].setText(self.tr('Unavailable'))
