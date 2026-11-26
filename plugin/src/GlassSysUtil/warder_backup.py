"""Portable Warder preferences. Never copy the complete Enigma2 settings file."""
import hashlib
import json
import os
import re
import secrets
import stat
import tempfile
from datetime import datetime
from pathlib import Path

from .warder_storage import mounts, LOCAL_FILE_SYSTEMS
from .warder_tools import Probe
from . import warder_backup_crypto as crypto

PRODUCTS=('FullHDGlass','PiconHub','Warder Radio','YouTube','GSU')
LIMIT=512*1024
NAME=re.compile(r'warder-backup-[0-9]{8}-[0-9]{6}-[a-z0-9_]{6,16}\.json\Z')
RADIO='/etc/enigma2/warder-radio/state.json'
ROOT='/etc/enigma2/warder-backups'
RADIO_PLUGIN='/usr/lib/enigma2/python/Plugins/Extensions/WarderRadio/plugin.py'
# Explicit portable preferences only. No generic prefix export, credentials,
# scripts, device paths, update state, automatic deletion settings or tokens.
# Visual preferences audited in FullHDGlass setupGlass17/plugin.py.
# Exclude device paths, network addresses, credentials and action toggles.
SKIN_KEYS=(1,2,6,7,8,14,16,17,18,19,20,24,25,26,28,29,30,31,32,33,41,42,
           44,45,46,47,48,49,53,54,55,56,60,63,66,67,68,69,72,73,74,76,77,
           79,81,82,83,84,86,87,92,93,94,95,96,97,102,103,105,106,107,108,
           109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,
           126,127,128,129,130,131,132,133,134,135,136,137,138,139,142,
           145,146,147,148,153,154,155,156,157,161,162,163,164,165,166,167,
           168,183,187,188,190,196,197,202,203,209,213,214,215)
PICON_MENU='/usr/lib/enigma2/python/Plugins/Extensions/WarderPiconHub/data/skin-menu.json'
PICON_METHODS=('sync_tv','sync_tv_radio','all_inc')
PICON_STYLES=('transparent','white','black','no_satellites_was_selected')
NATIVE={
    'FullHDGlass':tuple('setupGlass17.par%d'%i for i in SKIN_KEYS)+
        ('setupGlass17.radioSaverDelay','setupGlass17.descriptionScrollSpeed',
         'warderEvolutionPrimeTime.enabled','warderSkinMainMenu.enabled'),
    'PiconHub':('warder_piconhub_show_main_menu','chocholousekpicons_id')+
        tuple('chocholousekpicons.%d.%s'%(i,key) for i in range(5) for key in ('resolution','sats','warder_selectors','background','method')),
    'YouTube':('warderyoutube.max_quality','warderyoutube.player_mode','warderyoutube.show_main_menu'),
    'GSU':tuple('GlassSysUtil.par%d'%i for i in (0,4,5,51,52,53,54,55,56,60,61,62,78,80,81))+('GlassSysUtil.diagnosticAlerts',),
}
RADIO_KEYS=('show_main_menu','screensaver_delay','group','online_country',
            'radio_subscriptions','radio_home_category','radio_subscription_category')
PRIVATE_NATIVE={'YouTube':('warderyoutube.api_key',)}
PRIVATE_RADIO=('favourites','custom')


def native_keys(product,private=False):
    return NATIVE[product]+(PRIVATE_NATIVE.get(product,()) if private else ())


def radio_keys(private=False):
    return RADIO_KEYS+(PRIVATE_RADIO if private else ())


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


def radio_defaults(state):
    """Effective defaults from WarderRadio.model.Store; no history migration."""
    subscriptions=state.get('radio_subscriptions',[])
    subscriptions=subscriptions if radio_valid('radio_subscriptions',subscriptions) else []
    group=state.get('group','Slovensko')
    group=group if radio_valid('group',group) else 'Slovensko'
    return {'show_main_menu':False,'screensaver_delay':0,'group':'Slovensko',
            'online_country':group,'radio_subscriptions':[],'radio_home_category':'',
            'radio_subscription_category':next(iter(subscriptions),''),
            'favourites':[],'custom':[]}


def radio_state(p,allow_missing=False):
    table=mounts(p)
    owner=mount_owner(RADIO,table)
    if not owner or owner[2] not in LOCAL_FILE_SYSTEMS or owner[3]:return None
    try:
        raw=read_bytes(p.path(RADIO),16*1024*1024)
        value=json.loads(raw)
        return (raw,value) if isinstance(value,dict) and type(value.get('schema',1)) is int and value.get('schema',1)==1 else None
    except FileNotFoundError:
        path=p.path(RADIO)
        plugin=p.path(RADIO_PLUGIN)
        if (allow_missing and safe_chain(path) and safe_chain(plugin)
                and plugin.is_file() and p.path('/etc/enigma2').is_dir()):
            return None,{'schema':1}
        return None
    except (OSError,ValueError,UnicodeError,RecursionError):return None


def plain(value,limit=240):
    return isinstance(value,str) and len(value)<=limit and (not value or value.isprintable())


def radio_valid(key,value,private=False):
    if private and key in PRIVATE_RADIO:return station_list(value)
    if key=='show_main_menu':return type(value) is bool
    if key=='screensaver_delay':return type(value) is int and value in (0,10,20,30,60)
    if key=='radio_subscriptions':return isinstance(value,list) and len(value)<=80 and all(plain(v,60) for v in value)
    return key in RADIO_KEYS and plain(value,240 if key in ('group','online_country') else 60)


def station_list(value):
    """Validate all rows, never partially overwrite a user's favourite list."""
    from urllib.parse import urlsplit
    if not isinstance(value,list) or len(value)>1000:return False
    fields={'id','name','url','group','reference','stationuuid','codec','bitrate',
            'favicon','original_url','homepage','countrycode'}
    def url(v):
        if not plain(v,4096) or not v:return False
        try:
            parts=urlsplit(v)
            return (parts.scheme in ('http','https') and bool(parts.hostname)
                    and parts.username is None and parts.password is None
                    and (parts.port is None or 0<parts.port<=65535))
        except ValueError:return False
    for row in value:
        if not isinstance(row,dict) or not set(row).issubset(fields):return False
        if not plain(row.get('name'),240) or not row['name'] or not url(row.get('url')):return False
        for k,v in row.items():
            if k in ('url','favicon','original_url','homepage'):
                if not url(v):return False
            elif k=='bitrate':
                if type(v) is not int or not 1<=v<=10000:return False
            elif not plain(v,240):return False
        ref=row.get('reference','')
        if ref and not re.fullmatch(r'[0-9A-Fa-f]+(?::[0-9A-Fa-f]+){9}',ref):return False
    return True


def element(config,key):
    obj=config.plugins
    try:
        for part in key.split('.'):
            obj=obj[int(part)] if part.isdigit() else getattr(obj,part)
        return obj if callable(getattr(obj,'save',None)) else None
    except (AttributeError,KeyError,IndexError,TypeError):return None


def picon_catalog(probe=None):
    """Use the installed target's catalog, never import or start PiconHub."""
    p=probe or Probe()
    try:
        document=json.loads(read_bytes(p.path(PICON_MENU),256*1024))
        rows=document['selectors']
        if not isinstance(rows,list) or len(rows)>512:return None
        values={row['selector'] for row in rows}
        if not all(isinstance(v,str) and re.fullmatch(r'[A-Z0-9_-]{1,32}',v) for v in values):return None
        return values|{'DAB'}
    except (OSError,ValueError,KeyError,TypeError,RecursionError):return None


def selectors_valid(value):
    if not plain(value,512):return False
    parts=value.split()
    return len(parts)==len(set(parts)) and all(re.fullmatch(r'[A-Z0-9_-]{1,32}',v) and not v.startswith('IPTV-') for v in parts)


def native_valid(key,obj,value,private=False,probe=None):
    if obj is None or type(value) is not type(obj.value):return False
    if key in PRIVATE_NATIVE.get('YouTube',()):return private and plain(value,512) and (not value or re.fullmatch(r'[A-Za-z0-9_-]{10,256}',value) is not None)
    if key=='setupGlass17.par45':
        return isinstance(value,str) and re.fullmatch(r'#[0-9a-fA-F]{6}(?:[0-9a-fA-F]{2})?',value) is not None
    if key.endswith('.sats'):
        return plain(value,512) and all(re.fullmatch(r'\d{1,3}(?:\.\d)?[EWew]',v) for v in value.split())
    if key.endswith('.warder_selectors'):
        if not selectors_valid(value):return False
        catalog=picon_catalog(probe)
        return not value.strip() or (catalog is not None and set(value.split())<=catalog)
    if key.startswith('chocholousekpicons.') and key.endswith('.method') and value not in PICON_METHODS:return False
    if key.startswith('chocholousekpicons.') and key.endswith('.background') and value not in PICON_STYLES:return False
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


def snapshot(config,selected=PRODUCTS,probe=None,private=False):
    p=probe or Probe()
    result={}
    for product in PRODUCTS:
        if product not in selected:continue
        values={}
        if product=='Warder Radio':
            state=radio_state(p)
            if state:
                values={k:state[1][k] for k in radio_keys(private) if k in state[1] and radio_valid(k,state[1][k],private)}
        else:
            for key in native_keys(product,private):
                obj=element(config,key)
                if obj is not None and native_valid(key,obj,obj.value,private,p):values[key]=obj.value
        if values:result[product]=values
    return result


def save(directory,products,probe=None,password=None):
    p=probe or Probe()
    if not products:raise ValueError('No portable settings')
    directory=checked_dir(directory,p,True)
    payload={'schema':1,'created':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'projects':products}
    private=password is not None
    validate_payload(payload,private)
    if private:
        document=crypto.seal(canonical(payload),password)
    else:
        document={'payload':payload,'sha256':hashlib.sha256(canonical(payload)).hexdigest()}
    data=canonical(document)
    if len(data)>(crypto.MAX_ENVELOPE if private else LIMIT):raise ValueError('Backup too large')
    # Pin the opened directory: a detached USB must never redirect a write
    # or cleanup into the receiver's fallback mount directory.
    name='warder-backup-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+secrets.token_hex(6)+'.json'
    temporary='.'+name+'.writing'
    dirfd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    created=False
    def check_mount():
        checked_dir(directory,p)
        pinned,current=os.fstat(dirfd),directory.stat()
        if (pinned.st_dev,pinned.st_ino)!=(current.st_dev,current.st_ino):
            raise OSError('Backup storage changed')
    try:
        check_mount()
        fd=os.open(temporary,os.O_RDWR|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=dirfd)
        created=True
        with os.fdopen(fd,'w+b') as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
            handle.seek(0)
            if handle.read(len(data)+1)!=data:raise OSError('Backup write verification failed')
        check_mount()
        try:
            os.stat(name,dir_fd=dirfd,follow_symlinks=False)
        except FileNotFoundError:pass
        else:raise OSError('Backup name collision')
        os.rename(temporary,name,src_dir_fd=dirfd,dst_dir_fd=dirfd)
        created=False
        os.fsync(dirfd)
        check_mount()
        path=directory/name
        if load(path,p,password)!=payload:raise ValueError('Backup verification failed')
        check_mount()
        return path
    finally:
        if created:
            try:os.unlink(temporary,dir_fd=dirfd)
            except OSError:pass
        os.close(dirfd)


def validate_payload(payload,private=False):
    if not isinstance(payload,dict) or set(payload)!= {'schema','created','projects'} or type(payload['schema']) is not int or payload['schema']!=1:raise ValueError('Unsupported backup')
    if not plain(payload['created'],32) or not isinstance(payload['projects'],dict):raise ValueError('Invalid backup')
    for product,values in payload['projects'].items():
        if product not in PRODUCTS or not isinstance(values,dict):raise ValueError('Unknown product')
        allowed=radio_keys(private) if product=='Warder Radio' else native_keys(product,private)
        if not set(values).issubset(allowed):raise ValueError('Unsupported setting')
        for key,value in values.items():
            if product=='Warder Radio':
                if not radio_valid(key,value,private):raise ValueError('Invalid radio setting')
            elif key in PRIVATE_NATIVE.get(product,()):
                if not private or not plain(value,512) or (value and not re.fullmatch(r'[A-Za-z0-9_-]{10,256}',value)):raise ValueError('Invalid private setting')
            elif key.endswith('.warder_selectors'):
                if not selectors_valid(value):raise ValueError('Invalid picon selectors')
            elif key.startswith('chocholousekpicons.') and key.endswith('.method'):
                if value not in PICON_METHODS:raise ValueError('Unsafe picon update method')
            elif key.startswith('chocholousekpicons.') and key.endswith('.background'):
                if value not in PICON_STYLES:raise ValueError('Invalid picon style')
            elif not (type(value) in (bool,int) or plain(value,512)):raise ValueError('Invalid setting')
    return payload


def file_kind(path,probe=None):
    p=probe or Probe()
    path=Path(path)
    checked_dir(path.parent,p)
    if not NAME.fullmatch(path.name):raise ValueError('Invalid backup name')
    raw=read_bytes(path,crypto.MAX_ENVELOPE)
    document=json.loads(raw)
    if isinstance(document,dict) and document.get('format')==crypto.FORMAT:return 'private'
    if isinstance(document,dict) and set(document)=={'payload','sha256'} and len(raw)<=LIMIT:return 'standard'
    raise ValueError('Invalid backup')


def fingerprint(payload):
    return hashlib.sha256(canonical(payload)).hexdigest()


def load(path,probe=None,password=None):
    p=probe or Probe()
    path=Path(path)
    checked_dir(path.parent,p)
    if not NAME.fullmatch(path.name):raise ValueError('Invalid backup name')
    raw=read_bytes(path,crypto.MAX_ENVELOPE)
    document=json.loads(raw)
    if isinstance(document,dict) and document.get('format')==crypto.FORMAT:
        if password is None:raise ValueError('Private backup requires password')
        return validate_payload(json.loads(crypto.unseal(document,password)),True)
    if password is not None or len(raw)>LIMIT:raise ValueError('Invalid backup')
    if not isinstance(document,dict) or set(document)!= {'payload','sha256'}:raise ValueError('Invalid backup')
    payload=document['payload']
    if hashlib.sha256(canonical(payload)).hexdigest()!=document['sha256']:raise ValueError('Checksum mismatch')
    return validate_payload(payload)


def inventory(directory,probe=None):
    p=probe or Probe()
    try:directory=checked_dir(directory,p)
    except (OSError,ValueError):return []
    rows=[]
    try:
        with os.scandir(directory) as entries:
            for index,entry in enumerate(entries):
                if index>=512:break
                if NAME.fullmatch(entry.name) and entry.is_file(follow_symlinks=False):
                    rows.append(directory/entry.name)
    except OSError:return []
    return sorted(rows,reverse=True)[:50]


def plan(config,payload,selected=PRODUCTS,probe=None,private=False):
    validate_payload(payload,private)
    p=probe or Probe()
    changes=[]
    radio={}
    skipped={}
    state=None
    for product,values in payload['projects'].items():
        if product not in selected:continue
        skipped[product]=0
        if product=='Warder Radio':state=radio_state(p,allow_missing=True)
        for key,value in values.items():
            if product=='Warder Radio':
                if state is None or not radio_valid(key,value,private):skipped[product]+=1
                elif state[1].get(key,radio_defaults(state[1]).get(key))!=value:radio[key]=value
            else:
                obj=element(config,key)
                if not native_valid(key,obj,value,private,p):skipped[product]+=1
                elif obj.value!=value:changes.append((product,key,obj,value))
    return changes,radio,skipped,state


def outcome(payload,selected,changes,radio,skipped):
    """Disjoint counts from the same compatibility plan used for the restore.

    Never include configuration values, URLs or credentials in a presentation.
    """
    rows={}
    for product in PRODUCTS:
        if product not in payload['projects']:continue
        total=len(payload['projects'][product])
        if product not in selected:
            rows[product]=(0,0,0,total)
            continue
        changed=sum(change[0]==product for change in changes)
        if product=='Warder Radio':changed+=len(radio)
        incompatible=skipped.get(product,0)
        rows[product]=(changed,total-changed-incompatible,incompatible,0)
    return rows


class RestoreFailure(OSError):
    """Only non-secret recovery metadata escapes an unsuccessful transaction."""
    def __init__(self,rollback,recovered):
        super().__init__('Restore failed')
        self.rollback=rollback
        self.recovered=recovered


def restore(config,configfile,path,selected=PRODUCTS,probe=None,password=None,expected_digest=None,details=False):
    """Explicit apply, native choices/limits, verified rollback snapshot first."""
    p=probe or Probe()
    private=password is not None
    payload=load(path,p,password)
    if expected_digest is not None and fingerprint(payload)!=expected_digest:raise ValueError('Backup changed after preview')
    changes,radio,skipped,state=plan(config,payload,selected,p,private)
    summary=outcome(payload,selected,changes,radio,skipped)
    if not changes and not radio:
        result=(0,skipped,None)
        return (*result,summary) if details else result
    previous=snapshot(config,selected,p,private)
    if any(key not in previous.get(product,{}) for product,key,_,_ in changes):raise ValueError('Native rollback unavailable')
    if radio:
        # Missing keys on a new image have documented effective defaults.
        old=previous.setdefault('Warder Radio',{})
        defaults=radio_defaults(state[1])
        for key in radio:
            value=state[1].get(key,defaults[key])
            if not radio_valid(key,value,private):raise ValueError('Radio rollback unavailable')
            old[key]=value
    # Recovery must survive removal of the source USB. Never start changing
    # settings until the internal, verified rollback archive exists.
    rollback=save(p.path(ROOT),previous,p,password)
    originals=[]
    def persist():
        destination=Path(configfile.CONFIG_FILE)
        if destination!=p.path('/etc/enigma2/settings') or not safe_chain(destination):
            raise OSError('Unsafe native settings path')
        expected=config.pickle().encode('utf-8')
        configfile.save()
        if read_bytes(destination,16*1024*1024)!=expected:
            raise OSError('Native configuration save failed')
    radio_path=p.path(RADIO)
    radio_written=False
    try:
        for _,_,obj,value in changes:
            originals.append((obj,obj.value,obj.saved_value))
            obj.value=value
            if obj.value!=value:raise ValueError('Native setting rejected')
            obj.save()
        if changes:persist()
        if radio:
            # Compare raw original bytes, including the absence of a new file.
            current=radio_state(p,allow_missing=True)
            if current is None or current[0]!=state[0]:raise OSError('Radio settings changed')
            if not safe_chain(radio_path):raise OSError('Unsafe radio path')
            radio_path.parent.mkdir(mode=0o700,exist_ok=True)
            updated=dict(state[1],**radio)
            raw=canonical(updated)
            replace_bytes(radio_path,raw)
            radio_written=True
            if read_bytes(radio_path,16*1024*1024)!=raw:raise OSError('Radio verification failed')
    except BaseException:
        recovered=True
        for obj,value,saved in originals:
            try:
                obj.value=value
                obj.saved_value=saved
            except Exception:recovered=False
        if originals:
            try:persist()
            except Exception:recovered=False
        if radio_written:
            try:
                # Do not overwrite concurrent changes made by another writer.
                if read_bytes(radio_path,16*1024*1024)!=raw:raise OSError('Radio changed')
                if state[0] is None:radio_path.unlink()
                else:replace_bytes(radio_path,state[0])
            except Exception:recovered=False
        raise RestoreFailure(rollback,recovered) from None
    result=(len(changes)+len(radio),skipped,rollback)
    return (*result,summary) if details else result
