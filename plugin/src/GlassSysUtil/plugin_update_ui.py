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
            else:pane.update_info(text(self.api,'The plugin is up to date.'))
            return
        if error:
            print('[GSU update] '+error)
            if self.manual:self.screen.session.open(MessageBox,text(self.api,'Update check failed.')+'\n\n'+error,type=MessageBox.TYPE_ERROR)
        elif release:
            language=self.api['config'].osd.language.value.split('_')[0]
            notes=release.notes_i18n.get(language,release.notes)
            message='Glass System Utility Warder Evolution\n\n'+text(self.api,'New version: %s\nInstalled version: %s\n\n%s\n\nInstall the update?') % (release.version,self.screen.readVersion(),notes)
            self.screen.session.openWithCallback(lambda answer:self.answer(release,answer),MessageBox,message,type=MessageBox.TYPE_YESNO,default=False)
        elif self.manual:
            self.screen.session.open(MessageBox,text(self.api,'The plugin is up to date.'),type=MessageBox.TYPE_INFO,timeout=6)

    def answer(self,release,accepted):
        if accepted and self.alive:self.screen.session.open(PluginInstallScreen,release,self.api)

    def stop(self):
        self.alive=False;self.timer.stop()


class PluginInstallScreen(Screen):
    def __init__(self,session,release,api,install=install_release,thread_factory=threading.Thread):
        width=getDesktop(0).size().width()
        scale=width/1920
        def px(value):return max(1,int(value*scale))
        self.skin='''<screen position="center,center" size="%d,%d" title="Glass System Utility — Aktualizácia" backgroundColor="#181818">
          <widget name="status" position="%d,%d" size="%d,%d" font="Regular;%d" scrollbarMode="showOnDemand" transparent="1" />
          <widget name="red" position="%d,%d" size="%d,%d" font="Regular;%d" foregroundColor="#ff5555" halign="center" transparent="1" />
        </screen>''' % tuple(px(v) for v in (1200,600,30,30,1140,480,26,30,540,300,40,24))
        Screen.__init__(self,session)
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
