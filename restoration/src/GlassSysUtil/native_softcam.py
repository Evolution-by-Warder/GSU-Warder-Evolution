"""Read the image-selected SoftCAM; invoke its existing init script asynchronously.

Switch the image selection only after an explicit start of another installed CAM.
Never copy CAM binaries or write UCM status files.
"""
import os
import errno
import signal
import time
import re
import shlex
import shutil
import subprocess
import tempfile
import fcntl
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def command_lock(path='/run/gsu-softcam-operation.lock'):
    fd=os.open(path,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
    try:
        fcntl.flock(fd,fcntl.LOCK_EX)
        yield
    finally:os.close(fd)


class NativeSoftcam:
    def __init__(self, init_dir='/etc/init.d', bin_dir='/usr/bin', proc_dir='/proc', info_dirs=None):
        self.init_dir=Path(init_dir)
        self.bin_dir=Path(bin_dir)
        self.proc_dir=Path(proc_dir)
        self.info_dirs=[Path(p) for p in (info_dirs or ('/var/lib/opkg/info','/usr/lib/opkg/info'))]
        self.package_cache={}
        self.registered_packages=None

    def valid(self,name):
        if not name or name.lower()=='none' or not re.fullmatch(r'[A-Za-z0-9_+.-]+',name):return False
        try:
            script=(self.init_dir/('softcam.'+name)).resolve(strict=True)
            binary=self.bin_dir/name
            return script.parent==self.init_dir.resolve() and script.is_file() and os.access(script,os.X_OK) and binary.is_file() and os.access(binary,os.X_OK)
        except (OSError,RuntimeError):return False

    def available(self):
        return sorted(p.name[len('softcam.'):] for p in self.init_dir.glob('softcam.*') if self.valid(p.name[len('softcam.'):]))

    def selected(self):
        link=self.init_dir/'softcam'
        try:
            if not link.is_symlink():return None
            target=link.resolve(strict=True)
            if target.parent!=self.init_dir.resolve() or not target.name.startswith('softcam.'):return None
            name=target.name[len('softcam.'):]
            return name if self.valid(name) else None
        except (OSError,RuntimeError):return None

    def _identity(self,pid,binary):
        try:
            folder=self.proc_dir/str(pid)
            if (folder/'exe').resolve(strict=True)!=binary:return None
            # stat starttime distinguishes a process from a reused PID.
            fields=(folder/'stat').read_text().rsplit(')',1)[1].split()
            if fields[0] in ('Z','X','x'):return None
            return fields[19]
        except (OSError,RuntimeError,IndexError):return None

    def _matching_pids(self,name):
        if not self.valid(name):return {}
        binary=(self.bin_dir/name).resolve()
        try:folders=list(self.proc_dir.iterdir())
        except OSError:return {}
        return {int(p.name):identity for p in folders if p.name.isdigit()
                and (identity:=self._identity(p.name,binary)) is not None}

    def running(self,name=None):
        return bool(self._matching_pids(name or self.selected()))

    def _wait_stopped(self,name,seconds):
        deadline=time.monotonic()+seconds
        while self.running(name):
            remaining=deadline-time.monotonic()
            if remaining<=0:return False
            time.sleep(min(0.1,remaining))
        return True

    def _signal_matching(self,name,number):
        binary=(self.bin_dir/name).resolve()
        for pid,identity in self._matching_pids(name).items():
            fd=None
            try:
                if hasattr(os,'pidfd_open') and hasattr(signal,'pidfd_send_signal'):
                    try:fd=os.pidfd_open(pid)
                    except OSError as error:
                        if error.errno not in (errno.ENOSYS,errno.EINVAL):raise
                if self._identity(pid,binary)!=identity:continue
                if fd is not None:signal.pidfd_send_signal(fd,number)
                else:os.kill(pid,number)
            except ProcessLookupError:pass
            finally:
                if fd is not None:os.close(fd)

    def stop_verified(self,name):
        # This method runs in the command worker, never on Enigma's GUI thread.
        if not self.valid(name):raise ValueError('Invalid SoftCAM')
        try:self._run_script(name,'stop')
        except subprocess.TimeoutExpired:pass
        if self._wait_stopped(name,2):return 0
        # Missing/stale PID files must not leave the actual CAM running.
        self._signal_matching(name,signal.SIGTERM)
        if self._wait_stopped(name,2):return 0
        self._signal_matching(name,signal.SIGKILL)
        if not self._wait_stopped(name,1):raise OSError('SoftCAM could not be stopped')
        return 0

    def start_verified(self,name):
        if not self.valid(name) or self.selected()!=name:raise OSError('SoftCAM selection changed')
        active=self.active_name()
        if active and (self.bin_dir/active).resolve()!=(self.bin_dir/name).resolve():
            raise OSError('Another SoftCAM is already running')
        result=self._run_script(name,'start')
        if result or not self.running(name):raise OSError('SoftCAM did not start')
        return 0

    def restart_verified(self,name):
        self.stop_verified(name)
        result=self._run_script(name,'start')
        if result or not self.running(name):raise OSError('SoftCAM did not restart')
        return 0

    def active_name(self):
        selected=self.selected()
        if selected and self.running():return selected
        return next((name for name in self.available() if self.running(name)),None)

    def read_package_registry(self):
        opkg=shutil.which('opkg')
        if not opkg:raise OSError('opkg is unavailable')
        result=subprocess.run([opkg,'list-installed'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=8,check=False)
        if result.returncode:raise OSError('Installed package registry could not be read')
        return {line.split(' - ',1)[0].strip() for line in result.stdout.decode('utf-8','replace').splitlines() if ' - ' in line}

    def package_for(self,name):
        if name in self.package_cache:return self.package_cache[name]
        package=None
        if self.valid(name):
            candidates=('enigma2-plugin-softcams-'+name,'enigma2-plugin-cams-'+name,name)
            if self.registered_packages is not None:
                package=next((p for p in candidates if p in self.registered_packages),None)
                self.package_cache[name]=package
                return package
            for root in self.info_dirs:
                for candidate in candidates:
                    try:files=(root/(candidate+'.list')).read_text().splitlines()
                    except OSError:continue
                    if str(self.bin_dir/name) in files or str(self.init_dir/('softcam.'+name)) in files:
                        package=candidate;break
                if package:break
        self.package_cache[name]=package
        return package

    def command(self,name,action):
        if action not in ('start','stop','restart') or not self.valid(name):
            raise ValueError('Invalid SoftCAM or command')
        python=shutil.which('python3') or '/usr/bin/python3'
        if action!='stop' and name!=self.selected():
            args=[python,str(Path(__file__).resolve()),'--switch',name,'--expected',self.selected() or '']
        else:
            args=[python,str(Path(__file__).resolve()),'--action',action,'--name',name]
        return ' '.join(shlex.quote(value) for value in args)

    def _set_link(self,target):
        link=self.init_dir/'softcam'
        if link.exists() and not link.is_symlink():raise OSError('SoftCAM selection is not a symlink')
        if target is None:
            if link.is_symlink():link.unlink()
            return
        with tempfile.TemporaryDirectory(prefix='.warder-softcam-',dir=self.init_dir) as folder:
            temporary=Path(folder)/'softcam'
            temporary.symlink_to(target)
            os.replace(temporary,link)

    def _run_script(self,name,action):
        if action=='start' and 'oscam' in name.lower():
            if __package__:
                from .native_start_config import StartConfigStore
            else:
                from native_start_config import StartConfigStore
            StartConfigStore(init_dir=self.init_dir,bin_dir=self.bin_dir).ensure_adapter(name)
        return subprocess.run([str(self.init_dir/('softcam.'+name)),action],timeout=20,check=False).returncode

    def switch_to(self,name,expected):
        # Executed only in the separate worker process, never in the GUI.
        if not self.valid(name) or (self.selected() or '')!=expected:raise OSError('SoftCAM selection changed')
        link=self.init_dir/'softcam'
        if link.exists() and not link.is_symlink():raise OSError('SoftCAM selection is not a symlink')
        old_link=os.readlink(link) if link.is_symlink() else None
        old=self.selected()
        old_binary=(self.bin_dir/old).resolve() if old else None
        for other in self.available():
            if self.running(other) and (self.bin_dir/other).resolve()!=old_binary:
                raise OSError('Another SoftCAM is already running')
        was_running=bool(old and self.running(old))
        try:
            if was_running:
                self.stop_verified(old)
                if self.running(old):raise OSError('Previous SoftCAM could not be stopped')
            self._set_link(str(self.init_dir/('softcam.'+name)))
            result=self._run_script(name,'start')
            if result or not self.running(name):raise OSError('Selected SoftCAM did not start')
        except Exception:
            # Restore selection and the previously working CAM after failure.
            if name!=old and self.running(name):
                try:self.stop_verified(name)
                except Exception:pass
            self._set_link(old_link)
            if was_running and not self.running(old) and not self.running(name):self._run_script(old,'start')
            raise
        return 0


def refresh_state(screen,translate):
    active=screen.nativeSoftcam.active_name()
    screen['activCam'].setText(translate('Active')+' CAM: '+(active or translate('None')))
    screen['statCamSrvbin'].setText(translate('CAM/SRV Running') if active else translate('No Running CAM/SRV'))
    screen.statcommPics('piccam','green' if active else 'blue')


def handle_action(screen, action, container_factory, translate):
    """Return True when native handling consumes a button press."""
    native=screen.nativeSoftcam
    current=screen['config'].getCurrent()
    name=current[1].getText() if current else None
    if screen['config'].getCurrentIndex() != 0 or name not in native.available():
        # Preserve the legacy manager when stopped, but prevent two managers
        # from starting different CAMs at the same time.
        if native.active_name():
            screen['statCamSrvcmd'].setText(translate('Please First Stop CAM')+': '+str(native.active_name()))
            return True
        return False
    if not screen.enCommand:
        screen['statCamSrvcmd'].setText(translate('Try later ... working'))
        return True
    operation='restart' if action == 'start' and name==native.selected() and native.running() else action
    try:
        command=native.command(name,operation)
    except ValueError:
        screen['statCamSrvcmd'].setText(translate('No Command Allowed'))
        return True
    screen.enCommand=False
    screen['statCamSrvcmd'].setText(translate({'start':'Starting','stop':'Stopping','restart':'Restarting'}[operation])+' CAM '+name)
    screen.statcommPics('comm','yellow')
    container=container_factory()
    screen.nativeCommand=container
    from .native_autostart import manual_begin,manual_end
    ticket=manual_begin(name,operation)
    completed=False

    def finished(code):
        nonlocal completed
        if completed:return
        completed=True
        screen.enCommand=True
        running=native.running(name)
        active=native.active_name()
        success=code == 0 and running == (operation != 'stop')
        manual_end(ticket,success)
        screen['activCam'].setText(translate('Active')+' CAM: '+(active if active else translate('None')))
        screen['statCamSrvbin'].setText(translate('CAM/SRV Running') if active else translate('No Running CAM/SRV'))
        screen.statcommPics('piccam','green' if active else 'blue')
        screen.statcommPics('comm','green' if success else 'red')
        screen['statCamSrvcmd'].setText(translate({'start':'Start Script Executed','restart':'Restart Script Executed','stop':'Stop Script Executed'}[operation]) if success else name+' '+translate('Error'))

    signal=container.appClosed
    try:
        screen.nativeCommandConnection=signal.connect(finished)
    except AttributeError:
        (signal.get() if hasattr(signal,'get') else signal).append(finished)
    try:
        result=container.execute(command)
    except Exception:
        finished(-1)
    else:
        if result:
            finished(result)
    return True


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    operation=parser.add_mutually_exclusive_group(required=True)
    operation.add_argument('--switch')
    operation.add_argument('--autostart')
    operation.add_argument('--autocheck')
    operation.add_argument('--action',choices=('start','stop','restart'))
    parser.add_argument('--name')
    parser.add_argument('--expected')
    parser.add_argument('--guard')
    args=parser.parse_args()
    controller=NativeSoftcam()
    try:
        with command_lock():
            if args.autostart or args.autocheck:
                from native_autostart import start_if_needed
                if args.autocheck and not args.guard:parser.error('--guard is required with --autocheck')
                result=start_if_needed(controller,args.autostart or args.autocheck,args.guard,bool(args.autocheck))
            elif args.switch:
                if args.expected is None:parser.error('--expected is required with --switch')
                result=controller.switch_to(args.switch,args.expected)
            else:
                if not args.name:parser.error('--name is required with --action')
                if args.action in ('start','restart') and controller.selected()!=args.name:
                    raise OSError('SoftCAM selection changed')
                result={'start':controller.start_verified,'stop':controller.stop_verified,'restart':controller.restart_verified}[args.action](args.name)
        raise SystemExit(result)
    except (OSError,ValueError,subprocess.SubprocessError) as error:
        if args.autostart or args.autocheck:
            from native_autostart import log_event
            log_event('automatic start failed: '+str(error))
        print('SoftCAM command failed: '+str(error),flush=True)
        raise SystemExit(1)
