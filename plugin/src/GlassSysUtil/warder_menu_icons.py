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
    'network-overview':'network','network-test':'signal','network-interfaces':'network',
    'network-statistics':'trend','network-mounts':'storage','network-services':'service','2':'key','3':'key','4':'key',
    '6':'info','7':'settings','8':'tv','service-health':'health','service-ipk':'package',
    'forum-report':'clipboard','17':'service','16':'update','projects':'ecosystem',
    'FullHDGlass':'tv','PiconHub':'ecosystem','Warder Radio':'signal','YouTube':'tv','GSU':'system',
}

# Legacy CAM diagnostic navigation uses the same local functional icon set.
LEGACY_CAM_ICONS={
    'summary':'info','servers':'network','readers':'network','clients':'processes',
    'users':'processes','activeclients':'processes','shares':'ecosystem',
    'providers':'ecosystem','entitlements':'key','extend':'search','log':'log',
    'files':'settings','pid.info':'processes','share.info':'ecosystem',
    'share.onl':'network','stat.info':'info',
}


def legacy_cam_row(api,ident,title,enabled,icon_ident=None,show_status=True):
    """Preserve row identity; the embedded workspace has its own native geometry."""
    renderer=api.get('_warder_navigation_row')
    if renderer is not None:return renderer(ident,title,enabled,icon_ident,show_status)
    fhd=api['fhd']
    symbol=pixmap_entry(api,icon_ident or ident,(fhd(21 if show_status else 0),fhd(1)),(fhd(22),fhd(22)))
    left=(48 if show_status else 27) if symbol is not None else (25 if show_status else 0)
    row=[ident,api['MultiContentEntryText'](pos=(fhd(left),0),
        size=(fhd(560-left),fhd(22)),font=0,text=title,
        color=0xffffff if enabled else 0x666666)]
    if show_status:
        status=api['LoadPixmap'](api['BP_ICO'] % ('green' if enabled else 'red'))
        row.append(api['MultiContentEntryPixmapAlphaTest'](pos=(0,fhd(3)),
            size=(fhd(15),fhd(16)),png=status))
    if symbol is not None:row.append(symbol)
    return row


def icon_name(ident):
    if not isinstance(ident,str):return 'info'
    if ident.startswith('centre:'):return CENTRE_ICONS.get(ident.split(':',1)[1],'info')
    if ident.startswith('native:'):return 'reception'
    return ROUTE_ICONS.get(ident,CENTRE_ICONS.get(ident,LEGACY_CAM_ICONS.get(ident,'info')))

@lru_cache(maxsize=64)
def cached(loader,name):
    path=ROOT/('nav-'+name+'.png')
    if not path.is_file():return None
    try:return loader(path=str(path),cached=True)
    except (OSError,RuntimeError,TypeError,AttributeError):
        return None

PROJECT_ASSETS={
    'FullHDGlass':ROOT/'project-fullhdglass.png',
    'PiconHub':ROOT/'project-piconhub.png',
    'YouTube':ROOT/'project-youtube.png',
    'GSU':ROOT/'warder-plugin.png',
    'Warder Radio':Path('/usr/lib/enigma2/python/Plugins/Extensions/WarderRadio/plugin.png'),
}


@lru_cache(maxsize=16)
def project_cached(loader,ident,path):
    try:
        if not path.is_file() or path.stat().st_size>2*1024*1024:return None
        return loader(path=str(path),cached=True)
    except (OSError,RuntimeError,TypeError,AttributeError):
        return None


def pixmap_entry(api,ident,pos,size,project=False):
    loader,entry=api.get('LoadPixmap'),api.get('MultiContentEntryPixmapAlphaBlend')
    if not callable(loader) or not callable(entry):return None
    try:
        path=PROJECT_ASSETS.get(ident) if project else None
        pix=project_cached(loader,ident,path) if path is not None else None
        if pix is None:pix=cached(loader,icon_name(ident))
        if pix is None:return None
        flags=0
        for key in ('BT_SCALE','BT_KEEP_ASPECT_RATIO'):
            value=getattr(enigma,key,0)
            if isinstance(value,int):flags|=value
        return entry(pos=pos,size=size,png=pix,flags=flags)
    except (OSError,RuntimeError,TypeError,AttributeError,ValueError):
        return None
