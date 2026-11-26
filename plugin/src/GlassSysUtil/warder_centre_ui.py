"""Shared full-screen navigation using the established GSU list skin."""
from .warder_screen import Screen
from .warder_centres import legacy_routes
from .i18n import for_api
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel

class CentreMenu(Screen):
    def __init__(self, session, api, entries, enabled, initial=None):
        self.skin = api['ipkScript_center']
        Screen.__init__(self, session)
        self.api = api
        self.groups = legacy_routes(entries)
        self.enabled = dict(enabled)
        self.group = next((g for g in self.groups if g[0]==initial),None)
        self.direct = initial is not None
        self['list'] = api['ListboxSys2']([])
        self['list'].onSelectionChanged.append(self.describe)
        self['descriptions'] = Label('')
        self['red'] = Label(for_api(api,'Back'))
        self['green'] = Label(for_api(api,'Select'))
        self['actions'] = ActionMap(['WizardActions','ColorActions','SetupActions'],
            {'ok':self.select,'green':self.select,'red':self.back,'back':self.back,'cancel':self.back},-2)
        self.onLayoutFinish.append(self.render)

    def entries(self):
        if self.group is None:
            return [(key,for_api(self.api,label),'',bool(items)) for key,label,items in self.groups if items]
        return [(key,label,description,self.enabled.get(key,False)) for key,label,description in self.group[2]]

    def render(self):
        api=self.api
        self.setTitle(for_api(api,self.group[1] if self.group else 'GSU Warder Evolution'))
        rows=[]
        for key,label,description,enabled in self.entries():
            rows.append([key,api['MultiContentEntryText'](pos=(api['fhd'](25),0),
                size=(api['fhd'](535),api['fhd'](22)),font=0,text=label,
                color=0xffffff if enabled else 0x8291a5)])
        self['list'].l.setList(rows)
        self.describe()

    def describe(self):
        row=self['list'].getCurrent()
        entry=next((e for e in self.entries() if row and e[0]==row[0]),None)
        self['descriptions'].setText(entry[2] if entry else '')

    def select(self):
        row=self['list'].getCurrent()
        if not row:return
        if self.group is None:
            self.group=next((g for g in self.groups if g[0]==row[0]),None)
            self.render()
        elif self.enabled.get(row[0],False):
            self.close(row[0])

    def back(self):
        if self.group is not None and not self.direct:
            self.group=None
            self.render()
        else:self.close(None)

class DetailText(Screen):
    """Shared scrollable detail for processes or logs, not a second collector."""
    def __init__(self,session,api,title,content):
        self.skin=api['oscam_Files_scr2']
        Screen.__init__(self,session)
        self.title_text=title
        self['file_info']=ScrollLabel(content)
        self['red']=Label(for_api(api,'Back'))
        self['actions']=ActionMap(['ColorActions','SetupActions','DirectionActions'],
            {'red':self.close,'cancel':self.close,'up':self['file_info'].pageUp,
             'down':self['file_info'].pageDown,'left':self['file_info'].pageUp,
             'right':self['file_info'].pageDown},-2)
        self.onLayoutFinish.append(self.prepare)
    def prepare(self):self.setTitle(self.title_text)

def open_legacy_centres(screen, api):
    """Keep the parent alive; return a stable action ID to its existing dispatcher."""
    screen.session.openWithCallback(screen.dispatch_menu_id, CentreMenu, api,
                                    tuple(screen.menuListAll), dict(screen.status))


def open_centre(screen, api, key):
    groups = legacy_routes(screen.menuListAll)
    group = next((g for g in groups if g[0]==key and g[2]),None)
    if group is None:return
    screen.session.openWithCallback(screen.dispatch_menu_id, CentreMenu, api,
                                    tuple(screen.menuListAll), dict(screen.status), key)
