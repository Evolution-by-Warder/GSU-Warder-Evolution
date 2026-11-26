"""Portable Warder preferences. Never copy the complete Enigma2 settings file."""
import hashlib
import json
import os
import re
import stat
import tempfile
from datetime import datetime
from pathlib import Path

from .warder_storage import mounts, LOCAL_FILE_SYSTEMS
from .warder_tools import Probe

PRODUCTS=('FullHDGlass','PiconHub','Warder Radio','YouTube','GSU')
LIMIT=512*1024
NAME=re.compile(r'warder-backup-[0-9]{8}-[0-9]{6}-[a-z0-9_]{6,16}\.json\Z')
RADIO='/etc/enigma2/warder-radio/state.json'
ROOT='/etc/enigma2/warder-backups'
# Explicit portable preferences only. No generic prefix export, credentials,
# scripts, device paths, update state, automatic deletion settings or tokens.
SKIN_KEYS=(1,2,6,7,8,14,16,17,18,19,20,24,25,26,28,29,30,31,32,33,41,42,44,46,47,48,49,54,55,56,60,63,66,67,68,69,72,73,74)
NATIVE={
    'FullHDGlass':tuple('setupGlass17.par%d'%i for i in SKIN_KEYS)+
        ('setupGlass17.radioSaverDelay','warderEvolutionPrimeTime.enabled','warderSkinMainMenu.enabled'),
    'PiconHub':('warder_piconhub_show_main_menu','chocholousekpicons_id')+
        tuple('chocholousekpicons.%d.%s'%(i,key) for i in range(5) for key in ('resolution','sats')),
    'YouTube':('warderyoutube.max_quality','warderyoutube.player_mode','warderyoutube.show_main_menu'),
    'GSU':tuple('GlassSysUtil.par%d'%i for i in (0,5,51,52,53,54,55,56,61,62,78,80,81)),
}
RADIO_KEYS=('show_main_menu','screensaver_delay','group','online_country',
            'radio_subscriptions','radio_home_category','radio_subscription_category')


def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')


def safe_chain(path):
    return not any(p.is_symlink() for p in (path,*path.parents))


def mount_owner(path,table):
    value=str(path)
    candidates=[row for row in table if row[1]=='/' or value==row[1] or value.startswith(row[1].rstrip('/')+'/')]
    return max(candidates,key=lambda row:len(row[1]),default=None)


def destinations(probe=None):
    p=probe or Probe()
    table=mounts(p)
    result=[]
    candidates=[ROOT]
    candidates.extend(target.rstrip('/')+'/warder-backups' for device,target,kind,ro in table
                      if device.startswith('/dev/') and kind in LOCAL_FILE_SYSTEMS and not ro
                      and target.startswith(('/media/','/mnt/')))
    for candidate in dict.fromkeys(candidates):
        owner=mount_owner(candidate,table)
        parent=p.path(candidate).parent
        if (owner and owner[2] in LOCAL_FILE_SYSTEMS and not owner[3]
                and safe_chain(p.path(candidate)) and parent.is_dir()
                and (not p.path(candidate).exists() or p.path(candidate).is_dir())):
            result.append(p.path(candidate))
    return result


def checked_dir(directory,p,create=False):
    directory=Path(directory)
    if directory not in destinations(p):raise ValueError('Unsupported backup location')
    if create:directory.mkdir(mode=0o700,exist_ok=True)
    if not safe_chain(directory) or not directory.is_dir():raise ValueError('Backup folder unavailable')
    return directory


def read_bytes(path,limit=LIMIT):
    if not safe_chain(path):raise ValueError('Symlink refused')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):raise ValueError('Not a regular file')
        data=handle.read(limit+1)
    if len(data)>limit:raise ValueError('File too large')
    return data


def replace_bytes(path,data):
    if not safe_chain(path) or not path.parent.is_dir():raise ValueError('Unsafe destination')
    fd,tmp=tempfile.mkstemp(prefix='.warder-',dir=str(path.parent))
    try:
        with os.fdopen(fd,'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def radio_state(p):
    table=mounts(p)
    owner=mount_owner(RADIO,table)
    if not owner or owner[2] not in LOCAL_FILE_SYSTEMS or owner[3]:return None
    try:
        raw=read_bytes(p.path(RADIO),16*1024*1024)
        value=json.loads(raw)
        return (raw,value) if isinstance(value,dict) and value.get('schema',1)==1 else None
    except (OSError,ValueError,UnicodeError,RecursionError):return None


def plain(value,limit=240):
    return isinstance(value,str) and len(value)<=limit and (not value or value.isprintable())


def radio_valid(key,value):
    if key=='show_main_menu':return type(value) is bool
    if key=='screensaver_delay':return type(value) is int and value in (0,10,20,30,60)
    if key=='radio_subscriptions':return isinstance(value,list) and len(value)<=80 and all(plain(v,60) for v in value)
    return key in RADIO_KEYS and plain(value,240 if key in ('group','online_country') else 60)


def element(config,key):
    obj=config.plugins
    try:
        for part in key.split('.'):
            obj=obj[int(part)] if part.isdigit() else getattr(obj,part)
        return obj if callable(getattr(obj,'save',None)) else None
    except (AttributeError,KeyError,IndexError,TypeError):return None


def native_valid(key,obj,value):
    if obj is None or type(value) is not type(obj.value):return False
    if key.endswith('.sats'):
        return plain(value,512) and all(re.fullmatch(r'\d{1,3}(?:\.\d)?[EW]',v) for v in value.split())
    choices=getattr(obj,'choices',None)
    if choices is not None:
        try:return any(type(v) in (str,int) and str(v)==str(value) for v in choices)
        except (TypeError,ValueError):return False
    if type(value) is bool:return True
    if type(value) is int:
        limits=getattr(obj,'limits',None)
        try:return len(limits)==1 and limits[0][0]<=value<=limits[0][1]
        except (TypeError,IndexError):return False
    return False


def snapshot(config,selected=PRODUCTS,probe=None):
    p=probe or Probe()
    result={}
    for product in PRODUCTS:
        if product not in selected:continue
        values={}
        if product=='Warder Radio':
            state=radio_state(p)
            if state:
                values={k:state[1][k] for k in RADIO_KEYS if k in state[1] and radio_valid(k,state[1][k])}
        else:
            for key in NATIVE[product]:
                obj=element(config,key)
                if obj is not None and native_valid(key,obj,obj.value):values[key]=obj.value
        if values:result[product]=values
    return result


def save(directory,products,probe=None):
    p=probe or Probe()
    if not products:raise ValueError('No portable settings')
    directory=checked_dir(directory,p,True)
    payload={'schema':1,'created':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'projects':products}
    document={'payload':payload,'sha256':hashlib.sha256(canonical(payload)).hexdigest()}
    data=canonical(document)
    if len(data)>LIMIT:raise ValueError('Backup too large')
    fd,name=tempfile.mkstemp(prefix='warder-backup-'+datetime.now().strftime('%Y%m%d-%H%M%S-'),suffix='.json',dir=str(directory))
    try:
        with os.fdopen(fd,'wb') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        path=Path(name)
        if load(path,p)!=payload:raise ValueError('Backup verification failed')
        return path
    except BaseException:
        os.unlink(name)
        raise


def load(path,probe=None):
    p=probe or Probe()
    path=Path(path)
    checked_dir(path.parent,p)
    if not NAME.fullmatch(path.name):raise ValueError('Invalid backup name')
    document=json.loads(read_bytes(path))
    if not isinstance(document,dict) or set(document)!= {'payload','sha256'}:raise ValueError('Invalid backup')
    payload=document['payload']
    if hashlib.sha256(canonical(payload)).hexdigest()!=document['sha256']:raise ValueError('Checksum mismatch')
    if not isinstance(payload,dict) or set(payload)!= {'schema','created','projects'} or type(payload['schema']) is not int or payload['schema']!=1:raise ValueError('Unsupported backup')
    if not plain(payload['created'],32) or not isinstance(payload['projects'],dict):raise ValueError('Invalid backup')
    for product,values in payload['projects'].items():
        if product not in PRODUCTS or not isinstance(values,dict):raise ValueError('Unknown product')
        allowed=RADIO_KEYS if product=='Warder Radio' else NATIVE[product]
        if not set(values).issubset(allowed):raise ValueError('Unsupported setting')
        for key,value in values.items():
            if product=='Warder Radio':
                if not radio_valid(key,value):raise ValueError('Invalid radio setting')
            elif not (type(value) in (bool,int) or plain(value,512)):raise ValueError('Invalid setting')
    return payload


def inventory(directory,probe=None):
    p=probe or Probe()
    try:directory=checked_dir(directory,p)
    except (OSError,ValueError):return []
    rows=[]
    with os.scandir(directory) as entries:
        for index,entry in enumerate(entries):
            if index>=512:break
            if NAME.fullmatch(entry.name) and entry.is_file(follow_symlinks=False):
                rows.append(directory/entry.name)
    return sorted(rows,reverse=True)[:50]


def plan(config,payload,selected=PRODUCTS,probe=None):
    p=probe or Probe()
    changes=[]
    radio={}
    skipped={}
    state=None
    for product,values in payload['projects'].items():
        if product not in selected:continue
        skipped[product]=0
        if product=='Warder Radio':state=radio_state(p)
        for key,value in values.items():
            if product=='Warder Radio':
                if state is None or not radio_valid(key,value):skipped[product]+=1
                elif state[1].get(key)!=value:radio[key]=value
            else:
                obj=element(config,key)
                if not native_valid(key,obj,value):skipped[product]+=1
                elif obj.value!=value:changes.append((product,key,obj,value))
    return changes,radio,skipped,state


def restore(config,configfile,path,selected=PRODUCTS,probe=None):
    """Explicit apply, native choices/limits, verified rollback snapshot first."""
    p=probe or Probe()
    payload=load(path,p)
    changes,radio,skipped,state=plan(config,payload,selected,p)
    if not changes and not radio:return 0,skipped,None
    previous=snapshot(config,selected,p)
    if radio and (state is None or any(k not in previous.get('Warder Radio',{}) for k in radio)):
        # No exact rollback for absent keys in this first schema.
        raise ValueError('Radio rollback unavailable')
    rollback=save(path.parent,previous,p)
    originals=[(obj,obj.value,obj.saved_value) for _,_,obj,_ in changes]
    def persist():
        expected=config.pickle().encode('utf-8')
        configfile.save()
        if read_bytes(Path(configfile.CONFIG_FILE),16*1024*1024)!=expected:
            raise OSError('Native configuration save failed')
    radio_written=False
    try:
        for _,_,obj,value in changes:
            obj.value=value
            if obj.value!=value:raise ValueError('Native setting rejected')
            obj.save()
        if changes:persist()
        if radio:
            if read_bytes(p.path(RADIO),16*1024*1024)!=state[0]:raise OSError('Radio settings changed')
            updated=dict(state[1],**radio)
            replace_bytes(p.path(RADIO),canonical(updated))
            radio_written=True
            if json.loads(read_bytes(p.path(RADIO),16*1024*1024))!=updated:raise OSError('Radio verification failed')
    except BaseException:
        for obj,value,saved in originals:
            obj.value=value
            obj.saved_value=saved
        if changes:persist()
        if radio_written:replace_bytes(p.path(RADIO),state[0])
        raise
    return len(changes)+len(radio),skipped,rollback
