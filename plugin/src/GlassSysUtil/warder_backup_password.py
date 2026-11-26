"""Masked full-width Warder QWERTY password editor."""
import enigma
from Components.Label import Label
from Components.ActionMap import ActionMap
from xml.etree import ElementTree as ET
from .warder_screen import Screen
from . import warder_dashboard as dashboard
from .i18n import for_api
from .warder_backup_crypto import MIN_PASSWORD,MAX_PASSWORD

# Familiar YouTube-style QWERTY ordering, including all printable ASCII.
KEYS=(
    ("1","2","3","4","5","6","7","8","9","0"),
    ("q","w","e","r","t","y","u","i","o","p"),
    ("a","s","d","f","g","h","j","k","l","-"),
    ("z","x","c","v","b","n","m",".",",","?"),
    ("@","#",":","/","_","(",")","+","*","="),
    ("[","]","{","}","'","\"","\\","|","Aa"," "),
)
SHIFT_KEYS=(
    ("!","@","#","$","%","^","&","*","(",")"),
    ("Q","W","E","R","T","Y","U","I","O","P"),
    ("A","S","D","F","G","H","J","K","L","_"),
    ("Z","X","C","V","B","N","M","<",">","?"),
    ("~","`",":","/","-","+","=","|",";","}"),
    ("[","]","{","}","'","\"","\\","|","Aa"," "),
)
COLUMNS=10
ROW_HEIGHT=75


def password_skin(width,height):
    sx,sy=width/1920,height/1080
    root=ET.fromstring(dashboard.skin(width,height,'detail'))
    root.set('name','WarderBackupPassword')
    for node in list(root):
        if node.get('name') in ('report_status','file_info'):root.remove(node)
    def element(tag,x,y,w,h,**attrs):
        return ET.SubElement(root,tag,position='%d,%d'%(round(x*sx),round(y*sy)),
            size='%d,%d'%(round(w*sx),round(h*sy)),**attrs)
    style=dashboard.style
    def label(name,x,y,w,h,size,color):
        return element('widget',x,y,w,h,name=name,font='Regular;%d'%max(1,round(size*sy)),
            foregroundColor=color,backgroundColor=style.PANEL,transparent='1',
            halign='center',valign='center',zPosition='5')
    element('eLabel',214,293,1492,116,backgroundColor=style.CYAN,zPosition='1')
    element('eLabel',216,295,1488,112,backgroundColor=style.PANEL,zPosition='2')
    for i in range(3):
        label('password%d'%i,230,298+i*35,1460,35,26,'#00ffffff')
    label('hint',116,412,1680,38,23,'#00bcd2df')
    element('widget',210,454,1500,456,name='list',scrollbarMode='showNever',
        backgroundColor=style.PANEL,backgroundColorSelected=style.PANEL,
        foregroundColor='#00ffffff',foregroundColorSelected='#00ffffff',zPosition='3')
    label('result_status',116,913,1680,40,25,style.CYAN)
    return ET.tostring(root,encoding='unicode')


class BackupPassword(Screen):
    def __init__(self,session,api,title):
        self.api=api
        self.width,self.height=dashboard.dimensions(api)
        self.skin=password_skin(self.width,self.height)
        Screen.__init__(self,session)
        dashboard.install_header(self,api)
        self.secret=''
        self.revealed=False
        self.row=1
        self.column=0
        self.shifted=False
        self['list']=api['ListboxSys2']([])
        self['list'].l.setFont(0,api['gFont']('Regular',round(36*self.height/1080)))
        self['list'].l.setItemHeight(round(ROW_HEIGHT*self.height/1080))
        for name,text in (('heading',title),('result_status',''),
                          ('hint',self.tr('Use arrows and OK to enter characters. Green confirms.')),
                          ('red',self.tr('Back')),('green','OK'),('yellow',self.tr('Erase character')),
                          ('blue',self.tr('Show password'))):
            self[name]=Label(text)
        for i in range(3):self['password%d'%i]=Label('')
        self['actions']=ActionMap(['ColorActions','SetupActions','DirectionActions','NumberActions','MenuActions'],
            dict({'red':self.cancel,'cancel':self.cancel,'back':self.cancel,'green':self.accept,
                  'yellow':self.erase,'blue':self.toggle_visibility,'menu':self.toggle_shift,
                  'ok':self.add,'left':lambda:self.horizontal(-1),'right':lambda:self.horizontal(1),
                  'up':lambda:self.vertical(-1),'down':lambda:self.vertical(1)},
                 **{str(i):(lambda n=i:self.append(str(n))) for i in range(10)}),-2)
        self.onLayoutFinish.append(self.prepare_keyboard)
        self.onHide.append(self.hide_password)
        self.onClose.append(self.clear)

    def tr(self,key):return for_api(self.api,key)

    def clear(self):
        self.secret=''
        self.revealed=False
        self.mask()

    def hide_password(self):
        self.revealed=False
        self.mask()

    def toggle_visibility(self):
        self.revealed=not self.revealed
        self.mask()

    def index(self):return self.row

    def prepare_keyboard(self):
        instance=self['list'].instance
        if instance is not None:
            instance.setSelectionEnable(False)
        self.render()
        self.mask()

    def rows(self):return SHIFT_KEYS if self.shifted else KEYS

    def render(self):
        sx,sy=self.width/1920,self.height/1080
        rows=[]
        flags=0
        for name in ('RT_HALIGN_CENTER','RT_VALIGN_CENTER'):
            value=getattr(enigma,name,0)
            if isinstance(value,int):flags|=value
        for i,line in enumerate(self.rows()):
            row=[i]
            for pos,char in enumerate(line):
                active=(i==self.row and pos==self.column)
                color=0xffffff
                background=int(dashboard.style.SELECTION[1:],16) if active else 0x203548
                row.append(self.api['MultiContentEntryText'](
                    pos=(round((6+pos*150)*sx),round(4*sy)),size=(round(138*sx),round(67*sy)),
                    font=0,flags=flags,text='␣' if char==' ' else char,color=color,color_sel=color,
                    backcolor=background,backcolor_sel=background))
            rows.append(row)
        self['list'].l.setList(rows)
        # The native list never selects a row: only our cell is highlighted.
        self['list'].moveToIndex(0)

    def mask(self):
        value=self.secret if self.revealed else '•'*len(self.secret)
        for i in range(3):
            self['password%d'%i].setText(value[i*48:(i+1)*48] or ('—' if not value and i==0 else ''))
        self['blue'].setText(self.tr('Hide password' if self.revealed else 'Show password'))
        self['result_status'].setText('%d / %d  ·  %s'%(len(self.secret),MAX_PASSWORD,self.tr('At least 6 characters.')))

    def horizontal(self,direction):
        self.column=(self.column+direction)%COLUMNS
        self.render()

    def vertical(self,direction):
        self.row=(self.row+direction)%len(self.rows())
        self.render()

    def toggle_shift(self):
        self.shifted=not self.shifted
        self.render()

    def append(self,char):
        if len(self.secret)<MAX_PASSWORD:self.secret+=char
        self.mask()

    def add(self):
        key=self.rows()[self.row][self.column]
        if key=='Aa':self.toggle_shift()
        else:self.append(key)

    def erase(self):
        self.secret=self.secret[:-1]
        self.mask()

    def accept(self):
        if len(self.secret)<MIN_PASSWORD:
            self['result_status'].setText(self.tr('At least 6 characters.'))
            return
        value=self.secret
        self.clear()
        self.close(value)

    def cancel(self):
        self.clear()
        self.close(None)
