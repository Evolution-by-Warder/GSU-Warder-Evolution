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
