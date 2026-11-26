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
        self.model._inline_ecm_display=True
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
        self.align_channel_name()
        self.screen['red'].setText(main.text(self.api,'Back'))
        self.model.runECMTimer=self.timer
        self.model.startSearchInfo()
        self.refresh_labels()
    def align_channel_name(self):
        from enigma import ePoint,eSize
        size=self.api['getDesktop'](0).size()
        widget=self.screen['inline_ecm_channel_name'].instance
        if widget is not None:
            widget.move(ePoint(round(1160*size.width()/1920),round(672*size.height()/1080)))
            widget.resize(eSize(round(680*size.width()/1920),round(40*size.height()/1080)))
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


def compact_cam_version(value):
    if '@' not in value:return value
    return value.split('@',1)[0].rstrip(')\n')+')\n'


def file_identity(path='/tmp/ecm.info'):
    """Metadata only. Never store ECM payload, reader address or control words."""
    import os,stat
    try:
        st=os.stat(path,follow_symlinks=False)
        if stat.S_ISREG(st.st_mode) and 0<st.st_size<=65536:
            return (st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns,st.st_ctime_ns)
    except OSError:pass
    return None


def milliseconds(value):
    """Convert existing parser's normalized seconds, or explicitly stated units."""
    import re
    if not isinstance(value,str):return None
    match=re.fullmatch(r'\s*(\d+(?:\.\d+)?)\s*(ms|s)?\s*',value,re.I)
    if not match:return None
    # The legacy ECMparser normalizes bare millisecond integers to seconds.
    # A bare integer that survives its normalization is ambiguous.
    if not match[2] and '.' not in match[1]:return None
    number=float(match[1])*(1 if (match[2] or '').lower()=='ms' else 1000)
    return number if 0<=number<=60000 else None


class ECMHistory:
    def __init__(self,clock=None):
        from .warder_telemetry import History
        self.history=History(**({'clock':clock} if clock else {}))
        self.service=None
        self.last=None
        self.current=None

    def observe(self,service,crypted,before,after,value):
        # An existing file may belong to a previous channel. Establish a
        # baseline and wait for a new stable observation after a service change.
        if service!=self.service or crypted is not True:
            self.history.samples.clear()
            self.service=service
            self.last=after
            self.current=None
            return
        if service is None or before is None or before!=after:
            self.current=None
            return
        if after==self.last:return
        self.last=after
        self.current=milliseconds(value)
        self.history.append({'ecm':self.current})


def history_skin(width,height):
    from xml.etree import ElementTree as ET
    from .warder_dashboard import skin
    root=ET.fromstring(skin(width,height,'detail'))
    sx,sy=width/1920,height/1080
    for node in list(root):
        if node.get('name') in ('file_info','report_status'):root.remove(node)
    def add(tag,x,y,w,h,**attrs):
        return ET.SubElement(root,tag,position='%d,%d'%(round(x*sx),round(y*sy)),
            size='%d,%d'%(round(w*sx),round(h*sy)),**attrs)
    def label(name,x,y,w,h,font=26,**attrs):
        return add('widget',x,y,w,h,name=name,font='Regular;%d'%round(font*sy),
            foregroundColor='#00e2edf5',backgroundColor=main.PANEL,transparent='1',zPosition='3',**attrs)
    for x,y,w,h in ((92,286,834,648),(946,286,880,648)):
        for xx,yy,ww,hh in ((x,y,w,2),(x,y+h-2,w,2),(x,y,2,h),(x+w-2,y,2,h)):
            add('eLabel',xx,yy,ww,hh,backgroundColor=main.CYAN,zPosition='1')
    label('channel_name',116,302,786,58,32,noWrap='1')
    label('ecmlabels',116,376,225,450,24,noWrap='1',valign='top')
    label('ecmValues',350,376,552,450,24,noWrap='1',valign='top')
    add('widget',274,836,180,90,name='picchannel',scale='1',alphatest='blend',zPosition='3')
    add('widget',560,836,180,90,name='piccode',scale='1',alphatest='blend',zPosition='3')
    label('history_current',970,304,832,70,36,noWrap='1')
    label('history_top',970,386,832,32,23,halign='right')
    add('widget',970,424,832,304,source='ecm_history_plot',render='Canvas',zPosition='3')
    label('history_window',970,734,832,36,23,halign='right')
    for i in range(3):label('history_stat%d'%i,970+i*277,788,270,60,25,noWrap='1')
    label('history_count',970,872,832,42,24,noWrap='1')
    return ET.tostring(root,encoding='unicode')


def open_history(session,api):
    """Extend the existing ECM screen and timer rather than add a second reader."""
    original=api.get('ECMInfo')
    if not isinstance(original,type):
        if callable(original):return session.open(original)
        return
    from .warder_dashboard import dimensions,install_header
    from Components.Sources.CanvasSource import CanvasSource
    from .warder_chart import draw_trend,chart_scale
    from .warder_live import statistics
    from .i18n import for_api

    class HistoryECM(original):
        def __init__(self,session):
            super().__init__(session)
            self.width,self.height=dimensions(api)
            self.skin=history_skin(self.width,self.height)
            self.skinName=['WarderECMHistory']
            self.parsedSkin=None
            install_header(self,api)
            self.history=ECMHistory()
            self._history_closed=False
            self._history_suspended=False
            self._history_before=None
            self['ecm_history_plot']=CanvasSource()
            for name,value in (('heading','ECM Information'),('red','Back'),('green',''),('yellow',''),('blue','')):
                self[name]=api['Label'](for_api(api,value))
            for name in ('history_current','history_top','history_window','history_count',
                         'history_stat0','history_stat1','history_stat2'):
                self[name]=api['Label']('')
            self._warder_history_observer=self.observe_history
            self.onLayoutFinish.insert(0,self.render_history)
            self.onHide.append(self.suspend_history)
            self.onShow.append(self.resume_history)
            self.onClose.append(self.cleanup_history)

        def readEcmInfo(self):
            if self._history_closed or self._history_suspended:return
            self._history_before=file_identity()
            super().readEcmInfo()
            self.render_history()

        def observe_history(self,value):
            nav=self.session.nav
            try:
                ref=nav.getCurrentlyPlayingServiceReference()
                identity=ref.toString() if ref is not None else None
                service=nav.getCurrentService()
                info=service.info() if service else None
                crypted=info is not None and info.getInfo(api['iServiceInformation'].sIsCrypted)==1
            except (AttributeError,RuntimeError,TypeError,KeyError):
                identity,crypted=None,False
            self.history.observe(identity,crypted,self._history_before,file_identity(),value)

        def render_history(self):
            tr=lambda key:for_api(api,key)
            samples=self.history.history.snapshot()
            def shown(v):return '—' if v is None else '%.1f ms'%v
            self['history_current'].setText(tr('ECM Time:')+'   '+shown(self.history.current))
            _,top=chart_scale(samples,'ecm')
            self['history_top'].setText(shown(top) if any(v.get('ecm') is not None for _,v in samples) else '—')
            self['history_window'].setText('−60 s → 0 s')
            for i,(key,v) in enumerate(zip(('Minimum','Maximum','Average'),statistics(samples,'ecm'))):
                self['history_stat%d'%i].setText(tr(key)+'\n'+shown(v))
            self['history_count'].setText(tr('Total:')+'   '+str(sum(v.get('ecm') is not None for _,v in samples)))
            draw_trend(self['ecm_history_plot'],samples,'ecm',round(832*self.width/1920),
                round(304*self.height/1080),interval=5)

        def suspend_history(self):
            self._history_suspended=True
            if self.runECMTimer is not None:self.runECMTimer.stop()
            self.history=ECMHistory()

        def resume_history(self):
            if self._history_closed:return
            if self._history_suspended:
                self._history_suspended=False
                self.startSearchInfo()
                self.render_history()

        def cleanup_history(self):
            self._history_closed=True
            if self.runECMTimer is not None:self.runECMTimer.stop()

    return session.open(HistoryECM)
