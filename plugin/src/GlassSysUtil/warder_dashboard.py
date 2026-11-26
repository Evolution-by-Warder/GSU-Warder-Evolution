"""Resolution-independent panels for the diagnostic menu, reports and charts."""
from xml.etree import ElementTree as ET
from . import warder_main as style


def dimensions(api):
    size = api['getDesktop'](0).size()
    return size.width(), size.height()


def skin(width, height, mode):
    # Panel coordinates use the same design space and artwork as the main menu.
    sx, sy = width / 1920, height / 1080
    root = ET.Element('screen', name='GSUDiagnostics' + mode.title(),
                      position='0,0', size='%d,%d' % (width, height),
                      flags='wfNoBorder', backgroundColor=style.BASE)

    def element(tag, x, y, w, h, **attrs):
        return ET.SubElement(root, tag, position='%d,%d' % (round(x*sx), round(y*sy)),
                             size='%d,%d' % (round(w*sx), round(h*sy)), **attrs)

    def label(name, x, y, w, h, points, color, **attrs):
        element('widget', x, y, w, h, name=name, font='Regular;%d' % max(1, round(points*sy)),
                foregroundColor=color, backgroundColor=style.PANEL, transparent='1',
                zPosition='5', **attrs)

    # Native ScrollLabel forwards zPosition to child labels, not its parent.
    # Its root eWidget stays at zero; every covering backing must be negative.
    element('ePixmap', 0, 0, 1920, 1080, pixmap=style.BACKGROUND, scale='1', zPosition='-3')
    element('eLabel', 52, 167, 1816, 807, backgroundColor=style.CYAN, zPosition='-2')
    element('eLabel', 54, 169, 1812, 803, backgroundColor=style.PANEL, zPosition='-1')
    label('heading', 92, 183, 1700, 78, 43, style.CYAN, valign='center')
    element('eLabel', 92, 263, 1734, 2, backgroundColor='#00314b65', zPosition='3')
    if mode == 'menu':
        element('widget', 92, 300, 1018, 626, name='list', scrollbarMode='showOnDemand',
                backgroundColor=style.PANEL, foregroundColor='#00ffffff',
                foregroundColorSelected='#00ffffff', backgroundColorSelected=style.SELECTION,
                zPosition='3')
        label('descriptions', 1160, 308, 625, 570, 32, '#00d1e3f3')
    elif mode == 'overview':
        for index in range(6):
            col, row = index % 3, index // 3
            x, y = 92 + col*586, 290 + row*230
            element('eLabel', x, y, 558, 207, backgroundColor='#00172539', zPosition='3')
            element('eLabel', x, y+22, 4, 165, backgroundColor=style.CYAN, zPosition='4')
            label('label%d'%index, x+24, y+12, 505, 58, 26, '#00bcd2df')
            label('value%d'%index, x+24, y+72, 505, 108, 48, '#00ffffff', valign='center')
        label('summary', 92, 765, 1725, 165, 31, style.CYAN)
    elif mode == 'chart':
        label('metric', 95, 290, 1520, 105, 55, '#00ffffff', valign='center')
        element('widget', 95, 414, 1730, 330, source='history', render='Canvas', zPosition='3')
        label('details', 95, 765, 1705, 180, 31, '#00d1e3f3')
    else:
        label('file_info', 92, 295, 1740, 630, 32, '#00ffffff', scrollbarMode='showOnDemand')
    colors = ('#00ff526a', '#0039ff59', '#00ffdb52', '#0045b9ff')
    for i, (name, color) in enumerate(zip(('red', 'green', 'yellow', 'blue'), colors)):
        label(name, 55 + 455*i, 990, 443, 81, 28, color, halign='center', valign='center', noWrap='1')
    return ET.tostring(root, encoding='unicode')


def cam_panel(original, width, height, tr):
    """Present legacy CAM components in a TV-sized panel with separate footer space."""
    old = ET.fromstring(original)
    ow, oh = map(int,old.get('size').split(','))
    sx, sy = width/1920, height/1080
    frame = ET.Element('screen', name='Warder'+old.get('name','CAM'), position='0,0',
                       size='%d,%d' % (width,height), flags='wfNoBorder',backgroundColor=style.BASE)
    def box(node,x,y,w,h):
        node.set('position','%d,%d'%(round(x*sx),round(y*sy)))
        node.set('size','%d,%d'%(max(1,round(w*sx)),max(1,round(h*sy))))
    box(ET.SubElement(frame,'ePixmap',pixmap=style.BACKGROUND,scale='1',zPosition='-3'),0,0,1920,1080)
    box(ET.SubElement(frame,'eLabel',backgroundColor=style.PANEL,zPosition='-1'),55,168,1810,803)
    title = ET.SubElement(frame,'eLabel',text=tr(old.get('title','CAM')),font='Regular;%d'%round(40*sy),
                          foregroundColor=style.CYAN,backgroundColor=style.PANEL,zPosition='2')
    box(title,85,184,1740,68)
    footers = {'red','green','yellow','blue','enaButton','disButton'}
    cutoff = min((int(n.get('position').split(',')[1]) for n in old if n.get('name') in footers),default=oh)
    scale_y = 680/max(1,cutoff)
    for node in old:
        if 'position' not in node.attrib or 'size' not in node.attrib:
            continue
        x,y = map(int,node.get('position').split(','))
        w,h = map(int,node.get('size').split(','))
        name = node.get('name')
        if name in footers:
            box(node,55+x*1810/ow,990,w*1810/ow,70)
            node.set('halign','center')
            node.set('valign','center')
        elif y >= cutoff-16*height/1080 and node.tag=='eLabel' and not node.get('text'):
            continue
        else:
            box(node,85+x*1750/ow,273+y*scale_y,min(w,ow-x)*1750/ow,
                max(1,min(h,cutoff-y))*scale_y)
        node.set('zPosition','3')
        if node.tag=='widget':
            node.set('backgroundColor',style.PANEL)
            if name in style.LIST_WIDGETS:
                node.set('backgroundColorSelected',style.SELECTION)
                node.set('scrollbarMode','showOnDemand')
            elif node.get('font'):
                node.set('font','Regular;%d'%round((29 if name in footers else 26)*sy))
                if node.get('foregroundColor') in (None,'#666666'):
                    node.set('foregroundColor','#00e2edf5')
        frame.append(node)
    return ET.tostring(frame,encoding='unicode')


def cam_skin(original, api):
    from .i18n import for_api
    return cam_panel(original,*dimensions(api),lambda key:for_api(api,key))
