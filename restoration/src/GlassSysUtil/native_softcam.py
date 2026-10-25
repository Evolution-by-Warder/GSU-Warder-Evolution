"""Read the image-selected SoftCAM; invoke its existing init script asynchronously.

Switch the image selection only after an explicit start of another installed CAM.
Never copy CAM binaries or write UCM status files.
"""
import os
import re
import shlex
import shutil
import subprocess
import tempfile
from pathlib import Path


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

    def running(self,name=None):
        name=name or self.selected()
        if not self.valid(name):return False
        binary=(self.bin_dir/name).resolve()
        try:
            for pid in self.proc_dir.iterdir():
                if not pid.name.isdigit():continue
                try:
                    if (pid/'exe').resolve(strict=True)==binary:return True
                except (OSError,RuntimeError):continue
        except OSError:pass
        return False

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
        if action!='stop' and name!=self.selected():
            python=shutil.which('python3') or '/usr/bin/python3'
            args=[python,str(Path(__file__).resolve()),'--switch',name,'--expected',self.selected() or '']
            return ' '.join(shlex.quote(value) for value in args)
        return shlex.quote(str(self.init_dir/('softcam.'+name)))+' '+action

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
                self._run_script(old,'stop')
                if self.running(old):raise OSError('Previous SoftCAM could not be stopped')
            self._set_link(str(self.init_dir/('softcam.'+name)))
            result=self._run_script(name,'start')
            if result or not self.running(name):raise OSError('Selected SoftCAM did not start')
        except Exception:
            # Restore selection and the previously working CAM after failure.
            if name!=old and self.running(name):
                try:self._run_script(name,'stop')
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

    def finished(code):
        screen.enCommand=True
        running=native.running(name)
        active=native.active_name()
        success=code == 0 and running == (operation != 'stop')
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
    parser.add_argument('--switch',required=True)
    parser.add_argument('--expected',required=True)
    args=parser.parse_args()
    try:raise SystemExit(NativeSoftcam().switch_to(args.switch,args.expected))
    except (OSError,ValueError,subprocess.SubprocessError) as error:
        print('SoftCAM switch failed: '+str(error),flush=True)
        raise SystemExit(1)
