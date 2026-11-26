"""Centre navigation and on-demand diagnostics. Workers never modify GUI widgets."""
from threading import Event
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from twisted.internet.threads import deferToThread
from .warder_screen import Screen
from . import warder_dashboard as dashboard
from .warder_centres import legacy_routes, DIAGNOSTICS, description as route_description
from .i18n import for_api, language


# Read-only result routes. Actions changing tuner state or configuration remain
# explicit native screens; graphs and full-size tables remain available in Details.
INLINE_REPORTS=frozenset(('system-overview','system-processes','system-log',
    'tuner-details','transponder-services','storage-overview','storage-categories',
    'network-overview','network-test','service-health','service-ipk','forum-report','17'))
# Explicit actions must never run merely because the cursor passes over them.
MANUAL_INLINE=frozenset(('17','network-test'))
NATIVE_REPORTS=frozenset(('tuner-details','transponder-services'))


def collect_report(kind,tr,cancelled,cpu_order=False):
    if kind=='system-processes':
        from .warder_system_data import process_table
        return process_table(cancelled,cpu_order)
    if kind=='system-log':
        from .warder_system_data import detail_text
        return detail_text('log',tr)
    if kind=='storage-categories':
        from .warder_storage import category_snapshot
        return category_snapshot(cancelled=cancelled)
    if kind=='storage-overview':
        from .warder_storage import report
        return report(tr,False)
    if kind.startswith('network-'):
        from .warder_network import collect, overview_panels, diagnostics
        return overview_panels(collect(include_addresses=True),tr) if kind=='network-overview' else diagnostics(tr,cancelled)
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


def preview_text(kind,value,tr):
    if kind=='system-overview' and isinstance(value,dict):
        lines=[]
        for i,(label,number) in enumerate(zip(('CPU','RAM','Swap','Flash','HDD / SSD / USB','Temperature'),value['values'])):
            title=tr(label)
            if i in (3,4):title+=' · '+tr('free')
            if number is None:shown='—'
            elif i==4:shown='%.1f GiB'%(number/1073741824)
            elif i==5:shown='%.1f °C'%number
            else:shown='%.0f %%'%number
            lines.append(title+'    '+shown)
        health=value['health']
        lines.extend(('',tr('Resource score')+'    '+(str(health['score'])+'/100' if health['score'] is not None else '—'),
                      tr('Measured checks')+'    %d/%d (RAM / Flash)'%health['coverage']))
        return '\n'.join(lines)
    if kind=='system-processes' and isinstance(value,list):
        return '\n'.join('%s   %s   %s MiB'%(pid,name,'—' if rss is None else '%.1f'%(rss/1024))
                         for pid,name,state,rss,cpu in value)
    if kind=='storage-categories' and isinstance(value,list):
        from .warder_storage import category_size
        return '\n'.join('%s    %s%s'%(tr(name),category_size(size,complete),
                         '' if complete else ' · '+tr('Partial result')) for name,size,complete in value)
    if kind=='network-overview' and isinstance(value,tuple):
        return '\n\n'.join(value)
    if kind=='forum-report' and isinstance(value,str) and value:
        from .warder_service import format_preview
        return format_preview(value,tr)
    return value if isinstance(value,str) else ''


def card_result(kind, value, tr):
    """Build truthful, compact card data from the same collectors as Details."""
    if kind=='system-overview' and isinstance(value,dict):
        numbers=value['values']
        if len(numbers)!=6:raise ValueError('system card count')
        cards=[]
        for i,(caption,number) in enumerate(zip(('CPU','RAM','Swap','Flash','HDD / SSD / USB','Temperature'),numbers)):
            title=tr(caption)
            if i in (3,4):title+=' · '+tr('free')
            if number is None:shown='—'
            elif i==4:shown='%.1f GiB'%(number/1073741824)
            elif i==5:shown='%.1f °C'%number
            else:shown='%.0f %%'%number
            meter=round(max(0,min(100,number))) if i<4 and number is not None else None
            note=(str(value.get('disk_mount') or '') if i==4 else
                  str(value.get('temperature_source') or '').rsplit('/',1)[-1] if i==5 else '')
            cards.append((title,shown,meter,note))
        health=value['health']
        summary='%s  %s   ·   %s  %d/%d (RAM / Flash)'%(tr('Resource score'),
            str(health['score'])+'/100' if health['score'] is not None else '—',
            tr('Measured checks'),*health['coverage'])
        if health.get('state') in ('warning','critical'):
            summary+='\n'+tr('Review memory and storage')
        return cards,summary
    if kind=='storage-categories' and isinstance(value,list) and len(value)==6:
        total=sum(size for _,size,_ in value)
        complete=all(done for _,_,done in value)
        from .warder_storage import category_size
        cards=[]
        for name,size,done in value:
            shown=category_size(size,done)
            meter=round(100*size/total) if complete and total else None
            note='' if done else tr('Partial result')
            cards.append((tr(name),shown,meter,note))
        summary=tr('Measured categories total')+': '+('' if complete else '≥ ')+'%.1f MiB'%(total/1048576)
        if not complete:summary+=' · '+tr('Partial result')
        return cards,summary
    return None


def process_rows(api,rows,columns,sx,sy,row_height):
    """One data-to-native-row mapping for the compact and full process tables."""
    content=[]
    for pid,name,state,rss,cpu in rows:
        values=(str(pid),name,str(state),'—' if rss is None else '%.1f'%(rss/1024),
                '—' if cpu is None else '%.1f'%cpu)
        row=[pid]
        for i,((offset,span),value) in enumerate(zip(columns,values)):
            row.append(api['MultiContentEntryText'](
                pos=(round(offset*sx),0),size=(round(span*sx),round(row_height*sy)),
                font=0,text=value,color=0xbcd2df if i==2 else 0xffffff))
        content.append(row)
    return content


class CentreMenu(Screen):
    def __init__(self, session, api, entries, enabled, initial=None):
        self.width, self.height = dashboard.dimensions(api)
        self.skin = dashboard.skin(self.width, self.height, 'menu')
        Screen.__init__(self, session)
        self.api = api
        dashboard.install_header(self,api)
        self.groups = legacy_routes(entries)
        self.enabled = dict(enabled)
        self.group = next((g for g in self.groups if g[0] == initial), None)
        self.direct = initial is not None
        self.native_actions = {}
        self._result_key=None
        self._result_job=None
        self._result_queued=None
        self._result_closed=False
        self._auto_key=None
        self._auto_timer=api['eTimer']()
        signal=getattr(self._auto_timer,'timeout',None)
        if hasattr(signal,'connect'):
            self._auto_connection=signal.connect(self.auto_result)
        elif hasattr(signal,'get'):
            signal.get().append(self.auto_result)
        else:
            self._auto_timer.callback.append(self.auto_result)
        self.onClose.append(self.close_results)
        self['list'] = api['ListboxSys2']([])
        self['list'].l.setFont(0, api['gFont']('Regular', round(28*self.height/1080)))
        self['list'].l.setItemHeight(round(74*self.height/1080))
        self['list'].onSelectionChanged.append(self.describe)
        for name, key in [('heading',''), ('result_title',''), ('result_status',''), ('red','Back'), ('green','Select'), ('yellow',''), ('blue','')]:
            self[name] = Label(for_api(api, key))
        self['descriptions']=ScrollLabel('')
        self.cards_visible=False
        for i in range(6):
            for field in ('bg','name','value','note'):
                self['inline_%s%d'%(field,i)]=Label('')
            self['inline_meter%d'%i]=api['ProgressBar']()
        self['inline_summary']=Label('')
        self['inline_process_list']=api['ListboxSys2']([])
        self['inline_process_list'].l.setFont(0,api['gFont']('Regular',round(24*self.height/1080)))
        self['inline_process_list'].l.setItemHeight(round(42*self.height/1080))
        for i,title in enumerate(('PID','Process Info','S','RAM (MiB)','CPU (%)')):
            self['inline_process_column%d'%i]=Label(for_api(api,title) if i==1 else title)
        self.process_visible=False
        self.hide_cards()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'SetupActions','DirectionActions'],
            {'ok':self.select, 'green':self.select, 'red':self.back, 'back':self.back, 'cancel':self.back,
             'yellow':self.refresh_result,'blue':self.full_result,
             'left':lambda:self.page_result(-1),'right':lambda:self.page_result(1),
             'up':self['list'].up,'down':self['list'].down}, -2)
        self.onLayoutFinish.append(self.render)

    def entries(self):
        if self.group is None:
            return [(key,for_api(self.api,label),'',bool(items)) for key,label,items in self.groups if items]
        rows=[]
        for key,label,description in self.group[2]:
            if key=='tuner-native' and self.native_actions:
                rows.extend((ident,name,for_api(self.api,'A channel backup will be created before opening the tool.'),self.enabled.get(key,False))
                            for ident,(name,action) in self.native_actions.items())
            else:
                rows.append((key,label,description,self.enabled.get(key,False)))
        return rows

    def render(self):
        self.native_actions={}
        if self.group and self.group[0]=='reception' and self.enabled.get('tuner-native',False):
            from .warder_tuners import native_tools
            try:
                self.native_actions={'native:%d'%i:item for i,item in enumerate(native_tools(lambda key:for_api(self.api,key)))}
            except (ImportError,AttributeError,RuntimeError,TypeError):
                pass
        title = for_api(self.api, self.group[1] if self.group else 'GSU Warder Evolution')
        self.setTitle(title)
        self['heading'].setText(title)
        rows = []
        from .warder_menu_icons import pixmap_entry
        sx,sy=self.width/1920,self.height/1080
        for key,label,description,enabled in self.entries():
            project=key in getattr(self,'projects',{})
            tx,tw= (148,476) if project else (72,552)
            iw,ih=(120,58) if project else (48,48)
            row=[key,self.api['MultiContentEntryText'](pos=(round(tx*sx),round(12*sy)),
                size=(round(tw*sx),round(52*sy)),font=0,text=label,
                color=0xffffff if enabled else 0x8291a5)]
            icon=pixmap_entry(self.api,key,(round(12*sx),round((74-ih)*sy/2)),
                              (round(iw*sx),round(ih*sy)),project=project)
            if icon is not None:row.append(icon)
            rows.append(row)
        self['list'].l.setList(rows)
        self.describe()

    def hide_cards(self):
        self.cards_visible=False
        for i in range(6):
            for field in ('bg','name','value','note','meter'):
                self['inline_%s%d'%(field,i)].hide()
        self['inline_summary'].hide()
        self.hide_process_table()
        self['descriptions'].show()

    def hide_process_table(self):
        self.process_visible=False
        self['inline_process_list'].hide()
        self['inline_process_list'].l.setList([])
        for i in range(5):self['inline_process_column%d'%i].hide()

    def show_process_table(self,rows):
        self.hide_cards()
        self['descriptions'].hide()
        self.process_visible=True
        widget=self['inline_process_list']
        widget.l.setList(process_rows(self.api,rows,dashboard.INLINE_PROCESS_COLUMNS,
            self.width/1920,self.height/1080,42))
        widget.moveToIndex(0)
        widget.show()
        for i in range(5):self['inline_process_column%d'%i].show()
        from time import strftime
        self['result_status'].setText('%s · %s %d · RAM ↓'%(strftime('%H:%M:%S'),
            for_api(self.api,'Total:'),len(rows)))

    def page_result(self,direction):
        if self.process_visible:
            widget=self['inline_process_list']
        else:widget=self['descriptions']
        (widget.pageUp if direction<0 else widget.pageDown)()

    def show_cards(self,model):
        cards,summary=model
        self.hide_process_table()
        self['descriptions'].hide()
        self.cards_visible=True
        for i,(title,value,meter,note) in enumerate(cards):
            for field,text in (('name',title),('value',value),('note',note)):
                self['inline_%s%d'%(field,i)].setText(text)
            for field in ('bg','name','value'):
                self['inline_%s%d'%(field,i)].show()
            if meter is None:
                self['inline_meter%d'%i].hide()
                self['inline_note%d'%i].show()
            else:
                self['inline_note%d'%i].hide()
                bar=self['inline_meter%d'%i]
                bar.setValue(meter)
                bar.show()
        self['inline_summary'].setText(summary)
        self['inline_summary'].show()

    def describe(self):
        row = self['list'].getCurrent()
        entry = next((e for e in self.entries() if row and e[0] == row[0]), None)
        description=route_description(row[0],lambda key:for_api(self.api,key),entry[2]) if row and entry else ''
        backup=getattr(self,'_gsu_last_channel_backup',None)
        if row and row[0] in self.native_actions and isinstance(backup,str):
            description+='\n\n'+for_api(self.api,'Verified channel backup')+'\n'+backup
        key=row[0] if row and entry else None
        changed=key!=self._result_key
        if changed:
            self.cancel_result()
            self._result_key=key
            self.hide_cards()
            self['result_status'].setText('')
            self['descriptions'].setText(description)
        elif key in self.native_actions:
            self['descriptions'].setText(description)
        self['result_title'].setText(entry[1] if entry else '')
        inline=self.inline_route(key)
        self['yellow'].setText(for_api(self.api,'Refresh') if inline and key!='17' else '')
        self['blue'].setText(for_api(self.api,'Details') if inline and key!='17' else '')
        if changed and inline and key not in MANUAL_INLINE:
            # Debounce quick cursor movement while keeping all reads off the GUI
            # thread, apart from existing image-owned native component queries.
            self._auto_key=key
            self['result_status'].setText(for_api(self.api,'Loading…'))
            self._auto_timer.start(180,True)

    def auto_result(self):
        key=self._auto_key
        self._auto_key=None
        if key is not None and key==self._result_key and key not in MANUAL_INLINE:
            self.request_result(key)

    def inline_route(self,key):
        return key if key in INLINE_REPORTS and self.enabled.get(key,False) else None

    def collect_inline(self,key,tr,token):
        if key=='17':
            if token.is_set():return ''
            from .warder_tools import run_task
            from .warder_tools_ui import text
            result=run_task('bundle')
            return text(self.api,'Diagnostic bundle created:\n%s\n\nSize: %s KiB\n\nThe file is available on the receiver at the path above.') % (
                result['path'],max(1,(result['bytes']+1023)//1024))
        if key=='system-overview':
            from .warder_system_data import dashboard
            return dashboard(token)
        return collect_report(key,tr,token)

    def cancel_result(self):
        self._auto_timer.stop()
        self._auto_key=None
        self._result_queued=None
        if self._result_job is not None:self._result_job[1].set()

    def close_results(self):
        self._result_closed=True
        self.cancel_result()

    def refresh_result(self):
        key=self._result_key
        if self.inline_route(key) and key!='17':self.request_result(key)

    def full_result(self):
        if self._result_closed:return
        key=self._result_key
        if self.inline_route(key) and key!='17':
            self.cancel_result()
            open_diagnostic(self.session,self.api,key)

    def request_result(self,key):
        if self._result_closed or key!=self._result_key or not self.inline_route(key):return
        self._auto_timer.stop()
        self._auto_key=None
        if self._result_job is not None:
            if self._result_job[0]==key and not self._result_job[1].is_set():return
            self._result_queued=key
            self['result_status'].setText(for_api(self.api,'Loading…'))
            return
        token=Event()
        job=(key,token)
        self._result_job=job
        self.hide_cards()
        self['result_status'].setText(for_api(self.api,'Loading…'))
        self['descriptions'].setText('')
        tr=lambda k:for_api(self.api,k)
        def finish(value,failed=False):
            if self._result_job is not job:return
            self._result_job=None
            if not self._result_closed and not token.is_set() and self._result_key==key:
                model=None
                try:
                    if not failed:model=card_result(key,value,tr)
                    text=preview_text(key,value,tr) if not failed and model is None else ''
                except (ValueError,TypeError,AttributeError,KeyError,OverflowError):
                    model=None
                    text=''
                from time import strftime
                self['result_status'].setText(strftime('%H:%M:%S') if model or text.strip() else tr('Unavailable'))
                if not failed and key=='system-processes' and isinstance(value,list) and value and text.strip():
                    self.show_process_table(value)
                elif model:self.show_cards(model)
                else:
                    self.hide_cards()
                    if failed and key=='17':
                        from .warder_tools_ui import text as tool_text
                        self['descriptions'].setText(tool_text(self.api,'Diagnostic collection failed.'))
                    else:self['descriptions'].setText(text if text.strip() else tr('Unavailable'))
            queued=self._result_queued
            self._result_queued=None
            if queued is not None:self.request_result(queued)
        if key in NATIVE_REPORTS:
            try:
                if key=='tuner-details':
                    from .warder_tuners import details
                    value=details(self.session,self.api,tr)
                else:
                    from enigma import eServiceCenter,eServiceReference
                    from .warder_services import services,display
                    value=display(services(self.session.nav,eServiceCenter.getInstance(),eServiceReference),tr)
                finish(value)
            except (AttributeError,RuntimeError,TypeError,OSError,ImportError,ValueError):
                finish(None,True)
        else:
            def collect():
                return self.collect_inline(key,tr,token)
            try:deferToThread(collect).addCallbacks(finish,lambda failure:finish(None,True))
            except (RuntimeError,TypeError,OSError):finish(None,True)

    def select(self):
        row = self['list'].getCurrent()
        if not row:
            return
        if self.group is None:
            self.group = next((g for g in self.groups if g[0] == row[0]), None)
            self.render()
        elif row[0] in self.native_actions and self.enabled.get('tuner-native',False):
            from .warder_tuners import open_native
            open_native(self.session,lambda key:for_api(self.api,key),self.native_actions[row[0]][1])
        elif self.enabled.get(row[0], False):
            if self.inline_route(row[0]):
                if self._result_key!=row[0]:self.describe()
                self.request_result(row[0])
            elif row[0] in DIAGNOSTICS:
                open_diagnostic(self.session, self.api, row[0])
            elif row[0] in ('0','1'):
                # Open the child above this centre instead of closing the centre
                # and asking the main screen to dispatch it.
                name={'0':'GlassSysInfoBrowser','1':'channelInfoCenter'}[row[0]]
                target=self.api.get(name)
                if callable(target):self.session.open(target)
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
        self.width,self.height=dashboard.dimensions(api)
        mode={'system-processes':'process','storage-categories':'categories','network-overview':'network'}.get(kind,'detail')
        self.skin=dashboard.skin(self.width,self.height,mode)
        Screen.__init__(self, session)
        self.api, self.kind = api, kind
        dashboard.install_header(self,api)
        self['report_status']=Label(for_api(api,'Loading…'))
        self.cancelled = Event()
        self.pending = False
        self.preview = None
        self.services = []
        self.slot_number = None
        self.cpu_order = False
        self.history = []
        self['file_info'] = ScrollLabel('')
        if kind=='system-processes':
            self['process_list']=api['ListboxSys2']([])
            self['process_list'].l.setFont(0,api['gFont']('Regular',round(28*self.height/1080)))
            self['process_list'].l.setItemHeight(round(48*self.height/1080))
            for i,title in enumerate(('PID','Process Info','S','RAM (MiB)','CPU (%)')):
                self['column%d'%i]=Label(self.tr(title) if i==1 else title)
            self.show_process_table(False)
        if kind=='storage-categories':
            for i in range(6):
                for field in ('name','size','state'):
                    self['category_%s%d'%(field,i)]=Label('')
                self['category_meter%d'%i]=api['ProgressBar']()
            self.show_categories(False)
        if kind=='network-overview':
            self.network_focus=0
            self.network_visible=False
            for i in range(2):
                self['network_title%d'%i]=Label('')
                self['network_body%d'%i]=ScrollLabel('')
            self.show_network(False)
        for name, key in [('heading',title), ('red','Back'), ('green','TV' if kind == 'transponder-services' else ''), ('yellow','Refresh'),
                          ('blue','Tuner interfaces' if kind == 'tuner-details' else 'Radio' if kind == 'transponder-services' else 'Save' if kind == 'forum-report' else 'CPU / RAM' if kind == 'system-processes' else '')]:
            self[name] = Label(self.tr(key))
        self['actions'] = ActionMap(['ColorActions','SetupActions','DirectionActions'],
            {'red':self.close,'cancel':self.close,'yellow':self.start,'blue':self.action,'green':lambda:self.export_services('tv'),
             'up':lambda:self.scroll(-1), 'down':lambda:self.scroll(1),
             'left':lambda:self.scroll(-1,True),'right':lambda:self.scroll(1,True)}, -2)
        self.onLayoutFinish.append(self.start)
        self.onClose.append(self.cancelled.set)

    def tr(self, key):
        return for_api(self.api, key)

    def show_process_table(self, visible):
        self.table_visible=bool(visible)
        if self.kind!='system-processes':return
        for key in ('process_list',)+tuple('column%d'%i for i in range(5)):
            (self[key].show if visible else self[key].hide)()
        (self['file_info'].hide if visible else self['file_info'].show)()

    def show_categories(self,visible):
        if self.kind!='storage-categories':return
        for i in range(6):
            for field in ('name','size','state','meter'):
                widget=self['category_%s%d'%(field,i)]
                (widget.show if visible else widget.hide)()
        (self['file_info'].hide if visible else self['file_info'].show)()

    def display_categories(self,rows):
        total=sum(size for _,size,_ in rows)
        complete=all(done for _,_,done in rows)
        from .warder_storage import category_size
        self.show_categories(True)
        for i,(name,size,done) in enumerate(rows):
            self['category_name%d'%i].setText(self.tr(name))
            self['category_size%d'%i].setText(category_size(size,done))
            meter=self['category_meter%d'%i]
            if complete and total:
                share=100*size/total
                meter.setValue(round(share))
                meter.show()
                state='%d %%'%round(share)
            else:
                meter.hide()
                state='—' if done else self.tr('Partial result')
            self['category_state%d'%i].setText(state)
        from time import strftime
        self['report_status'].setText('%s   ·   %s: %.1f MiB%s' %
            (strftime('%H:%M:%S'),self.tr('Measured categories total'),total/1048576,
             '' if complete else ' · '+self.tr('Partial result')))

    def show_network(self,visible):
        if self.kind!='network-overview':return
        self.network_visible=bool(visible)
        for i in range(2):
            for field in ('title','body'):
                widget=self['network_%s%d'%(field,i)]
                (widget.show if visible else widget.hide)()
        (self['file_info'].hide if visible else self['file_info'].show)()

    def network_titles(self):
        titles=(self.tr('Network link'),self.tr('Default gateway')+' · DNS')
        for i,title in enumerate(titles):
            self['network_title%d'%i].setText(('› ' if i==self.network_focus else '  ')+title)

    def display_network(self,panels):
        self.network_focus=0
        for i,body in enumerate(panels):
            self['network_body%d'%i].setText(body or self.tr('Unavailable'))
        self.network_titles()
        self.show_network(True)
        from time import strftime
        self['report_status'].setText(strftime('%H:%M:%S'))

    def scroll(self,direction,page=False):
        if getattr(self,'network_visible',False) is True:
            if page:
                self.network_focus=(self.network_focus+direction)%2
                self.network_titles()
            else:
                widget=self['network_body%d'%self.network_focus]
                (widget.pageUp if direction<0 else widget.pageDown)()
            return
        if getattr(self,'table_visible',False):
            widget=self['process_list']
            method=('pageUp' if direction<0 else 'pageDown') if page else ('up' if direction<0 else 'down')
            getattr(widget,method)()
        else:
            (self['file_info'].pageUp if direction<0 else self['file_info'].pageDown)()

    def display_process_table(self,rows):
        api=self.api
        sx,sy=self.width/1920,self.height/1080
        content=process_rows(api,rows,dashboard.PROCESS_COLUMNS,sx,sy,48)
        self['process_list'].l.setList(content)
        self['process_list'].moveToIndex(0)
        self.show_process_table(True)
        from time import strftime
        self['report_status'].setText('%s   ·   %s %d   ·   %s ↓' %
            (strftime('%H:%M:%S'),self.tr('Total:'),len(rows),'CPU' if self.cpu_order else 'RAM'))

    def start(self):
        if self.pending or self.cancelled.is_set():
            return
        self.pending = True
        self.preview = None
        self.show_process_table(False)
        self.show_categories(False)
        self.show_network(False)
        self['report_status'].setText(self.tr('Loading…'))
        self['file_info'].setText(self.tr('Loading…'))
        if self.kind == 'transponder-services':
            try:
                from enigma import eServiceCenter, eServiceReference
                from .warder_services import services, display
                self.services = services(self.session.nav, eServiceCenter.getInstance(), eServiceReference)
                self.done(display(self.services,self.tr))
            except (RuntimeError, TypeError, ValueError, AttributeError, OSError, ImportError):
                self.services = []
                self.failed(None)
        elif self.kind == 'tuner-details':
            try:
                from .warder_tuners import details
                self.done(details(self.session, self.api, self.tr, self.slot_number))
            except (AttributeError, RuntimeError, TypeError, OSError, ImportError):
                self.failed(None)
        else:
            deferToThread(self.collect).addCallbacks(self.done, self.failed)

    def collect(self):
        return collect_report(self.kind,self.tr,self.cancelled,self.cpu_order)

    def done(self, result):
        self.pending = False
        if self.cancelled.is_set():
            return
        if self.kind=='system-processes' and isinstance(result,list) and result:
            self.display_process_table(result)
            return
        if self.kind=='storage-categories' and isinstance(result,list) and len(result)==6:
            self.display_categories(result)
            return
        if self.kind=='network-overview' and isinstance(result,tuple) and len(result)==2 and all(isinstance(v,str) for v in result):
            self.display_network(result)
            return
        self.show_process_table(False)
        self.show_categories(False)
        self.show_network(False)
        # Never display an empty screen on a missing/empty result. Only a real
        # report may become an export preview.
        if not isinstance(result, str) or not result.strip():
            self['report_status'].setText(self.tr('Unavailable'))
            self['file_info'].setText(self.tr('Unavailable'))
            return
        from time import strftime
        self['report_status'].setText(strftime('%H:%M:%S'))
        if self.kind == 'forum-report':
            from .warder_service import format_preview
            try:
                readable=format_preview(result,self.tr)
            except (ValueError,TypeError,KeyError,AttributeError):
                readable=result
            self.preview = result
            result=readable
        if self.kind == 'network-test':
            from time import strftime
            self.history.insert(0, strftime('%H:%M:%S')+'\n'+result)
            del self.history[8:]
            result = '\n\n'.join(self.history)
        self['file_info'].setText(result)

    def failed(self, failure):
        self.pending = False
        if not self.cancelled.is_set():
            self.show_process_table(False)
            self.show_categories(False)
            self.show_network(False)
            self['report_status'].setText(self.tr('Unavailable'))
            self['file_info'].setText(self.tr('Unavailable'))

    def export_services(self, kind):
        if self.kind != 'transponder-services' or self.pending or self.cancelled.is_set() or not self.services:
            return
        from .warder_services import export
        from .warder_dialog import show_info
        try:
            result = export(self.services,kind)
        except OSError:
            result = None
        show_info(self.session,self.api,result or self.tr('Unavailable'),self.tr('Unavailable') if not result else self.tr('Save'))

    def action(self):
        if self.pending or self.cancelled.is_set():
            return
        if self.kind == 'transponder-services':
            self.export_services('radio')
        elif self.kind == 'tuner-details':
            from .warder_tuners import slots
            from .warder_dialog import choose
            def selected(item):
                if item and not self.cancelled.is_set():
                    self.slot_number = item[1]
                    self.start()
            choose(self.session,self.api,selected,self.tr('Tuner interfaces'),
                   [(self.tr('Overview'),None)]+slots())
        elif self.kind == 'system-processes':
            self.cpu_order = not self.cpu_order
            self.start()
        elif self.kind == 'forum-report' and self.preview is not None:
            from .warder_service import save_preview
            from .warder_dialog import show_info
            try:
                path = save_preview(self.preview)
            except OSError:
                path = self.tr('Unavailable')
            show_info(self.session,self.api,path,self.tr('Save'))


def open_diagnostic(session, api, kind):
    if kind not in DIAGNOSTICS:
        return
    if kind == 'projects':
        session.open(ProjectMenu, api)
    elif kind == 'signal-quick':
        from .warder_quick import QuickSignal
        session.open(QuickSignal, api)
    elif kind == 'system-overview':
        from .warder_overview import Overview
        session.open(Overview, api)
    elif kind in ('system-live', 'signal-live'):
        from .warder_chart import LiveChart
        session.open(LiveChart, api, kind == 'signal-live')
    elif kind == 'tuner-native':
        from .warder_tuners import choose_native
        choose_native(session, lambda value: for_api(api, value))
    else:
        session.open(Report, api, kind, DIAGNOSTICS[kind][0])


class ProjectMenu(CentreMenu):
    def __init__(self, session, api):
        from .warder_projects import PROJECTS
        self.projects = {p[0]:p for p in PROJECTS}
        super().__init__(session,api,(),{},None)

    def entries(self):
        return [(name,name,self.tr('Installed version')+' · '+self.tr('Stable version'),True)
                for name in self.projects]

    def tr(self,key):
        return for_api(self.api,key)

    def render(self):
        super().render()
        self['heading'].setText(self.tr('Warder Evolution centre'))

    def inline_route(self,key):
        return key if key in self.projects else None

    def collect_inline(self,key,tr,token):
        from .warder_projects import report
        config=self.api['config']
        locale=language(config.osd.language.value) if config.plugins.GlassSysUtil.par62.value else 'en'
        return report(tr,locale,token,projects=(self.projects[key],))

    def select(self):
        row=self['list'].getCurrent()
        if row and row[0] in self.projects:
            if self._result_key!=row[0]:self.describe()
            self.request_result(row[0])

    def full_result(self):
        key=self._result_key
        if key in self.projects:
            self.cancel_result()
            self.session.open(ProjectReport,self.api,self.projects[key])


class ProjectReport(Report):
    def __init__(self,session,api,project):
        self.project=project
        super().__init__(session,api,'project',project[0])
        self['blue'].setText(self.tr('Update' if project[0] == 'GSU' else 'Open plugin'))

    def collect(self):
        from .warder_projects import report
        config=self.api['config']
        locale=language(config.osd.language.value) if config.plugins.GlassSysUtil.par62.value else 'en'
        return report(self.tr,locale,self.cancelled,projects=(self.project,))

    def action(self):
        from .warder_projects import entrypoint
        from .warder_dialog import show_info
        if self.project[0] == 'GSU':
            # The canonical in-plugin updater owns check, confirmation and installation.
            from .plugin_update_ui import StartupUpdateCheck
            if not hasattr(self,'update_controller'):
                self.update_controller=StartupUpdateCheck(self,self.api)
            self.update_controller.request(manual=True)
            return
        descriptor=entrypoint(self.project[0])
        if descriptor:
            descriptor(session=self.session)
        else:
            show_info(self.session,self.api,self.tr('Unavailable'),self.project[0])

    def update_status(self, value):
        self['file_info'].setText(value)

    def readVersion(self):
        from .warder_tools import read
        from pathlib import Path
        return read(Path(__file__).with_name('version'),128)
