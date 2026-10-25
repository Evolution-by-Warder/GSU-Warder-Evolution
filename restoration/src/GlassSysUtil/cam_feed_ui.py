"""Reuse the original download screen with an asynchronous system catalogue."""
import shlex
import shutil
from twisted.internet.threads import deferToThread
from .cam_feed import read_catalogue, is_cam_package


def initialize(screen):
    screen.feedMode=screen.wFtp is None
    if screen.feedMode:
        screen.feedClosed=False
        screen.feedGeneration=0
        screen.feedPackages={}
        screen.onClose.append(lambda:close(screen))


def close(screen):
    screen.feedClosed=True
    screen.feedGeneration+=1


def row(api,key,text,color='green'):
    fhd=api['fhd']
    return [key,api['MultiContentEntryText'](pos=(fhd(25),0),size=(fhd(640),fhd(25)),font=0,text=text),api['MultiContentEntryPixmapAlphaTest'](pos=(0,fhd(3)),size=(fhd(15),fhd(16)),png=api['LoadPixmap'](api['BP_ICO']%color))]


def load(screen,api,refresh=True):
    translate=api['_']
    screen.feedGeneration+=1
    generation=screen.feedGeneration
    screen.feedPackages={}
    screen.setTitle(translate('Download CAM/SRV'))
    screen.list=[row(api,'*',translate('Loading package list...'),'yellow')]
    screen['list'].l.setList(screen.list)

    def completed(result):
        if screen.feedClosed or screen.feedGeneration != generation:return
        screen.feedPackages={p['name']:p for p in result['packages']}
        items=[]
        if result['warning']:
            items.append(row(api,'*',translate('Feed refresh failed; showing cached packages.'),'red'))
        for package in result['packages']:
            display=package['name'].removeprefix('enigma2-plugin-softcams-').removeprefix('enigma2-plugin-cams-')
            text=display+'  ('+', '.join(package['versions'])+')'
            items.append(row(api,package['name'],text))
        if not screen.feedPackages:
            items.append(row(api,'*',translate('No CAM packages in configured feeds.'),'red'))
        screen.list=items
        screen['list'].l.setList(items)

    def failed(failure):
        if not screen.feedClosed and screen.feedGeneration == generation:
            screen.list=[row(api,'*',translate('Unable to read package feeds.'),'red')]
            screen['list'].l.setList(screen.list)
        return None

    try:
        screen.feedRequest=deferToThread(read_catalogue,refresh)
        screen.feedRequest.addCallback(completed)
        screen.feedRequest.addErrback(failed)
    except Exception:
        failed(None)


def select(screen,api):
    current=screen['list'].getCurrent()
    name=current[0] if current else '*'
    if name not in screen.feedPackages or not is_cam_package(name):return
    translate=api['_']
    if ('oscam' in name and api['oscamRunning']()) or ('osemu' in name and api['oscamRunning'](True)):
        screen.session.open(api['MessageBox'],translate('Before update OScam/OSEmu version, please, stop OScam/OSEmu'),api['MessageBox'].TYPE_ERROR,5)
        return

    def confirmed(answer):
        if not answer or screen.feedClosed:return
        opkg=shutil.which('opkg')
        if not opkg:return
        command=shlex.quote(opkg)+' install '+shlex.quote(name)
        screen.session.openWithCallback(lambda *args:load(screen,api,False) if not screen.feedClosed else None,api['Console'],title=translate('Installing package')+': '+name,cmdlist=[command])

    screen.session.openWithCallback(confirmed,api['MessageBox'],translate('Installing package')+': '+name+'?',api['MessageBox'].TYPE_YESNO)
