"""Restore a re-enabled local DVBAPI identity using the existing CAM controller.

All I/O runs in the clients' deferred worker. A restart is allowed only when the
running image-selected process configuration identifies both this account and
this exact local WebIF endpoint. Account changes elsewhere remain unchanged.
"""
from configparser import ConfigParser, Error as ConfigError
from pathlib import Path
import time
import subprocess
from urllib.parse import urlsplit
from .native_softcam import NativeSoftcam, command_lock
from .oscam_clients import ClientError, fetch_clients, parse_status, set_enabled


class RecoveryError(ClientError):
    pass


def local_endpoint(base):
    try:
        url=urlsplit(base)
        return url.hostname in ('127.0.0.1','::1','localhost') and url.scheme in ('http','https')
    except ValueError:return False


def config_paths(native,name):
    """Use actual process argv; never guess a directory from the CAM name."""
    pids=native._matching_pids(name)
    for pid in pids:
        try:args=(native.proc_dir/str(pid)/'cmdline').read_bytes().decode('utf-8').split('\0')
        except (OSError,UnicodeError):continue
        for index,arg in enumerate(args):
            if arg in ('-c','--config-dir') and index+1<len(args):
                yield Path(args[index+1])/'oscam.conf'
            elif arg.startswith('--config-dir='):
                yield Path(arg.split('=',1)[1])/'oscam.conf'
    # OSCam may use its compiled default without an argv config option.
    for path in (Path('/tmp/.oscam/oscam.version'),Path('/tmp/oscam.version')):
        try:
            fields=dict(line.split(':',1) for line in path.read_text().splitlines() if ':' in line)
            if int(fields.get('PID','-1').strip()) in pids:
                yield Path(fields['ConfigDir'].strip())/'oscam.conf'
        except (OSError,ValueError,KeyError):continue


def recovery_target(base,user,native):
    if not local_endpoint(base):return None
    selected=native.selected()
    if not selected:return None
    endpoint=urlsplit(base)
    try:port=endpoint.port or (443 if endpoint.scheme=='https' else 80)
    except ValueError:return None
    for path in config_paths(native,selected):
        config=ConfigParser(interpolation=None,strict=False,inline_comment_prefixes=('#',';'))
        try:
            if not path.is_absolute():continue
            with path.open() as handle:config.read_file(handle)
            if config.get('dvbapi','enabled',fallback='0').strip()!='1':continue
            if config.get('dvbapi','user',fallback='').strip()!=user:continue
            webport=config.get('webif','httpport',fallback='').strip()
            scheme='https' if webport.startswith('+') else 'http'
            if scheme!=endpoint.scheme or not webport.lstrip('+').isdigit():continue
            if int(webport.lstrip('+'))!=port:continue
            return selected
        except (OSError,ConfigError):continue
    return None


def wait_ready(base,login,password,fetch,user,timeout=20,clock=time.monotonic,sleep=time.sleep):
    deadline=clock()+timeout
    while clock()<deadline:
        try:
            records=parse_status(fetch(base.rstrip('/')+'/oscamapi.html?part=status',login,password))
            if any(row['name']==user and row['protocol'].split(' ',1)[0].lower()=='dvbapi' for row in records):
                return fetch_clients(base,login,password,fetch)
        except (ClientError,OSError):pass
        sleep(0.5)
    raise RecoveryError('DVBAPI did not reconnect before the deadline')


def change_account(base,login,password,fetch,user,disabled,*,native=None,lock=command_lock,wait=wait_ready):
    if disabled or not local_endpoint(base):
        return set_enabled(base,login,password,fetch,user,disabled)
    native=native or NativeSoftcam()
    with lock():
        target=recovery_target(base,user,native)
        # Verification must succeed before a restart is even considered.
        set_enabled(base,login,password,fetch,user,False)
        if target is None:return True
        try:
            if native.selected()!=target or recovery_target(base,user,native)!=target:
                raise RecoveryError('Selected OSCam changed during the account operation')
            native.restart_verified(target)
        except (OSError,ValueError,subprocess.SubprocessError) as error:
            raise RecoveryError('Account enabled, but OSCam restart failed') from error
    try:records=wait(base,login,password,fetch,user)
    except (ClientError,OSError) as error:raise RecoveryError('Account enabled, but OSCam reconnect failed') from error
    return {'restarted':True,'records':records}
