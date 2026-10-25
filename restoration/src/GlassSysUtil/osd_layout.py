"""Responsive scrolling ECM strip and shared on-screen position constraints."""
from xml.etree import ElementTree


def rolling_skin(skin,desktop_width):
    root=ElementTree.fromstring(skin)
    _,height=map(int,root.get('size').split(','))
    width=max(1,int(desktop_width)//2)
    root.set('size','%s,%s' % (width,height))
    x,y=map(int,root.get('position').split(','))
    root.set('position','%s,%s' % (max(0,min(x,int(desktop_width)-width)),y))
    edge=max(1,height//17);margin=edge*2
    # Native rectangles keep the old blue frame thin at any strip width.
    for node in list(root):
        if node.tag=='ePixmap':root.remove(node)
    for position,size,color,z in (
        ('0,0','%s,%s' % (width,height),'#00000080','0'),
        ('%s,%s' % (edge,edge),'%s,%s' % (max(1,width-2*edge),max(1,height-2*edge)),'#00101018','1')):
        root.append(ElementTree.Element('eLabel',position=position,size=size,backgroundColor=color,zPosition=z))
    text=next(node for node in root if node.get('name')=='OSD_Ecm_info')
    _,y=map(int,text.get('position').split(','));_,text_height=map(int,text.get('size').split(','))
    text.set('position','%s,%s' % (margin,y))
    text.set('size','%s,%s' % (max(1,width-2*margin),text_height))
    text.set('zPosition','2')
    return ElementTree.tostring(root,encoding='unicode')


def place(screen,api,editing=False):
    if screen.instance is None:return
    desktop=api['getDesktop'](0).size();window=screen.instance.size()
    settings=api['config'].plugins.GlassSysUtil
    x=max(0,min(settings.par1.value,max(0,desktop.width()-window.width())))
    y=max(0,min(settings.par2.value,max(0,desktop.height()-window.height())))
    if editing:
        settings.par1.value=x;settings.par2.value=y
    screen.instance.move(api['ePoint'](x,y))
