"""Local Warder navigation picons keyed by stable action identity, not translation."""
from functools import lru_cache
from pathlib import Path
import enigma

ROOT=Path(__file__).with_name('images')
CENTRE_ICONS={'system':'system','reception':'reception','storage':'storage',
              'network':'network','cam':'key','service':'service','warder':'ecosystem'}
ROUTE_ICONS={
    'system-overview':'health','system-live':'trend','system-processes':'processes',
    'system-log':'log','0':'info','1':'tv','signal-quick':'signal','signal-live':'history',
    'tuner-details':'reception','transponder-services':'tv','tuner-native':'settings',
    'storage-overview':'storage','storage-categories':'memory','9':'swap',
    'network-overview':'network','network-test':'signal','2':'key','3':'key','4':'key',
    '6':'info','7':'settings','8':'tv','service-health':'health','service-ipk':'package',
    'forum-report':'clipboard','17':'service','16':'update','projects':'ecosystem',
    'FullHDGlass':'tv','PiconHub':'ecosystem','Warder Radio':'signal','YouTube':'tv','GSU':'system',
}

def icon_name(ident):
    if not isinstance(ident,str):return 'info'
    if ident.startswith('centre:'):return CENTRE_ICONS.get(ident.split(':',1)[1],'info')
    if ident.startswith('native:'):return 'reception'
    return ROUTE_ICONS.get(ident,CENTRE_ICONS.get(ident,'info'))

@lru_cache(maxsize=64)
def cached(loader,name):
    path=ROOT/('nav-'+name+'.png')
    if not path.is_file():return None
    try:return loader(path=str(path),cached=True)
    except (OSError,RuntimeError,TypeError,AttributeError):
        return None

def pixmap_entry(api,ident,pos,size):
    loader,entry=api.get('LoadPixmap'),api.get('MultiContentEntryPixmapAlphaBlend')
    if not callable(loader) or not callable(entry):return None
    try:
        pix=cached(loader,icon_name(ident))
        if pix is None:return None
        flags=0
        for key in ('BT_SCALE','BT_KEEP_ASPECT_RATIO'):
            value=getattr(enigma,key,0)
            if isinstance(value,int):flags|=value
        return entry(pos=pos,size=size,png=pix,flags=flags)
    except (OSError,RuntimeError,TypeError,AttributeError,ValueError):
        return None
