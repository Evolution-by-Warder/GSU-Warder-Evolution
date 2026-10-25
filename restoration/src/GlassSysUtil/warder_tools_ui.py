"""Two focused Warder utilities in the original GSU screen style."""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Screens.Screen import Screen
from twisted.internet.threads import deferToThread
from .warder_tools import run_task,summary

_SK={
    'Tools':'Nástroje',
    'System health check':'Kontrola stavu',
    'Create diagnostic bundle':'Vytvoriť diagnostický balík',
    'System overview and a diagnostic file for support.':'Prehľad stavu systému a diagnostický súbor pre riešenie problémov.',
    'Overview of memory, storage, network, temperature, Enigma2 and CAM.':'Prehľad pamäte, diskov, siete, teplôt, Enigmy2 a CAM.',
    'Create one archive with system information and GSU logs.':'Vytvorenie jedného archívu s údajmi o systéme a logmi GSU.',
    'Collecting information…':'Načítavam údaje…',
    'Creating diagnostic bundle…':'Vytváram diagnostický balík…',
    'Diagnostic collection failed.':'Zber diagnostiky sa nepodaril.',
    'Diagnostic bundle created:\n%s\n\nSize: %s KiB\n\nThe file is available on the receiver at the path above.':'Diagnostický balík bol vytvorený:\n%s\n\nVeľkosť: %s KiB\n\nSúbor nájdeš v prijímači na uvedenej ceste.',
    'Back':'Naspäť',
    'Warning':'Pozor','Info':'Info','Available memory':'Dostupná pamäť','Storage':'Úložisko',
    'free':'voľné','read-only':'iba na čítanie','Unavailable':'Nedostupné','Not exposed':'Údaj nie je dostupný',
    'Network link':'Sieťové spojenie','No active link detected':'Aktívne spojenie nezistené',
    'Default gateway':'Predvolená brána','DNS configuration':'Nastavenie DNS',
    'Running':'Spustená','Not detected':'Nezistená','No known CAM process detected':'Bežiaci CAM nebol zistený',
    'Temperature':'Teplota','Network mounts':'Sieťové pripojenia diskov','Tuner interfaces':'Rozhrania tunerov','Detected':'Zistené',
    'This is a read-only check. Internet access, disk integrity and CAM decoding are not tested.':'Kontrola iba číta údaje. Netestuje prístup na internet, integritu diskov ani dekódovanie CAM.',
}


def text(api,value):
    result=api['_'](value)
    language=api['config'].osd.language.value
    return _SK.get(value,result) if result==value and language.startswith('sk') else result


def open_tools(session,api):session.open(ToolsScreen,api)


class ToolsScreen(Screen):
    def __init__(self,session,api):
        self.skin=api['ipkScript_center']
        Screen.__init__(self,session)
        self.api=api
        self.entries=[('health','System health check','Overview of memory, storage, network, temperature, Enigma2 and CAM.'),
                      ('bundle','Create diagnostic bundle','Create one archive with system information and GSU logs.')]
        self['list']=api['ListboxSys2']([])
        self['list'].onSelectionChanged.append(self.describe)
        self['descriptions']=Label('')
        self['red']=Label(text(api,'Back'));self['green']=Label(api['_']('Select'))
        self['actions']=ActionMap(['WizardActions','ColorActions'],{'ok':self.select,'green':self.select,'red':self.close,'back':self.close},-2)
        self.onLayoutFinish.append(self.prepare)

    def prepare(self):
        api=self.api;self.setTitle(text(api,'Tools'))
        rows=[]
        for kind,label,description in self.entries:
            rows.append([kind,api['MultiContentEntryText'](pos=(api['fhd'](25),0),size=(api['fhd'](535),api['fhd'](22)),font=0,text=text(api,label)),
                         api['MultiContentEntryPixmapAlphaTest'](pos=(0,api['fhd'](3)),size=(api['fhd'](15),api['fhd'](16)),png=api['LoadPixmap'](api['BP_ICO'] % 'green'))])
        self['list'].l.setList(rows);self.describe()

    def describe(self):
        row=self['list'].getCurrent()
        if row:
            entry=next((item for item in self.entries if item[0]==row[0]),None)
            self['descriptions'].setText(text(self.api,entry[2]) if entry else '')

    def select(self):
        row=self['list'].getCurrent()
        if row and row[0] in ('health','bundle'):self.session.open(DiagnosticScreen,row[0],self.api)


class DiagnosticScreen(Screen):
    def __init__(self,session,kind,api):
        self.skin=api['oscam_Files_scr2']
        Screen.__init__(self,session)
        self.kind,self.api=kind,api
        self.started,self.closed=False,False
        self['file_info']=ScrollLabel(text(api,'Collecting information…' if kind=='health' else 'Creating diagnostic bundle…'))
        self['red']=Label(text(api,'Back'))
        self['actions']=ActionMap(['ColorActions','SetupActions','DirectionActions'],{'red':self.close,'cancel':self.close,'up':self['file_info'].pageUp,'down':self['file_info'].pageDown,'left':self['file_info'].pageUp,'right':self['file_info'].pageDown},-2)
        self.onLayoutFinish.append(self.start)
        self.onClose.append(self.cleanup)

    def start(self):
        if self.started or self.closed:return
        self.started=True
        self.setTitle(text(self.api,'System health check' if self.kind=='health' else 'Create diagnostic bundle'))
        self.request=deferToThread(run_task,self.kind)
        self.request.addCallback(self.done)
        self.request.addErrback(self.failed)

    def done(self,result):
        if self.closed:return
        if self.kind=='health':value=summary(result,lambda value:text(self.api,value))
        else:value=text(self.api,'Diagnostic bundle created:\n%s\n\nSize: %s KiB\n\nThe file is available on the receiver at the path above.') % (result['path'],max(1,(result['bytes']+1023)//1024))
        self['file_info'].setText(value)

    def failed(self,failure):
        if not self.closed:self['file_info'].setText(text(self.api,'Diagnostic collection failed.'))
        return None

    def cleanup(self):self.closed=True
