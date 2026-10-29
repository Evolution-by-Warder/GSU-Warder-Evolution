"""Shared automatic/manual update flow, with all network/package work off GUI."""
from .i18n import for_api as _i18n_text
import queue
import threading

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from enigma import eTimer, getDesktop

from .plugin_update import check_release, install_release
from xml.etree import ElementTree as ET
from .warder_settings import skin as _window_skin
from .warder_system import install as _install_header
from .warder_main import text as _shared_text


_SK = {
    'Update': 'Aktualizácia',
    'Check for a new version of Glass System Utility Warder Evolution': 'Kontrola novej verzie Glass System Utility Warder Evolution',
    'Checking for plugin updates…': 'Kontrolujem aktualizáciu pluginu…',
    'The plugin is up to date.': 'Plugin je aktuálny.',
    'Update check failed.': 'Kontrola aktualizácie sa nepodarila.',
    'Downloading, verifying and installing the update…': 'Sťahujem, overujem a inštalujem aktualizáciu…',
    'Update failed.': 'Aktualizácia zlyhala.',
    'Back': 'Naspäť',
    'Plugin updated to %s.\nThe GUI will restart in 3 seconds.': 'Plugin bol aktualizovaný na %s.\nO 3 sekundy sa reštartuje GUI.',
    'New version: %s\nInstalled version: %s\n\n%s\n\nInstall the update?': 'Nová verzia: %s\nNainštalovaná verzia: %s\n\n%s\n\nNainštalovať aktualizáciu?',
}


def text(api,value):
    return _i18n_text(api,value,_SK)


def connect(timer, callback):
    try:return timer.timeout.connect(callback)
    except AttributeError:
        signal=timer.timeout
        (signal.get() if hasattr(signal,'get') else signal).append(callback)


class StartupUpdateCheck:
    def __init__(self, screen, api, check=check_release, thread_factory=threading.Thread):
        self.screen,self.api,self.check,self.thread_factory=screen,api,check,thread_factory
        self.alive,self.started,self.busy,self.manual=True,False,False,False
        self.results=queue.Queue()
        self.timer=api['eTimer']()
        self.connection=connect(self.timer,self.poll)
        screen.onLayoutFinish.append(self.start)
        screen.onClose.append(self.stop)

    def start(self):
        if not self.started:
            self.started=True
            self.request()

    def request(self,manual=False):
        if not self.alive:return False
        if manual and hasattr(self.screen,'_rightpane'):
            self.screen._rightpane.update_info(text(self.api,'Checking for plugin updates…'))
        if self.busy:
            self.manual=self.manual or manual
            return False
        self.busy,self.manual=True,manual
        self.current_version=self.screen.readVersion()
        if manual:self.screen['info'].setText(text(self.api,'Checking for plugin updates…'))
        try:self.thread_factory(target=self.work,daemon=True).start()
        except Exception as error:self.results.put((None,str(error)))
        self.timer.start(250,False)
        return True

    def work(self):
        try:self.results.put((self.check(self.current_version),None))
        except Exception as error:self.results.put((None,str(error)))

    def poll(self):
        if not self.alive:return
        # Opening from an inactive parent can crash native modal ownership.
        if getattr(self.screen.session,'current_dialog',self.screen) is not self.screen:return
        try:release,error=self.results.get_nowait()
        except queue.Empty:return
        self.timer.stop();self.busy=False
        if self.manual:self.screen.reactivate()
        pane=getattr(self.screen,'_rightpane',None)
        if self.manual and pane is not None:
            if not pane.active or pane.kind!='update':return
            if error:
                pane.update_info(text(self.api,'Update check failed.')+'\n\n'+error)
            elif release:
                language=self.api['config'].osd.language.value.split('_')[0]
                notes=release.notes_i18n.get(language,release.notes)
                message='GSU Warder Evolution\n\n'+text(self.api,'New version: %s\nInstalled version: %s\n\n%s\n\nInstall the update?')%(release.version,self.screen.readVersion(),notes)
                pane.update_info(message,release,self)
            else:pane.update_info('GSU Warder Evolution\n'+self.screen.readVersion()+'\n\n'+text(self.api,'The plugin is up to date.'))
            return
        if error:
            if self.manual:self.screen.session.open(MessageBox,text(self.api,'Update check failed.')+'\n\n'+error,type=MessageBox.TYPE_ERROR)
        elif release:
            language=self.api['config'].osd.language.value.split('_')[0]
            notes=release.notes_i18n.get(language,release.notes)
            message='Glass System Utility Warder Evolution\n\n'+text(self.api,'New version: %s\nInstalled version: %s\n\n%s\n\nInstall the update?') % (release.version,self.screen.readVersion(),notes)
            self.screen.session.openWithCallback(lambda answer:self.answer(release,answer),UpdateOffer,message,self.api,default=False)
        elif self.manual:
            self.screen.session.open(MessageBox,text(self.api,'The plugin is up to date.'),type=MessageBox.TYPE_INFO,timeout=6)

    def answer(self,release,accepted):
        if accepted and self.alive:self.screen.session.open(PluginInstallScreen,release,self.api)

    def stop(self):
        self.alive=False;self.timer.stop()


def update_skin(confirm=False):
    size=getDesktop(0).size();root=ET.fromstring(_window_skin(size.width(),size.height()))
    root.set('name','WarderGSUUpdate')
    node=root.find("widget[@name='config']");node.set('name','status')
    for key in ('itemHeight','backgroundColorSelected','foregroundColorSelected'):node.attrib.pop(key,None)
    sy=size.height()/1080
    node.set('size','%d,%d'%(round(1740*size.width()/1920),round((570 if confirm else 650)*sy)))
    ET.SubElement(root,'widget',name='decision',position='%d,%d'%(round(90*size.width()/1920),round(880*sy)),size='%d,%d'%(round(1740*size.width()/1920),round(55*sy)),font='Regular;%d'%round(28*sy),foregroundColor='#00ffffff',backgroundColor='#ff000000',transparent='1',halign='center',zPosition='3')
    return ET.tostring(root,encoding='unicode')


class UpdateOffer(Screen):
    """Native Warder confirmation; decline remains the default."""
    def __init__(self,session,message,api,default=False):
        self.skin=update_skin(True);Screen.__init__(self,session)
        self.api=api;self.accepted=default
        self['settings_title']=Label(text(api,'Update'))
        self['status']=ScrollLabel(message)
        self['red']=Label(_shared_text(api,'No'));self['green']=Label(_shared_text(api,'Yes'))
        self['decision']=Label('');self.select(default)
        self['actions']=ActionMap(['ColorActions','OkCancelActions','DirectionActions'],{'red':lambda:self.close(False),'cancel':lambda:self.close(False),'green':lambda:self.close(True),'ok':lambda:self.close(self.accepted),'up':self['status'].pageUp,'down':self['status'].pageDown},-2)
        _install_header(self,api)
    def select(self,accepted):
        self.accepted=accepted
        self['decision'].setText('')


class PluginInstallScreen(Screen):
    def __init__(self,session,release,api,install=install_release,thread_factory=threading.Thread):
        self.skin=update_skin()
        Screen.__init__(self,session)
        self['settings_title']=Label(text(api,'Update'))
        self['green']=Label('')
        self['decision']=Label('')
        _install_header(self,api)
        self.api,self.release,self.install,self.thread_factory=api,release,install,thread_factory
        self.closed,self.started,self.done=False,False,False
        self.results=queue.Queue()
        self['status']=ScrollLabel(text(api,'Downloading, verifying and installing the update…'))
        self['red']=Label('')
        self['actions']=ActionMap(['OkCancelActions','ColorActions','DirectionActions'],{'cancel':self.finish,'red':self.finish,'up':self['status'].pageUp,'down':self['status'].pageDown},-2)
        self.timer=api['eTimer']();self.connection=connect(self.timer,self.poll)
        self.restart_timer=api['eTimer']();self.restart_connection=connect(self.restart_timer,self.restart)
        self.onLayoutFinish.append(self.start)
        self.onClose.append(self.cleanup)

    def start(self):
        if self.started:return
        self.started=True
        try:self.thread_factory(target=self.work,daemon=True).start()
        except Exception as error:self.results.put((None,str(error)))
        self.timer.start(250,False)

    def work(self):
        try:self.results.put((self.install(self.release),None))
        except Exception as error:self.results.put((None,str(error)))

    def poll(self):
        if self.closed:return
        try:version,error=self.results.get_nowait()
        except queue.Empty:return
        self.timer.stop()
        if error:
            self.done=True
            self['status'].setText(text(self.api,'Update failed.')+'\n\n'+error)
            self['red'].setText(text(self.api,'Back'))
        else:
            self['status'].setText(text(self.api,'Plugin updated to %s.\nThe GUI will restart in 3 seconds.') % version)
            self.restart_timer.start(3000,True)

    def restart(self):
        if not self.closed:
            from enigma import quitMainloop
            quitMainloop(3)

    def finish(self):
        if self.done:self.close()

    def cleanup(self):
        self.closed=True;self.timer.stop();self.restart_timer.stop()
