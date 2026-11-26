"""Resolution-independent panels for the diagnostic menu, reports and charts."""
from xml.etree import ElementTree as ET
from . import warder_main as style


PROCESS_COLUMNS=((16,155),(188,690),(895,125),(1045,225),(1290,340))
INLINE_PROCESS_COLUMNS=((8,110),(126,410),(548,50),(610,150),(772,160))


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
    # All full-screen diagnostic views share the original brand/header.
    for name,x,y,w,h,points,color,align in (
            ('day',1100,25,280,36,25,'#00ffffff','right'),
            ('date',960,70,420,36,24,'#00ffffff','right'),
            ('clock',1398,27,190,85,62,'#00ffffff','center'),
            ('seconds',1590,52,66,54,38,'#00ffffff','left'),
            ('version_title',1680,25,210,36,25,style.CYAN,'center'),
            ('version',1680,70,210,36,24,style.CYAN,'center')):
        label(name,x,y,w,h,points,color,halign=align,valign='center',noWrap='1')
    element('eLabel',1392,25,2,84,backgroundColor=style.CYAN,zPosition='1')
    element('eLabel',1664,25,2,84,backgroundColor=style.CYAN,zPosition='1')
    label('heading', 92, 181, 1340 if mode in ('multichart','signal-multichart') else 1700, 72, 40, style.CYAN, valign='center',noWrap='1')
    element('eLabel', 92, 263, 1734, 2, backgroundColor='#00314b65', zPosition='3')
    if mode == 'menu':
        # Separate navigation and result surfaces. Native ScrollLabel's parent
        # remains at z=0, so every opaque backing is strictly below it.
        for x,w in ((92,690),(806,1020)):
            for bx,by,bw,bh in ((x,286,w,2),(x,934,w,2),(x,288,2,646),(x+w-2,288,2,646)):
                element('eLabel',bx,by,bw,bh,backgroundColor=style.CYAN,zPosition='1')
        element('widget',108,304,658,612,name='list',scrollbarMode='showOnDemand',
                backgroundColor=style.PANEL,foregroundColor='#00ffffff',
                foregroundColorSelected='#00ffffff',backgroundColorSelected=style.SELECTION,zPosition='3')
        label('result_title',834,303,960,54,32,style.CYAN,noWrap='1',valign='center')
        label('result_status',834,361,960,37,23,'#00bcd2df',noWrap='1')
        element('eLabel',834,406,960,2,backgroundColor='#00314b65',zPosition='-1')
        label('descriptions',834,425,960,486,28,'#00e2edf5',
              scrollbarMode='showOnDemand',valign='top')
        # The right panel also supports two independent diagnostic bodies
        # as the full report. Keep their scroll widget parents unobstructed.
        for i in range(2):
            x=834+i*488
            label('inline_network_title%d'%i,x+8,425,454,45,25,style.CYAN,
                  noWrap='1',valign='center')
            label('inline_network_body%d'%i,x+8,480,454,425,26,'#00e2edf5',
                  scrollbarMode='showOnDemand',valign='top')
        # The same right-hand area can show six native cards instead of text.
        # Card widgets are hidden together whenever a text report is selected.
        for i in range(6):
            x,y=834+(i%2)*488,425+(i//2)*130
            element('widget',x,y,470,120,name='inline_bg%d'%i,
                    backgroundColor='#00172539',transparent='0',zPosition='1',font='Regular;%d'%max(1,round(sy)))
            label('inline_name%d'%i,x+14,y+5,444,34,25,'#00bcd2df',noWrap='1')
            label('inline_value%d'%i,x+14,y+41,444,48,35,'#00ffffff',noWrap='1')
            element('widget',x+14,y+98,444,9,name='inline_meter%d'%i,
                    backgroundColor='#002f465a',foregroundColor=style.CYAN,
                    borderWidth='0',transparent='0',zPosition='5')
            label('inline_note%d'%i,x+14,y+90,444,28,20,'#00bcd2df',noWrap='1')
        label('inline_summary',834,823,954,82,24,style.CYAN,valign='top')
        for i,(offset,span) in enumerate(INLINE_PROCESS_COLUMNS):
            label('inline_process_column%d'%i,834+offset,425,span,42,23,style.CYAN,noWrap='1',valign='center')
        row_height=max(1,round(42*sy))
        table=element('widget',834,475,960,426,name='inline_process_list',
                scrollbarMode='showOnDemand',backgroundColor=style.PANEL,
                foregroundColor='#00ffffff',foregroundColorSelected='#00ffffff',
                backgroundColorSelected='#00203548',transparent='0',zPosition='3')
        table.set('itemHeight',str(row_height))
        table.set('size','%d,%d'%(round(960*sx),round(426*sy)//row_height*row_height))
    elif mode == 'overview':
        for index in range(6):
            col, row = index % 3, index // 3
            x, y = 92 + col*586, 290 + row*230
            element('eLabel', x, y, 558, 207, backgroundColor='#00172539', zPosition='3')
            element('eLabel', x, y+22, 4, 165, backgroundColor=style.CYAN, zPosition='4')
            label('label%d'%index, x+24, y+12, 505, 58, 26, '#00bcd2df')
            label('value%d'%index, x+24, y+66, 505, 92, 48, '#00ffffff', valign='center',noWrap='1')
            if index<4:
                element('widget',x+24,y+173,505,12,name='meter%d'%index,backgroundColor='#002f465a',foregroundColor=style.CYAN,borderWidth='0',transparent='0',zPosition='5')
            else:
                label('sub%d'%index,x+24,y+162,505,38,22,'#00bcd2df',noWrap='1')
        element('eLabel',92,755,1734,178,backgroundColor='#00172539',zPosition='-1')
        label('summary', 116, 775, 1680, 135, 29, style.CYAN)
    elif mode in ('multichart','signal-multichart'):
        # Six cards share one sampler and the same 60-second time axis.
        label('window',1470,190,350,60,25,'#00bcd2df',halign='right',noWrap='1',valign='center')
        for i in range(6):
            x,y=92+(i%3)*586,290+(i//3)*324
            element('eLabel',x,y,558,308,backgroundColor='#00172539',zPosition='-1')
            element('eLabel',x,y,558,3,backgroundColor=style.CYAN,zPosition='1')
            if mode=='signal-multichart' and i==5:
                label('signal_summary_title',x+18,y+12,520,50,27,'#00bcd2df',noWrap='1',valign='center')
                label('signal_loss_count',x+18,y+72,520,92,60,style.CYAN,halign='center',valign='center',noWrap='1')
                element('eLabel',x+18,y+172,520,2,backgroundColor='#00314b65',zPosition='1')
                label('signal_lock_state',x+18,y+183,520,50,30,'#00ffffff',halign='center',valign='center',noWrap='1')
                label('signal_summary_note',x+18,y+240,520,55,25,'#00bcd2df',halign='center',valign='center')
                continue
            label('metric_name%d'%i,x+18,y+12,288,58,28,'#00bcd2df',noWrap='1',valign='center')
            label('metric_value%d'%i,x+322,y+12,216,58,34,'#00ffffff',halign='right',noWrap='1',valign='center')
            element('widget',x+96,y+87,440,140,source='plot%d'%i,render='Canvas',zPosition='3')
            label('plot_top%d'%i,x+8,y+78,80,36,20,'#00bcd2df',halign='right',noWrap='1')
            label('plot_bottom%d'%i,x+8,y+202,80,36,20,'#00bcd2df',halign='right',noWrap='1')
            for k in range(3):
                label('stat_name%d_%d'%(i,k),x+18+k*180,y+234,172,32,20,'#00bcd2df',halign='center',noWrap='1')
                label('stat_value%d_%d'%(i,k),x+18+k*180,y+265,172,35,25,'#00ffffff',halign='center',noWrap='1')
    elif mode == 'chart':
        label('metric', 95, 290, 1520, 105, 55, '#00ffffff', valign='center')
        element('widget', 220, 414, 1600, 298, source='history', render='Canvas', zPosition='3')
        label('axis_top',95,405,116,45,23,'#00bcd2df',halign='right',noWrap='1')
        label('axis_bottom',95,675,116,45,23,'#00bcd2df',halign='right',noWrap='1')
        label('axis_start',220,720,380,38,23,'#00bcd2df',noWrap='1')
        label('axis_end',1440,720,380,38,23,'#00bcd2df',halign='right',noWrap='1')
        element('eLabel',92,773,1734,160,backgroundColor='#00172539',zPosition='-1')
        label('details', 116, 790, 1680, 125, 28, '#00d1e3f3')
    else:
        # Separate report surface and status strip; keep every full-size backing below z=0.
        element('eLabel',92,286,1734,650,backgroundColor='#00172539',zPosition='-1')
        element('eLabel',92,286,1734,3,backgroundColor='#00314b65',zPosition='-1')
        label('report_status',116,299,1680,48,25,'#00bcd2df',noWrap='1')
        element('eLabel',116,353,1680,2,backgroundColor='#00314b65',zPosition='-1')
        label('file_info', 116, 372, 1680, 540, 29, '#00ffffff', scrollbarMode='showOnDemand',valign='top')
        if mode=='network':
            # Bounded information is visible side by side, with independent
            # scroll containers only when a receiver exposes many interfaces.
            for i,x in enumerate((116,966)):
                element('eLabel',x,372,820,540,backgroundColor='#00102136',zPosition='-1')
                element('eLabel',x,372,820,3,backgroundColor=style.CYAN,zPosition='-1')
                label('network_title%d'%i,x+24,391,772,45,28,style.CYAN,noWrap='1',valign='center')
                element('eLabel',x+24,450,772,2,backgroundColor='#00314b65',zPosition='-1')
                label('network_body%d'%i,x+24,471,772,413,28,'#00e2edf5',
                      scrollbarMode='showOnDemand',valign='top')
        if mode=='categories':
            for i in range(6):
                y=371+i*88
                element('eLabel',116,y,1680,80,backgroundColor='#00203548' if i%2==0 else '#00172539',zPosition='-1')
                label('category_name%d'%i,132,y+5,430,70,28,'#00e2edf5',valign='center',noWrap='1')
                element('widget',580,y+34,530,12,name='category_meter%d'%i,
                        backgroundColor='#002f465a',foregroundColor=style.CYAN,borderWidth='0',
                        transparent='0',zPosition='5')
                label('category_size%d'%i,1140,y+5,290,70,29,'#00ffffff',halign='right',valign='center',noWrap='1')
                label('category_state%d'%i,1450,y+5,320,70,24,'#00bcd2df',valign='center',noWrap='1')
        if mode=='process':
            # Fixed columns in the same coordinate space as the row renderer.
            element('eLabel',116,369,1680,49,backgroundColor='#00243b50',zPosition='-1')
            for i,(offset,span) in enumerate(PROCESS_COLUMNS):
                label('column%d'%i,116+offset,372,span,42,25,style.CYAN,noWrap='1',valign='center')
            element('widget',116,425,1680,484,name='process_list',
                    scrollbarMode='showOnDemand',backgroundColor=style.PANEL,
                    foregroundColor='#00ffffff',foregroundColorSelected='#00ffffff',
                    backgroundColorSelected=style.SELECTION,transparent='0',zPosition='3')
    colors = ('#00ff526a', '#0039ff59', '#00ffdb52', '#0045b9ff')
    for i, (name, color) in enumerate(zip(('red', 'green', 'yellow', 'blue'), colors)):
        label(name, 55 + 455*i, 990, 443, 81, 28, color, halign='center', valign='center', noWrap='1')
    return ET.tostring(root, encoding='unicode')


class DiagnosticHeader(style.Header):
    """Same clock/version header without changing the diagnostic footer."""
    def __init__(self,screen,api):
        self.ready=False
        self.suspended=False
        super().__init__(screen,api)
        screen.onHide.append(self.suspend)
        screen.onShow.append(self.resume)

    def prepare(self):
        from pathlib import Path
        if self.closed:return
        try:version=Path(__file__).with_name('version').read_text(encoding='utf-8').strip()
        except OSError:version='—'
        self.screen['version'].setText(version)
        self.screen['version_title'].setText(style.text(self.api,'Version:'))
        self.ready=True
        self.resume()

    def tick(self):
        if self.ready and not self.suspended:
            super().tick()

    def suspend(self):
        self.suspended=True
        self.timer.stop()

    def resume(self):
        if self.closed or not self.ready:return
        self.suspended=False
        self.tick()
        self.timer.start(1000)


def install_header(screen,api):
    for name in ('day','date','clock','seconds','version_title','version'):
        screen[name]=api['Label']('')
    screen._diagnostic_header=DiagnosticHeader(screen,api)


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
