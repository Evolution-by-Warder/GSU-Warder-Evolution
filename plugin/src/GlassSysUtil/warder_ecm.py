"""Read-only ECM controller embedded in the main screen's right panel."""
from types import FunctionType
from . import warder_main as main

FIELDS={'ecmlabels':'inline_ecm_labels','ecmValues':'inline_ecm_values','piccode':'inline_ecm_picon','picchannel':'inline_ecm_channel','channel_name':'inline_ecm_channel_name'}

class Signal:
    def __init__(self):self.callbacks=[]
    def connect(self,callback):self.callbacks.append(callback);return callback
    def get(self):return self.callbacks

class Timer:
    def __init__(self,owner):
        self.owner=owner;self.timeout=Signal();self.callback=self.timeout.callbacks
        self.native=owner.api['eTimer']()
        signal=getattr(self.native,'timeout',None)
        if signal is not None and hasattr(signal,'connect'):self.connection=signal.connect(self.fire)
        elif signal is not None and hasattr(signal,'get'):signal.get().append(self.fire)
        else:self.native.callback.append(self.fire)
    def fire(self):
        if self.owner.active and not self.owner.closed:
            for callback in list(self.callback):callback()
            self.owner.refresh_labels()
    def start(self,*args):
        if self.owner.active and not self.owner.closed:self.native.start(*args)
    def stop(self):
        if self.native is not None:self.native.stop()
    def isActive(self):return self.owner.active and self.native is not None and self.native.isActive()
    def cleanup(self):self.stop();self.callback.clear();self.connection=None;self.native=None

class InlineECM:
    def __init__(self,screen,api):
        self.screen,self.api=screen,api;self.active=False;self.closed=False
        overlay=dict(api);overlay['eTimer']=self.make_timer
        original=api['ECMInfo'];methods={}
        for name,value in vars(original).items():
            if isinstance(value,FunctionType):
                fn=FunctionType(value.__code__,overlay,name,value.__defaults__,value.__closure__)
                fn.__kwdefaults__=value.__kwdefaults__;methods[name]=fn
        methods['setTitle']=lambda model,title:None
        methods['close']=lambda model,*args:self.hide()
        self.model=type('InlineECMController',(original,),methods)(screen.session)
        for source,target in FIELDS.items():screen[target]=self.model[source]
        screen['inline_ecm_mask']=api['Label']('')
        screen['inline_ecm_title']=api['Label'](main.text(api,'ECM Information'))
        # Keep backend labels private; render a separate localized display label.
        screen['inline_ecm_labels']=api['Label']('')
        self.refresh_labels()
        self.widgets=[screen[name] for name in ('inline_ecm_mask','inline_ecm_title',*FIELDS.values())]
        for widget in self.widgets:widget.hide()
        actions=screen['actions'].actions
        self.original_back=actions['back'];actions['red']=self.back;actions['back']=self.back
        screen.onHide.append(self.suspend);screen.onClose.append(self.cleanup)
    def refresh_labels(self):
        value=self.model['ecmlabels'].getText()
        lines=[]
        for line in value.split('\n'):
            name,separator,rest=line.partition(':')
            lines.append(main.text(self.api,name+separator)+rest)
        self.screen['inline_ecm_labels'].setText('\n'.join(lines))
    def make_timer(self):self.timer=Timer(self);return self.timer
    def pigs(self):return [r for r in getattr(self.screen,'renderer',[]) if type(r).__name__=='Pig']
    def show(self):
        if self.closed:return
        pane=getattr(self.screen,'_rightpane',None)
        if pane:
            if pane.active:pane.leave(restore=False)
            pane.glass(True)
        if not self.active:
            self.old_red=self.screen['red'].getText()
            for pig in self.pigs():
                pig.onHide()
                if pig.instance is not None:pig.instance.hide()
            self.screen['selection'].hide();self.screen['info'].hide()
            for widget in self.widgets:widget.show()
        self.active=True
        self.screen['red'].setText(main.text(self.api,'Back'))
        self.model.runECMTimer=self.timer
        self.model.startSearchInfo()
        self.refresh_labels()
    def hide(self,restore_video=True):
        if not self.active:return
        self.active=False;self.timer.stop()
        pane=getattr(self.screen,'_rightpane',None)
        if pane:pane.glass(False)
        for widget in self.widgets:widget.hide()
        self.screen['selection'].show();self.screen['info'].show()
        self.screen['red'].setText(self.old_red)
        for pig in self.pigs():
            if pig.instance is not None:pig.instance.show()
            if restore_video and not self.closed:pig.onShow()
    def back(self):
        if self.active:self.hide()
        else:self.original_back()
        return 1
    def suspend(self):self.hide(restore_video=False)
    def cleanup(self):
        self.closed=True;self.suspend();self.timer.cleanup()
        self.model.runECMTimer_conn=None


def install(screen,api):
    if api['getDesktop'](0).size().width()>=1280:screen._inline_ecm=InlineECM(screen,api)


def show(screen,api):
    view=getattr(screen,'_inline_ecm',None)
    if view is None:return screen.session.open(api['ECMInfo'])
    view.show()


def standalone_skin(original):
    from xml.etree import ElementTree as ET
    root=ET.fromstring(original)
    width,height=map(int,root.get('size').split(','))
    code=root.find("widget[@name='piccode']")
    if code is None:return original
    old_width=width;scale=old_width/525
    width+=round(100*scale);height+=round(45*scale)
    root.set('size','%d,%d'%(width,height))
    x,y=map(int,code.get('position').split(','));y+=round(20*scale)
    w,h=round(180*scale),round(108*scale)
    values=root.find("widget[@name='ecmValues']")
    if values is not None:
        values.set('noWrap','1')
        vw,vh=map(int,values.get('size').split(','));values.set('size','%d,%d'%(vw+width-old_width,vh))
    for node in list(root):
        if node.tag=='ePixmap' and 'frame' in node.get('pixmap',''):root.remove(node)
    gap=round(35*scale);start=(width-(2*w+gap))//2
    code.set('position','%d,%d'%(start+w+gap,y));code.set('size','%d,%d'%(w,h));code.set('scale','1')
    ET.SubElement(root,'widget',name='picchannel',position='%d,%d'%(start,y),size='%d,%d'%(w,h),scale='1',alphatest='blend',zPosition='4')
    ET.SubElement(root,'widget',name='channel_name',position='%d,%d'%(round(25*scale),y-round(42*scale)),size='%d,%d'%(width-round(50*scale),round(34*scale)),font='Regular;%d'%round(28*scale),foregroundColor=main.CYAN,backgroundColor='#ff000000',transparent='1',halign='center',valign='center',noWrap='1',zPosition='4')
    return ET.tostring(root,encoding='unicode')


def channel_picon(screen,api):
    service=screen.session.nav.getCurrentService()
    info=service and service.info()
    value=info.getName() if info is not None and hasattr(info,'getName') else ''
    screen['channel_name'].setText(value.replace('\x86','').replace('\x87','') if isinstance(value,str) else '')
    widget=screen['picchannel']
    if widget.instance is None:return
    ref=screen.session.nav.getCurrentlyPlayingServiceReference()
    if ref is None:
        screen._channel_picon_ref=None;widget.hide();return
    name='_'.join(ref.toString().split(':')[:10])
    if getattr(screen,'_channel_picon_ref',None)==name:return
    screen._channel_picon_ref=name
    path=api['resPicon'](name,'picon')
    if path:
        widget.instance.setPixmapFromFile(path);widget.show()
    else:widget.hide()
