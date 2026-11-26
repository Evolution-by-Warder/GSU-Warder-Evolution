"""Full-screen system information and shared header for other Warder screens."""
from pathlib import Path
from xml.etree import ElementTree as ET
from threading import Event
from . import warder_main as main
from .warder_screen import Screen

CARD_NAMES=('CPU','RAM','Swap','Flash','HDD / SSD / USB','Temperature')


def information_skin(width,height):
    from . import warder_dashboard as dashboard
    sx,sy=width/1920,height/1080
    root=ET.fromstring(dashboard.skin(width,height,'information'))
    header={'day','date','clock','seconds','version_title','version','red','green','yellow','blue'}
    for node in list(root):
        if node.get('name') in header or node.tag=='ePixmap':continue
        if int(node.get('position','0,0').split(',')[1])>=round(181*sy):root.remove(node)
    root.set('name','WarderGSUSystemInformation')
    def add(tag,x,y,w,h,**attrs):
        return ET.SubElement(root,tag,position='%d,%d'%(round(x*sx),round(y*sy)),
             size='%d,%d'%(round(w*sx),round(h*sy)),**attrs)
    def label(name,x,y,w,h,points,color='#00ffffff',**attrs):
        return add('widget',x,y,w,h,name=name,font='Regular;%d'%round(points*sy),
            foregroundColor=color,backgroundColor=main.PANEL,transparent='1',zPosition='3',**attrs)
    label('heading',92,181,1300,72,40,main.CYAN,valign='center',noWrap='1')
    label('stamp',1420,190,400,50,25,'#00bcd2df',halign='right',valign='center',noWrap='1')
    add('eLabel',92,263,1734,2,backgroundColor='#00314b65',zPosition='1')
    for i in range(6):
        x,y=92+(i%2)*879,286+(i//2)*183
        add('eLabel',x,y,855,170,backgroundColor='#00172539',zPosition='-1')
        add('eLabel',x,y,855,3,backgroundColor=main.CYAN,zPosition='1')
        label('title%d'%i,x+18,y+12,810,38,27,'#00bcd2df',noWrap='1')
        label('value%d'%i,x+18,y+50,810,55,40,noWrap='1')
        label('note%d'%i,x+18,y+105,810,48,22,'#00bcd2df',noWrap='1')
        if i<4:
            add('widget',x+18,y+154,810,8,name='meter%d'%i,backgroundColor='#002f465a',
                foregroundColor=main.CYAN,borderWidth='0',transparent='0',zPosition='3')
    label('summary',92,840,1734,42,24,main.CYAN,noWrap='1',valign='center')
    for i in range(5):
        x=92+i*350
        add('eLabel',x,890,334,67,backgroundColor='#00172539',zPosition='-1')
        label('service_name%d'%i,x+8,892,318,27,21,'#00bcd2df',halign='center',noWrap='1')
        label('service_value%d'%i,x+8,920,318,30,21,halign='center',noWrap='1')
    return ET.tostring(root,encoding='unicode')


def capacity_note(total,free,tr):
    if total is None or free is None or not 0<=free<=total:return '—'
    def unit(v):return '%.1f GiB'%(v/1073741824) if v>=1073741824 else '%.1f MiB'%(v/1048576)
    return '  ·  '.join(tr(k)+' '+unit(v) for k,v in (('Total:',total),('Free:',free),('Used:',total-free)))


def information_model(report,tr):
    numbers=report['values'];mem=report['memory']
    flash,disk=report['flash_usage'],report['disk_usage']
    titles=[tr(k) for k in CARD_NAMES]
    titles[1]+=' · '+tr('Used:').rstrip(':')
    titles[3]+=' · '+tr('free');titles[4]+=' · '+tr('free')
    notes=['',capacity_note(mem['ram_total'],mem['ram_available'],tr),
           capacity_note(mem['swap_total'],mem['swap_free'],tr),
           capacity_note(flash.total,flash.free,tr) if flash else '—',
           capacity_note(disk.total,disk.free,tr) if disk else '—',
           str(report.get('temperature_source') or '').rsplit('/',1)[-1]]
    if report.get('disk_mount'):titles[4]+=' · '+report['disk_mount']
    if report.get('disk_temperature') is not None:
        notes[5]+='  ·  '+(tr('Temp. %s:') % 'HDD/SSD')+' %s °C'%report['disk_temperature']
    cards=[]
    for i,n in enumerate(numbers):
        value='—' if n is None else ('%.1f GiB'%(n/1073741824) if i==4 else '%.1f °C'%n if i==5 else '%.0f %%'%n)
        meter=round(max(0,min(100,n))) if i<4 and n is not None else None
        cards.append((titles[i],value,notes[i],meter))
    health=report['health']
    summary=tr('Resource score')+'  '+(str(health['score'])+'/100' if health['score'] is not None else '—')+'  ·  '+tr('Measured checks')+'  %d/%d (RAM / Flash)'%health['coverage']
    return cards,summary,report['services']


class Information(Screen):
    def __init__(self,session,api):
        from . import warder_dashboard as dashboard
        from .warder_system_data import PROTOCOLS
        self.skin=information_skin(*dashboard.dimensions(api))
        Screen.__init__(self,session)
        self.api=api;self.cancelled=Event();self.pending=False
        self.setTitle(self.tr('System Information'))
        dashboard.install_header(self,api)
        for name,key in (('heading','System Information'),('stamp',''),('summary','Loading…'),
                         ('red','Back'),('green','Live monitoring'),('yellow','Refresh'),('blue','Details')):
            self[name]=api['Label'](self.tr(key))
        for i,key in enumerate(CARD_NAMES):
            self['title%d'%i]=api['Label'](self.tr(key))
            self['value%d'%i]=api['Label']('—');self['note%d'%i]=api['Label']('')
            if i<4:
                self['meter%d'%i]=api['ProgressBar']();self['meter%d'%i].hide()
        for i,name in enumerate(PROTOCOLS):
            self['service_name%d'%i]=api['Label'](name)
            self['service_value%d'%i]=api['Label']('—')
        self['actions']=api['ActionMap'](['ColorActions','SetupActions','WizardActions'],
            {'red':self.close,'cancel':self.close,'back':self.close,'green':self.live,
             'yellow':self.refresh,'blue':self.details},-2)
        self.onLayoutFinish.append(self.refresh);self.onClose.append(self.cancelled.set)

    def tr(self,key):return main.text(self.api,key)

    def live(self):
        from .warder_centre_ui import open_diagnostic
        open_diagnostic(self.session,self.api,'system-live')

    def details(self):
        from .warder_centre_ui import open_diagnostic
        open_diagnostic(self.session,self.api,'storage-overview')

    def refresh(self):
        from twisted.internet.threads import deferToThread
        from .warder_system_data import information
        if self.pending or self.cancelled.is_set():return
        self.pending=True
        self['summary'].setText(self.tr('Loading…'))
        try:deferToThread(information,self.cancelled).addCallbacks(self.done,self.failed)
        except (RuntimeError,TypeError,OSError):self.failed(None)

    def done(self,report):
        self.pending=False
        if self.cancelled.is_set():return
        if report is None:return self.failed(None)
        try:cards,summary,services=information_model(report,self.tr)
        except (KeyError,ValueError,TypeError,AttributeError):return self.failed(None)
        from time import strftime
        for i,(title,value,note,meter) in enumerate(cards):
            for key,v in (('title',title),('value',value),('note',note)):self[key+str(i)].setText(v)
            if i<4:
                bar=self['meter%d'%i]
                if meter is None:bar.hide()
                else:bar.setValue(meter);bar.show()
        for i,detected in enumerate(services):
            self['service_value%d'%i].setText('—' if detected is None else self.tr('Detected' if detected else 'Not detected'))
        self['stamp'].setText(strftime('%H:%M:%S'));self['summary'].setText(summary)

    def failed(self,failure):
        self.pending=False
        if not self.cancelled.is_set():
            for i in range(6):
                self['value%d'%i].setText('—');self['note%d'%i].setText('')
                if i<4:self['meter%d'%i].hide()
            for i in range(5):self['service_value%d'%i].setText('—')
            self['stamp'].setText('');self['summary'].setText(self.tr('Unavailable'))


class SystemHeader(main.Header):
    def prepare(self):
        if self.closed:return
        try:version=(Path(self.api['GSU_PATH'])/'version').read_text().strip()
        except OSError:version='—'
        self.screen['version'].setText(version)
        self.screen['version_title'].setText(main.text(self.api,'Version:'))
        self.tick()
        self.timer.start(1000)


def install(screen,api):
    for name in ('day','date','clock','seconds','version_title','version'):
        screen[name]=api['Label']('')
    screen._warder_header=SystemHeader(screen,api)
    if 'glass_header_art' in screen.skin:
        from .warder_glass import HeaderArtwork
        size=api['getDesktop'](0).size();screen['glass_header_art']=HeaderArtwork(size.width(),size.height())
    if 'system_help_text' in screen.skin:
        from .warder_system_help import install
        install(screen,api)
