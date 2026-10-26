"""Full-size common Warder presentation for existing GSU settings."""
from xml.etree import ElementTree as ET
from . import warder_main as main
from .warder_glass import apply,CLEAR
from .warder_system import install as install_header


def skin(width,height):
    root=ET.fromstring(main.main_skin(width,height));sx,sy=width/1920,height/1080
    for node in list(root):
        if node.get('name') not in ('day','date','clock','seconds','version_title','version') and not(node.tag=='ePixmap' and node.get('pixmap')==main.BACKGROUND):root.remove(node)
    root.set('name','WarderGSUSettings')
    def place(node,x,y,w,h):node.set('position','%d,%d'%(round(x*sx),round(y*sy)));node.set('size','%d,%d'%(round(w*sx),round(h*sy)))
    node=ET.SubElement(root,'widget',name='settings_title',foregroundColor=main.CYAN,font='Regular;%d'%round(28*sy),backgroundColor=CLEAR,transparent='1',halign='center',zPosition='3');place(node,80,200,1750,45)
    node=ET.SubElement(root,'widget',name='config',foregroundColor='#00ffffff',backgroundColor=CLEAR,transparent='1',backgroundColorSelected=main.SELECTION,foregroundColorSelected='#00ffffff',font='Regular;%d'%round(25*sy),itemHeight=str(round(48*sy)),zPosition='3',scrollbarMode='showOnDemand');place(node,90,270,1740,650)
    for i,(name,color) in enumerate((('red','#00ff526a'),('green','#0039ff59'))):
        x=55+910*i
        node=ET.SubElement(root,'eLabel',backgroundColor=color,zPosition='3');place(node,x+350,996,200,2)
        node=ET.SubElement(root,'widget',name=name,font='Regular;%d'%round(28*sy),foregroundColor=color,backgroundColor=main.BASE,halign='center',valign='center',zPosition='3');place(node,x,1006,900,50)
    return ET.tostring(apply(root,width,height),encoding='unicode')


def install(screen,api):
    size=api['getDesktop'](0).size()
    if size.width()<1280:return
    screen.skin=skin(size.width(),size.height());screen['settings_title']=api['Label'](main.text(api,'GSU Configuration'))
    install_header(screen,api)
