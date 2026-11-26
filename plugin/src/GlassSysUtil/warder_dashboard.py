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
                zPosition='3', **attrs)

    element('ePixmap', 0, 0, 1920, 1080, pixmap=style.BACKGROUND, scale='1', zPosition='0')
    element('eLabel', 52, 167, 1816, 807, backgroundColor=style.CYAN, zPosition='1')
    element('eLabel', 54, 169, 1812, 803, backgroundColor=style.PANEL, zPosition='2')
    label('heading', 92, 183, 1700, 78, 43, style.CYAN, valign='center')
    element('eLabel', 92, 263, 1734, 2, backgroundColor='#00314b65', zPosition='3')
    if mode == 'menu':
        element('widget', 92, 300, 1018, 626, name='list', scrollbarMode='showOnDemand',
                backgroundColor=style.PANEL, foregroundColor='#00ffffff',
                foregroundColorSelected='#00ffffff', backgroundColorSelected=style.SELECTION,
                zPosition='3')
        label('descriptions', 1160, 308, 625, 570, 32, '#00d1e3f3')
    elif mode == 'chart':
        label('metric', 95, 290, 1520, 105, 55, '#00ffffff', valign='center')
        element('widget', 95, 414, 1730, 330, source='history', render='Canvas', zPosition='3')
        label('details', 95, 765, 1705, 180, 31, '#00d1e3f3')
    else:
        label('file_info', 92, 295, 1740, 630, 32, '#00ffffff', scrollbarMode='showOnDemand')
    colors = ('#00ff526a', '#0039ff59', '#00ffdb52', '#0045b9ff')
    for i, (name, color) in enumerate(zip(('red', 'green', 'yellow', 'blue'), colors)):
        label(name, 55 + 455*i, 990, 443, 81, 28, color, halign='center', valign='center')
    return ET.tostring(root, encoding='unicode')
