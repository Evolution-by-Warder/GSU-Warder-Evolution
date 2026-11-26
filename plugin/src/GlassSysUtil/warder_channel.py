"""Shared Warder channel presentation; native data sources and actions are retained."""
from copy import deepcopy
from types import MethodType
from pathlib import Path
from xml.etree import ElementTree as ET
from . import warder_main as main
from .warder_system import install as _install_header

# Coordinates in the receiver's Full HD design space.
SLOTS={
    'ecmlabels':(96,362,165,352,22),'ecmValues':(269,362,425,352,22),
    'bit_labels':(96,780,120,126,20),'bit_min':(222,780,110,100,20),
    'bit_max':(339,780,110,100,20),'bit_avg':(456,780,110,100,20),
    'bit_act':(573,780,110,100,20),'stream_btr':(222,862,464,32,20),
    'tp_lab':(1150,362,246,536,20),'tp_values':(1404,362,414,536,20),
    'tp_lab_sat':(1150,900,246,32,20),'tp_sat':(1404,900,414,32,20),
    'tp_lab_ref':(96,940,150,30,19),'tp_ref':(254,940,1564,30,19),
    'picchannel':(734,382,114,70,None),'picprov':(860,382,114,70,None),
    'picsat':(986,382,114,70,None),'piccode':(790,488,114,70,None),
    'piccam':(928,488,114,70,None),
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
    # Each panel uses the same restrained border and heading treatment.
    for x,y,w,h in ((80,312,630,422),(80,746,630,180),(722,312,400,272),
                    (722,596,400,330),(1136,312,698,622)):
        fill(x,y,w,2,main.CYAN,1)
        fill(x,y+h-2,w,2,main.CYAN,1)
        fill(x,y,2,h,main.CYAN,1)
        fill(x+w-2,y,2,h,main.CYAN,1)
    headings={'ECM Info':(96,320,598,36,27),'Bitrate':(96,750,598,30,25),
              'Transporder':(1150,320,668,36,27),'Signal':(738,608,368,38,27)}
    original_root=ET.fromstring(original)
    source_width,source_height=map(int,original_root.get('size').split(','))
    source_sx=source_width/1920.0
    for original_node in original_root:
        node=deepcopy(original_node);name=node.get('name');text=node.get('text')
        pixmap=node.get('pixmap','')
        if node.tag=='ePixmap' and Path(pixmap).name=='frame.png':continue
        if name in SLOTS:position(node,*SLOTS[name])
        elif text in headings:
            position(node,*headings[text]);node.set('text',translator('Transponder' if text=='Transporder' else text))
            node.set('foregroundColor',main.CYAN);node.set('halign','left')
        elif node.get('source')=='session.CurrentService':
            convert=node.find('convert')
            if convert is not None and convert.text=='Name':position(node,96,190,1722,62,35)
            else:position(node,96,252,1722,42,24)
            node.set('halign','center');node.attrib.pop('shadowColor',None);node.attrib.pop('shadowOffset',None)
        elif node.get('source')=='session.FrontendStatus' or text in ('Snr:','Agc:','Ber:') or Path(pixmap).name=='barmm_back.png':
            # Classify by the source skin's size, not the destination size.
            # This also works for the original 1920 skin on a WQHD desktop.
            old_x=int(node.get('position').split(',')[0])/source_sx
            index=min(range(3),key=lambda i:abs(old_x-(790+112*i)))
            y=664+82*index
            if node.get('render')=='Progress' or Path(pixmap).name=='barmm_back.png':
                position(node,742,y+44,360,10)
                if node.get('render')=='Progress':node.set('orientation','orLeftToRight')
            elif node.get('render')=='Label':position(node,876,y,226,40,26);node.set('halign','right')
            else:position(node,742,y,120,40,26);node.set('text',('SNR:','AGC:','BER:')[index])
        else:
            # Only the old footer line is deliberately superseded.
            continue
        if node.tag in ('widget','eLabel'):
            node.set('backgroundColor',main.BASE if name=='red' else main.PANEL)
            node.set('transparent','1');node.set('zPosition','3')
            if node.get('foregroundColor') in (None,'#666666'):node.set('foregroundColor','#00d1e3f3')
        if (name and name.startswith('pic')) or node.tag=='ePixmap':node.set('alphatest','blend')
        if name in ('ecmlabels','ecmValues','tp_lab','tp_values'):
            node.set('valign','top')
            # Both columns must use identical line height. Long values are
            # shortened deliberately in the controller, never wrapped into the next row.
            node.set('noWrap','1')
        if name in ('tp_sat','tp_ref'):node.set('noWrap','1')
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


def compact_ecm_cam(name,version):
    """Keep the version, but omit a long source commit suffix in the narrow view."""
    from .warder_ecm import compact_cam_version
    return ' '.join(name.replace('\n',compact_cam_version(version)).split())


def caid_rows(caids,max_per_line=6):
    """Render all CAIDs over explicit rows; labels keep their original alignment."""
    values=caids.split()
    if values and all(len(v)==4 and all(c in '0123456789ABCDEFabcdef' for c in v) for v in values):
        return '\n'.join('  '.join(values[i:i+max_per_line]) for i in range(0,len(values),max_per_line))
    return caids


# Common Enigma2 stream type IDs verified against OpenATV and OpenPLi.
VIDEO_CODECS={0:'MPEG2',1:'AVC',2:'H263',3:'VC1',4:'MPEG4-VC',5:'VC1-SM',
              6:'MPEG1',7:'HEVC',8:'VP8',9:'VP9',10:'XVID',13:'DIVX 3.11',
              14:'DIVX 4',15:'DIVX 5',16:'AVS',18:'VP6',21:'SPARK',40:'AVS2'}


def video_codec(info,enum):
    """Return a known native stream codec, not a guess from resolution."""
    key=getattr(enum,'sVideoType',None)
    if info is None or key is None:return None
    try:value=info.getInfo(key)
    except (AttributeError,RuntimeError,TypeError,ValueError):return None
    return VIDEO_CODECS.get(value) if type(value) is int else None


def video_format(aspect,info,enum):
    codec=video_codec(info,enum)
    return aspect+' · '+codec if codec else aspect
