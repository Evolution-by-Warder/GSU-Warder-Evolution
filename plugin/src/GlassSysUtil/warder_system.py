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
            # Keep approved device size and horizontal centers; each picture
            # precedes its own data block. Navigation arrows are unchanged.
            side=min(round(pw*1.2),ph) if '/devices/' in pixmap else min(pw,ph)
            node.set('position','%d,%d'%(px+(pw-side)//2,py+(ph-side)//2))
            node.set('size','%d,%d'%(side,side))
            if '/devices/' in pixmap:
                row_y=190 if y/sy<400 else 445 if y/sy<700 else 700
                node.set('position','%d,%d'%(px+(pw-side)//2,round(row_y*sy)))
            node.set('scale','1')
            if '/devices/' in pixmap and y>=round(700*sy):
                lower_icons.append(node)
        elif '/bp_icons/' in pixmap and basename in ('red','green'):
            node.set('pixmap',main.BACKGROUND.rsplit('/',1)[0]+'/system-status-'+basename+'.png')
            node.set('scale','1')
        if node.tag=='ePixmap':node.set('alphatest','blend')
        if y/sy>=870:  # Protocol captions and both states of each status dot.
            nx,ny=map(int,node.get('position').split(','))
            nw,nh=map(int,node.get('size').split(','))
            ny+=round(26*sy)
            node.set('position','%d,%d'%(nx,ny))
            node.set('size','%d,%d'%(nw,min(nh,round(978*sy)-ny)))
        root.append(node)
    def move_meter(meter,target_y,backing_name):
        original_position=meter.get('position')
        original_size=meter.get('size')
        mx=int(original_position.split(',')[0])
        for node in root:
            if node is meter or (node.tag=='ePixmap' and
                    Path(node.get('pixmap','')).name==backing_name and
                    node.get('position')==original_position and node.get('size')==original_size):
                node.set('position','%d,%d'%(mx,target_y))

    # Keep memory/storage meters beside their data after moving each block.
    rows=(('ram',280,('mem_labels','ram','swap','mem_tot','root'),
           ('membar','swapbar','memtotalbar','rootbar')),
          ('hdd',535,('space_labels','hdd','usb','cf','sd'),
           ('hddbar','usbbar','cfbar','sdbar')),
          ('cpu',790,('HDDCPULabels','HDDTemperature','hdddev','cpu','sensors'),()))
    for reference,target,names,meters in rows:
        anchor=root.find("widget[@name='%s']"%reference)
        delta=round(target*sy)-int(anchor.get('position').split(',')[1])
        for name in meters:
            meter=root.find("widget[@name='%s']"%name)
            move_meter(meter,int(meter.get('position').split(',')[1])+delta,'bar_back.png')
        for name in names:
            field=root.find("widget[@name='%s']"%name)
            fx=int(field.get('position').split(',')[0])
            field.set('position','%d,%d'%(fx,round(target*sy)))
            if target==790:
                fw=int(field.get('size').split(',')[0])
                field.set('size','%d,%d'%(fw,round(58*sy)))

    # Lower meters stay bottom-aligned with their adjacent device pictures.
    for name in ('hddtempbar','hddstate','cpubar','tempDBbar'):
        meter=root.find("widget[@name='%s']"%name)
        if meter is None or not lower_icons:continue
        mx=int(meter.get('position').split(',')[0])
        mh=int(meter.get('size').split(',')[1])
        adjacent=[n for n in lower_icons if int(n.get('position').split(',')[0])>mx]
        if not adjacent:continue
        icon=min(adjacent,key=lambda n:int(n.get('position').split(',')[0])-mx)
        iy=int(icon.get('position').split(',')[1])
        ih=int(icon.get('size').split(',')[1])
        move_meter(meter,iy+ih-mh,'barm_back.png')
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
