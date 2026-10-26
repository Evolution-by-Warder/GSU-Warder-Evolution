"""One native Screen for OSCam navigation and its original data controllers.

Controllers only own Python components; the workspace owns their native widgets.
No controller is opened as a Session dialog. Requests and account actions retain
original implementations; timers and action maps are gated by the active pane.
"""
from copy import deepcopy
from types import FunctionType
from textwrap import wrap
from xml.etree import ElementTree as ET
from Screens.Screen import Screen
from . import warder_main as main, warder_system

CLASSES = {'intro':'oscamInfo','servers':'oscamInfoChoiceServer',
           'summary':'oscam_Summary','readers':'oscam_readers','users':'oscam_Users',
           'log':'oscam_logInfo','files':'oscam_Files','file':'oscam_Files_detailed',
           'entitlements':'oscam_entitlements'}
TITLES = dict(intro='OScam Information',servers='Select Server',summary='Summary Info',
              readers='Servers Status',users='Clients Status',log='Log view',
              files='Config Files',file='OScam File',entitlements='Entitlements')
FOOTERS = {'red':(55,'#00ff526a'),'green':(665,'#0039ff59'),
           'blue':(1275,'#0045b9ff'),'blue_button':(1275,'#0045b9ff')}


class Signal:
    def __init__(self):self.callbacks=[]
    def connect(self,callback):self.callbacks.append(callback);return callback
    def get(self):return self.callbacks


class PaneTimer:
    def __init__(self,pane):
        self.pane=pane;self.timeout=Signal();self.callback=self.timeout.callbacks
        self.native=pane.host.api['eTimer']();self.request=None
        signal=getattr(self.native,'timeout',None)
        if signal is not None and hasattr(signal,'connect'):self.connection=signal.connect(self.fire)
        elif signal is not None and hasattr(signal,'get'):signal.get().append(self.fire)
        else:self.native.callback.append(self.fire)
    def fire(self):
        if self.pane.active and not self.pane.host.closed:
            for callback in list(self.callback):callback()
            self.pane.host.footer()
    def start(self,*args):
        self.request=('start',args)
        if self.pane.active and not self.pane.host.closed:getattr(self.native,'start')(*args)
    def startLongTimer(self,*args):
        self.request=('startLongTimer',args)
        if self.pane.active and not self.pane.host.closed:self.native.startLongTimer(*args)
    def isActive(self):return bool(self.request and self.pane.active)
    def pause(self):
        if self.native is not None:self.native.stop()
    def stop(self):self.pause();self.request=None
    def close(self):self.stop();self.callback.clear();self.connection=None;self.native=None


class PaneSession:
    def __init__(self,pane):self.pane=pane
    def __getattr__(self,name):return getattr(self.pane.host.session,name)
    def open(self,target,*args,**kwargs):
        host=self.pane.host
        if host.closed:return
        for kind,name in CLASSES.items():
            if target is host.api[name]:return host.navigate(kind,*args)
        return host.session.open(target,*args,**kwargs)
    def openWithCallback(self,callback,target,*args,**kwargs):
        host=self.pane.host
        def done(*values):
            if not host.closed:callback(*values);host.footer()
        return host.session.openWithCallback(done,target,*args,**kwargs)


class Pane:
    def __init__(self,host,kind):
        self.host,self.kind,self.active=host,kind,False
        self.timers=[];self.widgets={};self.wanted={};self.actions=[];self.loaded=False
        api=dict(host.api)
        def timer():
            result=PaneTimer(self);self.timers.append(result);return result
        api['eTimer']=timer
        api['MultiContentEntryText']=self.text
        api['MultiContentEntryPixmapAlphaTest']=self.pixmap
        original=host.api[CLASSES[kind]]
        methods={}
        for name,value in vars(original).items():
            if isinstance(value,FunctionType):
                cloned=FunctionType(value.__code__,api,name,value.__defaults__,value.__closure__)
                cloned.__kwdefaults__=value.__kwdefaults__;methods[name]=cloned
        methods['close']=lambda model,*args:host.back()
        methods['setTitle']=lambda model,title:self.set_title(title)
        controller=type('Pane_'+kind,(original,),methods)
        proxy=PaneSession(self)
        if kind in ('intro','servers'):args=()
        elif kind=='file':args=('http://127.0.0.1:8888/','','','')
        elif kind=='entitlements':args=('http://127.0.0.1:8888/','','','')
        else:args=('http://127.0.0.1:8888/','','')
        self.model=controller(proxy,*args)
        self.xml=ET.fromstring(self.model.skin)
        self.list_node=next((n for n in self.xml if n.get('name') in ('list','log_info','entitlements_list')),None)
        self.old_width=int(self.list_node.get('size').split(',')[0]) if self.list_node is not None else host.width
        for name,component in list(self.model.items()):
            if isinstance(component,host.api['ActionMap']):
                self.actions.append(component);component.setEnabled(False)
                host[kind+'_'+name]=component
            elif self.xml.find("widget[@name='%s']"%name) is not None:
                self.widgets[name]=component;host[kind+'_'+name]=component
                self.wanted[name]=getattr(component,'visible',True)
                self.wrap_visibility(name,component)
                if kind=='log' and name=='log_info':
                    selection=component.selectionEnabled
                    component.selectionEnabled=lambda enabled,selection=selection:selection(1)
                if name in FOOTERS and name!='red':
                    original_set=component.setText
                    def set_text(value,original_set=original_set):
                        original_set(value)
                        if host.ready:host.footer()
                    component.setText=set_text
    def set_title(self,title):
        if self.active:self.host['pane_title'].setText(title)
    def wrap_visibility(self,name,component):
        show,hide=component.show,component.hide
        def visible():
            self.wanted[name]=True
            if self.active:show()
        def hidden():self.wanted[name]=False;hide()
        component.show=visible;component.hide=hidden
    def text(self,**kwargs):
        data=dict(kwargs);x,y=data.get('pos',(0,0));w,h=data.get('size',(0,0))
        scale=(690 if self.kind in ('intro','servers') else 1010)*self.host.sx/self.old_width
        data['pos']=(round(x*scale),y)
        available=round((690 if self.kind in ('intro','servers') else 1010)*self.host.sx)-data['pos'][0]
        data['size']=(max(1,min(round(w*scale),available)),h)
        if self.kind=='log':
            lines=wrap(str(data.get('text','')),width=100,replace_whitespace=False,drop_whitespace=False) or ['']
            data['text']='\n'.join(lines);data['font']=1
            height=round(max(42,len(lines)*24)*self.host.sy)
            self.log_height=max(getattr(self,'log_height',0),height)
            self.model['log_info'].l.setItemHeight(self.log_height)
            data['size']=(data['size'][0],height)
        if self.kind=='entitlements':
            base=self.host.api['fhd']
            # Original rows have eight or nine fields. Reflow into readable cards.
            columns=self.model.allLabelsCRD if getattr(self,'card',False) else self.model.allLabels
            if x in (base(20),base(30)):self.card=(x==base(30));self.field=0;columns=self.model.allLabelsCRD if self.card else self.model.allLabels
            index=getattr(self,'field',0);self.field=index+1
            data.update(pos=(round((index%2)*500*self.host.sx),round((index//2)*30*self.host.sy)),
                        size=(round(495*self.host.sx),round(30*self.host.sy)),font=0,
                        text=columns[min(index,len(columns)-1)]+': '+str(data.get('text','')))
        return self.host.api['MultiContentEntryText'](**data)
    def pixmap(self,**kwargs):
        data=dict(kwargs);scale=(690 if self.kind in ('intro','servers') else 1010)*self.host.sx/self.old_width
        x,y=data['pos'];w,h=data['size'];data['pos']=(round(x*scale),y);data['size']=(round(w*scale),h)
        return self.host.api['MultiContentEntryPixmapAlphaTest'](**data)
    def pause(self):
        self.active=False
        for timer in self.timers:timer.pause()
        for action in self.actions:action.setEnabled(False)
        for component in self.widgets.values():
            if component.instance is not None:component.instance.hide()
    def resume(self):
        self.active=True
        # Original exit handlers may clear their timer or mark async controllers closed.
        for name in ('readersClosed','clientsClosed'):
            if hasattr(self.model,name):setattr(self.model,name,False)
        if getattr(self.model,'refreshTimer','missing') is None and self.timers:self.model.refreshTimer=self.timers[0]
        for name,component in self.widgets.items():
            if name not in FOOTERS and self.wanted[name]:component.show()
        if self.kind=='intro' and self.loaded:
            for timer in self.timers:
                if timer.request:getattr(timer,timer.request[0])(*timer.request[1])
        else:
            for callback in self.model.onLayoutFinish:
                if not self.active:break
                callback()
        self.loaded=True


def skin(host):
    sx,sy=host.sx,host.sy
    root=ET.fromstring(main.main_skin(host.width,host.height))
    header={'day','date','clock','seconds','version_title','version'}
    for node in list(root):
        if node.get('name') in header:continue
        if node.tag=='ePixmap' and node.get('position')=='0,0':node.set('zPosition','-3');continue
        y=int(node.get('position','0,0').split(',')[1])
        if y>=round(164*sy):root.remove(node)
    root.set('name','WarderOscamWorkspace')
    def box(node,x,y,w,h):
        node.set('position','%d,%d'%(round(x*sx),round(y*sy)))
        node.set('size','%d,%d'%(round(w*sx),round(h*sy)))
    for x,w in ((55,1050),(1135,730)):
        for dx,dy,dw,dh,color,z in ((x,180,w,800,main.CYAN,-2),(x+2,182,w-4,796,main.PANEL,-1)):
            n=ET.SubElement(root,'eLabel',backgroundColor=color,zPosition=str(z));box(n,dx,dy,dw,dh)
    for kind,pane in host.panes.items():
        for source in pane.xml:
            name=source.get('name')
            if name not in pane.widgets:continue
            n=deepcopy(source);n.set('name',kind+'_'+name)
            for attribute in ('shadowColor','shadowOffset'):n.attrib.pop(attribute,None)
            n.set('backgroundColor',main.PANEL);n.set('transparent','0');n.set('zPosition','3')
            if name in FOOTERS:
                x,color=FOOTERS[name];box(n,x,1006,590,50)
                n.set('foregroundColor',color);n.set('backgroundColor',main.BASE)
                n.set('halign','center');n.set('font','Regular;%d'%round(26*sy))
            elif name in ('list','log_info','entitlements_list'):
                if kind in ('intro','servers'):bounds=(1155,255,690,665)
                elif kind in ('summary','users'):bounds=(75,255,1010,350)
                elif kind=='readers':bounds=(75,255,1010,450)
                elif kind=='entitlements':bounds=(75,360,1010,600)
                else:bounds=(75,255,1010,700)
                box(n,*bounds)
            elif name=='server_name':box(n,90,255,980,300);n.set('font','Regular;%d'%round(28*sy))
            elif name=='logo':box(n,450,575,220,132);n.set('scale','1')
            elif name=='info':box(n,90,760,980,190);n.set('font','Regular;%d'%round(23*sy))
            elif name=='file_info':box(n,75,255,1010,700);n.set('font','Regular;%d'%round(21*sy))
            elif name=='Crd_info':box(n,255,250,820,90);n.set('font','Regular;%d'%round(22*sy))
            elif name=='Crd_system':box(n,90,250,150,90);n.set('scale','1')
            elif name.startswith('status_'):
                column=int(name[-1]);labels='_labels_' in name
                # Three columns, readable labels above counters rather than overlaps.
                x=80+column*(500 if kind=='readers' else 335)
                y=755 if kind=='readers' else 640
                w=480 if kind=='readers' else 325
                if kind=='readers':box(n,x,y+(65 if not labels else 0),w,100)
                else:box(n,x+(0 if labels else 110),y,110 if labels else 215,290)
                n.set('font','Regular;%d'%round((20 if kind=='readers' else 18)*sy))
            elif name.startswith('server_detailed_'):
                box(n,90 if name.endswith('labels') else 310,300,210 if name.endswith('labels') else 760,350)
                n.set('font','Regular;%d'%round(25*sy))
            else:
                # Entitlement column labels are replaced by each card's field names.
                box(n,75,250,1,1)
            root.append(n)
    for name,x,y,w,h,color,font in (('pane_title',80,200,1000,42,main.CYAN,28),('menu_title',1160,200,680,42,main.CYAN,28),('focus_hint',1160,925,680,40,'#00d1e3f3',21),('red',55,1006,590,50,'#00ff526a',28),('green',665,1006,590,50,'#0039ff59',28)):
        n=ET.SubElement(root,'widget',name=name,font='Regular;%d'%round(font*sy),foregroundColor=color,backgroundColor=main.BASE if y>980 else main.PANEL,transparent='0',zPosition='4',halign='center',valign='center');box(n,x,y,w,h)
    for x,color in ((250,'#00ff526a'),(860,'#0039ff59'),(1470,'#0045b9ff')):
        n=ET.SubElement(root,'eLabel',backgroundColor=color,zPosition='2');box(n,x,996,200,2)
    return ET.tostring(root,encoding='unicode')


class OscamWorkspace(Screen):
    def __init__(self,session,api,select_server=False):
        Screen.__init__(self,session)
        self.api=api;self.closed=False;self.ready=False;self.current='intro';self.history=[];self.menu_focus=True
        size=api['getDesktop'](0).size();self.width,self.height=size.width(),size.height();self.sx,self.sy=self.width/1920,self.height/1080
        self.panes={kind:Pane(self,kind) for kind in CLASSES}
        for name in ('pane_title','menu_title','focus_hint','red','green'):self[name]=api['Label']('')
        self['red'].setText(main.text(api,'Back'));self['green'].setText(main.text(api,'Select with OK'))
        self['menu_title'].setText(main.text(api,'OScam Information'))
        self['workspace_actions']=api['ActionMap'](['ColorActions','SetupActions','WizardActions','DirectionActions'],
            {'red':self.back,'cancel':self.back,'back':self.back,'left':self.left,'right':self.right,
             'up':lambda:self.move(-1),'down':lambda:self.move(1),'ok':self.choose,'green':self.choose,
             'blue':self.color,'yellow':self.color},-10)
        self.skin=skin(self);warder_system.install(self,api)
        self.onLayoutFinish.append(lambda:self.begin(select_server));self.onClose.append(self.shutdown)
    def begin(self,select_server=False):
        self.ready=True
        for pane in self.panes.values():
            for name in ('list','log_info','entitlements_list'):
                if name in pane.widgets:
                    widget=pane.widgets[name]
                    for index in (0,1):widget.l.setFont(index,self.api['gFont']('Regular',round((20 if pane.kind=='entitlements' else 26)*self.sy)))
                    widget.l.setItemHeight(round((160 if pane.kind=='entitlements' else 42)*self.sy))
                    if pane.kind=='log':widget.l.setFont(1,self.api['gFont']('Regular',round(18*self.sy)))
        self.activate('servers' if select_server else 'intro')
    def activate(self,kind):
        for pane in self.panes.values():pane.pause()
        self.current=kind;self.menu_focus=kind in ('intro','servers')
        self['pane_title'].setText(main.text(self.api,TITLES[kind]))
        pane=self.panes[kind];pane.resume()
        if self.current!=kind:return
        if kind not in ('intro','servers'):
            widget=self.panes['intro'].model['list']
            if widget.instance is not None:widget.instance.show()
        self.focus(self.menu_focus)
    def focus(self,menu):
        self.menu_focus=menu
        pane=self.panes[self.current]
        for action in pane.actions:action.setEnabled(not menu)
        if self.current=='servers':
            for action in pane.actions:action.setEnabled(False)
        self['focus_hint'].setText('◀ '+main.text(self.api,'Details') if menu else main.text(self.api,'Menu')+' ▶')
        self.footer()
        kind='servers' if self.current=='servers' else ('intro' if menu else self.current)
        model=self.panes[kind].model
        name=next((n for n in ('list','log_info','entitlements_list','file_info') if n in model),None)
        if name and getattr(self,'instance',None) is not None:self.setFocus(model[name])
    def footer(self):
        if not self.ready:return
        for pane in self.panes.values():
            for name,component in pane.widgets.items():
                if name in FOOTERS and component.instance is not None:component.instance.hide()
        if self.menu_focus:self['green'].show()
        else:
            self['green'].hide()
            for name in ('green','blue','blue_button'):
                component=self.panes[self.current].widgets.get(name)
                if component is not None and component.getText():component.show()
    def navigate(self,kind,*args):
        if self.closed:return
        model=self.panes[kind].model
        if kind=='intro':
            url,server,login,passwd=args
            model.srv_name=server
            for pane in self.panes.values():
                pane.model.url=url;pane.model.login=login;pane.model.passwd=passwd;pane.loaded=False
            self.history=[]
        elif kind=='file':model.url,model.login,model.passwd,model.titleFile=args
        elif kind=='entitlements':model.url,model.reader,model.login,model.passwd=args
        else:model.url,model.login,model.passwd=args
        if kind in ('file','entitlements'):self.history.append(self.current)
        else:self.history=[]
        self.activate(kind)
    def back(self):
        if self.history:self.activate(self.history.pop())
        elif self.current not in ('intro','servers'):self.activate('intro')
        else:self.close()
        return 1
    def left(self):
        if self.current not in ('intro','servers'):self.focus(False)
        return 1
    def right(self):self.focus(True);return 1
    def move(self,delta):
        if not self.menu_focus:return 0
        pane=self.panes['servers' if self.current=='servers' else 'intro'];widget=pane.model['list']
        length=len(pane.model.list)
        if length:widget.moveToIndex((widget.getSelectedIndex()+delta)%length)
        return 1
    def choose(self):
        if not self.menu_focus:return 0
        pane=self.panes['servers' if self.current=='servers' else 'intro']
        if pane.model['list'].getCurrent():
            if self.current=='servers':pane.model.choiseServer()
            else:pane.model.selectedmenuitem()
        return 1
    def color(self):return 1 if self.menu_focus else 0
    def shutdown(self):
        self.closed=True
        for pane in self.panes.values():
            pane.pause()
            for callback in pane.model.onClose:callback()
            for timer in pane.timers:timer.close()


def open_workspace(session,api,**kwargs):return session.open(OscamWorkspace,api,**kwargs)
