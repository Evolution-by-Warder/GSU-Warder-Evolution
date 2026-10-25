"""Package actions for installed native CAMs, using original GSU screens."""
import shlex
import shutil
from .cam_feed import is_cam_package
from .native_softcam import NativeSoftcam


def context(screen):
    current=screen['config'].getCurrent()
    name=current[1].getText() if current else None
    if screen['config'].getCurrentIndex()!=0 or name not in screen.nativeSoftcam.available():return None
    return name,screen.nativeSoftcam.package_for(name)


def controls(screen):
    selected=context(screen)
    if selected is None:return False
    name,package=selected
    screen.enaBlue=False # The old UCM command-line editor is not a native editor.
    screen['txt4'].color2()
    if 'oscam' in name.lower() and package:screen['txt3'].color1()
    else:screen['txt3'].color2()
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
        command=shlex.quote(opkg)+' update && '+shlex.quote(opkg)+' install '+shlex.quote(package)
        screen.session.openWithCallback(screen.inicializeUCM,api['Console'],title=translate('Update OScam')+': '+name,cmdlist=[command])

    screen.session.openWithCallback(confirmed,api['MessageBox'],translate('Update OScam')+': '+package+'?',api['MessageBox'].TYPE_YESNO)
    return True


def remove(screen,api):
    package=screen.cmd
    if not is_cam_package(package):return False
    native=NativeSoftcam()
    for name in native.available():
        if native.package_for(name)==package and native.running(name):
            screen.session.open(api['MessageBox'],name+' '+api['_']('is in use, cannot be uninstalled'),api['MessageBox'].TYPE_ERROR,6)
            return True
    opkg=shutil.which('opkg')
    if opkg:
        screen.session.openWithCallback(screen.updateList,api['Console'],title=api['_']('Uninstalling package'),cmdlist=[shlex.quote(opkg)+' remove '+shlex.quote(package)])
    return True
