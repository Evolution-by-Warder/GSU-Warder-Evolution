"""Present existing system widgets inside the common Warder frame."""
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET
from . import warder_main as main


def system_skin(original,width,height):
    old=ET.fromstring(original)
    sx,sy=width/1920.0,height/1080.0
    root=ET.fromstring(main.main_skin(width,height))
    header={'day','date','clock','seconds','version_title','version'}
    # Keep the single shared backdrop and header, replacing the menu body.
    for node in list(root):
        y=int(node.get('position','0,0').split(',')[1])
        if not (node.tag=='ePixmap' and y==0) and node.get('name') not in header and y>=round(164*sy):
            root.remove(node)
    root.set('name','WarderGSUSystem')
    def fill(x,y,w,h,color):
        ET.SubElement(root,'eLabel',position='%d,%d'%(round(x*sx),round(y*sy)),size='%d,%d'%(round(w*sx),round(h*sy)),backgroundColor=color,zPosition='0')
    fill(55,180,1810,800,main.CYAN)
    fill(57,182,1806,796,main.PANEL)
    for original_node in old:
        node=deepcopy(original_node)
        if node.get('name') in ('red','green','yellow'):continue
        x,y=map(int,node.get('position','0,0').split(','))
        w,h=map(int,node.get('size','0,0').split(','))
        if y/sy>=975:continue  # Old footer and its full-width color lines.
        node.set('position','%d,%d'%(x,round((190+(y/sy-75)*0.84)*sy)))
        node.set('size','%d,%d'%(w,max(1,min(round(h*0.84),round(978*sy)-int(node.get('position').split(',')[1])))))
        if node.get('font'):
            family,size=node.get('font').rsplit(';',1)
            node.set('font','Regular;%d'%max(12,round(int(size)*0.84)))
        if node.tag in ('widget','eLabel'):
            node.set('backgroundColor',main.PANEL)
            node.set('transparent','0')
            if node.get('foregroundColor') in (None,'#666666'):
                node.set('foregroundColor','#00d1e3f3')
        root.append(node)
    for index,(name,color) in enumerate((('red','#00ff526a'),('green','#0039ff59'),('yellow','#00ffdb52'))):
        x=55+index*610
        fill(x+195,996,200,2,color)
        ET.SubElement(root,'widget',name=name,position='%d,%d'%(round(x*sx),round(1006*sy)),size='%d,%d'%(round(590*sx),round(50*sy)),font='Regular;%d'%round(28*sy),foregroundColor=color,backgroundColor=main.BASE,transparent='0',halign='center',valign='center',zPosition='3',noWrap='1')
    return ET.tostring(root,encoding='unicode')


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
