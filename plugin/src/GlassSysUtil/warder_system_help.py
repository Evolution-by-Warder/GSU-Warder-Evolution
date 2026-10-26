"""Help replaces the system body and restores native content without reopening it."""
from xml.etree import ElementTree as ET
from . import warder_main as main
from .warder_glass import CLEAR


def prepare(root,width,height):
    sx,sy=width/1920,height/1080
    index=0
    for node in root:
        x,y=map(int,node.get('position','0,0').split(','))
        if not (round(182*sy)<=y<round(978*sy)):continue
        if node.get('backgroundColor') in ('#1a102136',main.CYAN) and node.tag=='eLabel':continue
        if not node.get('name'):
            node.set('name','system_body_art_'+str(index));index+=1
            node.tag='widget'
    ET.SubElement(root,'widget',name='system_help_text',position='%d,%d'%(round(90*sx),round(225*sy)),size='%d,%d'%(round(1740*sx),round(710*sy)),font='Regular;%d'%round(28*sy),backgroundColor=CLEAR,transparent='1',foregroundColor='#00ffffff',zPosition='4',scrollbarMode='showOnDemand')


class Help:
    def __init__(self,screen,api):
        self.screen,self.api=screen,api;self.active=False;self.closed=False
        root=ET.fromstring(screen.skin);self.body=[]
        for node in root:
            name=node.get('name')
            if name=='system_help_text' or not name:continue
            y=int(node.get('position','0,0').split(',')[1])
            if 182*api['getDesktop'](0).size().height()/1080<=y<978*api['getDesktop'](0).size().height()/1080:
                if name not in screen:screen[name]=api['Pixmap']() if 'pixmap' in node.attrib else api['Label'](node.get('text',''))
                self.body.append(screen[name])
        screen['system_help_text']=api['ScrollLabel']('');screen['system_help_text'].hide()
        self.visibility=[]
        for widget in self.body:
            state={'visible':widget.visible,'show':widget.show,'hide':widget.hide}
            def show(state=state):
                state['visible']=True
                if not self.active:state['show']()
            def hide(state=state):state['visible']=False;state['hide']()
            widget.show,widget.hide=show,hide;self.visibility.append(state)
        screen['system_help_actions']=api['ActionMap'](['ColorActions','SetupActions','DirectionActions'],{'green':self.toggle,'red':self.back,'cancel':self.back,'ok':self.back,'up':self.up,'down':self.down,'left':self.up,'right':self.down,'yellow':self.consume},-10)
        screen.onClose.append(self.cleanup)
    def toggle(self):
        if self.active:return self.back()
        self.active=True
        for state in self.visibility:state['hide']()
        self.old_footer={n:self.screen[n].getText() for n in ('red','green','yellow')}
        text='\n\n'.join(self.api['_'](key) for key in ('To moving in the list of running aplications use LEFT/RIGHT','To moving in the list of system info use UP/DOWN','Refresh press a YELLOW button'))
        self.screen['system_help_text'].setText(main.text(self.api,'Help')+'\n\n'+text)
        self.screen['system_help_text'].show()
        self.screen['red'].setText(main.text(self.api,'Back'));self.screen['green'].setText('');self.screen['yellow'].setText('')
        return 1
    def back(self):
        if not self.active:return 0
        self.active=False;self.screen['system_help_text'].hide()
        for state in self.visibility:state['show' if state['visible'] else 'hide']()
        for name,value in self.old_footer.items():self.screen[name].setText(value)
        return 1
    def up(self):
        if not self.active:return 0
        self.screen['system_help_text'].pageUp();return 1
    def down(self):
        if not self.active:return 0
        self.screen['system_help_text'].pageDown();return 1
    def consume(self):return int(self.active)
    def cleanup(self):self.closed=True


def install(screen,api):screen._system_help=Help(screen,api)
