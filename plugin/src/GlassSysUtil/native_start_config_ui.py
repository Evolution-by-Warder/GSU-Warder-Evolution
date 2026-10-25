"""Original-style native OSCam start settings, with isolated per-CAM values."""
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.config import ConfigDirectory, ConfigInteger, ConfigSelection, ConfigText, ConfigYesNo, getConfigListEntry
from Screens.Screen import Screen
from twisted.internet.threads import deferToThread
from .native_start_config import StartConfigStore


_SK={
    'Debug level (0-65535)':'Úroveň ladenia (0–65535)',
    'Restart level (0-2)':'Úroveň reštartu (0–2)',
    'Wait for system time (0-300s)':'Čakanie na systémový čas (0–300 s)',
    'Maximum pending ECM packets (1-4096)':'Najviac čakajúcich ECM paketov (1–4096)',
    'Syslog ident':'Názov v systémovom zázname',
    'Saved. Changes apply at the next CAM start or restart.':'Uložené. Zmeny sa použijú pri ďalšom štarte alebo reštarte CAM-u.',
    'Unable to save OSCam start configuration.':'Nepodarilo sa uložiť štart konfiguráciu OSCam-u.',
    'Unable to read OSCam start configuration.':'Nepodarilo sa načítať štart konfiguráciu OSCam-u.',
    'Loading OSCam start configuration...':'Načítavam štart konfiguráciu OSCam-u...',
    'Saving':'Ukladám',
}

def translate(api,text):
    result=api['_'](text)
    settings=api.get('config')
    language=getattr(getattr(getattr(settings,'osd',None),'language',None),'value','')
    return _SK.get(text,result) if result==text and language.startswith('sk') else result


class NativeStartConfigScreen(Screen,ConfigListScreen):
    def __init__(self,session,snapshot,store,api):
        self.skin=api['oscam_start'];self.api=api;self.snapshot=snapshot;self.store=store
        self.translate=lambda text:translate(api,text);self.closed=False;self.saving=False
        Screen.__init__(self,session)
        self['red']=Label(self.translate('Exit'))
        self['green']=Label(self.translate('Save'))
        self['white']=Label(self.translate('Press OK to select dir'));self['white'].hide()
        self['actions']=ActionMap(['SetupActions','ColorActions'],{
            'green':self.save,'ok':self.choose,'red':self.cancel,'cancel':self.cancel,'yellow':self.cancel},-2)
        self.settings={};values=snapshot['values']
        for field,value in values.items():
            if field.endswith('_dir'):setting=ConfigDirectory(default=value)
            elif type(value) is bool:setting=ConfigYesNo(default=value)
            elif field in ('restart','gcollect'):
                choices=[('0',self.translate('Disabled')),('1','1'),('2','2')]
                setting=ConfigSelection(default=str(value),choices=choices)
            elif type(value) is int:
                limits={'debug':(0,65535),'wait':(0,300),'pending':(1,4096)}[field]
                setting=ConfigInteger(default=value,limits=limits)
            else:setting=ConfigText(default=value,fixed_size=False)
            self.settings[field]=setting
        self.list=[]
        labels={
            'config_dir':'Read configuration from','temp_dir':'Tmp dir',
            'debug':'Debug level (0-65535)','restart':'Restart level (0-2)',
            'wait':'Wait for system time (0-300s)','pending':'Maximum pending ECM packets (1-4096)',
            'capture':'Capture segmentation faults','crash':'Write oscam.crash on segfault',
            'gcollect':'Garbage collector debug mode','sensitive':'Do not filter sensitive info from the logs',
            'syslog_ident':'Syslog ident',
        }
        for field in ('config_dir','temp_dir','debug','capture','crash','restart','wait','pending','gcollect','syslog_ident','sensitive'):
            if field in self.settings:self.list.append(getConfigListEntry(self.translate(labels[field]),self.settings[field]))
        # These must match the image init script so boot/status/stop keep working.
        daemon=ConfigSelection(default='yes',choices=[('yes',self.translate('yes'))])
        pid=ConfigSelection(default=snapshot['pidfile'],choices=[(snapshot['pidfile'],snapshot['pidfile'])])
        self.list.extend([getConfigListEntry(self.translate('Start in background'),daemon),getConfigListEntry(self.translate('Pidfile name'),pid)])
        ConfigListScreen.__init__(self,self.list,session=session)
        self['config'].onSelectionChanged.append(self.selection_changed)
        self.onLayoutFinish.append(self.set_title)
        self.onLayoutFinish.append(self.selection_changed)
        self.onClose.append(lambda:setattr(self,'closed',True))

    def set_title(self):
        self.setTitle(self.translate('OScam start cfg')+': '+self.snapshot['name'])

    def selection_changed(self):
        current=self['config'].getCurrent()
        dirs=[v for k,v in self.settings.items() if k.endswith('_dir')]
        if current and current[1] in dirs:self['white'].show()
        else:self['white'].hide()

    def choose(self):
        if self.saving:return
        current=self['config'].getCurrent()
        if not current:return
        setting=current[1]
        if setting not in [v for k,v in self.settings.items() if k.endswith('_dir')]:return
        def chosen(path):
            if path is not None and not self.closed:
                setting.value=path
                self['config'].invalidateCurrent()
        self.session.openWithCallback(chosen,self.api['dirBrowser'],setting.value)

    def collect_values(self):
        return {field:int(setting.value) if field in ('restart','gcollect') else setting.value for field,setting in self.settings.items()}

    def save(self):
        if self.saving:return
        self.saving=True;self['green'].setText(self.translate('Saving'))
        pending=deferToThread(self.store.save,self.snapshot,self.collect_values())
        self.pending=pending
        def done(result):
            self.saving=False
            if not self.closed:
                self.session.openWithCallback(lambda *args:self.close(True),self.api['MessageBox'],self.translate('Saved. Changes apply at the next CAM start or restart.'),self.api['MessageBox'].TYPE_INFO,5)
        def failed(failure):
            self.saving=False
            if not self.closed:
                self['green'].setText(self.translate('Save'))
                detail=str(getattr(failure,'value',failure))
                self.session.open(self.api['MessageBox'],self.translate('Unable to save OSCam start configuration.')+'\n'+detail,self.api['MessageBox'].TYPE_ERROR,8)
            return None
        pending.addCallback(done);pending.addErrback(failed)

    def cancel(self):
        if not self.saving:self.close(False)


def open_start_config(screen,api,name):
    if not screen.enCommand:return True
    screen.enCommand=False
    screen['statCamSrvcmd'].setText(translate(api,'Loading OSCam start configuration...'))
    store=StartConfigStore(init_dir=screen.nativeSoftcam.init_dir,bin_dir=screen.nativeSoftcam.bin_dir)
    pending=deferToThread(store.snapshot,name);screen.nativeStartConfigRequest=pending
    def done(snapshot):
        screen.enCommand=True
        if getattr(screen,'nativeRegistryClosed',False):return
        screen.session.openWithCallback(screen.inicializeUCM,NativeStartConfigScreen,snapshot,store,api)
    def failed(failure):
        screen.enCommand=True
        if not getattr(screen,'nativeRegistryClosed',False):
            detail=str(getattr(failure,'value',failure))
            screen.session.open(api['MessageBox'],translate(api,'Unable to read OSCam start configuration.')+'\n'+detail,api['MessageBox'].TYPE_ERROR,8)
        return None
    pending.addCallback(done);pending.addErrback(failed)
    return True
