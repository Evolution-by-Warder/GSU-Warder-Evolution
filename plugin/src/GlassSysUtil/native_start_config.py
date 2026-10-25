"""Per-CAM OSCam startup options, applied by a small native-init adapter.

The package init script still owns daemon startup, PID tracking and service stop.
Only its executable invocation is prefixed; configured values are exec argv,
never shell text. A byte-for-byte original init backup is kept on first save.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import stat
import subprocess
import tempfile

# field: (long option, short option, default)
OPTIONS={
    'config_dir':('--config-dir','-c',None),
    'temp_dir':('--temp-dir','-t','/tmp/.oscam'),
    'debug':('--debug','-d',0),
    'restart':('--restart','-r',1),
    'wait':('--wait','-w',60),
    'pending':('--pending-ecm','-p',32),
    'capture':('--capture-segfaults','-s',False),
    'crash':('--crash-dump','-a',False),
    'gcollect':('--gcollect','-g',0),
    'sensitive':('--show-sensitive','-S',False),
    'syslog_ident':('--syslog-ident','-I','oscam'),
}
LIMITS={'debug':(0,65535),'restart':(0,2),'wait':(0,300),'pending':(1,4096),'gcollect':(0,2)}
BOOLS={'capture','crash','sensitive'}
ALIASES={option:field for field,definition in OPTIONS.items() for option in definition[:2]}


def atomic_write(path,data,mode=0o644):
    path=Path(path);fd,temporary=tempfile.mkstemp(prefix='.gsu-start-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as handle:
            handle.write(data);handle.flush();os.fsync(handle.fileno())
        os.chmod(temporary,mode)
        if path.exists():
            previous=path.stat();os.chown(temporary,previous.st_uid,previous.st_gid)
        os.replace(temporary,path)
    finally:
        if os.path.exists(temporary):os.unlink(temporary)


def split_options(args,fields=None):
    values={};unknown=[];index=0
    while index<len(args):
        token=args[index];option,separator,value=token.partition('=')
        field=ALIASES.get(option)
        if field and (fields is None or field in fields):
            if field in BOOLS:
                if separator:raise ValueError('Unexpected value for '+option)
                values[field]=True
            else:
                if not separator:
                    index+=1
                    if index>=len(args):raise ValueError('Missing value for '+option)
                    value=args[index]
                values[field]=int(value) if field in LIMITS else value
        else:unknown.append(token)
        index+=1
    return values,unknown


def validate(values,supported,paths=False):
    if set(supported)-set(OPTIONS) or not isinstance(values,dict) or set(values)-set(supported):raise ValueError('Unsupported OSCam settings')
    for field,value in values.items():
        if field in BOOLS:
            if type(value) is not bool:raise ValueError('Invalid '+field)
        elif field in LIMITS:
            low,high=LIMITS[field]
            if type(value) is not int or not low<=value<=high:raise ValueError('Invalid '+field)
        elif not isinstance(value,str) or not value or any(c in value for c in '\x00\r\n'):
            raise ValueError('Invalid '+field)
        elif field.endswith('_dir'):
            if not Path(value).is_absolute() or (paths and not Path(value).is_dir()):
                raise ValueError('Directory does not exist: '+value)
        elif field=='syslog_ident' and len(value)>128:raise ValueError('Syslog ident is too long')


def launch_args(original,values,supported):
    validate(values,supported)
    _,args=split_options(original,set(values))
    for field,value in values.items():
        option=OPTIONS[field][0]
        if field in BOOLS:
            if value:args.append(option)
        elif field!='gcollect' or value:args.extend([option,str(value)])
    return args


class StartConfigStore:
    def __init__(self,init_dir='/etc/init.d',bin_dir='/usr/bin',config_dir='/etc/enigma2/gsu-softcam-start'):
        self.init_dir=Path(init_dir);self.bin_dir=Path(bin_dir);self.config_dir=Path(config_dir)

    def _paths(self,name):
        if not name or not re.fullmatch(r'[A-Za-z0-9_+.-]+',name) or 'oscam' not in name.lower():raise ValueError('Invalid OSCam name')
        script=(self.init_dir/('softcam.'+name)).resolve(strict=True)
        binary=self.bin_dir/name
        if script.parent!=self.init_dir.resolve() or not script.is_file() or not os.access(script,os.X_OK) or not binary.is_file() or not os.access(binary,os.X_OK):
            raise ValueError('OSCam init script or executable is unavailable')
        return script,binary,self.config_dir/(name+'.json')

    def _line(self,text,name):
        pattern=re.compile(r'^([ \t]*)(\$DAEMON|"\$DAEMON"|\$\{DAEMON\}|"\$\{DAEMON\}"|'+re.escape(str(self.bin_dir/name))+r')(?=\s)',re.M)
        matches=list(pattern.finditer(text))
        if len(matches)!=1:raise ValueError('Unsupported native OSCam start command')
        match=matches[0];end=text.find('\n',match.end())
        if end<0:end=len(text)
        line=text[match.start():end]
        if '\\' in line:raise ValueError('Multiline OSCam start command is unsupported')
        return match,end,line

    def _original(self,text,name):
        marker='# GSU OSCam startup adapter: '+name
        if marker not in text:return text
        command=' '.join(shlex.quote(v) for v in ('/usr/bin/python3',str(Path(__file__).resolve()),'--launch',name,'--'))
        lines=text.splitlines(keepends=True)
        for index,line in enumerate(lines):
            if line.strip()!=marker:continue
            indent=line[:len(line)-len(line.lstrip())]
            if index+1>=len(lines) or not lines[index+1].startswith(indent+command+' '):
                raise ValueError('Managed init command changed; reopen original script')
            lines[index+1]=indent+lines[index+1][len(indent+command+' '):]
            del lines[index]
            return ''.join(lines)
        raise ValueError('Invalid managed init marker')

    def _default_args(self,text,name):
        _,_,line=self._line(text,name)
        pid=re.search(r'^PIDFILE=(.+)$',text,re.M)
        if not pid:raise ValueError('Native PIDFILE definition is missing')
        pid_value=pid[1].strip().strip('"\'').replace('${CAM}',name).replace('$CAM',name)
        if '$' in pid_value or not Path(pid_value).is_absolute():raise ValueError('Unsupported native PIDFILE')
        line=line.replace('${CAM}',name).replace('$CAM',name).replace('${PIDFILE}',pid_value).replace('$PIDFILE',pid_value)
        tokens=shlex.split(line);args=[]
        for token in tokens[1:]:
            if token in ('|','&',';') or token.startswith(('>','2>','1>')):break
            if '$' in token or '`' in token:raise ValueError('Unsupported init argument expansion')
            args.append(token)
        if not any(x in args for x in ('-b','--daemon')):raise ValueError('Native daemon startup is required')
        try:
            index=next(i for i,x in enumerate(args) if x in ('-B','--pidfile'))
            if args[index+1]!=pid_value:raise ValueError('Native PIDFILE arguments differ')
        except (StopIteration,IndexError):raise ValueError('Native PIDFILE argument is missing')
        return args,pid_value

    def _saved(self,path):
        if not path.exists():return None
        data=json.loads(path.read_text())
        if data.get('schema')!=1 or not isinstance(data.get('supported'),list):raise ValueError('Invalid saved OSCam options')
        validate(data.get('values'),data['supported'])
        return data

    def snapshot(self,name):
        script,binary,path=self._paths(name);current=script.read_bytes();original=self._original(current.decode(),name)
        args,pidfile=self._default_args(original,name)
        result=subprocess.run([str(binary),'--help'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=5,check=False)
        help_text=result.stdout.decode('utf-8','replace')
        supported=[field for field,definition in OPTIONS.items() if definition[0] in help_text]
        if not all(f in supported for f in ('config_dir','temp_dir','restart')):raise ValueError('OSCam help does not expose required options')
        values={field:OPTIONS[field][2] for field in supported}
        config=re.search(r'ConfigDir\s*:\s*([^\r\n]+)',help_text)
        values['config_dir']=config[1].strip() if config else None
        temp=re.search(r'--temp-dir[^\n]*\n\s*\.\s*Default:\s*([^\r\n]+)',help_text)
        if temp:values['temp_dir']=temp[1].strip()
        defaults,_=split_options(args);values.update({k:v for k,v in defaults.items() if k in supported})
        if values['config_dir'] is None:raise ValueError('Cannot determine native configuration directory')
        saved=self._saved(path)
        if saved:
            unknown=set(saved['values'])-set(supported)
            if unknown:raise ValueError('Installed OSCam no longer supports saved settings: '+', '.join(sorted(unknown)))
            values.update(saved['values'])
        validate(values,supported)
        return {'name':name,'script_sha256':hashlib.sha256(current).hexdigest(),'supported':supported,'values':values,'pidfile':pidfile}

    def _adapter(self,text,name):
        if '# GSU OSCam startup adapter: '+name in text:return text
        match,_,_=self._line(text,name)
        # Preserve the original shell expansions, pipes and redirections verbatim.
        prefix=match[1]+'# GSU OSCam startup adapter: '+name+'\n'+match[1]
        command=' '.join(shlex.quote(v) for v in ('/usr/bin/python3',str(Path(__file__).resolve()),'--launch',name,'--'))
        return text[:match.start()]+prefix+command+' '+text[match.start()+len(match[1]):]

    def save(self,snapshot,values):
        name=snapshot['name'];script,_,path=self._paths(name);before=script.read_bytes()
        if hashlib.sha256(before).hexdigest()!=snapshot['script_sha256']:raise OSError('OSCam init script changed; reopen settings')
        validate(values,snapshot['supported'],paths=True)
        original=self._original(before.decode(),name)
        self._default_args(original,name)
        self.config_dir.mkdir(parents=True,exist_ok=True)
        backup=self.config_dir/(name+'.init-backup')
        # Never overwrite the first original backup. Current package commands
        # remain in the adapted line and are used when the adapter launches.
        if not backup.exists():atomic_write(backup,original.encode(),stat.S_IMODE(script.stat().st_mode))
        data={'schema':1,'name':name,'supported':snapshot['supported'],'values':values}
        previous=path.read_bytes() if path.exists() else None
        try:
            atomic_write(path,(json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
            if script.read_bytes()!=before:raise OSError('OSCam init script changed while saving')
            atomic_write(script,self._adapter(before.decode(),name).encode(),stat.S_IMODE(script.stat().st_mode))
        except Exception:
            if previous is None:path.unlink(missing_ok=True)
            else:atomic_write(path,previous)
            raise

    def ensure_adapter(self,name):
        script,_,path=self._paths(name)
        if self._saved(path) is None:return
        text=script.read_text()
        if '# GSU OSCam startup adapter: '+name not in text:
            self._default_args(text,name)
            atomic_write(script,self._adapter(text,name).encode(),stat.S_IMODE(script.stat().st_mode))

    def restore(self,name):
        if not re.fullmatch(r'[A-Za-z0-9_+.-]+',name) or 'oscam' not in name.lower():raise ValueError('Invalid OSCam name')
        path=self.init_dir/('softcam.'+name)
        if not path.exists():return
        script=path.resolve(strict=True)
        if script.parent!=self.init_dir.resolve():raise ValueError('Init script points outside init directory')
        text=script.read_text()
        if '# GSU OSCam startup adapter: '+name in text:
            atomic_write(script,self._original(text,name).encode(),stat.S_IMODE(script.stat().st_mode))

    def restore_all(self):
        for path in sorted(self.config_dir.glob('*.json')):self.restore(path.stem)

    def launch(self,name,args):
        _,binary,path=self._paths(name)
        if not args or Path(args[0]).resolve()!=binary.resolve():raise ValueError('OSCam executable changed')
        saved=self._saved(path)
        actual=launch_args(args[1:],saved['values'],saved['supported']) if saved else args[1:]
        os.execv(str(binary),[str(binary)]+actual)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    operation=parser.add_mutually_exclusive_group(required=True)
    operation.add_argument('--launch');operation.add_argument('--restore-all',action='store_true')
    parser.add_argument('args',nargs=argparse.REMAINDER)
    args=parser.parse_args()
    try:
        if args.restore_all:StartConfigStore().restore_all()
        else:StartConfigStore().launch(args.launch,args.args[1:] if args.args[:1]==['--'] else args.args)
    except (OSError,ValueError) as error:
        print('OSCam start configuration failed: '+str(error),flush=True)
        raise SystemExit(1)
