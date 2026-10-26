"""Warder main screen presentation; existing menu IDs and actions stay in plugin.py."""
from .i18n import for_api as _i18n_text, language as _i18n_language
from datetime import datetime
from xml.sax.saxutils import escape
from xml.etree import ElementTree as ET

PLUGIN_NAME = 'GSU Warder Evolution'
BACKGROUND = '/usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/images/warder-main.png'
BASE = '#00071627'
PANEL = '#00102136'
CYAN = '#003ee8ff'
SELECTION = '#002a70ad'
LIST_WIDGETS = {'list','config','devices','txt','log_info','entitlements_list'}
DAYS = {
    'en': 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday'.split(),
    'sk': 'Pondelok Utorok Streda Štvrtok Piatok Sobota Nedeľa'.split(),
    'cs': 'Pondělí Úterý Středa Čtvrtek Pátek Sobota Neděle'.split(),
    'de': 'Montag Dienstag Mittwoch Donnerstag Freitag Samstag Sonntag'.split(),
    'pl': 'Poniedziałek Wtorek Środa Czwartek Piątek Sobota Niedziela'.split(),
    'hu': 'Hétfő Kedd Szerda Csütörtök Péntek Szombat Vasárnap'.split(),
    'ru': 'Понедельник Вторник Среда Четверг Пятница Суббота Воскресенье'.split(),
    'fr': 'Lundi Mardi Mercredi Jeudi Vendredi Samedi Dimanche'.split(),
    'it': 'Lunedì Martedì Mercoledì Giovedì Venerdì Sabato Domenica'.split(),
    'es': 'Lunes Martes Miércoles Jueves Viernes Sábado Domingo'.split(),
}
MONTHS = {
    'en': 'January February March April May June July August September October November December'.split(),
    'sk': 'januára februára marca apríla mája júna júla augusta septembra októbra novembra decembra'.split(),
    'cs': 'ledna února března dubna května června července srpna září října listopadu prosince'.split(),
    'de': 'Januar Februar März April Mai Juni Juli August September Oktober November Dezember'.split(),
    'pl': 'stycznia lutego marca kwietnia maja czerwca lipca sierpnia września października listopada grudnia'.split(),
    'hu': 'január február március április május június július augusztus szeptember október november december'.split(),
    'ru': 'января февраля марта апреля мая июня июля августа сентября октября ноября декабря'.split(),
    'fr': 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'.split(),
    'it': 'gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre'.split(),
    'es': 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split(),
}


def language(api):
    settings=api['config']
    enabled=getattr(getattr(getattr(getattr(settings,'plugins',None),'GlassSysUtil',None),'par62',None),'value',True)
    return _i18n_language(settings.osd.language.value) if enabled else 'en'


def text(api,value):
    return _i18n_text(api,value)


def clock_values(now, lang):
    """Format locally, without changing the process-wide locale used by Enigma2."""
    if lang in DAYS:
        day = DAYS[lang][now.weekday()]
        month = MONTHS[lang][now.month-1]
        date = '%d. %s %d' % (now.day, month, now.year)
    else:
        day = DAYS['en'][now.weekday()]
        date = '%d. %s %d' % (now.day,MONTHS['en'][now.month-1],now.year)
    return day, date, now.strftime('%H:%M'), now.strftime(':%S')


def main_skin(width=1920, height=1080, api=None):
    sx, sy = width/1920.0, height/1080.0
    def box(x,y,w,h):
        return 'position="%d,%d" size="%d,%d"' % (round(x*sx),round(y*sy),round(w*sx),round(h*sy))
    def fill(x,y,w,h,color):
        return '<eLabel %s backgroundColor="%s" zPosition="1" />' % (box(x,y,w,h),color)
    def label(name,x,y,w,h,font=28,color='#00ffffff',align='left',wrap=False):
        return '<widget name="%s" %s font="Regular;%d" foregroundColor="%s" backgroundColor="%s" transparent="0" zPosition="3" valign="center" halign="%s" noWrap="%d" />' % (name,box(x,y,w,h),round(font*sy),color,BASE if y<180 or y>=980 else PANEL,align,0 if wrap else 1)
    out=['<screen name="WarderGSUMain" position="0,0" size="%d,%d" flags="wfNoBorder" backgroundColor="%s">' % (width,height,BASE),
         '<ePixmap %s pixmap="%s" scale="1" zPosition="0" />' % (box(0,0,1920,1080),BACKGROUND)]
    # Header labels have transparent backgrounds over the static brand artwork.
    for spec in [('day',1100,25,280,36,25,'#00ffffff','right'),('date',960,70,420,36,24,'#00ffffff','right'),
                 ('clock',1398,27,190,85,62,'#00ffffff','center'),('seconds',1590,52,66,54,38,'#00ffffff','left'),
                 ('version_title',1680,25,210,36,25,CYAN,'center'),('version',1680,70,210,36,24,CYAN,'center')]:
        out.append(label(*spec).replace('transparent="0"','transparent="1"'))
    out += [fill(1392,25,2,84,CYAN),fill(1664,25,2,84,CYAN)]
    for x,w in ((55,1050),(1135,730)):
        out += [fill(x,180,w,800,CYAN),fill(x+2,182,w-4,796,PANEL)]
    out += ['<widget name="list" %s scrollbarMode="showOnDemand" backgroundColor="%s" foregroundColor="#00ffffff" foregroundColorSelected="#00ffffff" backgroundColorSelected="#002a70ad" transparent="0" zPosition="3" />' % (box(75,203,1010,759),PANEL),
            fill(1178,203,644,364,CYAN),
            '<widget source="session.VideoPicture" render="Pig" %s backgroundColor="#ff000000" zPosition="2" />' % box(1180,205,640,360),
            label('selection',1170,590,660,80,30,CYAN,wrap=True),fill(1170,683,660,2,'#00314b65'),
            label('info',1170,700,660,265,26,'#00d1e3f3',wrap=True)]
    # Hidden until ECM is selected; the main left menu stays active.
    out += [label('inline_ecm_mask',1137,182,726,796,1),
            label('inline_ecm_title',1160,203,680,45,28,CYAN,'center'),
            label('inline_ecm_labels',1160,270,160,460,24,'#00d1e3f3'),
            label('inline_ecm_values',1325,270,515,460,24),
            '<widget name="inline_ecm_picon" %s scale="1" alphaTest="blend" zPosition="5" />' % box(1390,760,220,132)]
    for index,node in enumerate(out):
        if 'name="inline_ecm_' in node:
            out[index]=node.replace('zPosition="3"','zPosition="4"' if 'name="inline_ecm_mask"' in node else 'zPosition="5"').replace('valign="center"','valign="top"' if 'inline_ecm_labels' in node or 'inline_ecm_values' in node else 'valign="center"')
    slot = (1810-3*20)/4
    for index,(name,color) in enumerate((('red','#00ff526a'),('green','#0039ff59'),('yellow','#00ffdb52'),('blue','#0045b9ff'))):
        x = 55+index*(slot+20)
        out += [fill(x+(slot-200)/2,996,200,2,color),label(name,x,1006,slot,50,28,color,'center')]
    return '\n'.join(out+['</screen>'])


def menu_row(api, ident, title, enabled, width, height):
    sx,sy=width/1920.0,height/1080.0
    def scaled(values):return tuple(round(v*(sx if i%2==0 else sy)) for i,v in enumerate(values))
    entry=api['MultiContentEntryText']
    return [ident,
            entry(pos=scaled((42,8)),size=scaled((940,45)),font=0,text=title,
                  color=0xffffff if enabled else 0x8291a5,color_sel=0xffffff if enabled else 0xb1bbc8),
            entry(pos=scaled((10,15)),size=scaled((26,32)),font=1,text='●',
                  color=0x39ff59 if enabled else 0xff526a,color_sel=0x39ff59 if enabled else 0xff526a)]


class Header:
    def __init__(self, screen, api):
        self.screen,self.api,self.closed=screen,api,False
        self.timer=api['eTimer']()
        signal=getattr(self.timer,'timeout',None)
        if signal is not None and hasattr(signal,'connect'):
            self.connection=signal.connect(self.tick)
        elif signal is not None and hasattr(signal,'get'):
            signal.get().append(self.tick)
        else:
            self.timer.callback.append(self.tick)
        self.last={}
        screen.onLayoutFinish.append(self.prepare)
        screen.onClose.append(self.cleanup)

    def prepare(self):
        if self.closed:return
        screen,api=self.screen,self.api
        screen['version'].setText(screen.readVersion())
        screen['version_title'].setText(text(api,'Version:'))
        screen['yellow'].setText(text(api,'Settings'))
        screen['green'].setText(text(api,'Select with OK'))
        self.tick()
        self.timer.start(1000)

    def tick(self):
        if self.closed:return
        values=clock_values(datetime.now(),language(self.api))
        for name,value in zip(('day','date','clock','seconds'),values):
            if self.last.get(name)!=value:
                self.screen[name].setText(value)
                self.last[name]=value

    def cleanup(self):
        self.closed=True
        self.timer.stop()


def install(screen,api):
    size=api['getDesktop'](0).size()
    if size.width()<1280:return
    for name in ('day','date','clock','seconds','version_title','version','selection'):
        screen[name]=api['Label']('')
    screen['selection'].setText(text(api,'Select a menu item'))
    screen['list'].l.setFont(0,api['gFont']('Regular',round(30*size.height()/1080.0)))
    screen['list'].l.setFont(1,api['gFont']('Regular',round(20*size.height()/1080.0)))
    screen['list'].l.setItemHeight(round(58*size.height()/1080.0))
    screen._warder_header=Header(screen,api)


def selection(screen,entry):
    if 'selection' in screen:
        screen['selection'].setText(str(entry[1]) if entry else '')


def style_list_skin(value):
    """Set GSU selection colors locally, leaving global image/skin styles alone."""
    if not isinstance(value,str) or not value.lstrip().startswith('<screen'):return value
    root=ET.fromstring(value)
    changed=False
    for node in root.findall('widget'):
        if node.get('name') in LIST_WIDGETS:
            node.set('backgroundColorSelected',SELECTION)
            node.set('foregroundColorSelected','#00ffffff')
            changed=True
    return ET.tostring(root,encoding='unicode') if changed else value


def style_lists(api):
    # Imported legacy skins are also used by configuration, tools and CAM lists.
    # Transform once at plugin import, before any Screen captures its skin.
    for name,value in list(api.items()):
        if isinstance(value,str) and value.lstrip().startswith('<screen'):
            api[name]=style_list_skin(value)
