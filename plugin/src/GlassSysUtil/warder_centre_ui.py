"""Centre navigation and on-demand diagnostics. Workers never modify GUI widgets."""
from threading import Event
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from twisted.internet.threads import deferToThread
from .warder_screen import Screen
from . import warder_dashboard as dashboard
from .warder_centres import legacy_routes, DIAGNOSTICS
from .i18n import for_api, language


class CentreMenu(Screen):
    def __init__(self, session, api, entries, enabled, initial=None):
        self.width, self.height = dashboard.dimensions(api)
        self.skin = dashboard.skin(self.width, self.height, 'menu')
        Screen.__init__(self, session)
        self.api = api
        self.groups = legacy_routes(entries)
        self.enabled = dict(enabled)
        self.group = next((g for g in self.groups if g[0] == initial), None)
        self.direct = initial is not None
        self['list'] = api['ListboxSys2']([])
        self['list'].l.setFont(0, api['gFont']('Regular', round(34*self.height/1080)))
        self['list'].l.setItemHeight(round(74*self.height/1080))
        self['list'].onSelectionChanged.append(self.describe)
        for name, key in [('heading',''), ('descriptions',''), ('red','Back'), ('green','Select'), ('yellow',''), ('blue','')]:
            self[name] = Label(for_api(api, key))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'SetupActions'],
            {'ok':self.select, 'green':self.select, 'red':self.back, 'back':self.back, 'cancel':self.back}, -2)
        self.onLayoutFinish.append(self.render)

    def entries(self):
        if self.group is None:
            return [(key,for_api(self.api,label),'',bool(items)) for key,label,items in self.groups if items]
        return [(key,label,description,self.enabled.get(key,False)) for key,label,description in self.group[2]]

    def render(self):
        title = for_api(self.api, self.group[1] if self.group else 'GSU Warder Evolution')
        self.setTitle(title)
        self['heading'].setText(title)
        rows = []
        for key, label, description, enabled in self.entries():
            rows.append([key, self.api['MultiContentEntryText'](pos=(round(20*self.width/1920),round(12*self.height/1080)),
                size=(round(960*self.width/1920),round(52*self.height/1080)), font=0, text=label,
                color=0xffffff if enabled else 0x8291a5)])
        self['list'].l.setList(rows)
        self.describe()

    def describe(self):
        row = self['list'].getCurrent()
        entry = next((e for e in self.entries() if row and e[0] == row[0]), None)
        self['descriptions'].setText(entry[2] if entry else '')

    def select(self):
        row = self['list'].getCurrent()
        if not row:
            return
        if self.group is None:
            self.group = next((g for g in self.groups if g[0] == row[0]), None)
            self.render()
        elif self.enabled.get(row[0], False):
            if row[0] in DIAGNOSTICS:
                open_diagnostic(self.session, self.api, row[0])
            else:
                self.close(row[0])

    def back(self):
        if self.group is not None and not self.direct:
            self.group = None
            self.render()
        else:
            self.close(None)


def open_centre(screen, api, key):
    screen.session.openWithCallback(screen.dispatch_menu_id, CentreMenu, api,
                                    tuple(screen.menuListAll), dict(screen.status), key)


class Report(Screen):
    def __init__(self, session, api, kind, title):
        self.skin = dashboard.skin(*dashboard.dimensions(api), 'detail')
        Screen.__init__(self, session)
        self.api, self.kind = api, kind
        self.cancelled = Event()
        self.pending = False
        self.preview = None
        self.cpu_order = False
        self.history = []
        self['file_info'] = ScrollLabel('')
        for name, key in [('heading',title), ('red','Back'), ('green',''), ('yellow','Refresh'),
                          ('blue','Save' if kind == 'forum-report' else 'CPU / RAM' if kind == 'system-processes' else '')]:
            self[name] = Label(self.tr(key))
        self['actions'] = ActionMap(['ColorActions','SetupActions','DirectionActions'],
            {'red':self.close,'cancel':self.close,'yellow':self.start,'blue':self.action,
             'up':self['file_info'].pageUp, 'down':self['file_info'].pageDown,
             'left':self['file_info'].pageUp,'right':self['file_info'].pageDown}, -2)
        self.onLayoutFinish.append(self.start)
        self.onClose.append(self.cancelled.set)

    def tr(self, key):
        return for_api(self.api, key)

    def start(self):
        if self.pending or self.cancelled.is_set():
            return
        self.pending = True
        self.preview = None
        self['file_info'].setText(self.tr('Loading…'))
        if self.kind == 'tuner-details':
            from .warder_tuners import details
            try:
                self.done(details(self.session, self.api, self.tr))
            except (AttributeError, RuntimeError, TypeError, OSError, ImportError):
                self.failed(None)
        else:
            deferToThread(self.collect).addCallbacks(self.done, self.failed)

    def collect(self):
        kind, tr = self.kind, self.tr
        if kind == 'system-overview':
            from .warder_system_data import overview
            report = overview()
            h = report['health']
            rows = [tr('Resource score')+'    '+('—' if h['score'] is None else '%d/100' % h['score']),
                    tr('Measured checks')+'    %d/%d' % h['coverage'], '']
            for item in report['checks']:
                state = {'ok':'OK','warning':'Warning','critical':'Critical','unknown':'Unavailable'}[item['state']]
                value = item['available_percent']
                rows.append('%s    %s    %s' % (item['name'], tr(state), '—' if value is None else '%.1f %% %s' % (value,tr('free'))))
            rows.append(report['memory']['ram_basis'] or '—')
            if h['state'] in ('critical','warning'):
                rows.extend(('', tr('Review memory and storage')))
            return '\n'.join(rows)
        if kind in ('system-processes','system-log'):
            from .warder_system_data import detail_text, cpu_processes
            if kind == 'system-processes' and self.cpu_order:
                return cpu_processes(tr, self.cancelled)
            return detail_text('log' if kind == 'system-log' else 'processes', tr)
        if kind.startswith('storage-'):
            from .warder_storage import report
            return report(tr, kind == 'storage-categories')
        if kind.startswith('network-'):
            from .warder_network import collect, summary, diagnostics
            return summary(collect(), tr) if kind == 'network-overview' else diagnostics(tr, self.cancelled)
        if kind == 'projects':
            from .warder_projects import report
            locale = language(self.api['config'].osd.language.value) if self.api['config'].plugins.GlassSysUtil.par62.value else 'en'
            return report(tr, locale, self.cancelled)
        if kind == 'forum-report':
            import json
            from .warder_service import forum_snapshot
            return json.dumps(forum_snapshot(), ensure_ascii=False, indent=2)
        if kind == 'service-ipk':
            from .warder_ipk import review
            return review(tr)
        if kind == 'service-health':
            from .warder_service import health
            return health(tr)
        raise ValueError('unknown diagnostic')

    def done(self, result):
        self.pending = False
        if self.cancelled.is_set():
            return
        if self.kind == 'forum-report':
            self.preview = result
        if self.kind == 'network-test':
            from time import strftime
            self.history.insert(0, strftime('%H:%M:%S')+'\n'+result)
            del self.history[8:]
            result = '\n\n'.join(self.history)
        self['file_info'].setText(result)

    def failed(self, failure):
        self.pending = False
        if not self.cancelled.is_set():
            self['file_info'].setText(self.tr('Unavailable'))

    def action(self):
        if self.pending or self.cancelled.is_set():
            return
        if self.kind == 'system-processes':
            self.cpu_order = not self.cpu_order
            self.start()
        elif self.kind == 'forum-report' and self.preview is not None:
            from .warder_service import save_preview
            from Screens.MessageBox import MessageBox
            try:
                path = save_preview(self.preview)
            except OSError:
                path = self.tr('Unavailable')
            self.session.open(MessageBox, path, type=MessageBox.TYPE_INFO)


def open_diagnostic(session, api, kind):
    if kind not in DIAGNOSTICS:
        return
    if kind in ('system-live', 'signal-live'):
        from .warder_chart import LiveChart
        session.open(LiveChart, api, kind == 'signal-live')
    elif kind == 'tuner-native':
        from .warder_tuners import choose_native
        choose_native(session, lambda value: for_api(api, value))
    else:
        session.open(Report, api, kind, DIAGNOSTICS[kind][0])
