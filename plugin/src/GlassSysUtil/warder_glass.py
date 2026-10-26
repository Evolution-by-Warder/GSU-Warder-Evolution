"""Shared clipped banner and single-layer translucent full-screen panels."""
from xml.etree import ElementTree as ET
from enigma import eSize,eWidget,ePixmap
from Components.GUIComponent import GUIComponent
from . import warder_main as main
PANEL_GLASS='#1a102136'
CLEAR='#ff000000'

class HeaderArtwork(GUIComponent):
    """Clip a full-desktop scaled picture inside a header-height native parent."""
    GUI_WIDGET=eWidget
    def __init__(self,width,height):
        GUIComponent.__init__(self);self.width=width;self.height=height;self.picture=None
    def postWidgetCreate(self,instance):
        self.picture=ePixmap(instance)
        self.picture.resize(eSize(self.width,self.height))
        self.picture.setScale(1)
        self.picture.setPixmapFromFile(main.BACKGROUND)
        self.picture.show()
    def preWidgetRemove(self,instance):self.picture=None


def apply(root,width,height):
    sx,sy=width/1920,height/1080
    root.set('backgroundColor',CLEAR)
    for node in list(root):
        if node.tag=='ePixmap' and node.get('pixmap')==main.BACKGROUND:root.remove(node);continue
        if node.tag=='eLabel' and node.get('backgroundColor') in (main.PANEL,main.CYAN):
            x,y=map(int,node.get('position').split(','));w,h=map(int,node.get('size').split(','))
            if h>round(700*sy) and w>round(1700*sx):root.remove(node);continue
        if node.tag in ('widget','eLabel') and node.get('backgroundColor')==main.PANEL:
            node.set('backgroundColor',CLEAR);node.set('transparent','1')
    def place(node,x,y,w,h):
        node.set('position','%d,%d'%(round(x*sx),round(y*sy)));node.set('size','%d,%d'%(round(w*sx),round(h*sy)))
    def fill(x,y,w,h,color,z):place(ET.SubElement(root,'eLabel',backgroundColor=color,zPosition=str(z)),x,y,w,h)
    place(ET.SubElement(root,'widget',name='glass_header_art',zPosition='-3'),0,0,1920,164)
    for bounds in ((0,164,1920,16),(0,180,55,800),(1865,180,55,800),(0,980,1920,100)):fill(*bounds,main.BASE,-2)
    for bounds in ((55,180,1810,2),(55,978,1810,2),(55,182,2,796),(1863,182,2,796)):fill(*bounds,main.CYAN,-2)
    fill(57,182,1806,796,PANEL_GLASS,-1)
    return root
