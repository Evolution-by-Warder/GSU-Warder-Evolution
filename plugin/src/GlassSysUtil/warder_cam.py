"""Warder CAM manager layout; native commands and action mapping are unchanged."""
from copy import deepcopy
from xml.etree import ElementTree as ET
from . import warder_main as main
from .warder_system import install as install_header

SLOTS={
 'config':(105,245,950,104,27),
 'commPic':(80,382,22,23,None),'statPic':(80,432,22,23,None),
 'statCamSrvcmd':(115,375,950,44,25),'statCamSrvbin':(115,425,950,44,25),
 'CamPic':(80,497,22,23,None),'SrvPic':(80,547,22,23,None),
 'activCam':(115,490,950,44,25),'activSrv':(115,540,950,44,25),
 'picECM':(95,620,210,126,None),'picchannel':(345,620,210,126,None),
 'picprov':(595,620,210,126,None),'picsat':(845,620,210,126,None),
 'fullEcmLine':(80,775,1000,78,24),'CAID_info':(80,865,1000,95,23),
 'helpTXT':(1165,735,670,170,25),'select_pict':(1160,250,680,48,None),
 'srvArrowLeft':(75,300,15,27,None),'srvArrowRight':(1070,300,15,27,None),
}
for index,name in enumerate(('txt0','txt1','txt2','txt3','txt4','txt6','txt7','txt8')):
    SLOTS[name]=(1190,250+index*56,640,48,26)


def cam_skin(original,width,height,translator=lambda value:value):
    sx,sy=width/1920,height/1080
    root=ET.fromstring(main.main_skin(width,height));headers={'day','date','clock','seconds','version_title','version'}
    for node in list(root):
        if node.get('name') not in headers and not(node.tag=='ePixmap' and node.get('pixmap')==main.BACKGROUND):root.remove(node)
    root.set('name','WarderGSUCam')
    root.find('ePixmap').set('zPosition','-3')
    def place(node,x,y,w,h,font=None):
        node.set('position','%d,%d'%(round(x*sx),round(y*sy)));node.set('size','%d,%d'%(round(w*sx),round(h*sy)))
        if font:node.set('font','Regular;%d'%round(font*sy))
        return node
    def fill(x,y,w,h,color,z=-1):return place(ET.SubElement(root,'eLabel',backgroundColor=color,zPosition=str(z)),x,y,w,h)
    for x,w in ((55,1050),(1135,730)):
        fill(x,180,w,800,main.CYAN,-2);fill(x+2,182,w-4,796,main.PANEL)
    title=ET.SubElement(root,'eLabel',text=translator('CAM/SRV Manager'),foregroundColor=main.CYAN,backgroundColor=main.PANEL,halign='center',zPosition='2')
    place(title,80,195,1000,40,28)
    for original_node in ET.fromstring(original):
        name=original_node.get('name')
        if name not in SLOTS:continue
        node=deepcopy(original_node);place(node,*SLOTS[name]);node.set('zPosition','3')
        node.attrib.pop('shadowColor',None);node.attrib.pop('shadowOffset',None)
        if name=='config':
            node.set('itemHeight',str(round(50*sy)));node.set('backgroundColor',main.PANEL)
            node.set('backgroundColorSelected',main.SELECTION);node.set('foregroundColorSelected','#00ffffff');node.set('transparent','0')
        elif name=='select_pict':
            node.attrib.pop('pixmap',None);node.set('backgroundColor',main.SELECTION);node.set('transparent','0');node.set('zPosition','2')
        elif name.startswith('pic') or name.endswith('Pic') or name.startswith('srvArrow'):
            node.set('alphatest','blend');node.set('scale','1')
        else:
            node.set('backgroundColor',main.PANEL);node.set('transparent','1');node.set('foregroundColor','#00ffffff')
            node.set('valign','center');node.set('halign','left' if name!='helpTXT' else 'center')
        root.append(node)
    # Keep first CAM-row arrows, separate from the conditional SRV arrows.
    for direction,x in (('left',75),('right',1070)):
        source=next((n for n in ET.fromstring(original) if n.tag=='ePixmap' and n.get('pixmap','').endswith('/'+direction+'.png')),None)
        if source is not None:
            node=deepcopy(source);place(node,x,250,15,27);root.append(node)
    hint=ET.SubElement(root,'widget',name='focus_hint',foregroundColor=main.CYAN,backgroundColor=main.PANEL,halign='center',valign='center',zPosition='3')
    place(hint,1165,925,670,38,22)
    for i,(name,color) in enumerate((('red','#00ff526a'),('green','#0039ff59'),('yellow','#00ffdb52'),('blue','#0055baff'))):
        x=55+i*457
        fill(x+129,996,200,2,color,3)
        node=ET.SubElement(root,'widget',name=name,foregroundColor=color,backgroundColor=main.BASE,halign='center',valign='center',zPosition='3',noWrap='1')
        place(node,x,1006,440,50,28)
    return ET.tostring(root,encoding='unicode')


def prepare(original,api):
    size=api['getDesktop'](0).size()
    return cam_skin(original,size.width(),size.height(),api['_']) if size.width()>=1280 else original


def install(screen,api):
    if api['getDesktop'](0).size().width()<1280:return
    screen['select_pict']=api['Label']('')
    screen['focus_hint']=api['Label']('')
    screen._warder_cam=Controls(screen,api)
    install_header(screen,api)


class Controls:
    def __init__(self,screen,api):
        self.screen,self.api=screen,api;self.menu=True
        screen['cam_panel_actions']=api['ActionMap'](['DirectionActions','SetupActions','ColorActions'],
            {'left':self.left,'right':self.right,'up':self.up,'down':self.down,'ok':self.choose,'blue':self.next_action},-10)
        screen.onLayoutFinish.append(self.begin)
    def begin(self):self.focus(True)
    def focus(self,menu):
        self.menu=menu
        (self.screen['select_pict'].show if menu else self.screen['select_pict'].hide)()
        self.screen['config'].selectionEnabled(int(not menu))
        self.screen['focus_hint'].setText('◀ '+main.text(self.api,'Details') if menu else main.text(self.api,'Select with OK')+'  |  '+main.text(self.api,'Menu')+' ▶')
        return 1
    def left(self):return self.focus(False)
    def right(self):return self.focus(True)
    def next_action(self):
        self.focus(True);return self.move(1)
    def up(self):return self.move(-1)
    def down(self):return self.move(1)
    def move(self,direction):
        s=self.screen
        if self.menu:
            if direction>0:s.selectFnc()
            else:
                valid=[0,1,2,3,4,6]+([7] if s.numSrv else [])+[8]
                s.idxAllFnc=valid[(valid.index(s.idxAllFnc)-1)%len(valid)]
                position=s['txt%s'%s.idxAllFnc].instance.position()
                s['select_pict'].move(self.api['ePoint'](position.x()-self.api['fhd'](30),position.y()))
                s['helpTXT'].setText(s.aa.get(s.idxAllFnc,''))
        elif s['config'].list:
            count=len(s['config'].list)
            s['config'].setCurrentIndex((s['config'].getCurrentIndex()+direction)%count)
        return 1
    def choose(self):
        s=self.screen
        if self.menu:s.ActivateselectedFnc();return 1
        current=s['config'].getCurrent()
        if not current:return 1
        setting=current[1];self.pending_setting=setting;choices=getattr(setting.choices,'choices',setting.choices)
        values=[(str(item[1]),item[0]) if isinstance(item,(tuple,list)) else (str(item),item) for item in choices]
        s.session.openWithCallback(self.selected,self.api['ChoiceBox'],title=str(current[0]),list=values)
        return 1
    def selected(self,answer):
        if answer:
            current=self.screen['config'].getCurrent()
            if current and current[1] is getattr(self,'pending_setting',None):
                current[1].value=answer[1]
                self.screen['config'].invalidateCurrent()
