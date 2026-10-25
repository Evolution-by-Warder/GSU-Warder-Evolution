"""Read the image-selected SoftCAM; invoke its existing init script asynchronously.

Never change image selection, copy CAM binaries, or write UCM status files.
"""
import os
import re
import shlex
from pathlib import Path


class NativeSoftcam:
    def __init__(self, init_dir='/etc/init.d', bin_dir='/usr/bin', proc_dir='/proc'):
        self.init_dir=Path(init_dir)
        self.bin_dir=Path(bin_dir)
        self.proc_dir=Path(proc_dir)

    def selected(self):
        link=self.init_dir/'softcam'
        try:
            if not link.is_symlink():
                return None
            target=link.resolve(strict=True)
            if target.parent != self.init_dir.resolve() or not target.name.startswith('softcam.'):
                return None
            name=target.name[len('softcam.'):]
            if name.lower() == 'none' or not re.fullmatch(r'[A-Za-z0-9_+.-]+',name):
                return None
            binary=self.bin_dir/name
            if not target.is_file() or not os.access(target,os.X_OK) or not binary.is_file() or not os.access(binary,os.X_OK):
                return None
            return name
        except (OSError,RuntimeError):
            return None

    def running(self):
        name=self.selected()
        if name is None:
            return False
        binary=(self.bin_dir/name).resolve()
        try:
            for pid in self.proc_dir.iterdir():
                if not pid.name.isdigit():
                    continue
                try:
                    if (pid/'exe').resolve(strict=True) == binary:
                        return True
                except (OSError,RuntimeError):
                    continue
        except OSError:
            pass
        return False

    def command(self, name, action):
        if action not in ('start','stop','restart') or name != self.selected():
            raise ValueError('SoftCAM selection changed or invalid command')
        return shlex.quote(str(self.init_dir/('softcam.'+name)))+' '+action


def handle_action(screen, action, container_factory, translate):
    """Return True when native handling consumes a button press."""
    native=screen.nativeSoftcam
    name=native.selected()
    if not name:
        return False
    current=screen['config'].getCurrent()
    selected=current[1].getText() if current else None
    if screen['config'].getCurrentIndex() != 0 or selected != name:
        # Preserve the legacy manager when stopped, but prevent two managers
        # from starting different CAMs at the same time.
        if native.running():
            screen['statCamSrvcmd'].setText(translate('Please First Stop CAM')+': '+name)
            return True
        return False
    if not screen.enCommand:
        screen['statCamSrvcmd'].setText(translate('Try later ... working'))
        return True
    operation='restart' if action == 'start' and native.running() else action
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
        running=native.running()
        success=code == 0 and running == (operation != 'stop')
        screen['activCam'].setText(translate('Active')+' CAM: '+(name if running else translate('None')))
        screen.statcommPics('piccam','green' if running else 'blue')
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
