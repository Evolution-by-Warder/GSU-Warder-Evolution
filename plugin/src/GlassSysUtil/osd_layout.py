"""Responsive scrolling ECM strip and shared on-screen position constraints."""
from xml.etree import ElementTree


def rolling_skin(skin,desktop_width):
    root=ElementTree.fromstring(skin)
    _,height=map(int,root.get('size').split(','))
    inset=max(1,int(desktop_width)//32)
    width=max(1,int(desktop_width)//2-inset)
    root.set('size','%s,%s' % (width,height))
    x,y=map(int,root.get('position').split(','))
    root.set('position','%s,%s' % (max(0,min(x,int(desktop_width)-width-inset)),y))
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


def right_limit(screen,api):
    width=api['getDesktop'](0).size().width()
    static=api['config'].plugins.GlassSysUtil.par3.value
    inset=0 if static else max(1,width//32)
    return max(0,width-screen.instance.size().width()-inset)


def place(screen,api,editing=False):
    if screen.instance is None:return
    desktop=api['getDesktop'](0).size();window=screen.instance.size()
    settings=api['config'].plugins.GlassSysUtil
    horizontal,vertical=position_settings(api)
    x=max(0,min(horizontal.value,right_limit(screen,api)))
    y=max(0,min(vertical.value,max(0,desktop.height()-window.height())))
    if editing:
        horizontal.value=x;vertical.value=y
    screen.instance.move(api['ePoint'](x,y))


def position_settings(api):
    settings=api['config'].plugins.GlassSysUtil
    if settings.par3.value and hasattr(settings,'static_osd_x'):
        return settings.static_osd_x,settings.static_osd_y
    return settings.par1,settings.par2


def init_static_position(api):
    """Migrate an explicitly stored legacy position, preserving user placement."""
    settings=api['config'].plugins.GlassSysUtil
    if any(getattr(getattr(settings,key),'saved_value',None) is not None for key in ('static_osd_x','static_osd_y')):return
    if (settings.par1.value,settings.par2.value)==(1030,70):return
    if not any(getattr(getattr(settings,key),'saved_value',None) is not None for key in ('par1','par2')):return
    for target,source in ((settings.static_osd_x,settings.par1),(settings.static_osd_y,settings.par2)):
        target.value=source.value;target.save()
