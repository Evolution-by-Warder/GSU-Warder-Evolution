"""Expose the original standalone-server controls only for installed UCM servers."""
import os
import re
import shlex
from pathlib import Path
from xml.etree import ElementTree


def binary_status(name,script_dir='/usr/UCM_CamSrv_script',bin_dir='/usr/UCM_CamSrv_bin'):
    if not re.fullmatch(r'[A-Za-z0-9_+.-]+',name or ''):return 'Error Reading Script'
    try:
        script=(Path(script_dir)/(name+'_Srv.sh')).resolve(strict=True)
        if script.parent!=Path(script_dir).resolve() or not script.is_file() or not os.access(script,os.X_OK):return 'Error Reading Script'
        with script.open() as stream:
            for line in stream.read(65536).splitlines():
                if not line.startswith('SrvBin='):continue
                values=shlex.split(line[len('SrvBin='):],comments=True)
                if len(values)!=1 or not re.fullmatch(r'[A-Za-z0-9_+.-]+',values[0]):return 'Undefined BIN'
                binary=Path(bin_dir)/values[0]
                return 'Ok' if binary.is_file() and os.access(binary,os.X_OK) else 'Missing BIN'
    except (OSError,ValueError,RuntimeError):return 'Error Reading Script'
    return 'Undefined BIN'


def menu_text(screen,translate,text):
    result=translate(text)
    return result if getattr(screen,'numSrv',0)>0 else result.replace('CAM/SRV','CAM')


def prepare_skin(skin):
    """Name the existing second-row arrows so they can follow SRV visibility."""
    root=ElementTree.fromstring(skin)
    arrows=[node for node in root if node.tag=='ePixmap' and node.get('pixmap','').endswith(('/left.png','/right.png'))]
    if arrows:
        second_y=max(int(node.get('position').split(',')[1]) for node in arrows)
        for node in arrows:
            if int(node.get('position').split(',')[1])==second_y:
                node.tag='widget'
                node.set('name','srvArrowLeft' if node.get('pixmap').endswith('/left.png') else 'srvArrowRight')
    return ElementTree.tostring(root,encoding='unicode')


def apply(screen,api):
    from enigma import eSize
    visible=screen.numSrv>0
    if not hasattr(screen,'srvLayout'):
        nodes={node.get('name'):node for node in ElementTree.fromstring(screen.skin) if node.tag=='widget'}
        screen.srvLayout={name:dict(node.attrib) for name,node in nodes.items()}
    layout=screen.srvLayout
    for name in ('activSrv','SrvPic','txt7','srvArrowLeft','srvArrowRight'):
        (screen[name].show if visible else screen[name].hide)()
    config=layout['config'];width,height=map(int,config['size'].split(','))
    item_height=int(config['itemHeight'])
    screen['config'].instance.resize(eSize(width,height if visible else item_height+2))
    for name,slot in (('txt8','txt7'),('txt9','txt8')):
        position=layout[name if visible else slot]['position']
        x,y=map(int,position.split(','));screen[name].instance.move(api['ePoint'](x,y))
    if not visible:
        if screen['config'].getCurrentIndex()!=0:screen['config'].setCurrentIndex(0)
        if screen.idxAllFnc==7:screen.idxAllFnc=8
    # Refresh translated captions after package installation/removal in this screen.
    for name,text in (('txt1','Download CAM/SRV'),('txt2','Delete CAM/SRV')):
        screen[name].setText(menu_text(screen,api['_'],text))
    screen.enaAutochckChck()
    help_text={0:'Exit CAM/SRV Manager',1:'Downloading CAM/SRV from server and installing to CAM/SRV Manager',2:'Deleting CAM/SRV from CAM/SRV Manager',6:'Delayed start in seconds of CAM/SRV after start E2',9:'Preparing experimental image to use CAM/SRV and disabling dccamd'}
    for key,text in help_text.items():screen.aa[key]=menu_text(screen,api['_'],text)
    screen['helpTXT'].setText(screen.aa.get(screen.idxAllFnc,''))
    screen.setTitle(menu_text(screen,api['_'],'CAM/SRV Manager'))
    selected=screen['txt%s' % screen.idxAllFnc].instance.position()
    screen['select_pict'].move(api['ePoint'](selected.x()-api['fhd'](30),selected.y()))
