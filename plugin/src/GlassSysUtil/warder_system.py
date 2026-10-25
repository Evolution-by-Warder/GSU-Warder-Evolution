"""Present existing system widgets inside the common Warder frame."""
from copy import deepcopy
from pathlib import Path
from xml.etree import ElementTree as ET
from . import warder_main as main


def system_skin(original,width,height,translator=lambda value:value):
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
    for node in root.findall('ePixmap'):
        node.set('zPosition','-3')
    def fill(x,y,w,h,color):
        ET.SubElement(root,'eLabel',position='%d,%d'%(round(x*sx),round(y*sy)),size='%d,%d'%(round(w*sx),round(h*sy)),backgroundColor=color,zPosition='-2' if color==main.CYAN else '-1')
    fill(55,180,1810,800,main.CYAN)
    fill(57,182,1806,796,main.PANEL)
    lower_icons=[]
    for original_node in old:
        node=deepcopy(original_node)
        if node.get('name') in ('red','green','yellow'):continue
        x,y=map(int,node.get('position','0,0').split(','))
        w,h=map(int,node.get('size','0,0').split(','))
        if y/sy>=975:continue  # Old footer and its full-width color lines.
        node.set('position','%d,%d'%(x,round((190+(y/sy-75)*0.84)*sy)))
        node.set('size','%d,%d'%(w,max(1,min(round(h*0.84),round(978*sy)-int(node.get('position').split(',')[1])))))
        if node.get('text'):node.set('text',translator(node.get('text')))
        if node.get('font'):
            family,size=node.get('font').rsplit(';',1)
            node.set('font','Regular;%d'%max(12,round(int(size)*0.84)))
        if node.tag in ('widget','eLabel'):
            node.set('backgroundColor',main.PANEL)
            node.set('transparent','1')
            if node.get('foregroundColor') in (None,'#666666'):
                node.set('foregroundColor','#00d1e3f3')
        pixmap=node.get('pixmap','')
        basename=Path(pixmap).stem
        if '/devices/' in pixmap or basename in ('lr','updown'):
            node.set('pixmap',main.BACKGROUND.rsplit('/',1)[0]+'/system-'+basename+'.png')
            px,py=map(int,node.get('position').split(','))
            pw,ph=map(int,node.get('size').split(','))
            # Device slots have spare horizontal room; retain their centers and
            # vertical bounds. Navigation arrows keep their approved size.
            side=min(round(pw*1.2),ph) if '/devices/' in pixmap else min(pw,ph)
            node.set('position','%d,%d'%(px+(pw-side)//2,py+(ph-side)//2))
            node.set('size','%d,%d'%(side,side))
            node.set('scale','1')
            if '/devices/' in pixmap and y>=round(700*sy):
                lower_icons.append(node)
        elif '/bp_icons/' in pixmap and basename in ('red','green'):
            node.set('pixmap',main.BACKGROUND.rsplit('/',1)[0]+'/system-status-'+basename+'.png')
            node.set('scale','1')
        if node.tag=='ePixmap':node.set('alphatest','blend')
        root.append(node)
    # Move each lower meter and its backing together to its adjacent icon.
    # Do this after collecting pictures so XML ordering cannot affect alignment.
    for name in ('hddtempbar','hddstate','cpubar','tempDBbar'):
        meter=root.find("widget[@name='%s']"%name)
        if meter is None or not lower_icons:continue
        mx,my=map(int,meter.get('position').split(','))
        mw,mh=map(int,meter.get('size').split(','))
        adjacent=[n for n in lower_icons if int(n.get('position').split(',')[0])>mx]
        if not adjacent:continue
        icon=min(adjacent,key=lambda n:int(n.get('position').split(',')[0])-mx)
        iy=int(icon.get('position').split(',')[1])
        ih=int(icon.get('size').split(',')[1])
        # Match the backing by its original geometry before moving the meter.
        original_position=meter.get('position')
        for node in root:
            if node is meter or (node.tag=='ePixmap' and
                    Path(node.get('pixmap','')).name=='barm_back.png' and
                    node.get('position')==original_position and
                    node.get('size')==meter.get('size')):
                node.set('position','%d,%d'%(mx,iy+ih-mh))
        meter.set('position','%d,%d'%(mx,iy+ih-mh))
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
