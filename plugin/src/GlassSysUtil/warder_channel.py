"""Shared Warder channel presentation; native data sources and actions are retained."""
from copy import deepcopy
from types import MethodType
from pathlib import Path
from xml.etree import ElementTree as ET
from . import warder_main as main
from .warder_system import install as _install_header

# Coordinates in the receiver's Full HD design space.
SLOTS={
    'ecmlabels':(85,355,175,365,22),'ecmValues':(270,355,395,365,22),
    'bit_labels':(85,800,125,130,20),'bit_min':(220,800,85,100,20),
    'bit_max':(310,800,85,100,20),'bit_avg':(400,800,85,100,20),
    'bit_act':(490,800,100,100,20),'stream_btr':(220,883,440,30,20),
    'tp_lab':(1205,355,255,510,21),'tp_values':(1470,355,360,510,21),
    'tp_lab_sat':(1205,900,255,35,21),'tp_sat':(1470,900,360,35,21),
    'tp_lab_ref':(85,935,155,30,19),'tp_ref':(245,935,1585,30,19),
    'picchannel':(710,360,140,84,None),'picprov':(865,360,140,84,None),
    'picsat':(1020,360,140,84,None),'piccode':(785,540,140,84,None),
    'piccam':(960,540,140,84,None),
    'red':(55,1006,1810,50,28),
}


def channel_skin(original,width,height,translator=lambda value:value):
    sx,sy=width/1920.0,height/1080.0
    root=ET.fromstring(main.main_skin(width,height))
    headers={'day','date','clock','seconds','version_title','version'}
    for node in list(root):
        if node.get('name') not in headers and not (node.tag=='ePixmap' and node.get('pixmap')==main.BACKGROUND):root.remove(node)
    root.set('name','WarderGSUChannel')
    root.find('ePixmap').set('zPosition','-3')
    def position(node,x,y,w,h,font=None):
        node.set('position','%d,%d'%(round(x*sx),round(y*sy)))
        node.set('size','%d,%d'%(round(w*sx),round(h*sy)))
        if font:node.set('font','Regular;%d'%round(font*sy))
        return node
    def fill(x,y,w,h,color,z):
        return position(ET.SubElement(root,'eLabel',backgroundColor=color,zPosition=str(z)),x,y,w,h)
    fill(55,180,1810,800,main.CYAN,-2)
    fill(57,182,1806,796,main.PANEL,-1)
    for x in (690,1185):fill(x,300,1,610,'#00364b61',0)
    headings={'ECM Info':(85,300,580,42,29),'Bitrate':(85,750,580,42,29),
              'Transporder':(1205,300,625,42,29),'Signal':(720,745,440,42,29)}
    for original_node in ET.fromstring(original):
        node=deepcopy(original_node);name=node.get('name');text=node.get('text')
        pixmap=node.get('pixmap','')
        if node.tag=='ePixmap' and Path(pixmap).name=='frame.png':continue
        if name in SLOTS:position(node,*SLOTS[name])
        elif text in headings:
            position(node,*headings[text]);node.set('text',translator('Transponder' if text=='Transporder' else text))
            node.set('foregroundColor',main.CYAN);node.set('halign','left')
        elif node.get('source')=='session.CurrentService':
            convert=node.find('convert')
            if convert is not None and convert.text=='Name':position(node,85,192,1745,53,34)
            else:position(node,710,260,460,45,24)
            node.set('halign','center');node.attrib.pop('shadowColor',None);node.attrib.pop('shadowOffset',None)
        elif node.get('source')=='session.FrontendStatus' or text in ('Snr:','Agc:','Ber:') or Path(pixmap).name=='barmm_back.png':
            old_x=int(node.get('position').split(',')[0])/sx
            index=min(range(3),key=lambda i:abs(old_x-(790+112*i)))
            x=735+145*index
            if node.get('render')=='Progress' or Path(pixmap).name=='barmm_back.png':position(node,x,804,7,65)
            elif node.get('render')=='Label':position(node,x+17,840,120,32,22)
            else:position(node,x+17,804,120,32,22)
        else:
            # Only the old footer line is deliberately superseded.
            continue
        if node.tag in ('widget','eLabel'):
            node.set('backgroundColor',main.BASE if name=='red' else main.PANEL)
            node.set('transparent','1');node.set('zPosition','3')
            if node.get('foregroundColor') in (None,'#666666'):node.set('foregroundColor','#00d1e3f3')
        if (name and name.startswith('pic')) or node.tag=='ePixmap':node.set('alphatest','blend')
        if name=='red':node.set('foregroundColor','#00ff526a');node.set('halign','center');node.set('valign','center')
        root.append(node)
    fill(860,996,200,2,'#00ff526a',3)
    from .warder_glass import apply
    apply(root,width,height)
    for node in root:
        if node.get('source')=='session.FrontendStatus' and node.get('render')=='Progress':
            node.set('backgroundColor','#00102136')
            node.set('transparent','0')
        elif node.tag=='ePixmap' and Path(node.get('pixmap','')).name=='barmm_back.png':
            node.set('backgroundColor','#00102136')
            node.set('alphatest','off')
    return ET.tostring(root,encoding='unicode')


def install(screen,api):
    _install_header(screen,api)
    def align_satellite(owner):
        from enigma import ePoint,eSize
        size=api['getDesktop'](0).size();sx,sy=size.width()/1920,size.height()/1080
        for name in ('tp_lab_sat','tp_sat'):
            node=owner[name].instance
            if node is not None:
                x,y,w,h,_=SLOTS[name]
                node.move(ePoint(round(x*sx),round(y*sy)))
                node.resize(eSize(round(w*sx),round(h*sy)))
    screen.onLayoutFinish.append(MethodType(align_satellite,screen))
