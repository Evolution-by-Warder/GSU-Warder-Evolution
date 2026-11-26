"""Scoped, scrollable informational dialogs for Warder diagnostic screens.

No global skin changes and no replacement of confirmation callbacks.
"""
from .warder_screen import Screen
from . import warder_dashboard as dashboard, warder_main as main


class InformationDialog(Screen):
    def __init__(self,session,api,message,title):
        from Components.ScrollLabel import ScrollLabel
        self.skin=dashboard.skin(*dashboard.dimensions(api),'detail')
        Screen.__init__(self,session)
        self.setTitle(title)
        dashboard.install_header(self,api)
        self['heading']=api['Label'](title)
        self['report_status']=api['Label']('')
        self['file_info']=ScrollLabel(str(message))
        self['red']=api['Label'](main.text(api,'Back'))
        self['green']=api['Label']('')
        self['yellow']=api['Label']('')
        self['blue']=api['Label']('')
        self['actions']=api['ActionMap'](['ColorActions','SetupActions','DirectionActions'],
            {'red':self.close,'cancel':self.close,'ok':self.close,
             'up':self['file_info'].pageUp,'down':self['file_info'].pageDown,
             'left':self['file_info'].pageUp,'right':self['file_info'].pageDown},-2)


def show_info(session,api,message,title):
    return session.open(InformationDialog,api,str(message),str(title))


def choice_skin(width,height):
    from xml.etree import ElementTree as ET
    root=ET.fromstring(dashboard.skin(width,height,'detail'))
    root.set('name','WarderDiagnosticChoice')
    for node in list(root):
        if node.get('name') in ('report_status','file_info'):root.remove(node)
    sx,sy=width/1920,height/1080
    row=max(1,round(64*sy))
    ET.SubElement(root,'widget',name='choices',position='%d,%d'%(round(116*sx),round(306*sy)),
        size='%d,%d'%(round(1680*sx),(round(600*sy)//row)*row),
        backgroundColor=main.PANEL,foregroundColor='#00ffffff',
        backgroundColorSelected=main.SELECTION,foregroundColorSelected='#00ffffff',
        scrollbarMode='showOnDemand',itemHeight=str(row),zPosition='3')
    return ET.tostring(root,encoding='unicode')


class ChoiceDialog(Screen):
    """Only a selection, never an implicit confirmation or an executable action."""
    def __init__(self,session,api,title,options):
        from .warder_menu_icons import pixmap_entry
        width,height=dashboard.dimensions(api)
        sx,sy=width/1920,height/1080
        self.skin=choice_skin(width,height)
        Screen.__init__(self,session)
        self.setTitle(title)
        dashboard.install_header(self,api)
        self['heading']=api['Label'](title)
        self['red']=api['Label'](main.text(api,'Back'))
        self['green']=api['Label'](main.text(api,'Select'))
        self['yellow']=api['Label']('')
        self['blue']=api['Label']('')
        self['choices']=api['ListboxSys2']([])
        self['choices'].l.setFont(0,api['gFont']('Regular',round(30*sy)))
        self['choices'].l.setItemHeight(round(64*sy))
        rows=[]
        for item in options:
            if not isinstance(item,(tuple,list)) or len(item)!=2:continue
            icon=pixmap_entry(api,'native:choice',(round(12*sx),round(12*sy)),
                (round(40*sy),round(40*sy)))
            left=70 if icon is not None else 14
            row=[item,api['MultiContentEntryText'](pos=(round(left*sx),round(6*sy)),
                size=(round((1640-left)*sx),round(52*sy)),font=0,text=str(item[0]))]
            if icon is not None:row.append(icon)
            rows.append(row)
        self['choices'].l.setList(rows)
        self['actions']=api['ActionMap'](['ColorActions','SetupActions','DirectionActions'],
            {'red':self.cancel,'cancel':self.cancel,'back':self.cancel,
             'ok':self.select,'green':self.select,'up':self['choices'].up,'down':self['choices'].down},-2)

    def select(self):
        row=self['choices'].getCurrent()
        if row:self.close(row[0])

    def cancel(self):
        self.close(None)


def choose(session,api,callback,title,options):
    return session.openWithCallback(callback,ChoiceDialog,api,title,tuple(options))
