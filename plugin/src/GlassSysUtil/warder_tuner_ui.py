"""Warder presentation of native scan screens; never implements tuning or scanning."""
from xml.etree import ElementTree as ET
from . import warder_dashboard as dashboard, warder_main as main

METRICS=('SNR','AGC','BER','LOCK')
FINDER_PLOT_SIZE=(522,196)
FINDER_QUALITY_SIZE=(522,10)


def skin(width,height,finder,components):
    sx,sy=width/1920,height/1080
    root=ET.fromstring(dashboard.skin(width,height,'native'))
    keep={'day','date','clock','seconds','version_title','version'}
    for node in list(root):
        if node.get('name') in keep or node.tag=='ePixmap':continue
        y=int(node.get('position','0,0').split(',')[1])
        if y>=round(181*sy):root.remove(node)
    root.set('name','WarderNativeFinder' if finder else 'WarderNativeScan')
    def add(tag,x,y,w,h,**attrs):
        return ET.SubElement(root,tag,position='%d,%d'%(round(x*sx),round(y*sy)),
            size='%d,%d'%(round(w*sx),round(h*sy)),**attrs)
    def label(name,x,y,w,h,points=28,color='#00ffffff',**attrs):
        return add('widget',x,y,w,h,name=name,font='Regular;%d'%round(points*sy),
            foregroundColor=color,backgroundColor=main.PANEL,transparent='1',zPosition='3',**attrs)
    def panel(x,y,w,h):
        for bx,by,bw,bh in ((x,y,w,2),(x,y+h-2,w,2),(x,y+2,2,h-4),(x+w-2,y+2,2,h-4)):
            add('eLabel',bx,by,bw,bh,backgroundColor=main.CYAN,zPosition='-1')
    label('warder_tuner_title',92,181,1734,72,40,main.CYAN,valign='center',noWrap='1')
    add('eLabel',92,263,1734,2,backgroundColor='#00314b65',zPosition='-1')
    config_width=1120 if finder else 1734
    panel(92,286,config_width,620)
    row=round(48*sy)
    cfg=add('widget',108,304,config_width-32,582,name='config',
        font='Regular;%d'%round(26*sy),itemHeight=str(row),
        backgroundColor=main.PANEL,foregroundColor='#00ffffff',
        backgroundColorSelected=main.SELECTION,foregroundColorSelected='#00ffffff',
        scrollbarMode='showOnDemand',zPosition='3')
    w,h=map(int,cfg.get('size').split(','));cfg.set('size','%d,%d'%(w,h//row*row))
    if finder:
        panel(1236,286,590,620)
        # Four stacked measurement rows: caption and value share a baseline.
        # The freed space belongs to the history plot, not more decoration.
        for i,(y,h) in enumerate(((306,70),(384,70),(462,48),(518,48))):
            x,w=1254,554
            add('eLabel',x,y,w,h,backgroundColor='#00172539',zPosition='-1')
            add('eLabel',x,y,4,h,backgroundColor=main.CYAN,zPosition='1')
            label('warder_metric_name%d'%i,x+16,y+5,116,38,27,'#00bcd2df',noWrap='1',valign='center')
            label('warder_metric%d'%i,x+140,y+5,398,38,27,noWrap='1',valign='center')
            if i==0:
                add('widget',x+16,y+51,*FINDER_QUALITY_SIZE,source='warder_quality',render='Canvas',zPosition='3')
            elif i==1:
                add('widget',x+16,y+51,522,8,name='warder_meter1',
                    backgroundColor='#002f465a',foregroundColor=main.CYAN,borderWidth='0',zPosition='3')
        add('eLabel',1254,576,554,314,backgroundColor='#00172539',zPosition='-1')
        label('warder_history_title',1270,582,522,34,25,main.CYAN,noWrap='1')
        add('widget',1270,622,*FINDER_PLOT_SIZE,source='warder_signal_history',render='Canvas',zPosition='3')
        label('warder_history_window',1270,820,522,27,21,'#00bcd2df',halign='right',noWrap='1')
        label('warder_lock_losses',1270,850,522,32,23,'#00ffffff',noWrap='1')
        label('warder_audio_state',92,914,1734,55,23,'#00bcd2df',halign='center',valign='center')
        label('warder_compare_key',510,990,443,81,28,'#0039ff59',halign='center',valign='center',noWrap='1')
        label('warder_save_key',965,990,443,81,28,'#00ffdb52',halign='center',valign='center',noWrap='1')
        label('warder_audio_key',1420,990,443,81,28,'#0045b9ff',halign='center',valign='center',noWrap='1')
    if not finder and 'introduction' in components:
        label('introduction',92,914,1734,55,23,'#00bcd2df',halign='center',valign='center')
    for name,x,color in (('key_red',55,'#00ff526a'),('key_green',510,'#0039ff59')):
        if name in components and (not finder or name!='key_green'):
            add('widget',x,990,443,81,source=name,render='Label',font='Regular;%d'%round(28*sy),
                foregroundColor=color,backgroundColor=main.BASE,transparent='1',halign='center',valign='center',zPosition='3')
    return ET.tostring(root,encoding='unicode')


def readings(status):
    """Read the raw driver values; unknown values never become zero or a lock."""
    def number(key):
        val=status.get(key)
        return val if type(val) in (int,float) and 0<=val<2**32-1 else None
    def percent(key):
        val=number(key)
        return round(val*100/65535) if val is not None and val<=65536 else None
    snr=percent('tuner_signal_quality');agc=percent('tuner_signal_power')
    db=number('tuner_signal_quality_db');ber=number('tuner_bit_error_rate')
    lock=status.get('tuner_locked')
    return snr,agc,db,ber,lock if type(lock) in (int,bool) and lock in (0,1) else None


def quality_color(snr,lock):
    """Relative visual guide only, not a universal reception threshold."""
    if lock==0:return 0xff526a
    if lock is None or snr is None:return 0x8291a5
    return 0xff526a if snr<35 else 0xffdb52 if snr<65 else 0x39ff59


def draw_quality(canvas,snr,lock,width,height):
    canvas.clear()
    canvas.fill(0,0,width,height,0x2f465a)
    if snr is not None:
        filled=round(width*max(0,min(100,snr))/100)
        if filled:canvas.fill(0,0,filled,height,quality_color(snr,lock))
    canvas.flush()


class Header(dashboard.DiagnosticHeader):
    def __init__(self,screen,api):
        from .warder_telemetry import History
        from .warder_quick import Tone
        self.history=History()
        self.finder='warder_metric0' in screen
        self.tone=Tone() if self.finder else None
        self.audio_enabled=False
        self.audio_busy=False
        self.audio_failed=False
        super().__init__(screen,api)
        if self.finder:
            self.audio_label()
            self.measurement_labels()

    def saved_records(self):
        records=getattr(self.screen.session,'_warder_signal_comparison',None)
        if not isinstance(records,list):
            records=[]
            self.screen.session._warder_signal_comparison=records
        return records

    def current_record(self):
        from .warder_signal import measurement_record
        from time import strftime
        return measurement_record(getattr(self.screen,'_warder_measurement_id',None),
            self.history.snapshot(),strftime('%Y-%m-%d %H:%M:%S'))

    def measurement_labels(self):
        if not self.finder:return
        tr=lambda key:main.text(self.api,key)
        records=self.saved_records()
        self.screen['warder_compare_key'].setText(tr('Compare')+' · %d'%len(records) if records else '')
        self.screen['warder_save_key'].setText(tr('Save') if self.current_record() else '')

    def save_measurement(self):
        if self.closed or self.suspended or not self.ready or not self.finder:return
        record=self.current_record()
        if record is None:return
        records=self.saved_records()
        records.append(record)
        del records[:-12]
        self.measurement_labels()

    def compare_measurements(self):
        if self.closed or self.suspended or not self.finder:return
        records=self.saved_records()
        if not records:return
        from .warder_signal import comparison_text
        from .warder_dialog import show_info
        tr=lambda key:main.text(self.api,key)
        show_info(self.screen.session,self.api,comparison_text(records,tr),tr('Compare'))

    def reset_history(self):
        self.history.samples.clear()
        if self.finder:self.measurement_labels()

    def audio_label(self):
        if not self.finder:return
        tr=lambda key:main.text(self.api,key)
        available=bool(self.tone and self.tone.command and not self.audio_failed)
        key=('yes' if self.audio_enabled else 'no') if available else 'Unavailable'
        self.screen['warder_audio_state'].setText(tr('Audio:')+' '+tr(key))
        self.screen['warder_audio_key'].setText(tr('Audio:') if available else '')

    def toggle_audio(self):
        if self.closed or self.suspended or not self.finder or not self.tone.command or self.audio_failed:return
        if self.audio_enabled:
            self.stop_audio()
        else:
            from .warder_quick import Tone
            self.tone=Tone()
            self.audio_enabled=bool(self.tone.command)
        self.audio_label()

    def stop_audio(self):
        self.audio_enabled=False
        self.audio_busy=False
        if self.tone:self.tone.close()

    def audio_done(self,result,tone):
        if self.closed or self.tone is not tone or not self.audio_enabled:return
        self.audio_busy=False
        if result is not True:
            self.audio_failed=True
            self.stop_audio()
            self.audio_label()

    def suspend(self):
        super().suspend()
        self.stop_audio()
        self.reset_history()
        self.audio_label()

    def cleanup(self):
        self.stop_audio()
        super().cleanup()

    def tick(self):
        super().tick()
        if self.closed or not self.ready or self.suspended or not self.finder:return
        try:status=self.screen['Frontend'].getFrontendStatus() or {}
        except (AttributeError,RuntimeError,TypeError,OSError):status={}
        if not isinstance(status,dict):status={}
        snr,agc,db,ber,lock=readings(status)
        def pct(v):return '—' if v is None else '%d %%'%v
        values=(pct(snr)+('  ·  %.1f dB'%(db/100) if db is not None else ''),pct(agc),
            '—' if ber is None else str(int(ber)),'—' if lock is None else str(int(lock)))
        for i,value in enumerate(values):self.screen['warder_metric%d'%i].setText(value)
        meter=self.screen['warder_meter1']
        if agc is None:meter.hide()
        else:meter.setValue(agc);meter.show()
        width,height=dashboard.dimensions(self.api)
        draw_quality(self.screen['warder_quality'],snr,lock,round(FINDER_QUALITY_SIZE[0]*width/1920),round(FINDER_QUALITY_SIZE[1]*height/1080))
        self.history.append({'snr':snr,'agc':agc,'db':db/100 if db is not None else None,
                             'ber':ber,'lock':lock})
        samples=self.history.snapshot()
        from .warder_chart import draw_trend
        from .warder_signal import lock_losses
        draw_trend(self.screen['warder_signal_history'],samples,'snr',
            round(FINDER_PLOT_SIZE[0]*width/1920),round(FINDER_PLOT_SIZE[1]*height/1080),100,1)
        tr=lambda key:main.text(self.api,key)
        losses=str(lock_losses(samples)) if any(v.get('lock') is not None for _,v in samples) else '—'
        self.screen['warder_lock_losses'].setText(tr('Lock losses')+'  '+losses)
        self.measurement_labels()
        if self.audio_enabled and not self.audio_busy and snr is not None and lock==1:
            from twisted.internet.threads import deferToThread
            tone=self.tone
            self.audio_busy=True
            try:deferToThread(tone.play,snr).addBoth(lambda result:self.audio_done(result,tone))
            except (RuntimeError,TypeError,OSError):self.audio_done(False,tone)


def install(screen,api,finder):
    # Fall back to the image's native skin for unknown component layouts.
    if not hasattr(screen,'keys') or 'config' not in screen:return False
    width,height=dashboard.dimensions(api)
    if width<1280 or height<720 or (finder and 'Frontend' not in screen):return False
    components=set(screen.keys())
    screen.skin=skin(width,height,finder,components)
    screen.skinName=['WarderNativeFinder' if finder else 'WarderNativeScan']
    screen.parsedSkin=None
    tr=lambda key:main.text(api,key)
    try:title=screen.getTitle()
    except (AttributeError,TypeError):title=''
    screen['warder_tuner_title']=api['Label'](str(title or tr('Signal' if finder else 'Manual scan')))
    for name in ('day','date','clock','seconds','version_title','version'):screen[name]=api['Label']('')
    if finder:
        for i,name in enumerate(METRICS):
            screen['warder_metric_name%d'%i]=api['Label'](name+':')
            screen['warder_metric%d'%i]=api['Label']('—')
        from Components.Sources.CanvasSource import CanvasSource
        screen['warder_meter1']=api['ProgressBar']()
        screen['warder_quality']=CanvasSource()
        screen['warder_signal_history']=CanvasSource()
        screen['warder_history_title']=api['Label'](tr('Signal history'))
        screen['warder_history_window']=api['Label']('−60 s → 0 s')
        screen['warder_lock_losses']=api['Label']('—')
        screen['warder_audio_state']=api['Label']('')
        screen['warder_audio_key']=api['Label']('')
        screen['warder_save_key']=api['Label']('')
        screen['warder_compare_key']=api['Label']('')
    screen._diagnostic_header=Header(screen,api)
    if finder:
        screen['warder_audio_actions']=api['ActionMap'](['ColorActions'],
            {'blue':screen._diagnostic_header.toggle_audio,
             'yellow':screen._diagnostic_header.save_measurement,
             'green':screen._diagnostic_header.compare_measurements},-4)
    return True


SCAN_COMPONENTS=frozenset(('scan_progress','scan_state','network','transponder','pass','servicelist'))


def progress_skin(width,height,components,source_keys=()):
    """Present the existing native scanner's own state, list and controls."""
    sx,sy=width/1920,height/1080
    root=ET.fromstring(dashboard.skin(width,height,'detail'))
    keep={'day','date','clock','seconds','version_title','version'}
    for node in list(root):
        if node.get('name') in keep or node.tag=='ePixmap':continue
        if int(node.get('position','0,0').split(',')[1])>=round(181*sy):root.remove(node)
    root.set('name','WarderServiceScan')
    def add(tag,x,y,w,h,**attrs):
        return ET.SubElement(root,tag,position='%d,%d'%(round(x*sx),round(y*sy)),
            size='%d,%d'%(round(w*sx),round(h*sy)),**attrs)
    def label(name,x,y,w,h,points=28,color='#00ffffff',**attrs):
        return add('widget',x,y,w,h,name=name,font='Regular;%d'%round(points*sy),
            foregroundColor=color,backgroundColor=main.PANEL,transparent='1',zPosition='3',**attrs)
    label('warder_scan_title',92,181,1734,72,40,main.CYAN,valign='center',noWrap='1')
    add('eLabel',92,263,1734,2,backgroundColor='#00314b65',zPosition='-1')
    # Native text is authoritative (including count, errors and completion).
    add('eLabel',92,286,1734,250,backgroundColor='#00172539',zPosition='-1')
    label('network',116,302,1170,48,30,main.CYAN,valign='center',noWrap='1')
    label('pass',1300,302,500,48,24,'#00bcd2df',halign='right',valign='center',noWrap='1')
    label('transponder',116,354,1684,66,27,'#00e2edf5',valign='center')
    label('scan_state',116,426,1684,66,29,'#00ffffff',valign='center')
    add('widget',116,504,1684,16,name='scan_progress',backgroundColor='#002f465a',
        foregroundColor=main.CYAN,borderWidth='0',transparent='0',zPosition='3')
    for x,y,w,h in ((92,550,1734,2),(92,944,1734,2),(92,552,2,392),(1824,552,2,392)):
        add('eLabel',x,y,w,h,backgroundColor=main.CYAN,zPosition='-1')
    row=max(1,round(42*sy))
    listing=add('widget',110,566,1698,360,name='servicelist',
        font='Regular;%d'%round(29*sy),itemHeight=str(row),scrollbarMode='showOnDemand',
        backgroundColor=main.PANEL,foregroundColor='#00ffffff',
        backgroundColorSelected=main.SELECTION,foregroundColorSelected='#00ffffff',zPosition='3')
    listing.set('size','%d,%d'%(round(1698*sx),round(360*sy)//row*row))
    for name,x,color in (('key_red',55,'#00ff526a'),('key_green',510,'#0039ff59')):
        if name not in components:continue
        binding={'source':name,'render':'Label'} if name in source_keys else {'name':name}
        add('widget',x,990,443,81,font='Regular;%d'%round(28*sy),
            foregroundColor=color,backgroundColor=main.BASE,transparent='1',
            halign='center',valign='center',zPosition='3',**binding)
    return ET.tostring(root,encoding='unicode')


def install_scan_progress(screen,api):
    if not hasattr(screen,'keys') or not SCAN_COMPONENTS.issubset(screen.keys()):return False
    width,height=dashboard.dimensions(api)
    if width<1280 or height<720:return False
    from Components.Sources.StaticText import StaticText
    components=set(screen.keys())
    source_keys={name for name in ('key_red','key_green')
                 if name in screen and isinstance(screen[name],StaticText)}
    screen.skin=progress_skin(width,height,components,source_keys)
    screen.skinName=['WarderServiceScan']
    screen.parsedSkin=None
    try:title=screen.getTitle()
    except (AttributeError,TypeError):title=''
    screen['warder_scan_title']=api['Label'](str(title or main.text(api,'Manual scan')))
    dashboard.install_header(screen,api)
    return True


def run_with_scan_progress(method,*args,**kwargs):
    """Clone the native launch method, substituting only its screen binding.

    No global monkeypatch or replacement of scan flags, callbacks, or service list.
    Unrecognized image implementations keep their native behavior.
    """
    from types import FunctionType,MethodType
    fn=getattr(method,'__func__',None)
    if not isinstance(fn,FunctionType):return method(*args,**kwargs)
    native=fn.__globals__.get('ServiceScan')
    if not isinstance(native,type) or native.__module__!='Screens.ServiceScan' or native.__name__!='ServiceScan':
        return method(*args,**kwargs)
    if 'ServiceScan' not in fn.__code__.co_names:return method(*args,**kwargs)

    class WarderServiceScan(native):
        def __init__(self,session,*scan_args,**scan_kwargs):
            super().__init__(session,*scan_args,**scan_kwargs)
            from . import plugin
            if not install_scan_progress(self,vars(plugin)):
                names=getattr(self,'skinName',None)
                names=names if isinstance(names,(list,tuple)) else [names]
                self.skinName=['ServiceScan']+[name for name in names if isinstance(name,str)
                    and name not in ('ServiceScan','WarderServiceScan')]

    namespace=dict(fn.__globals__,ServiceScan=WarderServiceScan)
    cloned=FunctionType(fn.__code__,namespace,fn.__name__,fn.__defaults__,fn.__closure__)
    cloned.__kwdefaults__=fn.__kwdefaults__
    return MethodType(cloned,method.__self__)(*args,**kwargs)
