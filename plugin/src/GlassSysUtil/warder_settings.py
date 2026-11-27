"""Full-size common Warder presentation for existing GSU settings."""
from xml.etree import ElementTree as ET
from . import warder_main as main
from .warder_glass import apply,CLEAR
from .warder_system import install as install_header


from .warder_menu_icons import ROOT as ICON_ROOT

# Resolve by ConfigElement identity; translated labels never determine the symbol.
SETTING_ICONS=(('par51','system'),('par52','ecosystem'),('par53','info'),
    ('par54','tv'),('par56','key'),('par60','key'),('par57','network'),
    ('par58','history'),('par61','log'),('par62','settings'))


def setting_icons(entries,settings):
    if len(entries)!=len(SETTING_ICONS):return ()
    result=[]
    for entry in entries:
        matches=[icon for key,icon in SETTING_ICONS
                 if getattr(settings,key,None) is entry[1]]
        if len(matches)!=1:return ()
        result.append(matches[0])
    return tuple(result)


def skin(width,height,icons=()):
    root=ET.fromstring(main.main_skin(width,height));sx,sy=width/1920,height/1080
    for node in list(root):
        if node.get('name') not in ('day','date','clock','seconds','version_title','version') and not(node.tag=='ePixmap' and node.get('pixmap')==main.BACKGROUND):root.remove(node)
    root.set('name','WarderGSUSettings')
    def place(node,x,y,w,h):node.set('position','%d,%d'%(round(x*sx),round(y*sy)));node.set('size','%d,%d'%(round(w*sx),round(h*sy)))
    node=ET.SubElement(root,'widget',name='settings_title',foregroundColor=main.CYAN,font='Regular;%d'%round(28*sy),backgroundColor=CLEAR,transparent='1',halign='center',zPosition='3');place(node,80,200,1750,45)
    node=ET.SubElement(root,'widget',name='config',foregroundColor='#00ffffff',backgroundColor=CLEAR,transparent='1',backgroundColorSelected=main.SELECTION,foregroundColorSelected='#00ffffff',font='Regular;%d'%round(25*sy),itemHeight=str(round(48*sy)),zPosition='3',scrollbarMode='showOnDemand');place(node,90,270,1740,650)
    row_height=int(node.get('itemHeight'))
    rows=round(650*sy)//row_height
    # Keep the native ConfigList and its edit semantics. Only use a fixed icon
    # gutter if every setting is known and every row fits without scrolling.
    valid=bool(icons) and len(icons)<=rows and all((ICON_ROOT/('nav-'+name+'.png')).is_file() for name in icons)
    left=150 if valid else 90
    node.set('position','%d,%d'%(round(left*sx),round(270*sy)))
    node.set('size','%d,%d'%(round((1830-left)*sx),rows*row_height))
    if valid:
        side=min(round(40*sy),row_height)
        for index,name in enumerate(icons):
            image=ET.SubElement(root,'ePixmap',pixmap=str(ICON_ROOT/('nav-'+name+'.png')),
                alphatest='blend',scale='1',zPosition='3')
            image.set('position','%d,%d'%(round(100*sx),round(270*sy)+index*row_height+(row_height-side)//2))
            image.set('size','%d,%d'%(side,side))
    for i,(name,color) in enumerate((('red','#00ff526a'),('green','#0039ff59'))):
        x=55+910*i
        node=ET.SubElement(root,'eLabel',backgroundColor=color,zPosition='3');place(node,x+350,996,200,2)
        node=ET.SubElement(root,'widget',name=name,font='Regular;%d'%round(28*sy),foregroundColor=color,backgroundColor=main.BASE,halign='center',valign='center',zPosition='3');place(node,x,1006,900,50)
    return ET.tostring(apply(root,width,height),encoding='unicode')


def install(screen,api):
    size=api['getDesktop'](0).size()
    if size.width()<1280:return
    icons=setting_icons(screen['config'].list,api['config'].plugins.GlassSysUtil)
    screen.skin=skin(size.width(),size.height(),icons);screen['settings_title']=api['Label'](main.text(api,'GSU Configuration'))
    install_header(screen,api)
