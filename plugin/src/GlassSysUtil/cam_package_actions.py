"""Package actions for installed native CAMs, using original GSU screens."""
import shlex
import shutil
from .cam_feed import is_cam_package
from .native_softcam import NativeSoftcam
from .softcam_feed_setup import ensure_softcam_feed
from twisted.internet.threads import deferToThread


def refresh_registry(screen):
    # Read package-manager truth once in a worker, not on every 500 ms UI tick.
    screen.nativeRegistryGeneration=getattr(screen,'nativeRegistryGeneration',0)+1
    generation=screen.nativeRegistryGeneration
    if not getattr(screen,'nativeRegistryInitialized',False):
        screen.nativeRegistryInitialized=True
        screen.nativeRegistryClosed=False
        screen.onClose.append(lambda:setattr(screen,'nativeRegistryClosed',True))
    def done(packages):
        if screen.nativeRegistryClosed or screen.nativeRegistryGeneration!=generation:return
        screen.nativeSoftcam.registered_packages=packages
        screen.nativeSoftcam.package_cache.clear()
        controls(screen)
    def failed(failure):return None
    screen.nativeRegistryRequest=deferToThread(screen.nativeSoftcam.read_package_registry)
    screen.nativeRegistryRequest.addCallback(done)
    screen.nativeRegistryRequest.addErrback(failed)


def context(screen):
    current=screen['config'].getCurrent()
    name=current[1].getText() if current else None
    if screen['config'].getCurrentIndex()!=0 or name not in screen.nativeSoftcam.available():return None
    return name,screen.nativeSoftcam.package_for(name)


def controls(screen):
    selected=context(screen)
    if selected is None:return False
    name,package=selected
    screen.enaBlue='oscam' in name.lower()
    if screen.enaBlue:screen['txt4'].color1()
    else:screen['txt4'].color2()
    if 'oscam' in name.lower() and package:screen['txt3'].color1()
    else:screen['txt3'].color2()
    return True


def start_config(screen,api):
    selected=context(screen)
    if selected is None:return False
    name,package=selected
    if 'oscam' in name.lower():
        from .native_start_config_ui import open_start_config
        return open_start_config(screen,api,name)
    return True


def update(screen,api):
    selected=context(screen)
    if selected is None:return False
    name,package=selected;translate=api['_']
    if not screen.enCommand:
        screen['statCamSrvcmd'].setText(translate('Try later ... working'));return True
    if 'oscam' not in name.lower():return True
    if not package:
        screen.session.open(api['MessageBox'],translate('This CAM has no installed package to update.'),api['MessageBox'].TYPE_INFO,5);return True
    if api['oscamRunning']():
        screen.session.open(api['MessageBox'],translate('Before update OScam/OSEmu version, please, stop OScam/OSEmu'),api['MessageBox'].TYPE_ERROR,5);return True

    def confirmed(answer):
        if not answer:return
        # Do not update a package after a CAM has been started in another menu.
        if api['oscamRunning']():
            screen.session.open(api['MessageBox'],translate('Before update OScam/OSEmu version, please, stop OScam/OSEmu'),api['MessageBox'].TYPE_ERROR,5);return
        opkg=shutil.which('opkg')
        if not opkg:return
        screen.enCommand=False
        def prepared(result):
            screen.enCommand=True
            if getattr(screen,'nativeRegistryClosed',False):return
            if api['oscamRunning']():
                screen.session.open(api['MessageBox'],translate('Before update OScam/OSEmu version, please, stop OScam/OSEmu'),api['MessageBox'].TYPE_ERROR,5);return
            command=shlex.quote(opkg)+' update && '+shlex.quote(opkg)+' install '+shlex.quote(package)
            screen.session.openWithCallback(screen.inicializeUCM,api['Console'],title=translate('Update OScam')+': '+name,cmdlist=[command])
        def failed(failure):
            screen.enCommand=True
            if not getattr(screen,'nativeRegistryClosed',False):
                screen.session.open(api['MessageBox'],translate('Unable to set up or read package feeds.'),api['MessageBox'].TYPE_ERROR,5)
            return None
        screen.nativeUpdatePrepare=deferToThread(ensure_softcam_feed)
        screen.nativeUpdatePrepare.addCallback(prepared)
        screen.nativeUpdatePrepare.addErrback(failed)

    screen.session.openWithCallback(confirmed,api['MessageBox'],translate('Update OScam')+': '+package+'?',api['MessageBox'].TYPE_YESNO)
    return True


def remove(screen,api):
    package=screen.cmd
    if not is_cam_package(package):return False
    native=NativeSoftcam()
    for name in native.available():
        candidates=('enigma2-plugin-softcams-'+name,'enigma2-plugin-cams-'+name,name)
        if (package in candidates or native.package_for(name)==package) and native.running(name):
            screen.session.open(api['MessageBox'],name+' '+api['_']('is in use, cannot be uninstalled'),api['MessageBox'].TYPE_ERROR,6)
            return True
    opkg=shutil.which('opkg')
    if opkg:
        screen.session.openWithCallback(screen.updateList,api['Console'],title=api['_']('Uninstalling package'),cmdlist=[shlex.quote(opkg)+' remove '+shlex.quote(package)])
    return True
