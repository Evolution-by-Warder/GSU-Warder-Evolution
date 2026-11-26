"""Masked remote-control keyboard for a local backup passphrase."""
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.ActionMap import ActionMap
from xml.etree import ElementTree as ET
from .warder_screen import Screen
from . import warder_dashboard as dashboard
from .i18n import for_api

KEYS=('1234567890','abcdefghij','klmnopqrst','uvwxyz-_.@',
      'ABCDEFGHIJ','KLMNOPQRST','UVWXYZ!?#$','%&*+=:;(),')


class BackupPassword(Screen):
    def __init__(self,session,api,title):
        self.api=api
        self.width,self.height=dashboard.dimensions(api)
        root=ET.fromstring(dashboard.skin(self.width,self.height,'menu'))
        root.set('name','WarderBackupPassword')
        for node in list(root):
            if node.get('name','').startswith('inline_'):root.remove(node)
        self.skin=ET.tostring(root,encoding='unicode')
        Screen.__init__(self,session)
        dashboard.install_header(self,api)
        self.secret=''
        self.column=0
        self['list']=api['ListboxSys2']([])
        self['list'].l.setFont(0,api['gFont']('Regular',round(28*self.height/1080)))
        self['list'].l.setItemHeight(round(74*self.height/1080))
        for name,text in (('heading',title),('result_title',title),('result_status',''),
                          ('red',self.tr('Back')),('green','OK'),('yellow',self.tr('Erase character')),('blue','')):
            self[name]=Label(text)
        self['descriptions']=ScrollLabel('')
        self['actions']=ActionMap(['ColorActions','SetupActions','DirectionActions','NumberActions'],
            dict({'red':self.cancel,'cancel':self.cancel,'back':self.cancel,'green':self.accept,
                  'yellow':self.erase,'ok':self.add,'left':lambda:self.horizontal(-1),'right':lambda:self.horizontal(1),
                  'up':self['list'].up,'down':self['list'].down},
                 **{str(i):(lambda n=i:self.append(str(n))) for i in range(10)}),-2)
        self.onLayoutFinish.append(self.render)
        self.onClose.append(self.clear)

    def tr(self,key):return for_api(self.api,key)

    def clear(self):self.secret=''

    def index(self):
        row=self['list'].getCurrent()
        return row[0] if row else 0

    def render(self):
        index=self.index()
        sx,sy=self.width/1920,self.height/1080
        rows=[]
        for i,line in enumerate(KEYS):
            row=[i]
            for pos,char in enumerate(line):
                row.append(self.api['MultiContentEntryText'](
                    pos=(round((12+pos*63)*sx),round(10*sy)),size=(round(63*sx),round(54*sy)),
                    font=0,text='['+char+']' if pos==self.column else char,
                    color=0x42c8ef if pos==self.column else 0xffffff))
            rows.append(row)
        self['list'].l.setList(rows)
        self['list'].moveToIndex(index)
        self.mask()

    def mask(self):
        self['descriptions'].setText(self.tr('Use arrows and OK to enter characters. Green confirms.')+
            '\n\n'+self.tr('At least 12 characters.')+'\n\n'+'•'*min(len(self.secret),64)+
            '\n'+str(len(self.secret)))
        self['result_status'].setText('')

    def horizontal(self,direction):
        self.column=(self.column+direction)%10
        self.render()

    def append(self,char):
        if len(self.secret)<128:self.secret+=char
        self.mask()

    def add(self):self.append(KEYS[self.index()][self.column])

    def erase(self):
        self.secret=self.secret[:-1]
        self.mask()

    def accept(self):
        if len(self.secret)<12:
            self['result_status'].setText(self.tr('At least 12 characters.'))
            return
        value=self.secret
        self.clear()
        self.close(value)

    def cancel(self):
        self.clear()
        self.close(None)
