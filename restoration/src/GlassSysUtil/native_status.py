"""Refresh the visible CAM indicator after external/automatic state changes."""
import time
from twisted.internet.threads import deferToThread
from .native_softcam import refresh_state


def request(screen,translate):
    if not screen.enCommand or getattr(screen,'nativeRegistryClosed',False):return
    if not screen.nativeSoftcam.selected():return
    if getattr(screen,'nativeStatusPending',False):return
    now=time.monotonic()
    if now-getattr(screen,'nativeStatusTime',-100)<1:return
    screen.nativeStatusTime=now
    screen.nativeStatusPending=True
    generation=getattr(screen,'nativeStatusGeneration',0)

    def done(active):
        screen.nativeStatusPending=False
        if getattr(screen,'nativeRegistryClosed',False) or not screen.enCommand:return
        if generation!=getattr(screen,'nativeStatusGeneration',0):return
        value=(active,getattr(screen,'numSrv',0)>0)
        if value!=getattr(screen,'nativeStatusValue',None):
            refresh_state(screen,translate,active)
            screen.nativeStatusValue=value

    def failed(failure):
        screen.nativeStatusPending=False
        return None

    pending=deferToThread(screen.nativeSoftcam.active_name)
    pending.addCallback(done)
    pending.addErrback(failed)
    screen.nativeStatusRequest=pending
