# uncompyle6 version 3.9.3
# Python bytecode version base 2.6 (62161)
# Decompiled from: Python 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]
# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/plugin.py
# Compiled at: 2021-03-28 16:56:23
from Plugins.Extensions.GlassSysUtil.editInputBox import editInputBox
from Components.Console import Console as CompConsole
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Tools.Directories import fileExists
from xml.etree.cElementTree import parse
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap
from enigma import ePixmap, eTimer, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePoint, addFont
from Components.Pixmap import *
from Tools.LoadPixmap import LoadPixmap
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Screens.MessageBox import MessageBox
from os import system, path, statvfs, remove, listdir, rename, symlink, unlink, mkdir
from Components.ConfigList import ConfigListScreen, ConfigList
from Components.config import *
from Components.ScrollLabel import ScrollLabel
from Components.ProgressBar import ProgressBar
from time import sleep
import gettext
import builtins
import platform
import shutil
_ = getattr(builtins, "_", lambda value: value)
ENA_TT = False
try:
    from enigma import iDVBFrontend
    ENA_TT = True
except:
    pass

try:
    from enigma import quitMainloop
except:
    pass

try:
    from Components.Sensors import sensors
except:
    pass

import os
from Tools.HardwareInfo import HardwareInfo
from re import sub
from Components.Sources.List import List
from Screens.ChoiceBox import ChoiceBox
from Screens.InputBox import InputBox
from Components.Input import Input
from Components.FileList import FileList
from enigma import eConsoleAppContainer
from ServiceReference import ServiceReference
from enigma import eServiceCenter, eDVBDB, eServiceReference, iServiceInformation, iPlayableService, eDVBFrontendParametersTerrestrial
from Tools.Transponder import ConvertToHumanReadable
try:
    from string import upper
except:
    pass

from Components.ServiceEventTracker import ServiceEventTracker
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Screens.Console import Console
import base64
try:
    import sys
    ISP38 = sys.version_info[0] == 3
except:
    ISP38 = os.path.exists('/usr/lib/python3.8')

from urllib import request as urllibXX
from urllib import request as urllibXX2
FTP_ALL = [(base64.b64decode('cGljb25zLnRlY2huZXRldXdlYi5ldQ==').decode('ascii'), base64.b64decode('ZnRwMTA4MTA0').decode('ascii'), base64.b64decode('UGljb25pQ3M1OQ==').decode('ascii'))]
DG = '°'
EACC = False
try:
    from enigma import iAudioType_ENUMS as iAt
    EACC = True
except:
    pass

PYTHONPATH = '/usr/lib/enigma2/python/'
GSU_PATH = PYTHONPATH + 'Plugins/Extensions/GlassSysUtil/'

_MACHINE = platform.machine().lower()
_HELPER_ARCH = 'arm' if _MACHINE.startswith('arm') else 'aarch64' if _MACHINE in ('aarch64','arm64') else 'mips' if _MACHINE.startswith('mips') else 'sh4'
def _gsu_helper(name):
    system_path=shutil.which(name)
    if system_path:
        return system_path
    bundled=os.path.join(GSU_PATH,'bin',_HELPER_ARCH,name)
    return bundled if os.path.isfile(bundled) else name

addFont(GSU_PATH + 'font/priveG.ttf', 'priveG', 100, False)
F_TMP = '/tmp/tmp.tmp'
RM_TMP = 'rm -rf %s' % F_TMP

def Writelog(txt):
    log = GSU_PATH + 'gsu.log'
    if os.path.isfile(log):
        if os.path.getsize(log) > 1000000:
            system('rm -rf ' + log)
    try:
        f = open(log, 'a')
        f.write('%s\n' % str(txt))
        f.close()
    except IOError:
        pass

    return


XCPU = 'mipsel'
try:
    with open('/proc/cpuinfo', 'r') as _cpu_file:
        cpu = _cpu_file.read()
    if cpu.find('sh4') != -1:
        XCPU = 'sh4'
    elif cpu.find('ARMv7') != -1:
        XCPU = 'arm'
    elif HardwareInfo().get_device_name() in ('one', 'two'):
        XCPU = 'aarch64'
    elif os.path.exists('/usr/lib/python2.7') or ISP38:
        XCPU = 'mips32el'
except:
    pass

FHD = getDesktop(0).size().width()
if FHD == 1920:
    from Plugins.Extensions.GlassSysUtil.GSU_skins_FHD import *
    FHD = 1.5
elif FHD == 3840:
    from Plugins.Extensions.GlassSysUtil.GSU_skins_UHD import *
    FHD = 3
else:
    from Plugins.Extensions.GlassSysUtil.GSU_skins import *
    FHD = 1
E4X = False
try:
    from enigma import eMediaDatabase
    E4X = True
except:
    pass

ENA_IF = False
try:
    from Components.Network import iNetwork
    ENA_IF = True
except:
    pass

# Architecture-specific helpers stay private; no mutation of /usr/bin on import.
FDISKG = shutil.which('fdisk') or 'fdisk'
MNG_DEV = bool(shutil.which('fdisk'))

def cpLibCr():
    return False


xxx = cpLibCr()

def chckPckg():
    if shutil.which('opkg'):
        return ('o', 'mipsel', 'ipk', '-')
    if shutil.which('dpkg'):
        return ('dpkg -i /tmp/%s', 'debpkg', 'deb', '-')
    return ('o', 'mipsel', 'ipk', '-')


(PKGBIN, TYPE_DIR, PKG, LISTIPK) = chckPckg()
ENA_D = TYPE_DIR == 'debpkg'

def chckPckgList():
    ttt = PKGBIN
    if ENA_D:
        ttt = 'o'
    try:
        system('%spkg list%sinstalled > %s' % (ttt, LISTIPK, F_TMP))
        f = open(F_TMP, 'r')
        content = f.read()
        f.close()
        system(RM_TMP)
    except:
        content = ''

    return content.split('\n')


ENAEBTR = False
ENAEBTR2 = False
try:
    from Plugins.Extensions.BitrateViewer.bitratecalc import eBitrateCalculator
    if not os.path.isfile(PYTHONPATH + 'Plugins/Extensions/BitrateViewer/bitratecalc.la') or ENA_D:
        ENAEBTR = True
        f = open(PYTHONPATH + 'Plugins/Extensions/BitrateViewer/plugin.py', 'r').read()
        if f.find('eBitrateCalculator(vpid, dvbnamespace') != -1:
            ENAEBTR2 = True
except:
    pass

ENA_Z = False
try:
    from enigma import eMediaDatabase
    ENA_Z = True
except:
    pass

import time
from socket import socket, AF_INET, SOCK_STREAM
import fcntl, struct
try:
    import ftplib
except:
    pass

from skin import parseColor
import re
from twisted.internet.protocol import Factory, DatagramProtocol
from twisted.internet import reactor, defer
from twisted.internet.error import CannotListenError
from Screens.InfoBarGenerics import InfoBarPlugins
config.plugins.GlassSysUtil = ConfigSubsection()
config.plugins.GlassSysUtil.par62 = ConfigYesNo(default=True)
DSC = '/tmp/.doscam/doscam.version'
NCM = '/tmp/.ncam/ncam.version'
GCM = '/tmp/.gcam/gcam.version'
BP_ICO = GSU_PATH + {3: 'uhd/', 1.5: 'fhd/', 1: ''}[FHD] + 'bp_icons/' + '%s.png'
A_TM = '/tmp/a.tmp'
RM_A_TMP = 'rm -rf %s' % A_TM
try:
    if config.plugins.GlassSysUtil.par62.value:
        gsu_language = []
        gsu_language = config.osd.language.value.split('_')
        if os.path.exists(GSU_PATH + 'locale/%s' % gsu_language[0]):
            _ = gettext.translation('gsu', GSU_PATH + 'locale', languages=gsu_language, fallback=True).gettext
except:
    pass

def fhd(t):
    return int(t * FHD)


def generatePS():
    try:
        rows = []
        for pid in os.listdir('/proc'):
            if not pid.isdigit():
                continue
            try:
                with open('/proc/%s/cmdline' % pid, 'rb') as handle:
                    command = handle.read(8192).replace(b'\x00', b' ').decode('utf-8', 'replace').strip()
                if not command:
                    with open('/proc/%s/comm' % pid) as handle:
                        command = handle.read().strip()
                rows.append('%s %s' % (pid, command))
            except OSError:
                continue
        with open(A_TM, 'w') as handle:
            handle.write('\n'.join(rows)+'\n')
        return bool(rows)
    except OSError:
        return False


ENA_PS = generatePS()
ucmInfoBarPlugins__init__ = None
GVIP = ''
PWDV = None
if os.path.isfile('/etc/version_act'):
    try:
        PWDV = open('/etc/version_act', 'r').readline().strip()
        GVIP = '-vip'
    except:
        pass

config.plugins.GlassSysUtil = ConfigSubsection()
config.plugins.GlassSysUtil.par0 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par1 = ConfigInteger(default=1030)
config.plugins.GlassSysUtil.par2 = ConfigInteger(default=70)
config.plugins.GlassSysUtil.par3 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par4 = ConfigInteger(500, (1, 2000))
config.plugins.GlassSysUtil.par5 = ConfigInteger(8, (4, 15))
config.plugins.GlassSysUtil.par6 = ConfigSelection(default='CIFS', choices=[('CIFS', _('CIFS')), ('NFS', _('NFS'))])
config.plugins.GlassSysUtil.par7 = ConfigText('/shareDir', False)
config.plugins.GlassSysUtil.par8 = ConfigText('/media/shareNet', False)
config.plugins.GlassSysUtil.par9 = ConfigText('root', False)
config.plugins.GlassSysUtil.par10 = ConfigText('', False)
config.plugins.GlassSysUtil.par11 = ConfigInteger(8192, (8192, 65535))
config.plugins.GlassSysUtil.par12 = ConfigInteger(8192, (8192, 65535))
config.plugins.GlassSysUtil.par13 = ConfigText('192.168.1.100', False)
config.plugins.GlassSysUtil.par14 = ConfigDirectory('/media/hdd/autoInstall/')
config.plugins.GlassSysUtil.par15 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par17 = ConfigDirectory('/var/tuxbox/config/')
config.plugins.GlassSysUtil.par18 = ConfigDirectory('/tmp/')
config.plugins.GlassSysUtil.par19 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par20 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par21 = ConfigText('/usr/UCM_CamSrv_bin/$SrvBin -b > /dev/null 2>&1 &', False)
config.plugins.GlassSysUtil.par22 = ConfigYesNo(default=True)
config.plugins.GlassSysUtil.par23 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par24 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par25 = ConfigInteger(60, (30, 300))
config.plugins.GlassSysUtil.par26 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par27 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par28 = ConfigSelection(default='1', choices=[('1', _('1 - Immediate free')), ('2', _('2 - Check for double frees'))])
config.plugins.GlassSysUtil.par29 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par30 = ConfigSelection(default='1', choices=[('0', _('Disabled')), ('1', _('WebIf restart is active')), ('2', _('Like 1, but also restart on segfaults'))])
config.plugins.GlassSysUtil.par31 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par32 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par33 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par34 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par35 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par36 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par37 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par38 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par39 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par40 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par41 = NoSave(ConfigInteger(0, (0, 59)))
config.plugins.GlassSysUtil.par42 = NoSave(ConfigText(fixed_size=False))
config.plugins.GlassSysUtil.par43 = NoSave(ConfigSelection(default='Daily', choices=[('Hourly', _('Hourly')), ('Daily', _('Daily')), ('Weekly', _('Weekly')), ('Monthly', _('Monthly')), ('0', _('Expert Setting'))]))
config.plugins.GlassSysUtil.par44 = NoSave(ConfigSelection(default='Monday', choices=[('Monday', _('Monday')), ('Tuesday', _('Tuesday')), ('Wednesday', _('Wednesday')), ('Thursday', _('Thursday')), ('Friday', _('Friday')), ('Saturday', _('Saturday')), ('Sunday', _('Sunday'))]))
config.plugins.GlassSysUtil.par45 = NoSave(ConfigInteger(default=1, limits=(1, 31)))
config.plugins.GlassSysUtil.par46 = NoSave(ConfigSelection(default='None', choices=[('1', '1'), ('2', '2')]))
config.plugins.GlassSysUtil.par47 = NoSave(ConfigSelection(choices=[('User', _('User')), ('/usr/script', '/usr/script')]))
config.plugins.GlassSysUtil.par48 = ConfigInteger(15, (1, 30))
config.plugins.GlassSysUtil.par49 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par50 = ConfigYesNo(default=True)
config.plugins.GlassSysUtil.par51 = ConfigYesNo(default=True)
config.plugins.GlassSysUtil.par52 = ConfigYesNo(default=True)
config.plugins.GlassSysUtil.par53 = ConfigYesNo(default=True)
config.plugins.GlassSysUtil.par54 = ConfigYesNo(default=True)
config.plugins.GlassSysUtil.par55 = ConfigYesNo(default=True)
config.plugins.GlassSysUtil.par56 = ConfigYesNo(default=True)
config.plugins.GlassSysUtil.par57 = ConfigSelection(default='0', choices=[('0', _('no')), ('1', _('yes')), ('2', _('with net check'))])
config.plugins.GlassSysUtil.par58 = ConfigInteger(10, (1, 120))
config.plugins.GlassSysUtil.par59 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par60 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par61 = ConfigSelection(default='10', choices=[('5', '5'), ('10', '10'), ('15', '15')])
config.plugins.GlassSysUtil.par62 = ConfigYesNo(default=True)
config.plugins.GlassSysUtil.par63 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par64 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par65 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par66 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par67 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par68 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par69 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par70 = ConfigInteger(96, (96, 4096))
config.plugins.GlassSysUtil.par71 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par72 = ConfigText('pidfile', False)
config.plugins.GlassSysUtil.par73 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par74 = ConfigText('oscam', False)
config.plugins.GlassSysUtil.par75 = ConfigYesNo(default=False)
config.plugins.GlassSysUtil.par76 = NoSave(ConfigText(fixed_size=False))
config.plugins.GlassSysUtil.par77 = NoSave(ConfigInteger(0, (0, 59)))
config.plugins.GlassSysUtil.par78 = ConfigInteger(150, (20, 500))
config.plugins.GlassSysUtil.par79 = NoSave(ConfigSelection(default='c', choices=[('c', ' ')]))
config.plugins.GlassSysUtil.par80 = ConfigSelection(default='1', choices=[('0', _('Static info')), ('1', _('Rolled info'))])
config.plugins.GlassSysUtil.par81 = ConfigInteger(4, (2, 12))
config.plugins.GlassSysUtil.par82 = ConfigSelection(default='udp', choices=[('udp', _('UDP')), ('tcp', _('TCP'))])
config.plugins.GlassSysUtil.par83 = NoSave(ConfigText('', False))

def main(session, **kwargs):
    session.open(SysUtilMngMain)
    return


def main1(session, **kwargs):
    session.open(GlassSysInfoBrowser)
    return


def main3(session, **kwargs):
    (c, o) = countServers()
    c = oscamRunning()
    if c or not c and not o:
        if o:
            session.open(oscamInfo)
        else:
            session.open(oscamInfoChoiceServer)
    return


def main2(session, **kwargs):
    session.open(univCamMng)
    return


def main4(session, **kwargs):
    session.open(channelInfoCenter)
    return


def main5(session, **kwargs):
    session.open(devMngMain)
    return


def startViaMenu(menuid, **kwargs):
    if menuid == 'setup':
        return [(_('Glass System Utility'), main, 'glass_sys_utils', None)]
    else:
        return []


def sessionAutostart(reason, **kwargs):
    global ucmInfoBarPlugins__init__
    if reason == 0:
        autocams.autoStartCheck(kwargs['session'])
        OnScreenEcm.startShowOSD(kwargs['session'])
        autoInstallMng.autoInstallStart(kwargs['session'])
    if config.plugins.GlassSysUtil.par40.value:
        if 'session' in kwargs:
            session = kwargs['session']
            if ucmInfoBarPlugins__init__ is None:
                ucmInfoBarPlugins__init__ = InfoBarPlugins.__init__
            InfoBarPlugins.__init__ = InfoBarPlugins__init__
            InfoBarPlugins.keyStartGreen = keyStartGreen
            InfoBarPlugins.keyStartRed = keyStartRed
    return


def InfoBarPlugins__init__(self):
    from Screens.InfoBarGenerics import InfoBarEPG
    if isinstance(self, InfoBarEPG):
        x = {'ucm_start_key': (self.keyStartGreen, 'UCM Start failed'), 'ecm_start_key': (self.keyStartRed, 'ECM Start failed')}
        self['GSUmain'] = HelpableActionMap(self, 'GSUmain', x)
    else:
        InfoBarPlugins.__init__ = InfoBarPlugins.__init__
        InfoBarPlugins.keyStartGreen = None
        InfoBarPlugins.keyStartRed = None
    ucmInfoBarPlugins__init__(self)
    return


def keyStartGreen(self):
    self.session.open(univCamMng)
    return


def keyStartRed(self):
    self.session.open(ECMInfo)
    return


def Plugins(path, **kwargs):
    ret = [
     PluginDescriptor(name=_('Glass System Utility'), description=_('Glass System Utility'), where=PluginDescriptor.WHERE_PLUGINMENU, icon='SysMgt.png', fnc=main),
     PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionAutostart)]
    if config.plugins.GlassSysUtil.par52.value:
        ret.append(PluginDescriptor(name='(GSU) ' + _('Glass System Utility'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main))
    if config.plugins.GlassSysUtil.par53.value:
        ret.append(PluginDescriptor(name='(GSU) ' + _('System Information'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main1))
    if config.plugins.GlassSysUtil.par54.value:
        ret.append(PluginDescriptor(name='(GSU) ' + _('Channel Information'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main4))
    if MNG_DEV and config.plugins.GlassSysUtil.par55.value:
        ret.append(PluginDescriptor(name='(GSU) ' + _('Devices Manager'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main5))
    if config.plugins.GlassSysUtil.par51.value:
        ret.append(PluginDescriptor(name=_('Glass System Utility'), where=PluginDescriptor.WHERE_MENU, fnc=startViaMenu))
    if ENA_PS and config.plugins.GlassSysUtil.par56.value:
        ret.append(PluginDescriptor(name='(GSU) ' + _('CAM/SRV Manager'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main2))
    if config.plugins.GlassSysUtil.par60.value:
        ret.append(PluginDescriptor(name='(GSU) ' + _('OScam Information'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main3))
    return ret


def chckMount(path):
    try:
        mounts = open('/proc/mounts')
        lines = mounts.readlines()
        mounts.close()
    except IOError:
        return False
    else:
        for line in lines:
            if line.__contains__(path):
                tmp = line.strip().split(' ')
                if len(tmp) > 1:
                    for i in range(0, len(tmp)):
                        if tmp[i] == path:
                            return True

                else:
                    return True

    return False


def getTunerPiconInfo(service):
    feinfo = service and service.frontendInfo()
    if feinfo is not None:
        frontendData = feinfo and feinfo.getAll(True)
        if frontendData is not None:
            tunerType = str(frontendData.get('tuner_type', _('None')))
            if ENA_TT and tunerType != _('None'):
                try:
                    tunerType = {(iDVBFrontend.feSatellite): '0', (iDVBFrontend.feCable): '1', (iDVBFrontend.feTerrestrial): '2', (iDVBFrontend.feSatellite2): '0', (iDVBFrontend.feTerrestrial2): '2'}[int(tunerType)]
                except:
                    try:
                        tunerType = {(iDVBFrontend.feSatellite): '0', (iDVBFrontend.feCable): '1', (iDVBFrontend.feTerrestrial): '2'}[int(tunerType)]
                    except:
                        pass

            if tunerType in ('DVB-S', 'DVB-S2', '0'):
                numSat = frontendData.get('orbital_position', 0)
                if numSat > 1800:
                    orbPic = str(3600 - numSat) + 'W'
                else:
                    orbPic = str(numSat) + 'E'
                return orbPic
            if tunerType in ('DVB-T', '2'):
                return 'picon_trs'
            if tunerType in ('DVB-C', '1'):
                return 'picon_cable'
            return ''
    return ''


def alternative(serviceName):

    def alternativeChannels(service):
        tmp = eServiceCenter.getInstance().list(eServiceReference(service))
        return tmp and tmp.getContent('S', True)

    if serviceName.startswith('1:134:'):
        channels = alternativeChannels(serviceName)
        if channels:
            return channels[0]
    return serviceName


def listDir(what):
    f = None
    try:
        f = listdir(what)
    except:
        pass

    return f


def realizeNetmount(typeNet, sIp, sDir, destDir, uName, pName, rSize, wSize, notFromF=True):
    if chckMount(destDir):
        if config.plugins.GlassSysUtil.par57.value == '2':
            chck = socket(AF_INET, SOCK_STREAM)
            chck.settimeout(1.0)
            state = False
            try:
                state = not bool(chck.connect_ex((sIp, 80)))
            except:
                pass
            else:
                if not state:
                    system('ifconfig eth0:fakenfs %s netmask 255.255.255.255' % sIp)
                    for x in ['', ' -l']:
                        system('umount -f%s %s' % (x, destDir))
                        state = chckMount(destDir)
                        if not state:
                            break

                    system('ifconfig eth0:fakenfs down')
                    if state:
                        return destDir + ': ' + _('failed to unmount')
        return '%s: %s ' % (typeNet, destDir) + _('is already mounted')
    if not os.path.exists(destDir):
        tmp = destDir.strip().split('/')
        p = ''
        for x in range(0, len(tmp)):
            if tmp[x] != '':
                p += '/' + tmp[x]
                if not os.path.exists(p):
                    system('mkdir ' + p)

    if typeNet == 'CIFS':
        if pName == '':
            system('mount -t cifs -o username=%s //%s%s %s' % (uName, sIp, sDir, destDir))
        else:
            system('mount -t cifs -o username=%s,password=%s //%s%s %s' % (uName, pName, sIp, sDir, destDir))
    elif config.plugins.GlassSysUtil.par59.value:
        system('mount -t nfs %s:%s %s -o %s,noatime,rsize=%s,wsize=%s,nolock,nfsvers=3' % (sIp, sDir, destDir, config.plugins.GlassSysUtil.par82.value, rSize, wSize))
    else:
        system('mount -t nfs -o rsize=%s,wsize=%s %s:%s %s' % (rSize, wSize, sIp, sDir, destDir))
    if chckMount(destDir):
        msg = _('Mount finished correctly')
        if typeNet == 'CIFS':
            if pName == '':
                writeFstab('//%s%s %s cifs username=%s 0 0\n' % (sIp, sDir, destDir, uName))
                if notFromF:
                    writeNCcfg('C: %s %s %s %s' % (sIp, sDir, destDir, uName), sIp, destDir)
            else:
                writeFstab('//%s%s %s cifs username=%s,password=%s 0 0\n' % (sIp, sDir, destDir, uName, pName))
                if notFromF:
                    writeNCcfg('C: %s %s %s %s %s' % (sIp, sDir, destDir, uName, pName), sIp, destDir)
        elif config.plugins.GlassSysUtil.par59.value:
            writeFstab('%s:%s %s nfs %s,noatime,rsize=%s,wsize=%s,nolock,nfsvers=3 1 0\n' % (sIp, sDir, destDir, config.plugins.GlassSysUtil.par82.value, rSize, wSize))
            if notFromF:
                writeNCcfg('N: %s %s %s %s %s %s' % (sIp, sDir, destDir, rSize, wSize, config.plugins.GlassSysUtil.par82.value), sIp, destDir)
        else:
            writeFstab('%s:%s %s nfs rsize=%s,wsize=%s 1 0\n' % (sIp, sDir, destDir, rSize, wSize))
            if notFromF:
                writeNCcfg('N: %s %s %s %s %s' % (sIp, sDir, destDir, rSize, wSize), sIp, destDir)
    else:
        msg = _('Mount failed')
    return typeNet + ': ' + msg


def writeNCcfg(w, ip, destDir):
    ff = '/etc/nfs_cifs.cfg'
    f = ''
    all = ''
    if os.path.isfile(ff):
        try:
            f = open(ff)
        except IOError:
            pass

    if f != '':
        for i in f.readlines():
            if ip not in i and destDir not in i and i != '\n':
                all += i

    all += w + '\n'
    try:
        f = open(ff, 'w')
        f.write(all)
        f.close()
    except IOError:
        pass

    return


def countServers():
    c = o = 0
    cnum = onum = True
    if fileExists('/etc/remote_servers.cfg'):
        try:
            f = open('/etc/remote_servers.cfg', 'r')
            content = f.read()
            f.close()
        except:
            content = ''
        else:
            contentInfo = content.split('\n')
            if content != '':
                for line in contentInfo:
                    if line.__contains__('127.0.0.1'):
                        pass
                    elif line.startswith('C:'):
                        tmp = line.strip().split(' ')
                        if len(tmp) > 2:
                            c += 1
                    elif line.startswith('O:'):
                        tmp = line.strip().split(' ')
                        if len(tmp) > 2:
                            o += 1

    if c > 0:
        cnum = False
    if o > 0:
        onum = False
    return (
     cnum, onum)


def fromFile2():
    ff = '/etc/nfs_cifs.cfg'
    if os.path.isfile(ff):
        msg = _('No CIFS/NFS defined in') + ' ' + ff
        try:
            file = open(ff)
        except IOError:
            file = ''
            msg = _('Error reading the file') + ' ' + ff
        else:
            if file != '':
                msg = ''
                for line in file.readlines():
                    if line.startswith('N:'):
                        line = line.strip().split(' ')
                        if len(line) == 6:
                            config.plugins.GlassSysUtil.par59.setValue(False)
                            msg += realizeNetmount('NFS', line[1], line[2], line[3], 'root', '', line[4], line[5], notFromF=False)
                        elif len(line) == 7:
                            config.plugins.GlassSysUtil.par82.setValue(str(line[6]))
                            config.plugins.GlassSysUtil.par59.setValue(True)
                            msg += realizeNetmount('NFS', line[1], line[2], line[3], 'root', '', line[4], line[5], notFromF=False)
                    elif line.startswith('C:'):
                        line = line.strip().split(' ')
                        if len(line) == 5:
                            msg += realizeNetmount('CIFS', line[1], line[2], line[3], line[4], '', '8192', '8192', notFromF=False)
                        elif len(line) == 6:
                            msg += realizeNetmount('CIFS', line[1], line[2], line[3], line[4], line[5], '8192', '8192', notFromF=False)

    else:
        msg = _('Missing file') + ' ' + ff
    if msg == '':
        msg = _('No CIFS/NFS defined in') + ' ' + ff
    return msg


def oscamRunning(osemu=False):
    try:
        for pid in os.listdir('/proc'):
            if pid.isdigit():
                try:
                    with open('/proc/%s/comm' % pid) as handle:
                        name = handle.read().strip().lower()
                    if (osemu and name.startswith('osemu')) or (not osemu and name.startswith('oscam')):
                        return True
                except OSError:
                    continue
    except OSError:
        pass
    return False


def resPicon(sname, path):
    pngname = findPicon(sname, path)
    if pngname == '' and path == 'picon' and len(sname) > 11:
        if sname.startswith('4097'):
            tmp = sname.split('_')
            tmp[0] = '1'
            sname = ('_').join(tmp)
            pngname = findPicon(sname, path)
        if pngname == '':
            pngname = findPicon(sname[:-10] + '0000_0_0_0', path)
            if pngname == '':
                tmp = sname.split('_')
                for i in ('1', '19', '16'):
                    if i != tmp[2]:
                        tmp[2] = i
                        sname = ('_').join(tmp)
                        pngname = findPicon(sname[:-10] + '0000_0_0_0', path)
                        if pngname != '':
                            break

    if pngname == '':
        pngname = findPicon('picon_default', path)
        if pngname == '':
            tmp = resolveFilename(SCOPE_CURRENT_SKIN, 'picon_default.png')
            if fileExists(tmp):
                pngname = tmp
            else:
                pngname = '/usr/share/enigma2/skin_default/picon_default.png'
    return pngname


def getServiceInfoValue(info, what, ref=None):
    v = ref and info.getInfo(ref, what) or info.getInfo(what)
    if v != iServiceInformation.resIsString:
        return 'N/A'
    return ref and info.getInfoString(ref, what) or info.getInfoString(what)


def findPicon(piconName, path1):
    pngname = None
    if FHD == 1:
        try:
            pngname = '%s/%s/%s.png' % (config.plugins.setupGlass16.par39.value, path1, piconName)
        except:
            pass

    elif FHD == 1.5:
        try:
            pngname = '%s/%s/%s.png' % (config.plugins.setupGlass17.par39.value, path1, piconName)
        except:
            pass

    else:
        try:
            pngname = '%s/%s/%s.png' % (config.plugins.setupGlass18.par39.value, path1, piconName)
        except:
            pass

    if pngname and fileExists(pngname):
        return pngname
    else:
        searchPaths = ('/usr/share/enigma2/%s/', '/media/usb/%s/', '/media/ba/%s/',
                       '/media/cf/%s/', '/media/hdd/%s/', '/media/sd/%s/', '/media/sda1/%s/',
                       '/media/sda/%s/')
        for path in searchPaths:
            pngname = path % path1 + piconName + '.png'
            if fileExists(pngname):
                return pngname

        return ''


def chckFtp():
    ena = _('"FTP server" is unavailable yet, check your internet connection or firewall settings')
    for x in FTP_ALL:
        try:
            ftp = ftplib.FTP(x[0])
            ftp.login(x[1], x[2])
            ftp.quit()
            ena = ''
        except:
            pass

        if ena == '':
            break

    return (
     ena, x)


def readURL():
    url = 'http://127.0.0.1:16001'
    username = None
    password = None
    try:
        f = open('/var/etc/CCcam.cfg', 'r')
        for line in f.readlines():
            if line.startswith('WEBINFO LISTEN PORT :'):
                tmp = line.split(':')
                port = tmp[1].replace('\n', '').replace('\r', '').replace(' ', '')
                if port != '':
                    url = url.replace('16001', port)
            elif line.startswith('WEBINFO USERNAME :'):
                tmp = line.split(':')
                username = tmp[1].replace('\n', '').replace('\r', '').replace(' ', '')
            elif line.startswith('WEBINFO PASSWORD :'):
                tmp = line.split(':')
                password = tmp[1].replace('\n', '').replace('\r', '').replace(' ', '')

        f.close()
    except:
        pass

    if username is not None and password is not None and username != '' and password != '':
        url = url.replace('http://', 'http://%s:%s@' % (username, password))
    return url


def Rst_E2(answer):
    if answer:
        try:
            quitMainloop(3)
        except:
            if ENA_D:
                system('systemctl restart enigma2')
            else:
                system('killall -9 enigma2')

    return


def providerCount(url):
    if url.__contains__('127.0.0.1'):
        url = readURL()
    try:
        file = urllibXX.urlopen(url + '/providers')
    except:
        file = ''

    if file == '':
        return -1
    firstLine = True
    count = 0
    for line in file.readlines():
        if line.startswith('|'):
            if firstLine:
                firstLine = False
            else:
                count = count + 1

    return count


def parseEcmInfoLine(line, what=':'):
    if line.__contains__(what):
        line = line.split(what)[1]
        line = line.replace('\n', '')
        return (' ').join(line.strip().split())
    else:
        return ''
    return


def ECMparser(cl=21):

    def chckIdx(what):
        if 'X' in what:
            idx = what.index('X')
            what = what[idx + 1:]
        return what

    def cutMe(c):
        c = c.replace('\n', '')
        if len(c) > cl:
            if c[-1] == ')':
                c = '%s..)' % c[:cl]
            else:
                c = '%s..' % c[:cl]
        return c + '\n'

    def setEcmTime(t):
        t = t.strip()
        if '.' not in t:
            if len(t) == 4:
                t = '%s.%s' % (t[0], t[1:])
            elif t.isdigit():
                t = '0.%003d' % int(t)
        return t + '\n'

    def fixCW(t):
        t = t.strip()
        if t[2] != ' ':
            b = ''
            for i in range(0, len(t), 2):
                b += t[i:i + 2] + ' '

            return b.strip()[:24]
        else:
            return t
        return

    try:
        tmp = open('/tmp/ecm.info', 'r')
        content = tmp.read()
        tmp.close
    except:
        content = ''

    lines = content.split('\n')
    config.plugins.GlassSysUtil.par83.value = ''
    system = caid = provider = pid = using = adress = hops = share = ecmTime = typecam = provid = dcw0 = dcw1 = chid = '..............\n'
    coding = '..............'
    oscVersion = '\n'
    doscam = ''
    if content != '':
        typcm = False
        for line in lines:
            if 'chid:' in line.lower():
                if ', chid:' in line:
                    chid = line.split('chid:')[1]
                    if ',' in chid:
                        chid = chid.split(',')[0]
                else:
                    chid = line.split(':')[1]
                chid = chckIdx(chid.upper()) + '\n'
            if line.startswith('CW0:') or line.startswith('cw0:'):
                dcw0 = fixCW(line.split(':')[1]) + '\n'
            elif line.startswith('CW1') or line.startswith('cw1:'):
                dcw1 = fixCW(line.split(':')[1]) + '\n'
            if line.startswith('Service:'):
                typecam = 'Wicardd\n'
            elif line.startswith('=====') and typecam == '..............\n':
                typecam = 'Mgcamd\n'
                typcm = True
            elif typecam == '..............\n':
                typecam = 'CCcam\n'
            elif typecam == 'CCcam\n' and line.startswith('reader:'):
                typecam = 'OScam\n'
            elif typecam == 'CCcam\n' and line.startswith('FROM:'):
                typecam = 'Camd3\n'
            if line.startswith('system:') or line.startswith('===='):
                if line.startswith('===='):
                    system = str(line.split(' ')[1].split())
                    system = system[2:-2] + ' ECM' + '\n'
                else:
                    system = parseEcmInfoLine(line) + '\n'
                system = cutMe(system)
            if line.startswith('caid:') or line.startswith('====') or line.startswith('CAID ') or line.startswith('CAID:'):
                if line.startswith('===='):
                    caid = str(parseEcmInfoLine(line, 'CaID')).upper()
                    caid = chckIdx(caid)
                    caid = caid[:4] + '\n'
                elif line.startswith('CAID'):
                    caid = str(line.split(' ')[1].split())
                    caid = caid[2:-2]
                    caid = chckIdx(caid.upper())
                    caid = caid[:4] + '\n'
                else:
                    caid = str(parseEcmInfoLine(line)).upper()
                    caid = chckIdx(caid)
                    if len(caid) == 3:
                        caid = '0%s' % caid
                    caid = caid + '\n'
                if caid.startswith('18'):
                    coding = 'Nagravision'
                elif caid in ('1702\n', '1722\n', '1762\n'):
                    coding = 'Betacrypt'
                elif caid.startswith('01'):
                    coding = 'Seca'
                elif caid.startswith('06'):
                    coding = 'Irdeto'
                elif caid.startswith('07'):
                    coding = 'DigiCipher'
                elif caid.startswith('22'):
                    coding = 'Codicrypt'
                elif caid.startswith('A1'):
                    coding = 'Rosscrypt'
                elif caid.startswith('05'):
                    coding = 'Viaccess'
                elif caid.startswith('0B'):
                    coding = 'Conax'
                elif caid.startswith('0D'):
                    coding = 'Cryptoworks'
                elif caid in ('4AE1\n', '4AE0\n'):
                    coding = 'DRE-crypt'
                elif caid == '4ABF\n':
                    coding = 'DGCrypt'
                elif caid == '4AEE\n':
                    coding = 'Bulcrypt'
                elif caid in ('4AD1\n', '4AD0\n'):
                    coding = 'XCrypt'
                elif caid == '4AFC\n':
                    coding = 'Panaccess'
                elif caid == '4A70\n':
                    coding = 'Dreamcrypt'
                elif caid in ('4AEA\n4B24\n', ):
                    coding = 'CryptoGuard'
                elif caid == '4B63\n':
                    coding = 'RedCrypter'
                elif caid == '4B64\n':
                    coding = 'TVkey'
                elif caid == '4AF4\n':
                    coding = 'MDC'
                elif caid == '4347\n':
                    coding = 'CryptOn'
                elif caid.startswith('09'):
                    coding = 'Videoguard'
                elif caid.startswith('55'):
                    if caid == '5581\n':
                        coding = 'Bulcrypt'
                    else:
                        coding = 'Griffin'
                elif caid.startswith('26'):
                    coding = 'Biss'
                elif caid.startswith('56') or caid.startswith('17'):
                    coding = 'Verimatrix'
                elif caid == '2710\n':
                    coding = 'Exset'
                elif caid.startswith('1010'):
                    coding = 'Tandberg'
                elif caid.startswith('0E'):
                    coding = 'PowerVU'
                elif caid == 'FFFF\n':
                    coding = 'Constant-CW'
                else:
                    coding = 'Unknown'
            if line.startswith('provid:') or line.startswith('CAID ') or line.startswith('SysID'):
                if line.startswith('CAID '):
                    provid = str(line.split(' ')[5].split())
                    provid = provid[2:-2]
                    provid = chckIdx(provid.upper())
                    provid += '\n'
                elif line.startswith('SysID'):
                    provid = str(line.split(' ')[1].split())
                    provid = provid[2:-2]
                    provid = provid.upper() + '\n'
                else:
                    provid = parseEcmInfoLine(line)
                    provid = provid.upper()
                    provid = provid[2:] + '\n'
            elif line.startswith('provider:') or line.startswith('prov: ') or line.startswith('Provider:'):
                provider = parseEcmInfoLine(line) + '\n'
                if provider.__contains__('key:'):
                    idx = provider.index('key:')
                    provider = provider[:idx] + '\n'
                if provider.__contains__(','):
                    idx = provider.index(',')
                    provider = provider[:idx] + '\n'
                if provider.__contains__('0X') or provider.__contains__('0x'):
                    provider = chckIdx(provider.upper())
                provider = cutMe(provider)
            if line.startswith('pid:') or line.startswith('====') or line.startswith('CAID '):
                if line.startswith('===='):
                    pid = str(line.split(' ')[7].split())
                    pid = pid.replace(',', '')
                    pid = pid[2:-2]
                elif line.startswith('CAID '):
                    pid = str(line.split(' ')[3].split())
                    pid = pid[2:-3]
                else:
                    pid = parseEcmInfoLine(line)
                pid = chckIdx(pid.upper())
                if len(pid) == 2:
                    pid = '00%s' % pid
                if len(pid) == 3:
                    pid = '0%s' % pid
                pid += '\n'
            if line.startswith('using:') or line.startswith('source:') or line.startswith('reader:') or line.startswith('decode:'):
                if line.startswith('source:'):
                    using = str(line.split(' ')[1].split())
                    using = using[2:-2] + '\n'
                elif line.startswith('decode:'):
                    if typcm:
                        typecam = 'Mgcamd\n'
                    else:
                        typecam = 'Gbox\n'
                    if line.__contains__('slot') or line.__contains__('Local'):
                        using = 'Cardreader\n'
                    elif line.__contains__('Internal'):
                        using = 'Emu\n'
                        typecam = 'Gbox\n'
                    elif line.__contains__('com'):
                        using = parseEcmInfoLine(line) + '\n'
                    else:
                        using = 'Network\n'
                else:
                    using = parseEcmInfoLine(line) + '\n'
                    if using == 'sci\n':
                        using = 'Cardreader\n'
                using = cutMe(using)
            if line.startswith('address:') or line.startswith('source:') or line.startswith('from:') or line.startswith('FROM:') or line.startswith('decode:'):
                if line.startswith('source: net'):
                    idex = line.index('(')
                    adress = line[idex:]
                    adress = adress.replace('\n', '')
                    adress = str(adress.split(' ')[2].split())
                    adress = adress[2:-3] + '\n'
                elif line.startswith('source: emu') or line.startswith('decode:'):
                    adress = '..............\n'
                    if line.startswith('decode:') and not using.__contains__('com'):
                        adress = parseEcmInfoLine(line) + '\n'
                else:
                    adress = parseEcmInfoLine(line) + '\n'
                    if adress == '/dev/sci0\n':
                        if 'dm800se' in HardwareInfo().get_device_name():
                            adress = 'Upper slot \n'
                        else:
                            adress = 'Lower slot \n'
                    elif adress == '/dev/sci1\n':
                        if 'dm800se' in HardwareInfo().get_device_name():
                            adress = 'Lower slot \n'
                        else:
                            adress = 'Upper slot \n'
                    elif adress.__contains__('local'):
                        adress = 'Local slot\n'
                    elif coding == 'Unknown':
                        adress = '..............\n'
                adress = cutMe(adress)
            elif line.startswith('hops:'):
                hops = parseEcmInfoLine(line) + '\n'
            elif line.startswith('prov:') and 'dist:' in line and ',' in line:
                l = ''
                for ii in line.split(','):
                    if 'prov:' in ii:
                        provid = chckIdx(parseEcmInfoLine(ii).upper()) + '\n'
                    if 'dist:' in ii:
                        hops = parseEcmInfoLine(ii)
                    if 'slot:' in ii:
                        l += ', Slot: ' + parseEcmInfoLine(ii)
                    if 'level:' in ii:
                        l += ', Level: ' + parseEcmInfoLine(ii)

                if '\n' not in hops:
                    hops += l + '\n'
            if line.startswith('share:') or line.startswith('source:'):
                if line.startswith('source: net'):
                    idex = line.index('(')
                    share = line[idex:]
                    share = share.replace('\n', '')
                    share = share.split(' ')[0].strip()
                    share = share[3:-2] + '\n'
                elif line.startswith('source: emu'):
                    share = '..............\n'
                else:
                    share = parseEcmInfoLine(line) + '\n'
                share = cutMe(share)
            elif line.startswith('response:') or line.startswith('ecm time:') or line.startswith('Time:(') or line.startswith('Time: (') or line.startswith('1') or line.startswith('2') or line.startswith('3') or line.startswith('4') or line.startswith('5') or line.startswith('6') or line.startswith('7') or line.startswith('8') or line.startswith('9'):
                if line.startswith('ecm time:') or line.startswith('response:'):
                    ecmTime = parseEcmInfoLine(line)
                elif line.startswith('Time:(') or line.startswith('Time: ('):
                    ecmTime = line.split('(')[1].strip()
                    if ' ' in ecmTime:
                        ecmTime = ecmTime.split(' ')[0].strip()
                    if ')' in ecmTime:
                        ecmTime = ecmTime.split(')')[0].strip()
                else:
                    ecmTime = line.split(' ')[0].strip()
            elif line.startswith('response time:'):
                ecmTime = line.strip().split('e:')[1]
                if '(' in ecmTime:
                    adress = cutMe(ecmTime.strip().split('(')[1].replace(')', '').replace('\n', ''))
                    typeCAviaCam2 = 'net'
                    using = cutMe(ecmTime.strip().split('(')[0].strip().split('decoded by')[1][1:])
                else:
                    using = cutMe(ecmTime.strip().split('decoded by')[1][1:])
                    if 'funcard' in using.lower() or 'goldcard' in using.lower():
                        typeCAviaCam2 = 'emu'
                    elif 'upper' in using.lower() or 'lower' in using.lower():
                        typeCAviaCam2 = 'crd'
                ecmTime = ecmTime.strip().split('ms')[0]
            if line.startswith('Signature OK') and typecam == 'CCcam\n':
                typecam = 'Mgcamd\n'
            if (line.startswith('Time:(') or line.startswith('Time: (')) and typecam == 'Mgcamd\n':
                typecam = 'Mbox\n'

        if typecam != 'OScam\n':
            try:
                ax = typecam
                from os import popen
                for f in popen('ps -ef').readlines():
                    f = f.upper()
                    if f.find('OSCAM') != -1:
                        typecam = 'OScam\n'
                        break
                    elif f.find('GCAM') != -1 and f.find('MGCAMD') == -1:
                        typecam = 'Gcam\n'
                        break
                    elif f.find('NCAM') != -1:
                        typecam = 'Ncam\n'
                        break

                if ax == typecam:
                    for f in popen('ps').readlines():
                        f = f.upper()
                        if f.find('OSCAM') != -1:
                            typecam = 'OScam\n'
                            break
                        elif f.find('GCAM') != -1 and f.find('MGCAMD') == -1:
                            typecam = 'Gcam\n'
                            break
                        elif f.find('NCAM') != -1:
                            typecam = 'Ncam\n'
                            break

            except:
                pass

        if typecam == 'Gbox\n' and using == 'Network\n':
            try:
                f = open('/tmp/share.info', 'r')
                for l in f.readlines():
                    l = l.replace('\n', '').strip().split(' ')
                    if len(l) == 10:
                        if provider[:-1] == parseEcmInfoLine(l[9]) and l[5].startswith(caid[:-1]):
                            adress = l[3] + '\n'
                            adress = cutMe(adress)
                            hops = '%s, %s, %s\n' % (l[6], l[7], l[8])
                            share = '%s, %s\n' % (l[5], l[9])
                            break

                f.close()
            except:
                pass

        elif typecam in ('OScam\n', 'Ncam\n', 'Gcam\n') and (os.path.isfile(GCM) or os.path.isfile(NCM) or os.path.isfile('/tmp/oscam.version') or os.path.isfile('/tmp/.oscam/oscam.version') or os.path.isfile(DSC)):
            oscfile = '/tmp/.oscam/oscam.version'
            if os.path.isfile('/tmp/oscam.version'):
                oscfile = '/tmp/oscam.version'
            ax = 0
            for xi in (DSC, NCM, oscfile, GCM):
                if os.path.isfile(xi):
                    l = os.stat(xi).st_mtime
                    if l > ax:
                        ax = l
                        oscfile = xi

            if 'ncam' in oscfile:
                typecam = 'Ncam\n'
            elif 'gcam' in oscfile:
                typecam = 'Gcam\n'
            try:
                f = open(oscfile, 'r')
                for l in f.readlines():
                    if l.startswith('Version:'):
                        if 'Rev.' in l:
                            if 'ymod' in l:
                                oscVersion = ' (ymod' + l.replace('\n', '').split('ymod')[1].split(' ')[0] + ')\n'
                            else:
                                idx = l.index('Rev.')
                                oscVersion = ' (' + l[idx + 4:].replace('\n', '').strip() + ')\n'
                        elif '-r' in l:
                            idx = l.index('-r')
                            oscVersion = ' (' + l[idx + 2:].replace('\n', '').strip() + ')\n'
                        if '(0)' in oscVersion:
                            idx = l.index('ymodv')
                            oscVersion = ' (' + l[idx + 5:].replace('\n', '').replace('Rev. 0', '').strip() + ')\n'
                        elif 'emu' in oscVersion:
                            oscVersion = oscVersion.replace('-r16-GS', '')
                        elif 'DOSC' in l:
                            idx = l.index('DOSC')
                            oscVersion = ' (' + l[idx + 7:].replace('\n', '').strip() + ')\n'
                            doscam = 'D'
                        if '(' not in oscVersion:
                            oscVersion = ' (' + l.split('Version:')[1].replace('ncam-', '').replace('gcam-', '').replace('\n', '').strip() + ')\n'
                        break

                f.close()
                oscVersion = cutMe('xxxxxxx' + oscVersion).replace('xxxxxxx', '')
            except:
                pass

        elif typecam == 'CCcam\n' and ecmTime == '..............\n' and adress == '..............\n':
            typecam = 'Scam\n'
        if provider == 'Unknown\n':
            provider = '..............\n'
        if ecmTime != '..............\n':
            ecmTime = setEcmTime(ecmTime)
        if chid != '..............\n':
            if provider == '..............\n':
                provider = chid
                config.plugins.GlassSysUtil.par83.value = 'Provider:'
            elif provid == '..............\n':
                provid = chid
                config.plugins.GlassSysUtil.par83.value = 'ProvID:'
    return (
     oscVersion, doscam + typecam, system, caid, provider, provid, pid, using, adress, hops, share, ecmTime, coding, dcw0, dcw1)


class ListboxSys(MenuList):

    def __init__(self, list, enableWrapAround=False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('priveG', fhd(18)))
        self.l.setFont(1, gFont('priveG', fhd(20)))
        self.l.setItemHeight(fhd(40))
        return


class ListboxSys2(MenuList):

    def __init__(self, list, enableWrapAround=False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('priveG', fhd(18)))
        self.l.setFont(1, gFont('priveG', fhd(15)))
        self.l.setItemHeight(fhd(25))
        return


class ListboxSys3(MenuList):

    def __init__(self, list, enableWrapAround=False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('priveG', fhd(26)))
        self.l.setFont(1, gFont('priveG', fhd(16)))
        self.l.setItemHeight(fhd(80))
        return


class ftp_center(Screen):

    def __init__(self, session, wFtp):
        self.skin = ftpScr
        Screen.__init__(self, session)
        self.list = []
        self.wFtp = wFtp
        dev = 'x'
        try:
            for x in ('boxtype', 'vumodel', 'model'):
                if os.path.exists('/proc/stb/info/' + x):
                    dev = open('/proc/stb/info/' + x, 'r').read().strip()
                    dev = dev.lower()
                    break

        except:
            pass

        a = ''
        if XCPU == 'arm' and ('dm9' in dev or 'duo4k' in dev):
            a = '-9x'
        self.typeProc = XCPU + a
        self['list'] = ListboxSys2(self.list)
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.doSelection), 
           'ok': (self.doSelection), 
           'red': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit), 
           'back': (self.exit)})
        self.arch = self.typeProc in ('arm', 'mips32el', 'aarch64', 'arm-9x')
        self.onLayoutFinish.append(self.updatemenulist)
        return

    def readType(self, tmp):
        tmp = tmp.strip().split('-', 1)[1]
        for x in ['cam.', 'srv.', '.ipk', '.deb', '_all', '_sh4', '_mipsel', '_1.01', 
         '_1.00']:
            tmp = tmp.replace(x, '')

        tmp = tmp.replace('oscamemu', 'oscam Ymod 18t')
        if not tmp.startswith('os'):
            for x in ['amd', 'cam', 'ox', 'dd', 'cs']:
                if x in tmp:
                    tt = tmp.strip().split(x)
                    tmp = '%s%s ver.%s' % (tt[0], x, tt[1])
                    break

        elif tmp.startswith('oscam_') or tmp.startswith('osemu_'):
            tmp = tmp.replace('oscam_', 'oscam rev.').replace('osemu_', 'osEmu ver.').replace('.40', ' PLi 4').replace('.23', ' EMU OE 2.0')
            tmp = tmp.replace('.16', ' OE 1.6').replace('.20', ' OE 2.0').replace('.43', ' EMU PLi 4').replace('.17', ' EMU OE 1.6')
            tmp = tmp.replace('.70', ' FPU OE 2.0').replace('.73', ' EMU FPU OE 2.0').replace('.22', ' OE 2.2')
            tmp = tmp.replace('.50', ' ARM').replace('.53', ' EMU ARM').replace('.90', ' ARM2').replace('.93', ' EMU ARM2')
            tmp = tmp.replace('.30', ' AARCH64').replace('.33', ' EMU AARCH64')
        if ENA_D and 'OE 2.0' in tmp:
            tmp = tmp.replace('OE 2.0', 'OE 2.2')
        return (tmp[0].upper() + tmp[1:]).replace('_', '')

    def exit(self):
        self.close('1')
        return

    def updatemenulist(self):
        filenames = []
        try:
            tt = True
            ftp = ftplib.FTP(self.wFtp[0])
            ftp.login(self.wFtp[1], self.wFtp[2])
            data = []
            if ENA_D and self.arch:
                ftp.cwd(TYPE_DIR)
            ftp.cwd(self.typeProc)
            ftp.dir(data.append)
            for line in data:
                tmp = re.sub('\\s+', '*', line)
                tmp = tmp.strip().split('*')
                if len(tmp) > 8:
                    if '.php' not in line and tmp[8] != '.' and tmp[8] != '..' and ':' in line:
                        idx = line.index(':')
                        zzz = line[idx + 4:]
                        filenames.append(zzz)

            ftp.quit()
        except:
            tt = False

        self.list = []
        if len(filenames) != 0:
            for x in range(0, len(filenames)):
                txt = str(filenames[x])
                item = [txt]
                led = 'green'
                if '-srv.' in txt:
                    led = 'blue'
                elif '-cam.' in txt:
                    led = 'yellow'
                if self.typeProc != 'settings':
                    txt = self.readType(txt)
                item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(600), fhd(25)), font=0, text=txt))
                pix = LoadPixmap(BP_ICO % led)
                item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                self.list.append(item)

        else:
            item = [
             '*']
            if tt:
                item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(600), fhd(25)), font=0, text=_('No files detected')))
            else:
                item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(600), fhd(25)), font=0, text=str(msg)))
            pix = LoadPixmap(BP_ICO % 'red')
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)
        self['list'].l.setList(self.list)
        return

    def doSelection(self):
        selectedItem = self['list'].getCurrent()[0]
        filename = str(selectedItem)
        if filename == '*':
            return
        if 'oscam' in filename and oscamRunning() and not ('doscam' in filename or 'oscamemu' in filename) or 'osemu' in filename and oscamRunning(True):
            self.session.open(MessageBox, _('Before update OScam/OSEmu version, please, stop OScam/OSEmu'), MessageBox.TYPE_ERROR, 5)
            return
        state = False
        try:
            ftp = ftplib.FTP(self.wFtp[0])
            ftp.login(self.wFtp[1], self.wFtp[2])
            if ENA_D and self.arch:
                ftp.cwd(TYPE_DIR)
            ftp.cwd(self.typeProc)
            ftp.retrbinary('RETR ' + filename, open('/tmp/' + filename, 'wb').write)
            state = True
            ftp.quit()
        except:
            pass

        if state and self.typeProc != 'settings':
            if ENA_D:
                cmd = PKGBIN % filename
            else:
                cmd = '%spkg install --force-overwrite --force-downgrade /tmp/%s' % (PKGBIN, filename)
            self.IPKfilename = filename
            self.session.openWithCallback(self.cmdAnsw, Console, title=_('Installing package') + ': %s' % self.IPKfilename, cmdlist=[cmd])
        elif state:
            self.session.open(MessageBox, filename + ' ' + _('was downloaded successfully into /tmp'), MessageBox.TYPE_INFO, 5)
        else:
            self.session.open(MessageBox, _('Error while downloading file') + ': ' + str(msg), MessageBox.TYPE_ERROR, 5)
        return

    def cmdAnsw(self):
        system('rm -rf /tmp/' + self.IPKfilename)
        return


class settings_satxml(Screen):

    def __init__(self, session):
        self.skin = settings_menu
        Screen.__init__(self, session)
        self.list = []
        self.menuListAll = [
         (
          '0', _('Update without satellites.xml'), 'yellow', _('Update channel settings from /tmp without update satellites.xml')),
         (
          '1', _('Update'), 'white', _('Update channel settings and satellites.xml (included in settings) from /tmp'))]
        self['list'] = ListboxSys(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['info'] = Label('')
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['SetupActions', 'WizardActions', 'ColorActions'], {'green': (self.doSelection), 
           'ok': (self.doSelection), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.updatemenulist)
        return

    def updatemenulist(self):
        self.list = []
        for x in self.menuListAll:
            item = [
             x[0]]
            item.append(MultiContentEntryText(pos=(fhd(25), fhd(7)), size=(fhd(600), fhd(26)), font=1, text=x[1]))
            pix = LoadPixmap(BP_ICO % x[2])
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(12)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)

        self['list'].l.setList(self.list)
        self.setTitle(_('Channel Settings'))
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            tmp2 = int(selection[0])
            tmp = str(self.menuListAll[tmp2][3])
            self['info'].setText(tmp)
        return

    def doSelection(self):
        selectedItem = self['list'].getCurrent()[0]
        if selectedItem == '0':
            self.session.open(settings_center)
        elif selectedItem == '1':
            self.session.open(settings_center, True)
        return


class settings_center(Screen):

    def __init__(self, session, rmSat=False, whereSrc=True):
        self.skin = settings_center_scr
        Screen.__init__(self, session)
        self.list = []
        self.rmSat = rmSat
        self.whereSrc = whereSrc
        self['list'] = ListboxSys2(self.list)
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.updateList)
        return

    def selectedmenuitem(self):
        self.zipFile = self['list'].getCurrent()[0]
        self.zipFileOS = self.zipFile.replace(' ', '\\ ')
        self.zipFileOS = self.zipFileOS[:-4]
        isOK = False
        if self.zipFile != 'None':
            if '.zip' in self.zipFile:
                system('unzip /tmp/%s -d /tmp' % self.zipFileOS)
            else:
                system('%s x /tmp/%s.rar /tmp' % (_gsu_helper('unrar_bin'),self.zipFileOS))
            self.zipFile = self.zipFile[:-4]
            num = 0
            userTv = userRadio = True
            f = listDir('/tmp/%s' % self.zipFile)
            if f:
                for tmp in f:
                    if tmp == 'blacklist' or tmp == 'whitelist' or tmp == 'satellites.xml' or tmp == 'lamedb' or tmp == 'bouquets.radio' or tmp == 'bouquets.tv':
                        num += 1
                    elif userTv and '.tv' in tmp:
                        userTv = False
                    elif userRadio and '.radio' in tmp:
                        userRadio = False

                if num == 6 and not userTv and not userRadio:
                    x = self.removeSetting()
                    for tmp in f:
                        if tmp == 'satellites.xml' and self.rmSat:
                            system('cp -f /tmp/' + self.zipFileOS + '/' + tmp + ' /etc/tuxbox/satellites.xml')
                        system('cp -f /tmp/' + self.zipFileOS + '/' + tmp + ' /etc/enigma2/' + tmp)

                    self.session.openWithCallback(self.restartAnswer, MessageBox, _('Settings successfully loaded, do you want restart E2 to activate settings?'), MessageBox.TYPE_YESNO)
                    isOK = True
            if not isOK:
                self.session.open(MessageBox, _('Incorrect files detected'), MessageBox.TYPE_ERROR, 4)
            self.removeZip()
        return

    def updateList(self):
        if self.whereSrc:
            del self.list[:]
            f = listDir('/tmp')
            if f:
                for i in ('.zip', '.rar'):
                    for x in f:
                        if i in x:
                            item = [
                             x]
                            item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=x))
                            self.list.append(item)

        if len(self.list) == 0:
            item = [
             'None']
            item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=_('No ZIP/RAR Files Found')))
            self.list.append(item)
        self['list'].l.setList(self.list)
        self.setTitle(_('Channel Settings'))
        return

    def restartAnswer(self, answer):
        Rst_E2(answer)
        return

    def removeSetting(self):
        if self.rmSat:
            system('rm -rf /etc/tuxbox/satellites.xml')
        for x in ('whitelist', 'whitelist_bak', 'whitelist_org', 'blacklist', 'blacklist_bak',
                  'blacklist_org', 'lamedb_org', 'lamedb_bak', 'lamedb', '*.tv',
                  '*.tv_bak', '*.tv_org', '*.radio', '*.radio_bak', '*.radio_org'):
            system('rm -rf /etc/enigma2/' + x)

        return True

    def removeZip(self):
        system('rm -rf /tmp/' + self.zipFileOS + '.zip')
        system('rm -rf /tmp/' + self.zipFileOS + '.rar')
        system('rm -rf /tmp/' + self.zipFileOS + '/*')
        system('rmdir /tmp/' + self.zipFileOS)
        self.updateList()
        return


class SysUtilMngMain(Screen):
    size = getDesktop(0).size().width()
    if size >= 1280:
        skin = ok_plugin
    else:
        skin = no_plugin

    def __init__(self, session):
        self.skin = SysUtilMngMain.skin
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.menuListAll = [
         (
          '0', _('System Information'), _('Displaying system info: temperature, used/available space on connected devices, etc.')),
         (
          '1', _('Channel Information'), _('Displaying channel info: transporder info, ECM info (if the channel is coded), etc.')),
         (
          '2', _('CCcam Information'), _('Management remote servers or local CCcam server. This item is enabled if CCcam is running or min 1 remote servers defined in /etc/remote_servers.cfg')),
         (
          '3', _('OScam Information'), _('Management remote servers or local OScam server. This item is enabled if OScam is running or min 1 remote servers defined in /etc/remote_servers.cfg')),
         (
          '4', _('Mbox Information'), _('Displaying Mbox info, local Cam only')),
         (
          '5', _('IPK/DEB and User Scripts'), _('Install or uninstall IPK, DEB, GZ, BZ2 files placed in /tmp or start user scripts')),
         (
          '6', _('ECM Information'), _('All about ECM info - will be available only if ecm.info file is generated')),
         (
          '7', _('CAM/SRV Manager'), _('Start, stop, restart, download, unistall CAM/SRV or set start cfg of OScam')),
         (
          '8', _('OSD ECM Information'), _('Enable/Disable OSD ECM Info, will be showed in top - right (default) of TV screen, show changes in ECM info only')),
         (
          '9', _('Swap Management'), _('Create,remove and show single/multi swap on mapped devices on your hw')),
         (
          '10', _('Channel Settings'), _('Update channel settings from /tmp (ZIP/RAR package)')),
         (
          '11', _('Devices Manager'), _('Management (format, mount, unmount) HDD, USB devices and autodetecting and managing (delete, create) of the partitions')),
         (
          '12', _('AutoInstall'), _('Enable/disable AutoInstall, define source dir, install all files from source dir, view status')),
         (
          '13', _('Crond Management'), _('Enable/disable Crond, add/delete commands(scripts) into crontabs')),
         (
          '14', _('Text Editor'), _('Editing text file, supported files are: txt, conf, py, cfg, cw, sh, xml, dvbapi, keys, key, server, services, provid, users, tiers. Limited size of file is 50kB')),
         (
          '15', _('Reset root user password'), _('Reset root user password') + '\n' + _('Password') + ': ' + _('None'))]
        self.status = {}
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['info'] = Label('')
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['yellow'] = Label(_('Menu'))
        self['blue'] = Label('')
        self['actions'] = ActionMap(['SetupActions', 'ColorActions', 'GlobalActions', 'WizardActions', 'MenuActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.close), 
           'yellow': (self.cfgGsu), 
           'blue': (self.updatechckact), 
           'back': (self.close), 
           'menu': (self.cfgGsu)})
        self.size = getDesktop(0).size().width()
        self.onLayoutFinish.append(self.updatemenulist)
        return

    def resetRootPass(self, a):
        if not a:
            return
        self._container = eConsoleAppContainer()
        if ENA_D:
            self.__appClosed_conn = self._container.appClosed.connect(self._commandFinished)
        else:
            self.__appClosed_conn = self._container.appClosed.append(self._commandFinished)
        ret = self._container.execute('passwd -d root')
        if ret == 0:
            msg = _('Successfully changed password for root user to: None')
        else:
            msg = _('Unable to reset password for root user')
        self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, 10)
        return

    def _commandFinished(self, retval):
        if ENA_D:
            try:
                del self._container
            except:
                pass

        else:
            try:
                del self._container.dataAvail[:]
                del self._container.appClosed[:]
                del self._container
            except:
                pass

        self.__appClosed_conn = None
        return

    def selectedmenuitem(self):
        if self.size < 1280:
            self.close()
        selectedItem = self['list'].getCurrent()[0]
        enabledItem = self.status.get(selectedItem)
        if enabledItem:
            if selectedItem == '0':
                self.session.open(GlassSysInfoBrowser)
            elif selectedItem == '1':
                self.session.open(channelInfoCenter)
            elif selectedItem == '2':
                if self.enaNonLocal:
                    self.session.open(cccamInfo)
                else:
                    self.session.open(cccamInfoChoiceServer)
            elif selectedItem == '3':
                if self.enaNonLocalOscam:
                    self.session.open(oscamInfo)
                else:
                    self.session.open(oscamInfoChoiceServer)
            elif selectedItem == '4':
                self.session.open(mboxInfo)
            elif selectedItem == '5':
                self.session.open(ipk_script_center)
            elif selectedItem == '7':
                self.session.open(univCamMng)
            elif selectedItem == '6':
                self.session.open(ECMInfo)
            elif selectedItem == '8':
                self.session.open(OSD_ECM_Menu)
            elif selectedItem == '9':
                self.session.open(swap_manager)
            elif selectedItem == '10':
                self.session.open(settings_satxml)
            elif selectedItem == '11':
                self.session.open(devMngMain)
            elif selectedItem == '12':
                self.session.open(autoInstallMain)
            elif selectedItem == '13':
                self.session.open(cronMng)
            elif selectedItem == '14':
                self.session.open(dirBrowser, '/', True)
            elif selectedItem == '15':
                self.session.openWithCallback(self.resetRootPass, MessageBox, _('Do you really want to reset password for user root?'), MessageBox.TYPE_YESNO, default=False)
        return

    def updatemenulist(self):
        self.setWindowTitle(_('GSU ver.') + ' ' + self.readVersion())
        (self.enaNonLocal, self.enaNonLocalOscam) = countServers()
        self.list = []
        tmp = self.checkCam()
        tmpCC = self.cccamRunning()
        tmpOS = oscamRunning()
        tmpMx = self.mboxRunning()
        for x in self.menuListAll:
            self.status[x[0]] = True
            if not os.path.exists('/etc/init.d/busybox-cron') and x[0] == '13' or not MNG_DEV and x[0] == '11' or x[0] in ['7', '13'] and not ENA_PS or x[0] == '4' and not tmpMx or x[0] == '2' and not tmpCC and self.enaNonLocal or x[0] == '3' and not tmpOS and self.enaNonLocalOscam or x[0] == '6' and not fileExists('/tmp/ecm.info') or x[0] == '7' and fileExists(PYTHONPATH + 'Plugins/Extensions/GlassBluePanel/plugin.pyo') and not tmp:
                self.status[x[0]] = False
            item = [
             x[0]]
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=x[1], color_sel=int({True: '0x00d100', False: '0xd10000'}[self.status.get(x[0])], 16), color=int({True: '0xffffff', False: '0x666666'}[self.status.get(x[0])], 16)))
            pix = LoadPixmap({True: (BP_ICO % 'green'), False: (BP_ICO % 'red')}[self.status.get(x[0])])
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)

        self['list'].l.setList(self.list)
        return

    def cfgGsu(self):
        if self.size < 1280:
            self.close()
        self.session.openWithCallback(self.cfgAnswer, cfgGsuScreen)
        return

    def cfgAnswer(self, answer):
        if answer:
            self.session.openWithCallback(self.rstAnswer, MessageBox, _('Configuration was changed. Do you want restart GUI to activate changes now?'), MessageBox.TYPE_YESNO)
        return

    def updatechckact(self):
        (tt, self.wFtp) = chckFtp()
        if tt != '':
            self.session.open(MessageBox, tt, MessageBox.TYPE_ERROR, 6)
            return
        filenames = []
        try:
            ftp = ftplib.FTP(self.wFtp[0])
            ftp.login(self.wFtp[1], self.wFtp[2])
            data = []
            ftp.cwd('gsu' + GVIP)
            ftp.cwd(TYPE_DIR)
            ftp.dir(data.append)
            for line in data:
                tmp = re.sub('\\s+', '*', line)
                tmp = tmp.strip().split('*')
                if len(tmp) > 8:
                    if '.php' not in line and tmp[8] != '.' and tmp[8] != '..' and ':' in line:
                        idx = line.index(':')
                        zzz = line[idx + 4:]
                        filenames.append(zzz)

            ftp.quit()
        except:
            pass

        msg = _('No files detected')
        if len(filenames) == 1:
            zzz = filenames[0].strip().split('_')[1]
            try:
                msg = _('Error reading version info')
                if float(zzz) > float(self.readVersion()):
                    msg = _('New version') + ' ' + zzz
                else:
                    msg = _('You have actual version installed, no update needed')
            except:
                pass

        if _('New version') in msg:
            self.fileName = filenames[0]
            self.session.openWithCallback(self.updAnswer, MessageBox, msg + ' ' + _('Do you want update GSU?'), MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, 6)
        return

    def updAnswer(self, answer):
        if answer:
            state = False
            try:
                ftp = ftplib.FTP(self.wFtp[0])
                ftp.login(self.wFtp[1], self.wFtp[2])
                ftp.cwd('gsu' + GVIP)
                ftp.cwd(TYPE_DIR)
                ftp.retrbinary('RETR ' + self.fileName, open('/tmp/' + self.fileName, 'wb').write)
                state = True
                ftp.quit()
            except:
                pass

            if state:
                if '.rar' in self.fileName:
                    system('%s x -p%s /tmp/%s /tmp' % (_gsu_helper('unrar_bin'),PWDV,self.fileName))
                    system('rm -rf /tmp/' + self.fileName)
                    if ENA_D:
                        cmd = '.deb'
                    else:
                        cmd = '.ipk'
                    self.fileName = self.fileName.replace('.rar', cmd)
                if os.path.isfile('/tmp/' + self.fileName):
                    if ENA_D:
                        cmd = PKGBIN % self.fileName
                    else:
                        cmd = '%spkg install --force-overwrite /tmp/%s' % (PKGBIN, self.fileName)
                    self.session.openWithCallback(self.cmdAnsw, Console, title=_('Installing package') + ': %s' % self.fileName, cmdlist=[cmd])
                else:
                    self.session.open(MessageBox, _('Error while downloading file'), MessageBox.TYPE_ERROR, 6)
            else:
                self.session.open(MessageBox, _('Error while downloading file'), MessageBox.TYPE_ERROR, 6)
        return

    def cmdAnsw(self):
        system('rm -rf /tmp/' + self.fileName)
        contentInfo = chckPckgList()
        tmp = ''
        lenT = -1
        if ENA_D:
            lenT = -2
        for line in contentInfo:
            if line.__contains__('-plugin-glasssysutil'):
                line = line.strip().split('-')
                tmp = line[lenT].strip().split()[0]
                break

        if tmp and tmp == self.readVersion():
            self.session.openWithCallback(self.rstAnswer, MessageBox, _('Update finished successfully. Do you want restart GUI to activate new version now?'), MessageBox.TYPE_YESNO)
        else:
            self.session.open(MessageBox, _('Error while updating to new version'), MessageBox.TYPE_INFO, 6)
        return

    def rstAnswer(self, answer):
        Rst_E2(answer)
        return

    def setWindowTitle(self, titleName):
        self.setTitle(titleName)
        return

    def readVersion(self):
        version = 'x.xx'
        if os.path.isfile(GSU_PATH + 'version') is True:
            myfile = open(GSU_PATH + 'version', 'r')
            version = myfile.readline().strip()
        return version

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            tmp2 = int(selection[0])
            tmp = str(self.menuListAll[tmp2][2])
            self['info'].setText(tmp)
        return

    def checkCam(self):
        stat = False
        if generatePS():
            f = open(A_TM, 'r')
            for z in f.readlines():
                p = str(z).lower()
                if 'mpcs' in p or 'cam' in p or 'gbox' in p or 'mbox' in p or 'newcs' in p:
                    if '/usr/ucm_camsrv_bin' in p:
                        stat = True
                        break

            f.close()
            system(RM_A_TMP)
        return stat

    def cccamRunning(self):
        stat = False
        if generatePS():
            f = open(A_TM, 'r')
            for z in f.readlines():
                p = str(z).lower()
                if 'cccam' in p:
                    stat = True
                    break

            f.close()
            system(RM_A_TMP)
        return stat

    def mboxRunning(self):
        stat = False
        if generatePS():
            f = open(A_TM, 'r')
            for z in f.readlines():
                p = str(z).lower()
                if 'mbox' in p:
                    stat = True
                    break

            f.close()
            system(RM_A_TMP)
        return stat


class GlassSysInfoBrowser(Screen):

    def __init__(self, session):
        self.skin = GlassSysInfo
        self.session = session
        Screen.__init__(self, session)
        self['mem_labels'] = Label('\nTotal:\nFree:\nUsed:\nUsed(%):')
        self['ram'] = Label('')
        self['root'] = Label('')
        self['swap'] = Label('')
        self['mem_tot'] = Label('')
        self['space_labels'] = Label('\nTotal:\nFree:\nUsed:\nUsed(%):')
        self['cf'] = Label('')
        self['sd'] = Label('')
        self['usb'] = Label('')
        self['hdd'] = Label('')
        self['cpu'] = Label('')
        self['HDDTemperature'] = Label('')
        self['hdddev'] = Label('')
        self['sensors'] = Label('')
        self['HDDCPULabels'] = Label('What:\nValue:')
        self['ProccessInfo'] = ScrollLabel('')
        self['DmesgInfo'] = ScrollLabel('')
        self['cfbar'] = ProgressBar()
        self['sdbar'] = ProgressBar()
        self['usbbar'] = ProgressBar()
        self['hddbar'] = ProgressBar()
        self['membar'] = ProgressBar()
        self['rootbar'] = ProgressBar()
        self['swapbar'] = ProgressBar()
        self['hddtempbar'] = ProgressBar()
        self['hddstate'] = ProgressBar()
        self['cpubar'] = ProgressBar()
        self['memtotalbar'] = ProgressBar()
        self['tempDBbar'] = ProgressBar()
        self['telnet_on'] = Pixmap()
        self['ftp_on'] = Pixmap()
        self['vpn_on'] = Pixmap()
        self['smb_on'] = Pixmap()
        self['nfs_on'] = Pixmap()
        self['telnet_on'].hide()
        self['ftp_on'].hide()
        self['vpn_on'].hide()
        self['smb_on'].hide()
        self['nfs_on'].hide()
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Help'))
        self['yellow'] = Label(_('Refresh'))
        self.cpuTimer = None
        self.cpu_count = 0
        self.prev_info = self.getCpuInfo(-3)
        self.curr_info = self.getCpuInfo()
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'left': (self.pageUp1), 
           'right': (self.pageDown1), 
           'down': (self.pageDown), 
           'up': (self.pageUp), 
           'green': (self.HelpKey), 
           'ok': (self.exit), 
           'red': (self.exit), 
           'cancel': (self.exit), 
           'blue': (self.exit), 
           'yellow': (self.LetsgoParty)}, -2)
        self.size = getDesktop(0).size().width()
        self.onLayoutFinish.append(self.LetsgoParty)
        return

    def HelpKey(self):
        help = _('To moving in the list of running aplications use LEFT/RIGHT') + '\n' + _('To moving in the list of system info use UP/DOWN') + '\n' + _('Refresh press a YELLOW button')
        self.session.open(MessageBox, help, MessageBox.TYPE_INFO)
        return

    def exit(self):
        system('rm -rf /tmp/top.info')
        if self.cpuTimer is not None:
            self.cpuTimer.stop()
        self.cpuTimer = None
        self.close()
        return

    def LetsgoParty(self):
        self.ena = True
        if self.size < 1280:
            self.close()
            return
        self.getMemInfo()
        self.getSpaceInfo()
        self.getServicesInfo()
        self['sensors'].setText(self.getTempSensorsInfo())
        if self.cpuTimer is None:
            self.cpuTimer = eTimer()
            try:
                self.cpuTimer_conn = self.cpuTimer.timeout.connect(self.getCPUInfo)
            except AttributeError:
                self.cpuTimer.timeout.get().append(self.getCPUInfo)
        self.cpuTimer.start(200)
        self['ProccessInfo'].setText(self.getProccess())
        self['DmesgInfo'].setText(self.getDmesg())
        return

    def pageUp(self):
        self['DmesgInfo'].pageUp()
        return

    def pageDown(self):
        self['DmesgInfo'].pageDown()
        return

    def pageUp1(self):
        self['ProccessInfo'].pageUp()
        return

    def pageDown1(self):
        self['ProccessInfo'].pageDown()
        return

    def getMemInfo(self):

        def parse(i):
            return int(i.strip().split(':')[1].strip().split(' ')[0])

        def setUnits(value):
            if value >= 1048576:
                return '%.1f%s' % (float(value) / 1048576, 'GB')
            else:
                if value >= 1024:
                    return '%.1f%s' % (float(value) / 1024, 'MB')
                return '%.1f%s' % (float(value), 'kB')
            return

        ramperc = swapperc = ramtot = swaptot = ramfree = swapfree = ramused = swapused = totalperc = 0
        try:
            tmp = open('/proc/meminfo').readlines()
            ramfree = parse(tmp[1])
            ramtot = parse(tmp[0])
            ramused = ramtot - ramfree
            for x in tmp:
                if 'SwapTotal' in x:
                    swaptot = parse(x)
                elif 'SwapFree' in x:
                    swapfree = parse(x)

            swapused = swaptot - swapfree
            if ramtot != 0:
                ramperc = int(ramused * 100 / ramtot)
            if swaptot != 0:
                swapperc = int(swapused * 100 / swaptot)
            if swaptot != 0 or ramtot != 0:
                totalperc = int((ramused + swapused) * 100 / (ramtot + swaptot))
        except:
            pass

        self['ram'].setText('RAM:\n' + setUnits(ramtot) + '\n' + setUnits(ramfree) + '\n' + setUnits(ramused) + '\n' + str(ramperc) + '%')
        self['swap'].setText('Swap:\n' + setUnits(swaptot) + '\n' + setUnits(swapfree) + '\n' + setUnits(swapused) + '\n' + str(swapperc) + '%')
        self['mem_tot'].setText('Total:\n' + setUnits(ramtot + swaptot) + '\n' + setUnits(ramfree + swapfree) + '\n' + setUnits(ramused + swapused) + '\n' + str(totalperc) + '%')
        self['memtotalbar'].setValue(int(totalperc))
        self['swapbar'].setValue(int(swapperc))
        self['membar'].setValue(int(ramperc))
        return

    def getSpaceInfo(self):
        temperature = 'Temp. HDD:\nN/A'
        tmp1 = 0
        isHdd = 'N/A'
        tt = 'HDD'
        for i in ['a', 'b', 'c', 'd']:
            for x in ['smartctl -a /dev/sd%s | grep Temperature > %s', (_gsu_helper('hdd_temp_g') + ' -q -n /dev/sd%s > %s'), 
             'hddtemp -n -q /dev/sd%s > %s', (_gsu_helper('hdd_temp_g') + ' -q -n -w /dev/sd%s > %s'), 
             'hddtemp -n -q -w /dev/sd%s > %s']:
                try:
                    tta = x % (i, A_TM)
                    system(tta)
                    f = open(A_TM, 'r')
                    temp = f.readlines()
                    if 'smartctl' in tta:
                        tmp1 = int(temp[0].strip().split('-')[1].replace('\n', '').replace('\t', '').replace(' ', ''))
                    else:
                        tmp1 = int(temp[0].strip().split(' ')[0])
                    f.close()
                except:
                    pass

                system(RM_A_TMP)
                if tmp1 != 0 and tmp1 < 80:
                    isHdd = 'sd%s' % i
                    if checkHdd(i) == 2:
                        tt = 'SSD'
                    break

            if tmp1 != 0 and tmp1 < 80:
                break

        if tmp1 > 80:
            tmp = 0
        self['hddtempbar'].setRange((0, 100))
        self['hddtempbar'].setValue(tmp1)
        self['hddstate'].setRange((0, 100))
        if tmp1 != 0:
            temperature = 'Temp. %s:\n' % tt + str(tmp1) + DG + 'C'
            self['hddstate'].setValue(100)
        self['hdddev'].setText(tt + ':\n' + isHdd)
        self['HDDTemperature'].setText(temperature)
        os.system('df -h > /tmp/tempinfo.tmp')
        cfperc = usbperc = hddperc = sdperc = rootperc = 0
        rootsumm = cfsumm = sdsumm = usbsumm = hddsumm = '....\n....\n....\n....'
        if fileExists('/tmp/tempinfo.tmp'):
            f = open('/tmp/tempinfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[0] == '/dev/root' or parts[totsp] == '/':
                    rootperc = parts[4]
                    rootsumm = str(parts[1]) + 'B\n' + str(parts[3]) + 'B\n' + str(parts[2]) + 'B\n' + str(rootperc)
                    rootperc = rootperc.replace('%', '')
                if parts[totsp] == '/media/cf':
                    cfperc = int(parts[totsp - 1].replace('%', ''))
                    cfsumm = parts[totsp - 4] + 'B\n' + parts[totsp - 2] + 'B\n' + parts[totsp - 3] + 'B\n' + parts[totsp - 1]
                if parts[totsp] == '/media/sd' or parts[totsp] == '/media/mmc' or parts[totsp] == '/media/ba' and parts[0] == '/dev/mmcblk1p1':
                    sdperc = int(parts[totsp - 1].replace('%', ''))
                    sdsumm = parts[totsp - 4] + 'B\n' + parts[totsp - 2] + 'B\n' + parts[totsp - 3] + 'B\n' + parts[totsp - 1]
                if parts[totsp] == '/media/usb' or parts[totsp] == '/media/ba' and parts[0] == '/dev/sdb1':
                    usbperc = int(parts[totsp - 1].replace('%', ''))
                    usbsumm = parts[totsp - 4] + 'B\n' + parts[totsp - 2] + 'B\n' + parts[totsp - 3] + 'B\n' + parts[totsp - 1]
                if parts[totsp] == '/media/hdd':
                    strview = parts[totsp - 1].replace('%', '')
                    if strview.isdigit():
                        hddperc = int(parts[totsp - 1].replace('%', ''))
                        hddsumm = parts[totsp - 4] + 'B\n' + parts[totsp - 2] + 'B\n' + parts[totsp - 3] + 'B\n' + parts[totsp - 1]

            f.close()
            os.remove('/tmp/tempinfo.tmp')
        self['root'].setText('Root:\n' + rootsumm)
        self['cf'].setText('CF:\n' + cfsumm)
        self['sd'].setText('SD:\n' + sdsumm)
        self['usb'].setText('USB:\n' + usbsumm)
        self['hdd'].setText(tt + ':\n' + hddsumm)
        self['rootbar'].setValue(int(rootperc))
        self['cfbar'].setValue(int(cfperc))
        self['sdbar'].setValue(int(sdperc))
        self['usbbar'].setValue(int(usbperc))
        self['hddbar'].setValue(int(hddperc))
        return

    def getProccess(self):
        process = ''
        if generatePS():
            f = open(A_TM, 'r')
            for line in f.readlines():
                txt = line.strip() + '\n'
                if txt.find('ps -ef') == -1:
                    process += txt

            f.close()
            system(RM_A_TMP)
        return process

    def getDmesg(self):
        dmesg = ''
        os.system('dmesg > /tmp/tempinfo.tmp')
        if fileExists('/tmp/tempinfo.tmp'):
            f = open('/tmp/tempinfo.tmp', 'r')
            for line in f.readlines():
                dmesg += line.strip() + '\n'

            f.close()
            os.remove('/tmp/tempinfo.tmp')
        return dmesg

    def getServicesInfo(self):
        if fileExists('/etc/inetd.conf'):
            f = open('/etc/inetd.conf', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                try:
                    if parts[0] == 'telnet':
                        self['telnet_on'].show()
                    if parts[0] == 'ftp':
                        self['ftp_on'].show()
                except:
                    pass

            f.close()
        if generatePS():
            f = open(A_TM, 'r').read()
            if f.find('/usr/sbin/openvpn') != -1:
                self['vpn_on'].show()
            if f.find('smbd') != -1:
                self['smb_on'].show()
            if f.find('/usr/sbin/mountd') != -1 or f.find('[nfsd]') != -1:
                self['nfs_on'].show()
            if f.find('/usr/sbin/telnetd') != -1:
                self['telnet_on'].show()
            if f.find('/usr/sbin/vsftpd') != -1:
                self['ftp_on'].show()
            os.remove(A_TM)
        return

    def getCPUInfo(self):
        self.cpuTimer.stop()
        tmp = 'N/A'
        zataz = 0
        self.prev_info, self.curr_info = self.curr_info, self.getCpuInfo()
        for i in range(len(self.curr_info)):
            try:
                zataz = int(100 * (self.curr_info[i][2] - self.prev_info[i][2]) / (self.curr_info[i][1] - self.prev_info[i][1]))
                tmp = str(zataz) + ' %'
            except ZeroDivisionError:
                tmp = 'N/A'

        self['cpubar'].setValue(zataz)
        self['cpu'].setText('CPU using:\n' + tmp)
        self.cpuTimer.start(3500)
        return

    def getCpuInfo(self, cpu=-1):

        def validCpu(c):
            if cpu == -3 and c.isdigit():
                return True
            if c == ' ' and cpu == -1:
                return True
            if c == str(cpu):
                return True
            return False

        res = []
        calc_cpus = cpu == -3 and self.cpu_count == 0
        try:
            fd = open('/proc/stat', 'r')
            for l in fd:
                if l[0] != 'c':
                    continue
                if l.find('cpu') == 0 and validCpu(l[3]):
                    if calc_cpus:
                        self.cpu_count += 1
                        continue
                    total = busy = 0
                    tmp = l.split()
                    for i in range(1, len(tmp)):
                        tmp[i] = int(tmp[i])
                        total += tmp[i]

                    busy = total - tmp[4] - tmp[5]
                    res.append([tmp[0], total, busy])

            fd.close()
        except:
            pass

        return res

    def getTempSensorsInfo(self):
        temperature = 'Temp. DB:\nN/A'
        self['tempDBbar'].setRange((0, 100))
        temp = 0
        try:
            allsensors = sensors.getSensorsList(sensors.TYPE_TEMPERATURE)
            numtemp = len(allsensors)
            for num in range(numtemp):
                idx = allsensors[num]
                isMax = sensors.getSensorValue(idx)
                if isMax > temp:
                    temp = isMax

        except:
            pass

        if temp > 0:
            self['tempDBbar'].setValue(int(temp))
            temperature = 'Temp. DB:\n' + str(temp) + DG + 'C'
        elif fileExists('/sys/devices/virtual/thermal/thermal_zone0/temp'):
            try:
                temp = open('/sys/devices/virtual/thermal/thermal_zone0/temp').read()[:2]
                temp = temp.replace('\n', '')
                temperature = 'CPU Temp.: ' + temp + DG + 'C'
                self['tempDBbar'].setValue(int(temp))
            except:
                pass

        else:
            self['tempDBbar'].setValue(int(0))
        return temperature


class channelInfoCenter(Screen):

    def __init__(self, session):
        self.skin = channelInfo_Center
        self.session = session
        Screen.__init__(self, session)
        self['ecmValues'] = Label()
        self.e = 'CAM:\nSystem:\nCAID:\nProvider:\nProvID:\nPID:\nUsing:\nAddress:\nHops:\nShare:\nECM Time:'
        self['ecmlabels'] = Label(self.e)
        self['bit_labels'] = Label('\nVideo:\nAudio:\nStream:')
        self['bit_min'] = Label()
        self['bit_max'] = Label()
        self['bit_avg'] = Label()
        self['bit_act'] = Label()
        self['picsat'] = Pixmap()
        self['picprov'] = Pixmap()
        self['picchannel'] = Pixmap()
        self['piccode'] = Pixmap()
        self['piccam'] = Pixmap()
        self['stream_btr'] = Label('....')
        self['tp_lab'] = Label('System:\nModulation:\nFrequency:\nPolarisation:\nSymbol Rate:\nFEC:\nVideo PID:\nAudio PID:\nPCR PID:\nPMT PID:\nTXT PID:\nTSID:\nONID:\nSID:\nVideo Size:\nVideo Format:\nAudio Type:\nAudio Tracks:\nCAIDs:')
        self['tp_lab_sat'] = Label('Satellite:')
        self['tp_lab_ref'] = Label('Reference:')
        self['tp_values'] = Label('')
        self['tp_ref'] = Label('')
        self['tp_sat'] = Label('')
        self['red'] = Label(_('Exit'))
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.exit), 
           'red': (self.exit), 
           'ok': (self.exit), 
           'cancel': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit)}, -2)
        self.isBit = False
        self.dataV = 0
        self.dataA = 0
        self.runECMTimer1 = None
        self.runBitTimer1 = None
        self.onLayoutFinish.append(self.startInfo)
        return

    def startInfo(self):
        for x in ('picprov', 'picsat', 'picchannel', 'piccode', 'piccam'):
            self[x].instance.setScale(1)

        service = self.session.nav.getCurrentService()
        info = service and service.info()
        self['bit_min'].setText('Min:\n.... \n....')
        self['bit_max'].setText('Max:\n.... \n....')
        self['bit_avg'].setText('Avg:\n.... \n....')
        self['bit_act'].setText('Act:\n.... \n....')
        system = caid = provider = pid = using = adress = hops = share = ecmTime = coding = typecam = provid = '..............\n'
        vpid = apid = ppid = ref = '..............'
        self['ecmValues'].setText(typecam + system + caid + provider + pid + using + adress + hops + share + ecmTime + coding + provid)
        addr = ''
        if info:
            self.runBitTimer1 = eTimer()
            try:
                self.runBitTimer1_conn = self.runBitTimer1.timeout.connect(self.startBitrate)
            except:
                self.runBitTimer1.timeout.get().append(self.startBitrate)
            self.runBitTimer1.start(1000)
            self.runECMTimer1 = eTimer()
            try:
                self.runECMTimer1_conn = self.runECMTimer1.timeout.connect(self.readEcmInfo)
            except:
                self.runECMTimer1.timeout.get().append(self.readEcmInfo)
            serviceinfo = service.info()
            data = []
            data.append('%0.4X' % serviceinfo.getInfo(iServiceInformation.sVideoPID))
            data.append('%0.4X' % serviceinfo.getInfo(iServiceInformation.sAudioPID))
            data.append('%0.4X' % serviceinfo.getInfo(iServiceInformation.sPCRPID))
            data.append('%0.4X' % serviceinfo.getInfo(iServiceInformation.sPMTPID))
            data.append('%0.4X' % serviceinfo.getInfo(iServiceInformation.sTXTPID))
            data.append('%0.4X' % serviceinfo.getInfo(iServiceInformation.sTSID))
            data.append('%0.4X' % serviceinfo.getInfo(iServiceInformation.sONID))
            data.append('%0.4X' % serviceinfo.getInfo(iServiceInformation.sSID))
            data.append('%s x %s' % (serviceinfo.getInfo(iServiceInformation.sVideoWidth), serviceinfo.getInfo(iServiceInformation.sVideoHeight)))
            for x in range(0, len(data)):
                if str(data[x]) == '-0001' or '-1' in str(data[x]):
                    data[x] = '..............'

            ref = eServiceReference(info.getInfoString(iServiceInformation.sServiceref))
            if ref is not None:
                ref = ref.toString()
                if ref.startswith('-1:'):
                    ref = self.session.nav.getCurrentlyPlayingServiceReference()
                    if ref is not None:
                        ref = ref.toString()
            tmp = alternative(ref).split(':', 10)
            if len(tmp) > 10:
                addr = tmp[10].split(':')[0].replace('%3a', ':')
            if tmp[0] == '4097' and addr == '':
                ac = self.session.nav.getCurrentlyPlayingServiceReference()
                if ac is not None:
                    ac = ac.toString()
                    ac = ac.split(':', 10)
                    if len(ac) > 10:
                        addr = ac[10].split(':')[0].replace('%3a', ':')
            tmp = tmp[:10]
            ref = (':').join(tmp)
            self.setPicons(('_').join(tmp))
            tmp = self.getCaidInfo(info)
            if serviceinfo.getInfo(iServiceInformation.sIsCrypted) and tmp != _('No CA info available'):
                self.runECMTimer1.start(100)
            else:
                self.showPicCode('Fta-fs8', 'Fta-fs8')
            ac = iswide = '..............'
            if len(data) > 8:
                if data[8] != '..............':
                    if serviceinfo.getInfo(iServiceInformation.sAspect) in (3,
                                                                            4,
                                                                            7,
                                                                            8,
                                                                            11,
                                                                            12,
                                                                            15,
                                                                            16):
                        iswide = '16:9'
                    else:
                        iswide = '4:3'
            num = 0
            audio = service.audioTracks()
            if audio:
                num = audio.getNumberOfTracks()
                try:
                    i = audio.getTrackInfo(audio.getCurrentTrack())
                    x = i.getDescription().upper()
                    idx = i.getLanguage().upper()
                    if '5.1' in x or '5.1' in idx:
                        ac = 'Dolby Digital 5.1'
                    elif '2.0' in x or '2.0' in idx:
                        ac = 'Dolby Digital 2.0'
                    elif 'MPEG' in x or 'MPEG' in idx:
                        ac = 'MPEG'
                    elif 'DTS' in x or 'DTS' in idx:
                        ac = 'DTS'
                    elif 'AAC' in x or 'AAC' in idx:
                        ac = 'AAC'
                    elif 'DOLBY' in x or 'AC3' in x or 'DOLBY' in idx or 'AC3' in idx:
                        ac = 'AC3'
                except:
                    pass
                else:
                    if EACC and ac == '..............':
                        try:
                            idx = i.getType()
                            if idx in (iAt.atDTS, iAt.atDTSHD):
                                ac = 'DTS'
                            elif idx == iAt.atMPEG:
                                ac = 'MPEG'
                            elif idx in (iAt.atAAC, iAt.atAACHE):
                                ac = 'AAC'
                            elif idx in (iAt.atDDP, iAt.atAC3):
                                ac = 'AC3'
                        except:
                            pass

        try:
            (x, i) = self.getTunerInfo(service)
            self['tp_values'].setText('%s%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s' % (i, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], iswide, ac, str(num), tmp))
            self['tp_ref'].setText(ref)
            if addr != '':
                self['tp_lab_sat'].setText('Address:')
                if len(addr) > 50:
                    addr = '%s..' % addr[:50]
                self['tp_sat'].setText(addr)
            else:
                self['tp_sat'].setText(x)
        except:
            pass

        return

    def getCaidInfo(self, info):
        cainfo = ''
        if info:
            caids = info.getInfoObject(iServiceInformation.sCAIDs)
            if caids:
                if len(caids) > 0:
                    for caid in caids:
                        cainfo += '%0.4X' % caid + '  '

                    return cainfo
        return _('No CA info available')

    def getServiceInfoString(self, info, what, convert=(lambda x: '%d' % x)):
        v = info.getInfo(what)
        if v == -1:
            return 'N/A'
        if v == -2:
            return info.getInfoString(what)
        return convert(v)

    def getTunerInfo(self, service):
        orb = system = modulation = frequency = pol = symbolrate = fec = '..............'
        feinfo = service and service.frontendInfo()
        if feinfo is not None:
            frontendData = feinfo and feinfo.getAll(True)
            if frontendData is not None:
                dataTP = {}
                try:
                    dataTP = ConvertToHumanReadable(frontendData)
                except:
                    pass

                tunerType = str(frontendData.get('tuner_type', _('None')))
                if ENA_TT and tunerType != _('None'):
                    try:
                        tunerType = {(iDVBFrontend.feSatellite): '0', (iDVBFrontend.feCable): '1', (iDVBFrontend.feTerrestrial): '2', (iDVBFrontend.feSatellite2): '0', (iDVBFrontend.feTerrestrial2): '2'}[int(tunerType)]
                    except:
                        try:
                            tunerType = {(iDVBFrontend.feSatellite): '0', (iDVBFrontend.feCable): '1', (iDVBFrontend.feTerrestrial): '2'}[int(tunerType)]
                        except:
                            pass

                symbolrate = str(int(frontendData.get('symbol_rate', 0) / 1000))
                fq = int(round(1.0 * frontendData.get('frequency', 0) / 1000))
                if fq > 9999 and fq < 99999 and (tunerType == '1' or 'DVB-C' in tunerType) or fq > 99999:
                    frequency = str(int(round(1.0 * fq / 1000))) + ' MHz'
                else:
                    frequency = str(fq) + ' MHz'
                if tunerType in ('DVB-S', 'DVB-S2', '0'):
                    allSat = {}
                    try:
                        satellites = parse('/etc/tuxbox/satellites.xml').getroot()
                        if satellites is not None:
                            for x in satellites.findall('sat'):
                                name = x.get('name') or None
                                position = x.get('position') or None
                                if name is not None and position is not None:
                                    position = '%s.%s' % (position[:-1], position[-1:])
                                    if position.startswith('-'):
                                        position = '%sW' % position[1:]
                                    else:
                                        position = '%sE' % position
                                    if position.startswith('.'):
                                        position = '0%s' % position
                                    allSat[position] = name

                    except:
                        pass

                    numSat = frontendData.get('orbital_position', 0)
                    if numSat > 1800:
                        idx = str(float(3600 - numSat) / 10.0) + 'W'
                    else:
                        idx = str(float(numSat) / 10.0) + 'E'
                    if idx in allSat:
                        orb = allSat.get(idx)
                    else:
                        orb = 'Satellite at position: %s' % idx
                    pol = dataTP.get('polarization', 'Horizontal')
                    fec = dataTP.get('fec_inner', 'Auto')
                    system = dataTP.get('system', 'DVB-S')
                    modulation = dataTP.get('modulation', 'Auto')
                elif tunerType == '1' or 'DVB-C' in tunerType:
                    fec = dataTP.get('fec_inner', 'Auto')
                    modulation = dataTP.get('modulation', 'Auto')
                    system = 'DVB-C'
                    orb = 'Cable'
                elif tunerType == '2' or 'DVB-T' in tunerType:
                    system = 'DVB-T'
                    orb = 'Terrestrial'
                    try:
                        system = {(eDVBFrontendParametersTerrestrial.System_DVB_T): 'DVB-T', (eDVBFrontendParametersTerrestrial.System_DVB_T2): 'DVB-T2'}[frontendData.get('system', eDVBFrontendParametersTerrestrial.System_DVB_T)]
                    except:
                        pass

                    modulation = dataTP.get('constellation', 'Auto')
                    if 'fec_inner' in dataTP:
                        fec = dataTP.get('fec_inner', 'Auto')
                    else:
                        fec = dataTP.get('code_rate_hp', 'Auto') + ':' + dataTP.get('code_rate_lp', 'Auto')
                else:
                    system = _('No detected')
        return (
         orb, '%s\n%s\n%s\n%s\n%s\n%s\n' % (system, modulation, frequency, pol, symbolrate, fec))

    def startBitrate(self):
        self.runBitTimer1.stop()
        if not ENAEBTR and not ENA_Z:
            self.container = eConsoleAppContainer()
            self.container.dataAvail.append(self.dataAvail)
        service = self.session.nav.getCurrentService()
        info = service and service.info()
        if info:
            vpid = apid = dvbnamespace = tsid = onid = -1
            serviceinfo = service.info()
            vpid = serviceinfo.getInfo(iServiceInformation.sVideoPID)
            apid = serviceinfo.getInfo(iServiceInformation.sAudioPID)
            if ENAEBTR:
                ref = self.session.nav.getCurrentlyPlayingServiceReference()
                if not ref.getPath():
                    tsid = ref.getData(2)
                    onid = ref.getData(3)
                    dvbnamespace = ref.getData(4)
                if vpid > 0:
                    if not ENAEBTR2:
                        try:
                            self.videoBitrate = eBitrateCalculator(vpid, ref.toString(), 1000, 1048576)
                            self.videoBitrate.callback = self.getVideoBitrateData
                        except:
                            try:
                                self.videoBitrate = eBitrateCalculator(vpid, ref.toString(), 1000, 1048576)
                                self.videoBitrate.callback.append(self.getVideoBitrateData)
                            except:
                                pass

                    else:
                        try:
                            self.videoBitrate = eBitrateCalculator(vpid, dvbnamespace, tsid, onid, 1000, 1048576)
                            self.videoBitrate.callback.append(self.getVideoBitrateData)
                        except:
                            pass

                if apid > 0:
                    if not ENAEBTR2:
                        try:
                            self.audioBitrate = eBitrateCalculator(apid, ref.toString(), 1000, 65536)
                            self.audioBitrate.callback = self.getAudioBitrateData
                        except:
                            try:
                                self.audioBitrate = eBitrateCalculator(apid, ref.toString(), 1000, 65536)
                                self.audioBitrate.callback.append(self.getAudioBitrateData)
                            except:
                                pass

                    else:
                        try:
                            self.audioBitrate = eBitrateCalculator(apid, dvbnamespace, tsid, onid, 1000, 65536)
                            self.audioBitrate.callback.append(self.getAudioBitrateData)
                        except:
                            pass

            elif not ENA_Z and os.path.isfile(_gsu_helper('bitgenerator')) and self.isBit == False:
                demux = 2
                a = ''
                try:
                    stream = service.stream()
                    if stream:
                        streamdata = stream.getStreamingData()
                        if streamdata:
                            if 'demux' in streamdata:
                                demux = streamdata['demux']
                            if XCPU == 'arm':
                                a = '0 '
                                if 'adapter' in streamdata:
                                    a = str(streamdata['adapter']) + ' '
                except:
                    pass
                else:
                    cmd = '%s %s%s %s %s' % (_gsu_helper('bitgenerator'), a, str(demux), str(vpid), str(apid))
                    self.container.execute(cmd)
                    self.isBit = True
        return

    def getVideoBitrateData(self, value, status):
        if status:
            self.dataV = value
            self.updBtrData()
        else:
            self.videoBitrate = None
        return

    def getAudioBitrateData(self, value, status):
        if status:
            self.dataA = value
            self.updBtrData()
        else:
            self.audioBitrate = None
        return

    def updBtrData(self):
        self['bit_act'].setText('Act:\n' + str(self.dataV) + '\n' + str(self.dataA))
        return

    def dataAvail(self, str):
        try:
            if ISP38:
                str = str.decode('ascii')
            cmddata = str.split(' ')
            tmp = cmddata[3].split('\n')
            tmp1 = cmddata[6]
            self['bit_min'].setText('Min:\n' + cmddata[0] + '\n' + tmp[1])
            self['bit_max'].setText('Max:\n' + cmddata[1] + '\n' + cmddata[4])
            self['bit_avg'].setText('Avg:\n' + cmddata[2] + '\n' + cmddata[5])
            self['bit_act'].setText('Act:\n' + tmp[0] + '\n' + tmp1[:-1])
        except:
            pass

        return

    def exit(self):
        if self.isBit == True and os.path.isfile(_gsu_helper('bitgenerator')):
            self.isBit = False
            self.container.kill()
        if self.runECMTimer1 is not None:
            self.runECMTimer1.stop()
            self.runECMTimer1 = None
            self.runECMTimer1_conn = None
        if self.runBitTimer1 is not None:
            self.runBitTimer1.stop()
            self.runBitTimer1 = None
            self.runBitTimer1_conn = None
        self.close()
        return

    def readEcmInfo(self):
        self.runECMTimer1.stop()
        (oscVer, typecam, system, caid, provider, provid, pid, using, adress, hops, share, ecmTime, coding, dcw0, dcw1) = ECMparser()
        if using == 'unsupported CAs\n':
            self['ecmValues'].setText('..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n')
            coding = 'Unknown'
        else:
            if config.plugins.GlassSysUtil.par83.value != '':
                self['ecmlabels'].setText(self.e.replace(config.plugins.GlassSysUtil.par83.value, 'CHID:'))
            else:
                self['ecmlabels'].setText(self.e)
            self['ecmValues'].setText(typecam.replace('\n', oscVer) + coding + '\n' + caid + provider + provid + pid + using + adress + hops + share + ecmTime)
        if coding == '..............':
            coding = 'Unknown'
        self.showPicCode(coding + '-fs8', typecam[:-1] + '-fs8')
        self.runECMTimer1.start(3000)
        return

    def showPicCode(self, what, cam):

        def res(w):
            if w == '':
                if what == 'Fta-fs8':
                    w = BP_ICO % 'ca_small/Fta-fs8'
                else:
                    w = BP_ICO % 'ca_small/Unknown-fs8'
            return w

        self['piccode'].instance.setPixmapFromFile(res(findPicon(what, 'piconCam')))
        self['piccam'].instance.setPixmapFromFile(res(findPicon(cam, 'piconCam')))
        return

    def setPicons(self, sname):
        service = self.session.nav.getCurrentService()
        if service:
            info = service and service.info()
            enaIp = False
            refer = None
            if info is not None:
                refer = eServiceReference(info.getInfoString(iServiceInformation.sServiceref))
                if refer is not None:
                    refer = refer.toString()
                    if refer.startswith('-1:'):
                        refer = self.session.nav.getCurrentlyPlayingServiceReference()
                        if refer is not None:
                            refer = refer.toString()
                    enaIp = refer.startswith('4097:0') or '3a//' in refer or 'http' in refer
            self['picchannel'].instance.setPixmapFromFile(resPicon(sname, 'picon'))
            if enaIp:
                pngname = resPicon(self.chckIPTVprov(refer), 'piconProv')
            else:
                provname = getServiceInfoValue(info, iServiceInformation.sProvider, None)
                if provname.startswith('T-K'):
                    provname = 'T-KABEL'
                elif provname == 'T-Systems/MTI':
                    provname = 'T-SYSTEMS'
                else:
                    provname = provname.upper()
                if refer is not None and refer != '':
                    refer = refer.split(':', 10)[:10]
                    refer = ('_').join(refer)
                    refer = refer[:-10].split('_')[6].upper()
                    pngname = resPicon(refer + 'x' + provname, 'piconProv')
                if 'picon_default' in pngname:
                    pngname = resPicon(provname, 'piconProv')
            self['picprov'].instance.setPixmapFromFile(pngname)
            provname = self.getServiceInfoString(info, iServiceInformation.sTransferBPS, (lambda x: '%d kB/s' % (x / 1024)))
            if provname != 'N/A':
                self['stream_btr'].setText(provname)
            if enaIp:
                sname = 'IPTV'
                if provname == 'N/A':
                    self['stream_btr'].setText(str(int(info.getInfo(iServiceInformation.sTagBitrate)) / 1000) + ' kb/s')
            else:
                sname = getTunerPiconInfo(service)
            self['picsat'].instance.setPixmapFromFile(resPicon(sname, 'piconSat'))
        return

    def chckIPTVprov(self, r):
        ret = 'STREAM'
        allIPTVprov = {}
        for x in ('my_', 'enigma2/my_', '', 'enigma2/'):
            if os.path.isfile('/etc/%siptvprov.list' % x) is True:
                f = open('/etc/%siptvprov.list' % x, 'r')
                for i in f.readlines():
                    if ',' in i:
                        a = i.replace('\n', '')
                        a = a.strip().split(',')
                        if len(a) == 2 and a[0] not in allIPTVprov:
                            allIPTVprov[a[0]] = a[1].upper()

        if len(allIPTVprov) != 0 and r is not None:
            for x in list(allIPTVprov.keys()):
                if x in r:
                    ret = allIPTVprov.get(x)
                    break

        return ret


class cccamInfo(Screen):

    def __init__(self, session, url='http://127.0.0.1:16001', srv_name='Box'):
        self.skin = cccam_Info
        self.session = session
        Screen.__init__(self, session)
        self.url = url
        self.srv_name = srv_name
        self.list = []
        self.menuListAll = [('summary', _('Summary Info'), 'summary.png', ''),
         (
          'servers', _('Servers Status'), 'servers.png', 'Server connections:'),
         (
          'clients', _('Clients Status'), 'clients.png', 'Connected clients:'),
         (
          'activeclients', _('Active Clients Status'), 'activeclients.png', 'Connected clients:'),
         (
          'shares', _('Share Information'), 'shares.png', 'Available shares:'),
         (
          'providers', _('Providers Information'), 'providers.png', 'Available providers:'),
         (
          'entitlements', _('Info About Local Cards'), 'entitlements.png', 'abcd'),
         (
          'extend', _('Extend View'), 'entitlements.png', 'abcd')]
        self.status = {}
        self['list'] = ListboxSys2(self.list)
        self['info'] = Label('')
        self['server_name'] = Label('')
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit), 
           'back': (self.exit)})
        self.onLayoutFinish.append(self.updatemenulist)
        return

    def selectedmenuitem(self):
        selectedItem = self['list'].getCurrent()[0]
        enabledItem = self.status.get(selectedItem)
        if enabledItem:
            if selectedItem == 'summary':
                self.session.open(cccamSummary, self.url)
            if selectedItem == 'servers':
                self.session.open(serversStatus, self.url)
            elif selectedItem == 'clients':
                self.session.open(clientsStatus, self.url)
            elif selectedItem == 'activeclients':
                self.session.open(activeClientsStatus, self.url)
            elif selectedItem == 'shares':
                self.session.open(sharesStatus, self.url)
            elif selectedItem == 'providers':
                self.session.open(providerStatus, self.url)
            elif selectedItem == 'entitlements':
                self.session.open(entitlements, self.url)
            elif selectedItem == 'extend':
                self.session.open(providerCardView, self.url)
        return

    def updatemenulist(self):
        self.list = []
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        try:
            file = urllibXX.urlopen(url + '/servers')
        except:
            file = ''

        infoline = ''
        if file != '':
            tmptxt = []
            for line in file.readlines():
                line = line.replace('<BR>', '\n')
                line = sub('<br(\\s+/)?>', '\n', line)
                line = sub('<(.*?)>', '', line)
                line = line.replace('\t', ' ')
                tmptxt.append(line)

            for line in tmptxt:
                if line.__contains__('CCcam'):
                    if len(line) > 37:
                        infoline = line.strip()[27:]
                        infoline = infoline[:11]
                        break

        if url.__contains__('@'):
            idx = url.index('@')
            self['server_name'].setText(self.srv_name + '  at  http://' + url[idx + 1:] + '\n' + infoline)
        else:
            self['server_name'].setText(self.srv_name + '  at  ' + url + '\n' + infoline)
        num = providerCount(url)
        c = s = 0
        tstftpurl = self.testFtp(url)
        if tstftpurl:
            try:
                r = open('/var/etc/CCcam.cfg', 'r')
                for line in r.readlines():
                    if (line.startswith('F: ') or line.startswith('#F: ')) and not line.__contains__('>'):
                        c = c + 1
                    if (line.startswith('C: ') or line.startswith('#C: ')) and not line.__contains__('>') or (line.startswith('N: ') or line.startswith('#N: ')) and not line.__contains__('>'):
                        s = s + 1

                r.close()
            except:
                pass

        for x in self.menuListAll:
            self.status[x[0]] = False
            if x[0] != 'summary':
                try:
                    file = urllibXX.urlopen(url + '/' + x[0])
                    for line in file.readlines():
                        if line.__contains__('card'):
                            if line.__contains__('no or unknown card inserted'):
                                self.status[x[0]] = False
                            else:
                                self.status[x[0]] = True
                        elif x[0] == 'providers' and num > 0:
                            self.status[x[0]] = True
                        elif x[0] == 'clients' and c > 0 and tstftpurl:
                            self.status[x[0]] = True
                        elif x[0] == 'servers' and s > 0 and tstftpurl:
                            self.status[x[0]] = True
                        elif line.__contains__(x[3]):
                            polozka = line.strip().split(':')
                            tmp = polozka[1].strip()
                            if tmp != '0' or tmp == '':
                                self.status[x[0]] = True

                except:
                    pass

            elif num != -1:
                self.status[x[0]] = True
            if x[0] == 'extend' and num != -1:
                self.status[x[0]] = True
            item = [
             x[0]]
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=x[1], color=int({True: '0xffffff', False: '0x666666'}[self.status.get(x[0])], 16)))
            pix = LoadPixmap({True: (BP_ICO % 'green'), False: (BP_ICO % 'red')}[self.status.get(x[0])])
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)

        self['list'].l.setList(self.list)
        return

    def exit(self):
        self.close()
        return

    def testFtp(self, url):
        if url.__contains__('127.0.0.1'):
            return True
        return False


class serversStatus(Screen):

    def __init__(self, session, url):
        self.skin = cccam_servers_Info
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.url = url
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['server_detailed_labels'] = Label('Uptime:\nType:\nVersion:\nNode:\nCAID:')
        self['server_detailed_values'] = Label('')
        self['enaButton'] = Label(_('Enable'))
        self['disButton'] = Label(_('Disable'))
        self['red'] = Label(_('Exit'))
        self['yellow'] = Label(_('Refresh'))
        self.stateRefresh = False
        self.serverrefreshTimer = eTimer()
        try:
            self.serverrefreshTimer_conn = self.serverrefreshTimer.timeout.connect(self.readServersStatus)
        except:
            self.serverrefreshTimer.timeout.get().append(self.readServersStatus)

        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.enaServer), 
           'ok': (self.enaServer), 
           'red': (self.exit), 
           'yellow': (self.refresh), 
           'blue': (self.disServer), 
           'back': (self.exit)})
        self.onLayoutFinish.append(self.readServersStatus)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('Servers Status'))
        return

    def exit(self):
        self.serverrefreshTimer = None
        self.close()
        return

    def enaServer(self):
        if self.isReadyToChange:
            if self.stateRefresh:
                selection = self['list'].getCurrent()
                if selection:
                    tmp = selection[0]
                    parts = tmp.__contains__('|') or tmp.strip().split(' ')
                    tmp2 = parts[1].strip()
                    tmp3 = parts[2].strip()
                    self.writecfg(tmp2, tmp3, True)
        return

    def disServer(self):
        if self.isReadyToChange and self.stateRefresh:
            selection = self['list'].getCurrent()
            if selection:
                tmp = selection[0]
                if tmp.__contains__('|'):
                    parts = tmp.split('|')
                    tmp2 = parts[1].strip()
                    idx = tmp2.index(':')
                    tmp4 = tmp2[:idx - 1]
                    tmp3 = tmp2[idx + 1:]
                    self.writecfg(tmp4, tmp3, False)
        return

    def writecfg(self, adr, port, ena_state):
        try:
            allLines = ''
            r = open('/var/etc/CCcam.cfg', 'r')
            for line in r.readlines():
                if line.__contains__(adr) and line.__contains__(port):
                    if ena_state:
                        line = line[1:]
                    else:
                        line = '#' + line
                allLines = allLines + line

            r.close()
            r = open('/var/etc/CCcam.cfg', 'w')
            r.write(allLines)
            r.close()
            self.refresh()
        except:
            pass

        return

    def refresh(self):
        if not self.stateRefresh:
            return
        self.serverrefreshTimer.stop()
        self.serverrefreshTimer.start(4000)
        self.stateRefresh = False
        return

    def readServersStatus(self):
        self.serverrefreshTimer.stop()
        self['enaButton'].hide()
        self['disButton'].hide()
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        self.isReadyToChange = self.testFtp(url)
        file = ''
        try:
            file = urllibXX.urlopen(url + '/servers')
        except:
            file = ''

        if file == '':
            self.exit()
            return
        firstLine = True
        self.list = []
        item = []
        for line in file.readlines():
            if line.startswith('|'):
                if firstLine:
                    firstLine = False
                else:
                    parts = line.strip().split('|')
                    isExists = parts[1].strip()
                    if isExists:
                        num = parts[6].strip()
                        txtId = isExists + ',  ' + num
                        if int(num) != 1:
                            txtId += ' Cards'
                        else:
                            txtId += ' Card'
                        item = [
                         line]
                        isConnected = parts[2].strip()
                        pngname = BP_ICO % 'red'
                        if isConnected:
                            pngname = BP_ICO % 'green'
                        item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=txtId))
                        pix = LoadPixmap(pngname)
                        item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                        self.list.append(item)

        if self.isReadyToChange:
            try:
                pngname = BP_ICO % 'white'
                pix = LoadPixmap(pngname)
                r = open('/var/etc/CCcam.cfg', 'r')
                for line in r.readlines():
                    if line.startswith('#C: ') or line.startswith('#N: '):
                        parts = line.strip().split(' ')
                        if len(parts) > 4 and not parts[1].__contains__('>'):
                            item = [
                             line]
                            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=parts[1].strip() + ':' + parts[2].strip() + ', ' + _('blocked')))
                            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                            self.list.append(item)

                r.close()
            except:
                pass

        self['list'].l.setList(self.list)
        self.stateRefresh = True
        self.reactivate()
        return

    def reactivate(self):
        if not self.stateRefresh:
            return
        selection = self['list'].getCurrent()
        if selection:
            tmp = selection[0]
            if tmp.__contains__('|'):
                parts = tmp.split('|')
                self['server_detailed_values'].setText(parts[2].strip() + '\n' + parts[3].strip() + '\n' + parts[4].strip() + '\n' + parts[5].strip() + '\n' + parts[7].strip())
                if self.isReadyToChange:
                    self['enaButton'].hide()
                    self['disButton'].show()
            else:
                parts = tmp.strip().split(' ')
                if parts[0].__contains__('C'):
                    typesrv = 'CCcam'
                elif parts[0].__contains__('N'):
                    typesrv = 'Newcamd'
                self['server_detailed_values'].setText('.............\n' + typesrv + '\n.............\n.............\n.............')
                self['enaButton'].show()
                self['disButton'].hide()
        return

    def testFtp(self, url):
        if url.__contains__('127.0.0.1'):
            return True
        return False


class providerStatus(Screen):

    def __init__(self, session, url):
        self.skin = cccam_providers_Info
        self.session = session
        Screen.__init__(self, session)
        self.url = url
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['prov_detailed_labels'] = Label('CAID:\nProvider:\nSystem:')
        self['prov_detailed_values'] = Label('')
        self['red'] = Label(_('Exit'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.readProvidersStatus)
        return

    def readProvidersStatus(self):
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        file = ''
        try:
            file = urllibXX.urlopen(url + '/providers')
        except:
            file = ''

        if file == '':
            self.exit()
            return
        firstLine = True
        self.list = []
        item = []
        for line in file.readlines():
            if line.startswith('|'):
                if firstLine:
                    firstLine = False
                else:
                    parts = line.strip().split('|')
                    item = [line]
                    item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(535), fhd(22)), font=0, text=parts[3].strip()))
                    self.list.append(item)

        self.reactivate()
        self['list'].l.setList(self.list)
        self.setTitle(_('Providers Information'))
        return

    def exit(self):
        self.close()
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            tmp = selection[0]
            parts = tmp.split('|')
            self['prov_detailed_values'].setText(parts[1].strip() + '\n' + parts[2].strip() + '\n' + parts[4].strip())
        return


class sharesStatus(Screen):

    def __init__(self, session, url):
        self.skin = cccam_shares_Info
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.url = url
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['shares_detailed_labels'] = Label('Type:\nCAID:\nProvider:\nMaxDown:\nNodes:')
        self['shares_detailed_values'] = Label('')
        self['red'] = Label(_('Exit'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.readSharesStatus)
        return

    def readSharesStatus(self):
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        count = 0
        file = ''
        try:
            file = urllibXX.urlopen(url + '/shares')
        except:
            file = ''

        if file == '':
            self.exit()
            return
        self.list = []
        item = []
        for line in file.readlines():
            if line.startswith('|'):
                if count < 2:
                    count = count + 1
                else:
                    parts = line.strip().split('|')
                    item = [line]
                    item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(535), fhd(22)), font=0, text=parts[1].strip() + ', ' + _('using') + ' ' + parts[4].strip()))
                    self.list.append(item)

        self.reactivate()
        self['list'].l.setList(self.list)
        self.setTitle(_('Share Information'))
        return

    def exit(self):
        self.close()
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            tmp = selection[0]
            parts = tmp.split('|')
            self['shares_detailed_values'].setText(parts[2].strip() + '\n' + parts[3].strip() + '\n' + parts[5].strip() + '\n' + parts[6].strip() + '\n' + parts[7].strip())
        return


class clientsStatus(Screen):

    def __init__(self, session, url):
        self.skin = cccam_clients_Info
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.url = url
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['client_detailed_labels'] = Label('Connected:\nIdle Time:\nEcm:\nEmm:\nVersion:\nLast share:')
        self['client_detailed_values'] = Label('')
        self['enaButton'] = Label('Enable')
        self['disButton'] = Label('Disable')
        self['red'] = Label(_('Exit'))
        self['yellow'] = Label(_('Refresh'))
        self.stateRefresh = False
        self.clientrefreshTimer = eTimer()
        try:
            self.clientrefreshTimer_conn = self.clientrefreshTimer.timeout.connect(self.readClientsStatus)
        except:
            self.clientrefreshTimer.timeout.get().append(self.readClientsStatus)

        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.writecfg), 
           'ok': (self.writecfg), 
           'red': (self.exit), 
           'yellow': (self.refresh), 
           'blue': (self.writecfg), 
           'back': (self.exit)})
        self.onLayoutFinish.append(self.readClientsStatus)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('Clients Status'))
        return

    def writecfg(self):
        if self.isReadyToChange and self.stateRefresh:
            selection = self['list'].getCurrent()
            if selection:
                tmp = selection[0]
                if tmp.__contains__('|'):
                    parts = tmp.split('|')
                else:
                    parts = tmp.strip().split(' ')
                tmp2 = parts[1].strip()
                try:
                    allLines = ''
                    r = open('/var/etc/CCcam.cfg', 'r')
                    for line in r.readlines():
                        if line.__contains__(tmp2) and line.startswith('F: '):
                            line = '#' + line
                        elif line.__contains__(tmp2) and line.startswith('#F: '):
                            line = line[1:]
                        allLines = allLines + line

                    r.close()
                    r = open('/var/etc/CCcam.cfg', 'w')
                    r.write(allLines)
                    r.close()
                    self.refresh()
                except:
                    pass

        return

    def refresh(self):
        if not self.stateRefresh:
            return
        self.clientrefreshTimer.stop()
        self.clientrefreshTimer.start(4000)
        self.stateRefresh = False
        return

    def readClientsStatus(self):
        self.clientrefreshTimer.stop()
        self['enaButton'].hide()
        self['disButton'].hide()
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        self.isReadyToChange = self.testFtp(url)
        file = ''
        try:
            file = urllibXX.urlopen(url + '/clients')
        except:
            file = ''

        if file == '':
            self.exit()
            return
        firstLine = True
        self.list = []
        item = []
        count = 0
        for line in file.readlines():
            if line.startswith('|') and count < 4:
                if firstLine:
                    firstLine = False
                else:
                    parts = line.strip().split('|')
                    tmp = parts[1].strip() + '  at  ' + parts[2].strip()
                    item = [line]
                    isConnected = parts[3].strip()
                    pngname = BP_ICO % 'red'
                    if isConnected:
                        pngname = BP_ICO % 'green'
                    item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=tmp))
                    pix = LoadPixmap(pngname)
                    item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                    self.list.append(item)
            if line.startswith('+'):
                count = count + 1

        if self.isReadyToChange:
            try:
                r = open('/var/etc/CCcam.cfg', 'r')
                for line in r.readlines():
                    if line.startswith('#F: '):
                        parts = line.strip().split(' ')
                        if len(parts) > 2 and not parts[1].__contains__('>'):
                            pngname = BP_ICO % 'white'
                            pix = LoadPixmap(pngname)
                            item = [line]
                            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=parts[1].strip() + ', ' + _('blocked')))
                            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                            self.list.append(item)
                    elif line.startswith('F: '):
                        count = 0
                        firstLine = True
                        tmp = ''
                        for line1 in file.readlines():
                            if line1.startswith('|') and count < 4:
                                if firstLine:
                                    firstLine = False
                                else:
                                    parts1 = line1.strip().split('|')
                                    tmp = parts1[1].strip()
                                    count = count + 1

                        parts = line.strip().split(' ')
                        if len(parts) > 2 and not parts[1].__contains__('>') and parts[1].strip() != tmp:
                            pngname = BP_ICO % 'blue'
                            pix = LoadPixmap(pngname)
                            item = [line]
                            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=parts[1].strip() + ', ' + _('not connected')))
                            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                            self.list.append(item)

                r.close()
            except:
                pass

        self.stateRefresh = True
        self['list'].l.setList(self.list)
        self.reactivate()
        return

    def exit(self):
        self.clientrefreshTimer = None
        self.close()
        return

    def reactivate(self):
        if not self.stateRefresh:
            return
        selection = self['list'].getCurrent()
        if selection:
            tmp = selection[0]
            if tmp.__contains__('|'):
                parts = tmp.split('|')
                tmp1 = parts[3]
                tmp2 = parts[4]
                self['client_detailed_values'].setText(tmp1[4:] + '\n' + tmp2[4:] + '\n' + parts[5].strip() + '\n' + parts[6].strip() + '\n' + parts[7].strip() + '\n' + parts[8].strip())
                if self.isReadyToChange:
                    self['enaButton'].hide()
                    self['disButton'].show()
            elif tmp.startswith('F: '):
                self['client_detailed_values'].setText('.............\n.............\n.............\n.............\n.............\n.............')
                self['enaButton'].hide()
                self['disButton'].show()
            else:
                self['client_detailed_values'].setText('.............\n.............\n.............\n.............\n.............\n.............')
                self['enaButton'].show()
                self['disButton'].hide()
        return

    def testFtp(self, url):
        if url.__contains__('127.0.0.1'):
            return True
        return False


class activeClientsStatus(Screen):

    def __init__(self, session, url):
        self.skin = cccam_activeClients_Info
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.url = url
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['active_client_detailed_labels'] = Label('Connected:\nIdle Time:\nECM:\nEMM:\nVersion:\nLast share:')
        self['active_client_detailed_values'] = Label('')
        self['red'] = Label(_('Exit'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.readActiveClientsStatus)
        return

    def readActiveClientsStatus(self):
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        file = ''
        try:
            file = urllibXX.urlopen(url + '/activeclients')
        except:
            file = ''

        if file == '':
            self.exit()
            return
        firstLine = True
        self.list = []
        count = 0
        for line in file.readlines():
            if line.startswith('|') and count < 4:
                if firstLine:
                    firstLine = False
                else:
                    parts = line.strip().split('|')
                    tmp = parts[1].strip() + ',  ' + parts[2].strip()
                    item = [line]
                    item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(535), fhd(22)), font=0, text=tmp))
                    self.list.append(item)
            if line.startswith('+'):
                count = count + 1

        self['list'].l.setList(self.list)
        self.reactivate()
        self.setTitle(_('Active Clients Status'))
        return

    def exit(self):
        self.close()
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            tmp = selection[0]
            parts = tmp.split('|')
            tmp1 = parts[3]
            tmp2 = parts[4]
            self['active_client_detailed_values'].setText(tmp1[4:] + '\n' + tmp2[4:] + '\n' + parts[5].strip() + '\n' + parts[6].strip() + '\n' + parts[7].strip() + '\n' + parts[8].strip())
        return


class entitlements(Screen):

    def __init__(self, session, url):
        self.skin = cccam_entitlements
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.url = url
        self['entitlements_info'] = ScrollLabel('')
        self['red'] = Label(_('Exit'))
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'left': (self.pageUp), 
           'right': (self.pageDown), 
           'down': (self.pageDown), 
           'up': (self.pageUp), 
           'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'cancel': (self.close), 
           'blue': (self.close), 
           'yellow': (self.close)}, -2)
        self.onLayoutFinish.append(self.readEntitlements)
        return

    def pageUp(self):
        self['entitlements_info'].pageUp()
        return

    def pageDown(self):
        self['entitlements_info'].pageDown()
        return

    def readEntitlements(self):
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        tmptxt = ''
        file = ''
        try:
            file = urllibXX.urlopen(url + '/entitlements')
        except:
            file = ''

        if file == '':
            self.exit()
            return
        for line in file.readlines():
            line = line.replace('<BR>', '\n')
            line = sub('<br(\\s+/)?>', '\n', line)
            line = sub('<(.*?)>', '', line)
            tmptxt += line

        tmptxt = tmptxt.replace('CCcam info pages', '\n')
        tmptxt = tmptxt.replace('server ', 'server\n\n')
        self['entitlements_info'].setText(tmptxt)
        self.setTitle(_('Info About Local Cards'))
        return

    def exit(self):
        self.close()
        return


class cccamSummary(Screen):

    def __init__(self, session, url):
        self.skin = cccam_summary_Info
        self.session = session
        Screen.__init__(self, session)
        self.url = url
        self['summary_labels'] = Label("Current time:\nNodeID:\nUptime:\nServer connections:\nAvailable providers:\nAvailable shares:\nConnected clients:\nActive clients:\nTotal handled client ecm's:\nTotal handled client emm's:\nPeak load:")
        self['summary_values'] = Label('')
        self['red'] = Label(_('Exit'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.readSummaryStatus)
        return

    def readSummaryStatus(self):
        time = nodeId = uptime = serverConnections = availableProvides = availableShares = connectedClients = activeClients = clientsEcm = clientsEmm = peak = '....'
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        file = ''
        try:
            file = urllibXX.urlopen(url)
        except:
            file = ''

        if file == '':
            self.exit()
            return
        for lines in file.readlines():
            tmp = lines.split('<BR>')
            for line in tmp:
                if line.__contains__('Current time'):
                    pomocna = line.strip().split('Current time')
                    time = str(pomocna[1])
                elif line.__contains__('Uptime:'):
                    pomocna = line.strip().split(':')
                    uptime = str(pomocna[1])
                elif line.__contains__('NodeID:'):
                    pomocna = line.strip().split(':')
                    nodeId = str(pomocna[1])
                elif line.__contains__('Connected clients:'):
                    pomocna = line.strip().split(':')
                    connectedClients = str(pomocna[1])
                elif line.__contains__('Active clients:'):
                    pomocna = line.strip().split(':')
                    activeClients = str(pomocna[1])
                elif line.__contains__("Total handled client ecm's:"):
                    pomocna = line.strip().split(':')
                    clientsEcm = str(pomocna[1])
                elif line.__contains__("Total handled client emm's:"):
                    pomocna = line.strip().split(':')
                    clientsEmm = str(pomocna[1])
                elif line.__contains__('Peak load (max queued requests per workerthread):'):
                    pomocna = line.strip().split(':')
                    peak = str(pomocna[1])

        try:
            file = urllibXX.urlopen(url + '/servers')
            for line in file.readlines():
                if line.__contains__('Server connections:'):
                    pomocna = line.strip().split(':')
                    serverConnections = str(pomocna[1])

        except:
            pass

        try:
            file = urllibXX.urlopen(url + '/shares')
            for line in file.readlines():
                if line.__contains__('Available shares:'):
                    pomocna = line.strip().split(':')
                    availableShares = str(pomocna[1])

        except:
            pass

        availableProvides = str(providerCount(url))
        self['summary_values'].setText(time + '\n' + nodeId + '\n' + uptime + '\n' + serverConnections + '\n' + availableProvides + '\n' + availableShares + '\n' + connectedClients + '\n' + activeClients + '\n' + clientsEcm + '\n' + clientsEmm + '\n' + peak)
        self.setTitle(_('Summary Info'))
        return

    def exit(self):
        self.close()
        return


class cccamInfoChoiceServer(Screen):

    def __init__(self, session):
        self.skin = cccam_InfoChoiseServer
        self.session = session
        Screen.__init__(self, session)
        self.status = {}
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['server_detailed_labels'] = Label(_('Name') + ':\n' + _('Ip adress') + ':\n' + _('Port') + ':\n' + _('Login') + ':\n' + _('Pass') + ':')
        self['server_detailed_values'] = Label('')
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.choiseServer), 
           'ok': (self.choiseServer), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.readCccamServers)
        return

    def readCccamServers(self):
        item = []
        c = 0
        if fileExists('/etc/remote_servers.cfg'):
            try:
                f = open('/etc/remote_servers.cfg', 'r')
                content = f.read()
                f.close()
            except:
                content = ''
            else:
                contentInfo = content.split('\n')
                if content != '':
                    for line in contentInfo:
                        if line.startswith('C:'):
                            tmp = line.strip().split(' ')
                            if len(tmp) > 2:
                                if tmp[2].__contains__('127.0.0.1'):
                                    url = readURL()
                                else:
                                    url = 'http://' + tmp[2]
                                    if len(tmp) > 4:
                                        if tmp[3] is not None and tmp[4] is not None and tmp[3] != '' and tmp[4] != '':
                                            url = url.replace('http://', 'http://%s:%s@' % (tmp[3], tmp[4]))
                                self.status[line] = False
                                try:
                                    file = urllibXX.urlopen(url + '/shares')
                                except:
                                    file = ''
                                else:
                                    if file != '':
                                        self.status[line] = True
                                    c = c + 1
                                    item = [line]
                                    item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(35), fhd(22)), font=0, text=str(c) + '.'))
                                    item.append(MultiContentEntryText(pos=(fhd(65), 0), size=(fhd(310), fhd(22)), font=0, text=tmp[1], color_sel=int({True: '0x00d100', False: '0xd10000'}[self.status.get(line)], 16), color=int({True: '0xffffff', False: '0x666666'}[self.status.get(line)], 16)))
                                    pix = LoadPixmap({True: (BP_ICO % 'green'), False: (BP_ICO % 'red')}[self.status.get(line)])
                                    item.append(MultiContentEntryPixmapAlphaTest(pos=(fhd(40), fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                                    self.list.append(item)

                    self['list'].l.setList(self.list)
                    self.reactivate()
                    self.setTitle(_('Select Server'))
                else:
                    self.close()
        else:
            self.close()
        return

    def choiseServer(self):
        line = self['list'].getCurrent()[0]
        if self.status.get(line):
            tmp = line.strip().split(' ')
            if tmp[2].__contains__('127.0.0.1'):
                url = readURL()
            else:
                url = 'http://' + tmp[2]
                if len(tmp) > 4:
                    if tmp[3] is not None and tmp[4] is not None and tmp[3] != '' and tmp[4] != '':
                        url = url.replace('http://', 'http://%s:%s@' % (tmp[3], tmp[4]))
            self.session.open(cccamInfo, url, tmp[1])
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        serverName = serverPort = loginName = passwordName = '........'
        if selection:
            lineRq = selection[0]
            tmp = lineRq.strip().split(' ')
            name = tmp[1]
            if lineRq.__contains__('127.0.0.1'):
                serverName = '127.0.0.1'
                serverPort = '16001'
                try:
                    f = open('/var/etc/CCcam.cfg', 'r')
                    for line in f.readlines():
                        if line.startswith('WEBINFO LISTEN PORT :'):
                            tmp = line.split(':')
                            port = tmp[1].replace('\n', '').replace('\r', '').replace(' ', '')
                            if port != '':
                                serverPort = port
                        elif line.startswith('WEBINFO USERNAME :'):
                            tmp = line.split(':')
                            loginName = tmp[1].replace('\n', '').replace('\r', '').replace(' ', '')
                        elif line.startswith('WEBINFO PASSWORD :'):
                            tmp = line.split(':')
                            passwordName = tmp[1].replace('\n', '').replace('\r', '').replace(' ', '')

                    f.close()
                except:
                    pass

            else:
                serverName = tmp[2]
                if len(tmp) > 4:
                    loginName = tmp[3]
                    passwordName = tmp[4]
                server = tmp[2].split(':')
                if len(server) > 1:
                    serverName = server[0]
                    serverPort = server[1]
            self['server_detailed_values'].setText(name + '\n' + serverName + '\n' + serverPort + '\n' + loginName + '\n' + passwordName)
        return


class providerCardView(Screen):

    def __init__(self, session, url):
        self.skin = cccam_providerCardView_Info
        self.session = session
        Screen.__init__(self, session)
        self.url = url
        self.providerList = []
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['count'] = Label('')
        self['red'] = Label(_('Exit'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.fillProviderCardList)
        return

    def readProviders(self):
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        file = ''
        try:
            file = urllibXX.urlopen(url + '/providers')
        except:
            file = ''

        if file == '':
            self.exit()
            return
        firstLine = True
        item = []
        for line in file.readlines():
            if line.startswith('|'):
                if firstLine:
                    firstLine = False
                else:
                    parts = line.strip().split('|')
                    if parts[2].strip() == '':
                        parts[2] = '0'
                    item = [
                     parts[1].strip()]
                    item.append(parts[2].strip())
                    item.append(parts[3].strip())
                    item.append(parts[4].strip())
                    item.append(0)
                    self.providerList.append(item)

        return

    def fillProviderCardList(self):
        self.readProviders()
        url = self.url
        if url.__contains__('127.0.0.1'):
            url = readURL()
        count = 0
        file = ''
        try:
            file = urllibXX.urlopen(url + '/shares')
        except:
            file = ''

        if file == '':
            self.exit()
            return
        firstLine = True
        for line in file.readlines():
            if line.startswith('|'):
                if firstLine:
                    firstLine = False
                else:
                    parts = line.strip().split('|')
                    if parts[1].strip() != '':
                        a1 = parts[3].strip()
                        a2 = parts[5].strip()
                        pp = a2.split(',')
                        for provider in self.providerList:
                            if len(pp) > 1:
                                for ppp in pp:
                                    if a1 == provider[0] and ppp == provider[1]:
                                        provider[4] = provider[4] + 1

                            elif a1 == provider[0] and a2 == provider[1]:
                                provider[4] = provider[4] + 1

        item = []
        for line in self.providerList:
            count = count + line[4]
            item = [line]
            item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(100), fhd(22)), font=1, text=line[3].strip()))
            item.append(MultiContentEntryText(pos=(fhd(110), 0), size=(fhd(100), fhd(22)), font=1, text=line[0].strip() + ':' + line[1].strip()))
            item.append(MultiContentEntryText(pos=(fhd(220), 0), size=(fhd(580), fhd(22)), font=1, text=line[2].strip()))
            item.append(MultiContentEntryText(pos=(fhd(810), 0), size=(fhd(50), fhd(22)), font=1, text=str(line[4]).strip()))
            self.list.append(item)

        self['count'].setText('Count:' + str(count))
        self['list'].l.setList(self.list)
        self.setTitle(_('Extend View'))
        return

    def exit(self):
        self.close()
        return


class oscamLineCfg(Screen, ConfigListScreen):

    def __init__(self, session):
        Screen.__init__(self, session)
        if ENA_D:
            self.skin = oscam_start.replace('<widget name="config" font="priveG;30"', '<widget name="config"').replace('<widget name="config" font="priveG;60"', '<widget name="config"')
        else:
            self.skin = oscam_start
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['white'] = Label(_('Press OK to select dir'))
        self['white'].hide()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': (self.save), 
           'ok': (self.ActivateselectedFnc), 
           'yellow': (self.exitCancel), 
           'red': (self.exitCancel), 
           'cancel': (self.exitCancel)}, -2)
        self.list = []
        ConfigListScreen.__init__(self, self.list, session)
        self.onLayoutFinish.append(self.setTitlenew)
        self.onLayoutFinish.append(self.runSetup)
        self.old = config.plugins.GlassSysUtil.par38
        self.chckTimer = eTimer()
        try:
            self.chckTimer_conn = self.chckTimer.timeout.connect(self.chckWhite)
        except:
            self.chckTimer.timeout.get().append(self.chckWhite)

        self.chckTimer.start(1000, True)
        return

    def chckWhite(self):
        self.chckTimer.stop()
        t = self['config'].getCurrent()[1]
        if self.old != t:
            self.old = t
            if t in (config.plugins.GlassSysUtil.par17, config.plugins.GlassSysUtil.par18):
                self['white'].show()
            else:
                self['white'].hide()
        self.chckTimer.start(1000, True)
        return

    def setTitlenew(self):
        self.setTitle(_('OScam start cfg'))
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.chckSetup()
        return

    def chckSetup(self):
        t = self['config'].getCurrent()[1]
        if t in (config.plugins.GlassSysUtil.par73, config.plugins.GlassSysUtil.par71, config.plugins.GlassSysUtil.par69, config.plugins.GlassSysUtil.par29, config.plugins.GlassSysUtil.par19, config.plugins.GlassSysUtil.par24, config.plugins.GlassSysUtil.par27):
            self.runSetup()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.chckSetup()
        return

    def runSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Read configuration from'), config.plugins.GlassSysUtil.par17))
        self.list.append(getConfigListEntry(_('Tmp dir'), config.plugins.GlassSysUtil.par18))
        self.list.append(getConfigListEntry(_('Enable debug'), config.plugins.GlassSysUtil.par19))
        if config.plugins.GlassSysUtil.par19.value:
            self.list.append(getConfigListEntry(_('(debug option) Detailed error messages'), config.plugins.GlassSysUtil.par31))
            self.list.append(getConfigListEntry(_('(debug option) ATR parsing info, ECM, EMM and CW dumps'), config.plugins.GlassSysUtil.par32))
            self.list.append(getConfigListEntry(_('(debug option) Traffic from/to the reader'), config.plugins.GlassSysUtil.par33))
            self.list.append(getConfigListEntry(_('(debug option) Traffic from/to the clients'), config.plugins.GlassSysUtil.par34))
            self.list.append(getConfigListEntry(_('(debug option) Traffic to the reader-device on IFD layer'), config.plugins.GlassSysUtil.par35))
            self.list.append(getConfigListEntry(_('(debug option) Traffic to the reader-device on I/O layer'), config.plugins.GlassSysUtil.par36))
            self.list.append(getConfigListEntry(_('(debug option) EMM logging'), config.plugins.GlassSysUtil.par37))
            self.list.append(getConfigListEntry(_('(debug option) DVB API logging'), config.plugins.GlassSysUtil.par38))
            self.list.append(getConfigListEntry(_('(debug option) Loadbalancer logging'), config.plugins.GlassSysUtil.par63))
            self.list.append(getConfigListEntry(_('(debug option) CACHEEX logging'), config.plugins.GlassSysUtil.par64))
            self.list.append(getConfigListEntry(_('(debug option) Client ECM logging'), config.plugins.GlassSysUtil.par65))
            self.list.append(getConfigListEntry(_('(debug option) CSP logging'), config.plugins.GlassSysUtil.par66))
            self.list.append(getConfigListEntry(_('(debug option) CWC logging'), config.plugins.GlassSysUtil.par67))
            self.list.append(getConfigListEntry(_('(debug option) Debug all'), config.plugins.GlassSysUtil.par39))
        self.list.append(getConfigListEntry(_('Capture segmentation faults'), config.plugins.GlassSysUtil.par20))
        self.list.append(getConfigListEntry(_('Start in background'), config.plugins.GlassSysUtil.par22))
        self.list.append(getConfigListEntry(_('Write oscam.crash on segfault'), config.plugins.GlassSysUtil.par23))
        self.list.append(getConfigListEntry(_('Wait up to (s) for the system time'), config.plugins.GlassSysUtil.par24))
        if config.plugins.GlassSysUtil.par24.value:
            self.list.append(getConfigListEntry(_('(Wait) ...30-300... seconds'), config.plugins.GlassSysUtil.par25))
        self.list.append(getConfigListEntry(_('Enable output of web interface in UTF-8 charset'), config.plugins.GlassSysUtil.par26))
        self.list.append(getConfigListEntry(_('Garbage collector debug mode'), config.plugins.GlassSysUtil.par27))
        if config.plugins.GlassSysUtil.par27.value:
            self.list.append(getConfigListEntry(_('(garbage) mode'), config.plugins.GlassSysUtil.par28))
        self.list.append(getConfigListEntry(_('Enable restart level'), config.plugins.GlassSysUtil.par29))
        if config.plugins.GlassSysUtil.par29.value:
            self.list.append(getConfigListEntry(_('(restart level) type'), config.plugins.GlassSysUtil.par30))
        self.list.append(getConfigListEntry(_('Do not filter sensitive info from the logs'), config.plugins.GlassSysUtil.par68))
        self.list.append(getConfigListEntry(_('Set the maximum number of pending ECM packets'), config.plugins.GlassSysUtil.par69))
        if config.plugins.GlassSysUtil.par69.value:
            self.list.append(getConfigListEntry(_('(ECM packets) ...96-4096'), config.plugins.GlassSysUtil.par70))
        self.list.append(getConfigListEntry(_('Create pidfile when starting'), config.plugins.GlassSysUtil.par71))
        if config.plugins.GlassSysUtil.par71.value:
            self.list.append(getConfigListEntry(_('Pidfile name'), config.plugins.GlassSysUtil.par72))
        self.list.append(getConfigListEntry(_('CSet syslog ident'), config.plugins.GlassSysUtil.par73))
        if config.plugins.GlassSysUtil.par73.value:
            self.list.append(getConfigListEntry(_('ident name'), config.plugins.GlassSysUtil.par74))
        self['config'].list = self.list
        self['config'].setList(self.list)
        return

    def ActivateselectedFnc(self):
        self.t = self['config'].getCurrent()[1]
        if self.t in (config.plugins.GlassSysUtil.par18, config.plugins.GlassSysUtil.par17):
            self.session.openWithCallback(self.dirSelected, dirBrowser, self.t.value)
        return

    def dirSelected(self, answer):
        if answer is not None:
            self.t.value = answer
            self.runSetup()
        return

    def save(self):
        cfgPath = config.plugins.GlassSysUtil.par17.value
        if cfgPath.endswith('/'):
            cfgPath = cfgPath[:-1]
        if not os.path.exists(cfgPath):
            system('mkdir ' + cfgPath)
            if not os.path.exists(cfgPath):
                self.session.open(MessageBox, _('Cannot create path, please, enter another'), MessageBox.TYPE_ERROR, 4)
                return
        tmpPath = config.plugins.GlassSysUtil.par18.value
        if tmpPath.endswith('/'):
            tmpPath = tmpPath[:-1]
        if not os.path.exists(tmpPath):
            system('mkdir ' + tmpPath)
            if not os.path.exists(tmpPath):
                self.session.open(MessageBox, _('Cannot create path, please, enter another'), MessageBox.TYPE_ERROR, 4)
                return
        lineCfgAll = '/usr/UCM_CamSrv_bin/$SrvBin -c ' + cfgPath + ' -t ' + tmpPath
        if config.plugins.GlassSysUtil.par23.value:
            lineCfgAll += ' -a'
        if config.plugins.GlassSysUtil.par22.value:
            lineCfgAll += ' -b'
        if config.plugins.GlassSysUtil.par20.value:
            lineCfgAll += ' -s'
        if config.plugins.GlassSysUtil.par19.value:
            if config.plugins.GlassSysUtil.par39.value:
                lineCfgAll += ' -d 65535'
            else:
                d_level = 0
                if config.plugins.GlassSysUtil.par31.value:
                    d_level += 1
                if config.plugins.GlassSysUtil.par32.value:
                    d_level += 2
                if config.plugins.GlassSysUtil.par33.value:
                    d_level += 4
                if config.plugins.GlassSysUtil.par34.value:
                    d_level += 8
                if config.plugins.GlassSysUtil.par35.value:
                    d_level += 16
                if config.plugins.GlassSysUtil.par36.value:
                    d_level += 32
                if config.plugins.GlassSysUtil.par37.value:
                    d_level += 64
                if config.plugins.GlassSysUtil.par38.value:
                    d_level += 128
                if config.plugins.GlassSysUtil.par63.value:
                    d_level += 256
                if config.plugins.GlassSysUtil.par64.value:
                    d_level += 512
                if config.plugins.GlassSysUtil.par65.value:
                    d_level += 1024
                if config.plugins.GlassSysUtil.par66.value:
                    d_level += 2048
                if config.plugins.GlassSysUtil.par67.value:
                    d_level += 4096
                if d_level != 0:
                    lineCfgAll += ' -d ' + str(d_level)
        if config.plugins.GlassSysUtil.par29.value:
            lineCfgAll += ' -r ' + str(config.plugins.GlassSysUtil.par30.value)
        if config.plugins.GlassSysUtil.par27.value:
            lineCfgAll += ' -g ' + str(config.plugins.GlassSysUtil.par28.value)
        if config.plugins.GlassSysUtil.par24.value:
            lineCfgAll += ' -w ' + str(config.plugins.GlassSysUtil.par25.value)
        if config.plugins.GlassSysUtil.par26.value:
            lineCfgAll += ' -u'
        if config.plugins.GlassSysUtil.par68.value:
            lineCfgAll += ' -S'
        if config.plugins.GlassSysUtil.par69.value:
            lineCfgAll += ' -p ' + str(config.plugins.GlassSysUtil.par70.value)
        if config.plugins.GlassSysUtil.par71.value:
            lineCfgAll += ' -B ' + str(config.plugins.GlassSysUtil.par72.value)
        if config.plugins.GlassSysUtil.par73.value:
            lineCfgAll += ' -I ' + str(config.plugins.GlassSysUtil.par74.value)
        config.plugins.GlassSysUtil.par21.value = lineCfgAll + ' > /dev/null 2>&1 &'
        x = writeOscamCfgPath()
        if not x:
            self.session.open(MessageBox, _('Saving start cfg to "Oscam_Srv.sh" failed'), MessageBox.TYPE_INFO, 4)
            return
        for x in self['config'].list:
            x[1].save()

        config.plugins.GlassSysUtil.par21.save()
        configfile.save()
        self.close()
        return

    def exitCancel(self):
        self.chckTimer.stop()
        self.chckTimer = None
        self.chckTimer_conn = None
        for x in self['config'].list:
            x[1].cancel()

        self.close()
        return


class univCamMng(Screen):

    def __init__(self, session):
        if ENA_D:
            self.skin = UCM.replace('<widget name="config" font="priveG;30"', '<widget name="config"').replace('<widget name="config" font="priveG;60"', '<widget name="config"')
        else:
            self.skin = UCM
        self.session = session
        Screen.__init__(self, session)
        self['picECM'] = Pixmap()
        self['commPic'] = Pixmap()
        self['statPic'] = Pixmap()
        self['CamPic'] = Pixmap()
        self['SrvPic'] = Pixmap()
        self['picprov'] = Pixmap()
        self['picsat'] = Pixmap()
        self['picchannel'] = Pixmap()
        self['red'] = Label(_('Stop'))
        self['green'] = Label(_('Start/Re-start'))
        self['yellow'] = Label(_('Activate'))
        self['blue'] = Label(_('Move Selection'))
        self['helpTXT'] = Label()
        self['txt0'] = Label(_('Exit'))
        self['txt1'] = Label(_('Download CAM/SRV'))
        self['txt2'] = Label(_('Delete CAM/SRV'))
        self['txt3'] = ColorLabel(_('Update OScam'))
        self['txt4'] = ColorLabel(_('OScam Start cfg'))
        self['txt5'] = ColorLabel(_('Keystart'))
        self['txt6'] = ColorLabel(_('Delay'))
        self['txt7'] = ColorLabel(_('SRV Restart'))
        self['txt8'] = ColorLabel(_('Autocheck CAM/SRV'))
        self['txt9'] = ColorLabel(_('Prepare Exp. Image'))
        self.aa = {0: (_('Exit CAM/SRV Manager')), 1: (_('Downloading CAM/SRV from server and installing to CAM/SRV Manager')), 
           2: (_('Deleting CAM/SRV from CAM/SRV Manager')), 
           3: (_('Update OScam to the highest available version')), 
           4: (_('OScam starting with command line options like path to OScam cfg and more')), 
           5: (_('Enabling or Disabling quick(direct) start CAM/SRV Manager(press Green button) and ECM Info(press Red button). This action have lowest priority so if Red/Green button have joined function in image no action will be taken')), 
           6: (_('Delayed start in seconds of CAM/SRV after start E2')), 
           7: (_('Enabling or Disabling Restart SRV if CAM is running')), 
           8: (_('Enabling or Disabling Autocheck of running CAM/SRV every 10 min and try to start CAM/SRV if is not running')), 
           9: (_('Preparing experimental image to use CAM/SRV and disabling dccamd'))}
        self['select_pict'] = Pixmap()
        self.idxAllFnc = 0
        self.list = []
        self['config'] = ConfigList(self.list)
        self['statCamSrvcmd'] = Label(_('No Command Active'))
        self['statCamSrvbin'] = Label(_('Checking Bin Files'))
        self['fullEcmLine'] = Label(_('Searching ECM Info'))
        self['CAID_info'] = Label(_('Searching CAID Info'))
        self['activCam'] = Label(_('Searching Active CAM'))
        self['activSrv'] = Label(_('Searching Active SRV'))
        self['actions'] = ActionMap(['UCMActions'], {'left': (self.keyLeft), 
           'right': (self.keyRight), 
           'green': (self.start), 
           'ok': (self.start), 
           'red': (self.stop), 
           'cancel': (self.exit), 
           'exit': (self.exit), 
           'yellow': (self.ActivateselectedFnc), 
           'blue': (self.selectFnc)}, -1)
        self.checkCam = self.enCommand = self.typecmd = self.enaBlue = False
        self.keyState = config.plugins.GlassSysUtil.par40.value
        self.capic = 'None'
        self.enaYellow = True
        self.FirstInfoTimer = eTimer()
        try:
            self.FirstInfoTimer_conn = self.FirstInfoTimer.timeout.connect(self.firstInfo)
        except:
            self.FirstInfoTimer.timeout.get().append(self.firstInfo)

        self.FirstInfoTimer.start(3000, True)
        self.EcmInfoTimer = eTimer()
        try:
            self.EcmInfoTimer_conn = self.EcmInfoTimer.timeout.connect(self.showEcmInfo)
        except:
            self.EcmInfoTimer.timeout.get().append(self.showEcmInfo)

        self.chckOscamTimer = eTimer()
        try:
            self.chckOscamTimer_conn = self.chckOscamTimer.timeout.connect(self.chckOscam)
        except:
            self.chckOscamTimer.timeout.get().append(self.chckOscam)

        self.onLayoutFinish.append(self.inicializeUCM)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('CAM/SRV Manager'))
        self['helpTXT'].setText(self.aa.get(self.idxAllFnc, ''))
        try:
            for x in ('picECM', 'picprov', 'picsat', 'picchannel'):
                self[x].instance.setScale(1)

        except:
            pass

        self['picECM'].instance.setPixmapFromFile(BP_ICO % 'ca_small/Unknown-fs8')
        return

    def ActivateselectedFnc(self):
        if self.idxAllFnc == 0:
            self.exit()
        elif self.idxAllFnc == 1:
            self.moreCamSrv()
        elif self.idxAllFnc == 2:
            self.lessCamSrv()
        elif self.idxAllFnc == 3:
            self.setLatestOscam()
        elif self.idxAllFnc == 4:
            self.setOscam()
        elif self.idxAllFnc == 5:
            self.enaDisKeystart()
        elif self.idxAllFnc == 6:
            self.changeDelay()
        elif self.idxAllFnc == 7:
            self.enaSrvRestart()
        elif self.idxAllFnc == 8:
            self.enaAutochck()
        elif self.idxAllFnc == 9:
            self.killDccamd()
        return

    def selectFnc(self):
        self.idxAllFnc += 1
        if self.idxAllFnc > 9:
            self.idxAllFnc = 0
        self['select_pict'].move(ePoint(self['txt%s' % self.idxAllFnc].instance.position().x() - fhd(30), self['txt%s' % self.idxAllFnc].instance.position().y()))
        self['helpTXT'].setText(self.aa.get(self.idxAllFnc, ''))
        return

    def changeDelay(self):
        self.session.openWithCallback(self.setNewDelay, InputBox, title=_('Please enter Autostart delay (1-30s)') + ': ', text='0' + str(config.plugins.GlassSysUtil.par48.value), maxSize=3, type=Input.NUMBER)
        return

    def setNewDelay(self, answer):
        if answer:
            try:
                answer = int(answer)
            except:
                answer = -1
            else:
                if answer > 0 and answer < 31:
                    config.plugins.GlassSysUtil.par48.value = answer
                    config.plugins.GlassSysUtil.par48.save()
                    configfile.save()
                else:
                    self.session.open(MessageBox, _('Autostart delay have to be in range: 1 - 30'), MessageBox.TYPE_ERROR, 6)
                self.showActDelay()
        return

    def showActDelay(self):
        self['txt6'].setText(_('Autostart delay') + ' (%ss)' % str(config.plugins.GlassSysUtil.par48.value))
        return

    def enaAutochck(self):
        if config.plugins.GlassSysUtil.par50.value:
            config.plugins.GlassSysUtil.par50.value = False
        else:
            config.plugins.GlassSysUtil.par50.value = True
        config.plugins.GlassSysUtil.par50.save()
        configfile.save()
        self.enaAutochckChck()
        return

    def enaAutochckChck(self):
        if config.plugins.GlassSysUtil.par50.value:
            self['txt8'].setText(_('Disable Autocheck CAM/SRV'))
            self['txt8'].colorGreen()
        else:
            self['txt8'].setText(_('Enable Autocheck CAM/SRV'))
            self['txt8'].colorOrange()
        return

    def enaSrvRestart(self):
        if config.plugins.GlassSysUtil.par49.value:
            config.plugins.GlassSysUtil.par49.value = False
        else:
            config.plugins.GlassSysUtil.par49.value = True
        config.plugins.GlassSysUtil.par49.save()
        configfile.save()
        self.enaSrvRestartChck()
        return

    def enaSrvRestartChck(self):
        if config.plugins.GlassSysUtil.par49.value:
            self['txt7'].setText(_('Disable SRV Restart'))
            self['txt7'].colorGreen()
        else:
            self['txt7'].setText(_('Enable SRV Restart'))
            self['txt7'].colorOrange()
        return

    def enaDisKeystart(self):
        if config.plugins.GlassSysUtil.par40.value:
            config.plugins.GlassSysUtil.par40.value = False
        else:
            config.plugins.GlassSysUtil.par40.value = True
        config.plugins.GlassSysUtil.par40.save()
        configfile.save()
        self.enaDisKeystartChck()
        return

    def enaDisKeystartChck(self):
        if config.plugins.GlassSysUtil.par40.value:
            self['txt5'].setText(_('Disable CAM/SRV and ECM Start'))
            self['txt5'].colorGreen()
        else:
            self['txt5'].setText(_('Enable CAM/SRV and ECM Start'))
            self['txt5'].colorOrange()
        return

    def lessCamSrv(self):
        if self.enCommand == False:
            self.statcommPics('comm', 'red')
            self['statCamSrvcmd'].setText(_('Try later ... working'))
            return
        self.session.openWithCallback(self.inicializeUCM, ipk_uninstall_center, 'ucm')
        return

    def moreCamSrv(self):
        if self.enCommand == False:
            self.statcommPics('comm', 'red')
            self['statCamSrvcmd'].setText(_('Try later ... working'))
            return
        (tt, self.wFtp) = chckFtp()
        if tt != '':
            self.session.open(MessageBox, tt, MessageBox.TYPE_ERROR, 6)
            return
        self.session.openWithCallback(self.inicializeUCM, ftp_center, self.wFtp)
        return

    def chckOscam(self):
        self.chckOscamTimer.stop()
        tmp = str(self['config'].getCurrent()[1].getText()).lower()
        if self['config'].getCurrentIndex() == 1 and 'oscam' in tmp and (not ('emu' in tmp or 'dos' in tmp) or ' emu' in tmp):
            self['txt3'].color1()
            self['txt4'].color1()
            self.enaBlue = True
        else:
            self.enaBlue = False
            self['txt3'].color2()
            self['txt4'].color2()
        self.chckOscamTimer.start(500)
        return

    def setLatestOscam(self):
        if self.enCommand == False:
            self.statcommPics('comm', 'red')
            self['statCamSrvcmd'].setText(_('Try later ... working'))
            return
        else:
            if self.checkCam == False:
                self.statcommPics('comm', 'red')
                self['statCamSrvcmd'].setText(_('No Command Allowed'))
                return
            if not self.enaBlue:
                return
            currOsc = None
            all = chckPckgList()
            idx = -1
            if ENA_D:
                idx = -2
            for i in all:
                if i.startswith('glasssysutil-srv.oscam'):
                    i = i.strip().split('-')
                    currOsc = i[idx].strip().split()[0]
                    break

            if not currOsc:
                self.statcommPics('comm', 'red')
                self['statCamSrvcmd'].setText(_('Error detecting current OScam version'))
                return
            (tt, wFtp) = chckFtp()
            if tt != '':
                self.statcommPics('comm', 'red')
                self['statCamSrvcmd'].setText(tt)
                return
            dev = 'x'
            try:
                for x in ('boxtype', 'vumodel', 'model'):
                    if os.path.exists('/proc/stb/info/' + x):
                        dev = open('/proc/stb/info/' + x, 'r').read().strip()
                        dev = dev.lower()
                        break

            except:
                pass

            a = ''
            if XCPU == 'arm' and ('dm9' in dev or 'duo4k' in dev):
                a = '-9x'
            typeProc = XCPU + a
            arch = typeProc in ('arm', 'mips32el', 'aarch64', 'arm-9x')
            filenames = []
            try:
                ftp = ftplib.FTP(wFtp[0])
                ftp.login(wFtp[1], wFtp[2])
                data = []
                if ENA_D and arch:
                    ftp.cwd(TYPE_DIR)
                ftp.cwd(typeProc)
                ftp.dir(data.append)
                for line in data:
                    tmp = re.sub('\\s+', '*', line)
                    tmp = tmp.strip().split('*')
                    if len(tmp) > 8:
                        if '.php' not in line and tmp[8] != '.' and tmp[8] != '..' and ':' in line:
                            idx = line.index(':')
                            zzz = line[idx + 4:]
                            filenames.append(zzz)

                ftp.quit()
            except:
                pass

            if len(filenames) == 0:
                self.statcommPics('comm', 'red')
                self['statCamSrvcmd'].setText(_('No files detected'))
                return
            maxOsc = None
            a = None
            try:
                zzz = currOsc.split('.')
                currOsc = int(zzz[0])
                for x in range(0, len(filenames)):
                    txt = str(filenames[x])
                    if 'glasssysutil-srv.oscam_' in txt:
                        tmp = txt.split('glasssysutil-srv.oscam_')[1].split('_')
                        idx = tmp[0].split('.')
                        if int(idx[0]) > currOsc and idx[1] == zzz[1]:
                            currOsc = int(idx[0])
                            maxOsc = idx[0]
                            a = 'glasssysutil-srv.oscam_%s.%s_%s' % (maxOsc, zzz[1], tmp[1])

            except:
                pass

            if not maxOsc or not a:
                self.statcommPics('comm', 'blue')
                self['statCamSrvcmd'].setText(_('No OScam to Update'))
                return
            if 'srv.oscam_' not in a:
                self.statcommPics('comm', 'red')
                self['statCamSrvcmd'].setText(_('Error to download OScam') + ' %s' % a)
                return
            try:
                ftp = ftplib.FTP(wFtp[0])
                ftp.login(wFtp[1], wFtp[2])
                if ENA_D and arch:
                    ftp.cwd(TYPE_DIR)
                ftp.cwd(typeProc)
                ftp.retrbinary('RETR ' + a, open('/tmp/' + a, 'wb').write)
                ftp.quit()
            except:
                pass

            if not os.path.isfile('/tmp/' + a):
                self.statcommPics('comm', 'red')
                self['statCamSrvcmd'].setText(_('Error to download OScam') + ' %s' % maxOsc)
                return
            system('/usr/UCM_CamSrv_script/Oscam_Srv.sh stop')
            if ENA_D:
                zzz = PKGBIN % a
            else:
                zzz = '%spkg install --force-overwrite --force-downgrade /tmp/%s' % (PKGBIN, a)
            system(zzz)
            self.CamSrvList()
            if self['config'].getCurrentIndex() != 1:
                self['config'].setCurrentIndex(1)
            idx = 0
            while maxOsc not in str(self['config'].getCurrent()[1].getText()) and idx < 30:
                self['config'].handleKey(KEY_RIGHT)
                idx += 1

            if idx > 29:
                self.statcommPics('comm', 'red')
                self['statCamSrvcmd'].setText(_('Error to activate OScam') + ' %s' % maxOsc)
                return
            self.start()
            return

    def setOscam(self):
        if not self.enaBlue:
            return
        self.session.open(oscamLineCfg)
        return

    def chckOscamFiles(self):
        allFiles = [
         'conf', 'server', 'user']
        tmp = ''
        for x in allFiles:
            if os.path.isfile(config.plugins.GlassSysUtil.par17.value + '/oscam.' + x) is False:
                tmp += 'oscam.' + x + ', '

        if tmp != '':
            tmp = tmp[:-2]
        return tmp

    def start(self):
        if self.enCommand == False:
            self.statcommPics('comm', 'red')
            self['statCamSrvcmd'].setText(_('Try later ... working'))
            return
        self.checkCam = self.checkStatCam()
        if self.checkCam == False:
            self.statcommPics('comm', 'red')
            self['statCamSrvcmd'].setText(_('No Command Allowed'))
            return
        if self.numCam == 0 and self['config'].getCurrentIndex() == 0:
            self.statcommPics('stat', 'red')
            self.CamSrvMsg('0 CAM - ' + _('No Command Allowed'))
            return
        if self.checkCam == True and self['config'].getCurrentIndex() == 0:
            self.newCam = self['config'].getCurrent()[1].getText()
            self.Camactive = self.getCamName()
            self.newCamscript = self.Cam_list[self.newCam]
            self.Camactivescript = self.Cam_list[self.Camactive]
            if self.Camactive != _('None') and self.newCam != _('None'):
                if self.Camactive == self.newCam:
                    self.typecmd = False
                    mesg = _('Restarting') + ' CAM ' + self.newCam
                    cmd = '/usr/UCM_CamSrv_script/%s_Cam.sh restart' % self.Camactive
                    self.executeCommand(mesg, cmd, 18000, 'Cam')
                    self.statcommPics('comm', 'yellow')
                    return
                self.typecmd = True
                mesg = _('Stopping') + ' CAM ' + self.Camactive
                cmd = '/usr/UCM_CamSrv_script/%s_Cam.sh stop' % self.Camactivescript
                self.executeCommand(mesg, cmd, 8000, 'Cam')
                self.statcommPics('comm', 'red')
                self.startstopTimer = eTimer()
                try:
                    self.startstopTimer_conn = self.startstopTimer.timeout.connect(self.startCam)
                except:
                    self.startstopTimer.timeout.get().append(self.startCam)
                else:
                    self.startstopTimer.start(5000, True)
                    return
            if self.newCam != _('None'):
                self.typecmd = False
                mesg = _('Starting') + ' CAM ' + self.newCam
                cmd = '/usr/UCM_CamSrv_script/%s_Cam.sh start' % self.newCamscript
                self.executeCommand(mesg, cmd, 15000, 'Cam')
                self.statcommPics('comm', 'green')
            else:
                self.statcommPics('stat', 'yellow')
                self.CamSrvMsg(_('Please Select Cam'))
                return
        if self.numSrv == 0 and self['config'].getCurrentIndex() == 1:
            self.statcommPics('stat', 'red')
            self.CamSrvMsg('0 SRV - ' + _('No Command Allowed'))
            return
        if self.checkCam == True and self['config'].getCurrentIndex() == 1:
            self.Camactive = self.getCamName()
            self.newSrv = self['config'].getCurrent()[1].getText()
            self.Srvactive = self.getSrvName()
            self.newSrvscript = self.Srv_list[self.newSrv]
            self.Srvactivescript = self.Srv_list[self.Srvactive]
            tstO = self.newSrv.lower()
            tt = tstO.split(' ')
            ttX = False
            if len(tt) > 3:
                ttX = tt[len(tt) - 1].isdigit() and tt[len(tt) - 2] == 'emu'
            if 'oscam' in tstO and (not ('emu' in tstO or 'dos' in tstO) or ttX):
                tt = chckOscamScript()
                if tt != '':
                    if config.plugins.GlassSysUtil.par21.value != tt:
                        x = writeOscamCfgPath()
                        if not x:
                            self.CamSrvMsg(_('Detected wrong start cfg, writing new start cfg failed'))
                            self.statcommPics('stat', 'red')
                            return
                    if ttX:
                        tt = '/lib/libcrypto.so.'
                        for x in ('0.9.8', '1.0.2'):
                            if not os.path.exists(tt + x):
                                ttX = False

                        if not ttX:
                            ttX = True
                            for x in ('0.9.8', '1.0.2'):
                                if not os.path.exists('/usr' + tt + x):
                                    ttX = False

                        if not ttX:
                            x = cpLibCr()
                            ttX = os.path.exists(tt + '0.9.8') and os.path.exists(tt + '1.0.2') or os.path.exists('/usr' + tt + '0.9.8') and os.path.exists('/usr' + tt + '1.0.2')
                        if not ttX:
                            self.CamSrvMsg(_('Detected missing files') + ': /lib/libcrypto.so.0.9.8 ' + _('or') + ' /lib/libcrypto.so.1.0.2')
                            self.statcommPics('stat', 'red')
                            return
                    tt = self.chckOscamFiles()
                    if tt != '':
                        self.CamSrvMsg(_('Missing cfg files') + ': ' + tt)
                        self.statcommPics('stat', 'red')
                        return
                else:
                    self.CamSrvMsg(_('Detected wrong script, please use GSU standard script'))
                    self.statcommPics('stat', 'red')
                    return
            if self.Srvactive != _('None') and self.newSrv != _('None'):
                if self.Srvactive == self.newSrv:
                    if not config.plugins.GlassSysUtil.par49.value:
                        if self.Camactive != _('None'):
                            self.CamSrvMsg(_('Before Restart SRV, First Stop CAM'))
                            self.statcommPics('stat', 'red')
                            return
                    self.typecmd = False
                    mesg = _('Restarting') + ' SRV ' + self.newSrv
                    cmd = '/usr/UCM_CamSrv_script/%s_Srv.sh restart' % self.Srvactivescript
                    self.executeCommand(mesg, cmd, 18000, 'Srv')
                    self.statcommPics('comm', 'blue')
                    return
                if self.Camactive != _('None'):
                    self.CamSrvMsg(_('Before Changing SRV, First Stop CAM'))
                    self.statcommPics('stat', 'red')
                    return
                self.typecmd = True
                mesg = _('Stopping') + ' SRV ' + self.Srvactive
                cmd = '/usr/UCM_CamSrv_script/%s_Srv.sh stop' % self.Srvactivescript
                self.executeCommand(mesg, cmd, 8000, 'Srv')
                self.statcommPics('comm', 'red')
                self.startstopTimer = eTimer()
                try:
                    self.startstopTimer_conn = self.startstopTimer.timeout.connect(self.startSrv)
                except:
                    self.startstopTimer.timeout.get().append(self.startSrv)
                else:
                    self.startstopTimer.start(5000, True)
                    return
            if self.newSrv != _('None') and self.Camactive == _('None'):
                self.typecmd = False
                mesg = _('Starting') + ' SRV ' + self.newSrv
                cmd = '/usr/UCM_CamSrv_script/%s_Srv.sh start' % self.newSrvscript
                self.executeCommand(mesg, cmd, 15000, 'Srv')
                self.statcommPics('comm', 'green')
                return
            if self.newSrv != _('None') and self.Camactive != _('None'):
                self.CamSrvMsg(_('Please First Stop CAM'))
                self.statcommPics('stat', 'red')
                return
            if self.newSrv == _('None'):
                self.statcommPics('stat', 'yellow')
                self.CamSrvMsg(_('Please Select SRV'))
                return
        return

    def ChckMsg(self):
        if self.numCam == 0 and self.numSrv == 0:
            self.statcommPics('comm', 'red')
            self.textComm = _('No Scripts Found')
        elif self.CamSrvMsgErr != '                    ':
            self.statcommPics('comm', 'red')
            self.textComm = self.CamSrvMsgErr
        else:
            self.statcommPics('comm', 'green')
            self.textComm = _('BIN Files OK, CAM/SRV Found')
        if len(self.textComm) > 44:
            self.xComm = len(self.textComm) - 45
            self.idxComm = 0
            self.backtextComm = self.textComm
            self.statusComm = 'start'
            self.moveTimerTextComm = eTimer()
            try:
                self.moveTimerTextComm_conn = self.moveTimerTextComm.timeout.connect(self.moveTimerCommRun)
            except:
                self.moveTimerTextComm.timeout.get().append(self.moveTimerCommRun)
            else:
                self.moveTimerTextComm.start(2000)
        else:
            self['statCamSrvcmd'].setText(self.textComm)
        return

    def moveTimerCommRun(self):
        self.moveTimerTextComm.stop()
        if self.xComm > 0:
            txttmpComm = self.backtextComm[self.idxComm:]
            self['statCamSrvcmd'].setText(txttmpComm[:45])
            self.idxComm = self.idxComm + 1
            self.xComm = self.xComm - 1
        if self.xComm == 0:
            self.statusComm = 'end'
            self.textComm = self.backtextComm
            if len(self.textComm) > 45:
                self.textComm = self.textComm[:47] + '...'
                self['statCamSrvcmd'].setText(self.textComm)
        if self.statusComm != 'end':
            self.moveTimerTextComm.start(300)
        return

    def checkStatCam(self):
        stat = False
        if generatePS():
            f = open(A_TM, 'r')
            for z in f.readlines():
                p = str(z).lower()
                if ('mpcs' in p or 'cam' in p or 'gbox' in p or 'mbox' in p or 'newcs' in p) and 'dreambox' not in p and '{' not in p and 'defunct' not in p:
                    if '/usr/ucm_camsrv_bin' in p:
                        self.CamSrvMsg(_('CAM/SRV Running'))
                        self.statcommPics('stat', 'green')
                        f.close()
                        system(RM_A_TMP)
                        return True
                    else:
                        msg = _('Found another Cam running') + ':  ' + str(z) + '  ' + _('Please stop all CAM/SRV before using CAM/SRV') + '                    '
                        self.CamSrvMsg(msg)
                        self.statcommPics('stat', 'red')
                        f.close()
                        system(RM_A_TMP)
                        return False

            f.close()
            system(RM_A_TMP)
        self.CamSrvMsg(_('No Running CAM/SRV'))
        self.statcommPics('stat', 'blue')
        return True

    def killDccamd(self):
        if self.enaYellow:
            return
        if self.chckDccamd():
            if ENA_D:
                system('systemctl stop dccamd')
                system('systemctl disable dccamd')
                system('dpkg -r dccamd')
                tmp = _('Dccamd disabled')
            else:
                tmp = ''
                if fileExists('/usr/bin/dccamd'):
                    try:
                        system('rm -rf /usr/bin/dccamd')
                        if not fileExists('/usr/bin/dccamd'):
                            tmp = '1.' + _('step - OK') + '\n'
                        else:
                            tmp = '1.' + _('step - NOT OK') + '\n'
                    except:
                        tmp = '1.' + _('step - NOT OK') + '\n'

                else:
                    tmp = '1.' + _('step - no needed') + '\n'
                if fileExists('/etc/init.d/dccamd'):
                    try:
                        system('rm -rf /etc/init.d/dccamd')
                        if not fileExists('/etc/init.d/dccamd'):
                            tmp += '2.' + _('step - OK') + '\n'
                        else:
                            tmp += '2.' + _('step - NOT OK') + '\n'
                    except:
                        tmp += '2.' + _('step - NOT OK') + '\n'

                else:
                    tmp += '2.' + _('step - no needed') + '\n'
                try:
                    system('rm -rf /etc/rcS.d/S15dccamd')
                    tmp += '3.' + _('step - OK') + '\n'
                except:
                    tmp += '3.' + _('step - NOT OK') + '\n'

                tmp += '\n\n' + _('Please hard restart your box to finishing operation')
            self.session.open(MessageBox, tmp, MessageBox.TYPE_INFO, 4)
            self['txt9'].color2()
            self.enaYellow = True
        if not os.path.exists('/usr/keys'):
            x = self.doLnk('/var/keys', '/usr/keys')
            self.session.open(MessageBox, '(/var/keys -> /usr/keys) ' + _('Symlink created'), MessageBox.TYPE_INFO, 4)
            self['txt9'].color2()
            self.enaYellow = True
        if not os.path.exists('/var/etc'):
            x = self.doLnk('/var/etc', '/etc')
            self.session.open(MessageBox, '(/var/etc -> /etc) ' + _('Symlink created'), MessageBox.TYPE_INFO, 4)
            self['txt9'].color2()
            self.enaYellow = True
        return

    def doLnk(self, what, what1):
        try:
            allLines = ''
            isLnk = True
            flag = False
            fileName = ''
            if fileExists('/etc/init.d/bootup'):
                fileName = '/etc/init.d/bootup'
            elif fileExists('/etc/init.d/bootmisc.sh'):
                fileName = '/etc/init.d/bootmisc.sh'
            if fileName != '':
                r = open(fileName, 'r')
                for line in r.readlines():
                    if not line.__contains__('exit 0'):
                        allLines = allLines + line
                        flag = True
                    if line.__contains__(what) and line.__contains__(what1):
                        isLnk = False

                r.close()
                if isLnk:
                    allLines += '\nln -sfn %s %s' % (what1, what)
                    if flag:
                        allLines += '\n: exit 0\n'
                    r = open(fileName, 'w')
                    r.write(allLines)
                    r.close()
            system('mkdir %s' % what1)
            system('ln -sfn %s %s' % (what1, what))
        except:
            pass

        return True

    def chckDccamd(self):
        isDc = False
        if generatePS():
            f = open(A_TM, 'r')
            for z in f.readlines():
                proc = str(z)
                if 'dccamd' in proc or 'Dccamd' in proc or 'dcCamd' in proc:
                    isDc = True
                    break

            f.close()
            system(RM_A_TMP)
        return isDc

    def inicializeUCM(self, answer=True):
        self.showActDelay()
        self.enaDisKeystartChck()
        self.enaSrvRestartChck()
        self.enaAutochckChck()
        self.CamSrvList()
        self.chckOscamTimer.start(500)
        service = self.session.nav.getCurrentService()
        if not service:
            self['CAID_info'] = Label(_('No CAID Info'))
        info = service and service.info()
        if info is not None:
            ref = eServiceReference(info.getInfoString(iServiceInformation.sServiceref))
            if ref is not None:
                ref = ref.toString()
                if ref.startswith('-1:'):
                    ref = self.session.nav.getCurrentlyPlayingServiceReference()
                    if ref is not None:
                        ref = ref.toString()
            tmp = alternative(ref).split(':', 10)[:10]
            sname = ('_').join(tmp)
            self['picchannel'].instance.setPixmapFromFile(resPicon(sname, 'picon'))
            enaIp = sname.startswith('4097_0') or '3a//' in sname or 'http' in sname
            if enaIp:
                sname = 'STREAM'
            else:
                provname = getServiceInfoValue(info, iServiceInformation.sProvider, None)
                if provname.startswith('T-K'):
                    sname = 'T-KABEL'
                elif provname == 'T-Systems/MTI':
                    sname = 'T-SYSTEMS'
                else:
                    sname = provname.upper()
            self['picprov'].instance.setPixmapFromFile(resPicon(sname, 'piconProv'))
            if enaIp:
                sname = 'IPTV'
            else:
                sname = getTunerPiconInfo(service)
            self['picsat'].instance.setPixmapFromFile(resPicon(sname, 'piconSat'))
        self['txt4'].color2()
        self['txt9'].color2()
        if self.chckDccamd():
            self['txt9'].color1()
            self.enaYellow = False
        if not os.path.exists('/usr/keys'):
            self['txt9'].color1()
            self.enaYellow = False
        if not os.path.exists('/var/etc'):
            self['txt9'].color1()
            self.enaYellow = False
        return

    def CamSrvMsg(self, msg):
        self.enCommand = True
        self.text = msg
        if len(self.text) > 28:
            self.x = len(self.text) - 27
            self.idx = 0
            self.backtext = self.text
            self.status = 'start'
            self.moveTimerText = eTimer()
            try:
                self.moveTimerText_conn = self.moveTimerText.timeout.connect(self.moveTimerTextRun)
            except:
                self.moveTimerText.timeout.get().append(self.moveTimerTextRun)
            else:
                self.moveTimerText.start(2000)
        else:
            self['statCamSrvbin'].setText(self.text)
        return

    def moveTimerTextRun(self):
        self.moveTimerText.stop()
        if self.x > 0:
            txttmp = self.backtext[self.idx:]
            self['statCamSrvbin'].setText(txttmp[:27])
            self.idx = self.idx + 1
            self.x = self.x - 1
        if self.x == 0:
            self.status = 'end'
            self.text = self.backtext
            if len(self.text) > 27:
                self.text = self.text[:29] + '...'
                self['statCamSrvbin'].setText(self.text)
        if self.status != 'end':
            self.moveTimerText.start(300)
        return

    def stop(self):
        if self.enCommand == False:
            self.statcommPics('comm', 'red')
            self['statCamSrvcmd'].setText(_('Try later ... working'))
            return
        self.checkCam = self.checkStatCam()
        if self.checkCam == False:
            self.statcommPics('comm', 'red')
            self['statCamSrvcmd'].setText(_('No Command Allowed'))
            return
        if self.numCam == 0 and self['config'].getCurrentIndex() == 0:
            self.statcommPics('stat', 'blue')
            self.CamSrvMsg('0 CAM - ' + _('No Command Allowed'))
            return
        if self.checkCam == True and self['config'].getCurrentIndex() == 0:
            self.newCam = self['config'].getCurrent()[1].getText()
            self.Camactive = self.getCamName()
            self.Camactivescript = self.Cam_list[self.Camactive]
            if self.Camactive != _('None') and self.Camactive == self.newCam:
                self.typecmd = True
                mesg = _('Stopping') + ' CAM ' + self.Camactive
                cmd = '/usr/UCM_CamSrv_script/%s_Cam.sh stop' % self.Camactivescript
                self.executeCommand(mesg, cmd, 8000, 'Cam')
                self.statcommPics('comm', 'red')
            else:
                self.statcommPics('stat', 'yellow')
                self.CamSrvMsg(_('Please Select Running') + ' CAM')
        if self.numSrv == 0 and self['config'].getCurrentIndex() == 1:
            self.statcommPics('stat', 'blue')
            self.CamSrvMsg('0 SRV - ' + _('No Command Allowed'))
            return
        if self.checkCam == True and self['config'].getCurrentIndex() == 1:
            self.newSrv = self['config'].getCurrent()[1].getText()
            self.Srvactive = self.getSrvName()
            self.Srvactivescript = self.Srv_list[self.Srvactive]
            if self.Srvactive != _('None') and self.Srvactive == self.newSrv:
                self.typecmd = True
                mesg = _('Stopping') + ' SRV ' + self.Srvactive
                cmd = '/usr/UCM_CamSrv_script/%s_Srv.sh stop' % self.Srvactivescript
                self.executeCommand(mesg, cmd, 8000, 'Srv')
                self.statcommPics('comm', 'red')
            else:
                self.statcommPics('stat', 'yellow')
                self.CamSrvMsg(_('Please Select Running') + ' Srv')
        return

    def keyLeft(self):
        self['config'].handleKey(KEY_LEFT)
        return

    def keyRight(self):
        self['config'].handleKey(KEY_RIGHT)
        return

    def exit(self):
        if self.enCommand == False:
            self.statcommPics('comm', 'red')
            self['statCamSrvcmd'].setText(_('Try later ... working'))
            return
        else:
            if self.EcmInfoTimer.isActive():
                self.EcmInfoTimer.stop()
            self.EcmInfoTimer = None
            if self.chckOscamTimer.isActive():
                self.chckOscamTimer.stop()
            self.chckOscamTimer = None
            self.FirstInfoTimer = None
            if self.keyState != config.plugins.GlassSysUtil.par40.value:
                restartbox = self.session.openWithCallback(self.rstAnswer, MessageBox, _('Do you want restart GUI to activate keystart change now?'), MessageBox.TYPE_YESNO)
                restartbox.setTitle(_('Restart'))
            else:
                self.setCamSrvinfoTimer = None
                self.refreshinfoTimer = None
                self.close()
            return

    def rstAnswer(self, answer):
        Rst_E2(answer)
        self.close()
        return

    def startCam(self):
        self.startstopTimer.stop()
        self.typecmd = False
        mesg = _('Starting') + ' CAM ' + self.newCam
        cmd = '/usr/UCM_CamSrv_script/%s_Cam.sh start' % self.newCamscript
        self.executeCommand(mesg, cmd, 18000, 'Cam')
        self.statcommPics('comm', 'green')
        return

    def startSrv(self):
        self.startstopTimer.stop()
        self.typecmd = False
        mesg = _('Starting') + ' SRV ' + self.newSrv
        cmd = '/usr/UCM_CamSrv_script/%s_Srv.sh start' % self.newSrvscript
        self.executeCommand(mesg, cmd, 18000, 'Srv')
        self.statcommPics('comm', 'green')
        return

    def executeCommand(self, mesg, cmd, waitime, typeCamSrv):
        self.enCommand = False
        self.typeCamSrv = typeCamSrv
        self['statCamSrvcmd'].setText(mesg)
        if typeCamSrv == 'Cam':
            self['activCam'].setText('CAM ' + _('Wait for Info'))
            self.statcommPics('piccam', 'white')
        else:
            self['activSrv'].setText('SRV ' + _('Wait for Info'))
            self.statcommPics('picsrv', 'white')
        self.scriptexecute = eConsoleAppContainer()
        self.scriptexecute.execute(cmd)
        self.refreshinfoTimer = eTimer()
        try:
            self.refreshinfoTimer_conn = self.refreshinfoTimer.timeout.connect(self.refreshinfo)
        except:
            self.refreshinfoTimer.timeout.get().append(self.refreshinfo)

        self.refreshinfoTimer.start(waitime, True)
        return

    def refreshMsgScriptInfo(self):
        if not self.typecmd:
            if not self.isStartedCamSrv():
                if self.typeCamSrv == 'Cam':
                    msg = self.newCam + ' ' + _('not started, please check config files or atributes') + '              '
                    self['statCamSrvbin'].setText(self.newCam + ' ' + _('Error'))
                else:
                    msg = self.newSrv + ' ' + _('not started, please check config files or atributes') + '              '
                    self['statCamSrvbin'].setText(self.newSrv + ' ' + _('Error'))
            else:
                msg = _(self.getMsgInfo())
        else:
            msg = _(self.getMsgInfo())
        if msg == _('No Script Message'):
            self.statcommPics('stat', 'white')
        elif msg == _('Start Script Executed') or msg == _('Restart Script Executed'):
            self.statcommPics('stat', 'green')
        elif msg == _('Stop Script Executed'):
            self.statcommPics('stat', 'yellow')
        else:
            self.statcommPics('stat', 'red')
        self.setCamSrvinfoTimer = eTimer()
        try:
            self.setCamSrvinfoTimer_conn = self.setCamSrvinfoTimer.timeout.connect(self.setCamSrvinfo)
        except:
            self.setCamSrvinfoTimer.timeout.get().append(self.setCamSrvinfo)

        self.setCamSrvinfoTimer.start(4000)
        self.CamSrvMsg(msg)
        return

    def isStartedCamSrv(self):
        stmp = ''
        if self.typeCamSrv == 'Cam':
            what = '/usr/UCM_CamSrv_script/%s_Cam.sh' % self.newCamscript
        else:
            what = '/usr/UCM_CamSrv_script/%s_Srv.sh' % self.newSrvscript
        try:
            f = open(what, 'r')
            c = f.readlines()
            f.close()
        except:
            c = ''

        for line in c:
            if line.startswith('SrvBin=') or line.startswith('CamBin='):
                stmp = '/usr/UCM_CamSrv_bin/' + line.split('=')[1][:-1]
                break

        state = False
        if generatePS():
            f = open(A_TM, 'r')
            for z in f.readlines():
                proc = str(z)
                if stmp in proc:
                    state = True
                    break

            f.close()
            system(RM_A_TMP)
        if state:
            return True
        cmd = '%s stop' % what
        self.scriptexecute = eConsoleAppContainer()
        self.scriptexecute.execute(cmd)
        return False

    def setCamSrvinfo(self):
        self.setCamSrvinfoTimer.stop()
        actem = _('Active') + ' CAM: ' + self.getCamName()
        self['activCam'].setText(actem)
        if _('None') in actem:
            self.statcommPics('piccam', 'blue')
        else:
            self.statcommPics('piccam', 'green')
        actem = _('Active') + ' SRV: ' + self.getSrvName()
        if _('None') in actem:
            self.statcommPics('picsrv', 'blue')
        else:
            self.statcommPics('picsrv', 'green')
        self['activSrv'].setText(actem)
        return

    def refreshinfo(self):
        self['statCamSrvcmd'].setText(_('No Command Active'))
        self.statcommPics('comm', 'white')
        self.refreshMsgScriptInfo()
        return

    def CamSrvList(self):
        self.CamSrvMsgErr = ''
        Cam = []
        Cam.append(_('None'))
        self.Cam_list = {}
        self.Cam_list[_('None')] = _('None')
        Srv = []
        Srv.append(_('None'))
        self.Srv_list = {}
        self.Srv_list[_('None')] = _('None')
        f = listDir('/usr/UCM_CamSrv_script')
        if f:
            for x in f:
                if '_Cam.sh' in x:
                    CamName = self.readCamName(x[:-7])
                    CamBinStatus = self.checkCamBin(x[:-7])
                    if CamBinStatus != 'Ok':
                        self.CamSrvMsgErr += CamBinStatus
                    else:
                        Cam.append(CamName)
                        self.Cam_list[CamName] = x[:-7]
                elif '_Srv.sh' in x:
                    SrvName = self.readSrvName(x[:-7])
                    SrvBinStatus = self.checkSrvBin(x[:-7])
                    if SrvBinStatus != 'Ok':
                        self.CamSrvMsgErr += SrvBinStatus
                    else:
                        Srv.append(SrvName)
                        self.Srv_list[SrvName] = x[:-7]

        selCam = ConfigSelection(default=self.getCamName(), choices=Cam)
        selSrv = ConfigSelection(default=self.getSrvName(), choices=Srv)
        self.numCam = len(Cam) - 1
        self.numSrv = len(Srv) - 1
        self.list = []
        self.list.append(getConfigListEntry(_('CAMs') + ' (%s): ' % str(self.numCam), selCam))
        self.list.append(getConfigListEntry(_('SRVs') + ' (%s): ' % str(self.numSrv), selSrv))
        self['config'].list = self.list
        self['config'].l.setList(self.list)
        self.CamSrvMsgErr += '                    '
        return

    def checkSrvBin(self, srv):
        try:
            f = open('/usr/UCM_CamSrv_script/' + srv + '_Srv.sh', 'r')
            for line in f.readlines():
                if line.startswith('SrvBin='):
                    f.close()
                    stmp = '/usr/UCM_CamSrv_bin/%s' % line.split('=')[1][:-1]
                    if fileExists(stmp):
                        return 'Ok'
                    return srv + '_Srv.sh ' + _('Missing BIN')

            f.close()
            return srv + '_Srv.sh ' + _('Undefined BIN')
        except:
            return srv + '_Srv.sh ' + _('Error Reading Script')

        return

    def checkCamBin(self, srv):
        try:
            f = open('/usr/UCM_CamSrv_script/' + srv + '_Cam.sh', 'r')
            for line in f.readlines():
                if line.startswith('CamBin='):
                    ctmp = line.split('=')[1][:-1]
                    f.close()
                    ctmp = '/usr/UCM_CamSrv_bin/%s' % ctmp
                    if fileExists(ctmp):
                        return 'Ok'
                    return srv + '_Cam.sh ' + _('Missing BIN')

            f.close()
            return srv + '_Cam.sh ' + _('Undefined BIN')
        except:
            return srv + '_Cam.sh ' + _('Error Reading Script')

        return

    def readSrvName(self, srv):
        try:
            f = open('/usr/UCM_CamSrv_script/' + srv + '_Srv.sh', 'r')
            for line in f.readlines():
                if line.startswith('SrvName='):
                    stmp = line.split('=')[1][:-1]
                    stmp = stmp[:-1]
                    stmp = stmp[1:]
                    f.close()
                    return stmp

            f.close()
            return srv
        except:
            return _('None')

        return

    def getSrvName(self):
        try:
            f = open('/tmp/ucm_srv.info', 'r')
            content = f.read()
            f.close()
        except:
            content = ''

        contentInfo = content[:-1]
        if content != '':
            return contentInfo
        return _('None')

    def getMsgInfo(self):
        try:
            f = open('/tmp/msg.info', 'r')
            content = f.read()
            f.close()
        except:
            content = ''

        contentInfo = content[:-1]
        if content != '':
            return contentInfo
        return 'No Script Message'

    def readCamName(self, cam):
        try:
            f = open('/usr/UCM_CamSrv_script/' + cam + '_Cam.sh', 'r')
            for line in f.readlines():
                if line.startswith('CamName='):
                    ctmp = line.split('=')[1][:-1]
                    ctmp = ctmp[:-1]
                    ctmp = ctmp[1:]
                    f.close()
                    return ctmp

            f.close()
            return cam
        except:
            return _('None')

        return

    def getCamName(self):
        try:
            f = open('/tmp/ucm_cam.info', 'r')
            content = f.read()
            f.close()
        except:
            content = ''

        contentInfo = content[:-1]
        if content != '':
            return contentInfo
        return _('None')

    def firstInfo(self):
        self.FirstInfoTimer.stop()
        self.enCommand = True
        self.checkCam = self.checkStatCam()
        actem = _('Active') + ' CAM: '
        if self.checkCam == True:
            actem += self.getCamName()
            self['activCam'].setText(actem)
            if _('None') in actem:
                self.statcommPics('piccam', 'blue')
            else:
                self.statcommPics('piccam', 'green')
        else:
            actem += _('None')
            self['activCam'].setText(actem)
            self.statcommPics('piccam', 'red')
        actem = _('Active') + ' SRV: '
        if self.checkCam == True:
            actem += self.getSrvName()
            self['activSrv'].setText(actem)
            if _('None') in actem:
                self.statcommPics('picsrv', 'blue')
            else:
                self.statcommPics('picsrv', 'green')
        else:
            actem += _('None')
            self['activSrv'].setText(actem)
            self.statcommPics('picsrv', 'red')
        self.ChckMsg()
        self.EcmInfoTimer.start(5000, True)
        service = self.session.nav.getCurrentService()
        self.fta = False
        if service:
            info = service and service.info()
            if info:
                actem = self.getCaidInfo(info)
                self['CAID_info'].setText(actem)
                if not (info.getInfo(iServiceInformation.sIsCrypted) and actem != _('No CA info available')):
                    self.fta = True
                    self['fullEcmLine'].setText('***    ' + _('Free To Air') + '    ***')
                    pngName = findPicon('Fta-fs8', 'piconCam')
                    if pngName == '':
                        pngName = BP_ICO % 'ca_small/Fta-fs8'
                    self['picECM'].instance.setPixmapFromFile(pngName)
        self.showEcmInfo()
        return

    def showEcmInfo(self):
        self.EcmInfoTimer.stop()
        if self.fta:
            return
        (oscVer, typecam, system, caid, provider, provid, pid, using, adress, hops, share, ecmTime, coding, dcw0, dcw1) = ECMparser()
        tmpline = ''
        if using == 'unsupported CAs\n':
            self['fullEcmLine'].setText('***    ' + _('Unsuported CA found, incorrect ECM info') + '    ***')
            coding = 'Unknown'
        elif typecam == '..............\n' and system == '..............\n' and caid == '..............\n' and provider == '..............\n' and provid == '..............\n' and pid == '..............\n' and using == '..............\n' and adress == '..............\n' and hops == '..............\n' and share == '..............\n' and ecmTime == '..............\n':
            self['fullEcmLine'].setText('***    ' + _('No Info from CAM/SRV') + '    ***')
            coding = 'Unknown'
        elif caid != '..............\n':
            tmpline = tmpline + 'CAID: ' + caid[:-1]
        if provider != '..............\n':
            tmpline = tmpline + ' ... Provider: ' + provider[:-1]
        if provid != '..............\n':
            tmpline = tmpline + ' ... ProvID: ' + provid[:-1]
        if pid != '..............\n':
            tmpline = tmpline + ' ... PID: ' + pid[:-1]
        if using != '..............\n':
            tmpline = tmpline + ' ... Using: ' + using[:-1]
        if adress != '..............\n':
            tmpline = tmpline + ' ... Address: ' + adress[:-1]
        if hops != '..............\n':
            tmpline = tmpline + ' ... Hops: ' + hops[:-1]
        if ecmTime != '..............\n':
            tmpline = tmpline + ' ... ECM Time: ' + ecmTime[:-1]
        if config.plugins.GlassSysUtil.par83.value != '':
            tmpline = tmpline.replace(config.plugins.GlassSysUtil.par83.value, 'CHID:')
        self['fullEcmLine'].setText(tmpline)
        pngName = findPicon(coding + '-fs8', 'piconCam')
        if pngName == '':
            pngName = BP_ICO % 'ca_small/Unknown-fs8'
        self['picECM'].instance.setPixmapFromFile(pngName)
        self.EcmInfoTimer.start(5000, True)
        return

    def getCaidInfo(self, info):
        cainfo = _('Available CAIDs') + ': '
        caids = info.getInfoObject(iServiceInformation.sCAIDs)
        if caids:
            if len(caids) > 0:
                for caid in caids:
                    cainfo += '%0.4X' % caid + '  '

                return cainfo
        return _('No CA info available')

    def statcommPics(self, statcom, selpic):
        pngname = BP_ICO % selpic
        if fileExists(pngname):
            if statcom == 'stat':
                self['statPic'].instance.setPixmapFromFile(pngname)
                self['statPic'].show()
            if statcom == 'comm':
                self['commPic'].instance.setPixmapFromFile(pngname)
                self['commPic'].show()
            if statcom == 'piccam':
                self['CamPic'].instance.setPixmapFromFile(pngname)
                self['CamPic'].show()
            if statcom == 'picsrv':
                self['SrvPic'].instance.setPixmapFromFile(pngname)
                self['SrvPic'].show()
        elif statcom == 'stat':
            self['statPic'].hide()
        if statcom == 'comm':
            self['commPic'].hide()
        if statcom == 'piccam':
            self['CamPic'].hide()
        if statcom == 'picsrv':
            self['SrvPic'].hide()
        return


class AutoCams():

    def __init__(self):
        self.cmd = ''
        return

    def autoStartCheck(self, session):
        self.session = session
        if not fileExists(PYTHONPATH + 'Plugins/Extensions/GlassBluePanel/plugin.pyo'):
            self.firstautostart = False
            self.startCamSrvTimer_UCM = eTimer()
            try:
                self.startCamSrvTimer_UCM_conn = self.startCamSrvTimer_UCM.timeout.connect(self.startCamSrv)
            except:
                self.startCamSrvTimer_UCM.timeout.get().append(self.startCamSrv)
            else:
                self.startCamSrvTimer_UCM.startLongTimer(int(config.plugins.GlassSysUtil.par48.value))
                self.isAutoStartedCamSrvTimer = eTimer()
                try:
                    self.isAutoStartedCamSrvTimer_conn = self.isAutoStartedCamSrvTimer.timeout.connect(self.isAutoStartedCamSrv)
                except:
                    self.isAutoStartedCamSrvTimer.timeout.get().append(self.isAutoStartedCamSrv)

        else:
            self.startCamSrvEvent('clean.sh', 2)
        if config.plugins.GlassSysUtil.par57.value != '0':
            self.cifsNfsTimer = eTimer()
            try:
                self.cifsNfsTimer_conn = self.cifsNfsTimer.timeout.connect(self.chckCifsNfs)
            except:
                self.cifsNfsTimer.timeout.get().append(self.chckCifsNfs)
            else:
                self.chckCifsNfs()
        return

    def chckCifsNfs(self):
        self.cifsNfsTimer.stop()
        msg = fromFile2()
        self.cifsNfsTimer.startLongTimer(config.plugins.GlassSysUtil.par58.value * 60)
        return

    def startCamSrv(self):
        self.startCamSrvTimer_UCM.stop()
        if not config.plugins.GlassSysUtil.par50.value and self.firstautostart:
            self.startCamSrvTimer_UCM.startLongTimer(600)
            return
            if fileExists(GSU_PATH + 'Auto_start/' + 'Oscam_Srv.sh'):
                tmp = chckOscamScript()
                if tmp != '':
                    if config.plugins.GlassSysUtil.par21.value != tmp:
                        if not writeOscamCfgPath():
                            self.startCamSrvEvent('clean.sh', 2)
                else:
                    self.startCamSrvEvent('clean.sh', 2)
            self.CamScript = ''
            SrvScript = ''
            f = listDir(GSU_PATH + 'Auto_start')
            if f:
                for x in f:
                    if '_Cam.sh' in x:
                        self.CamScript = self.CheckbinCamSrv(x)
                    elif '_Srv.sh' in x:
                        SrvScript = self.CheckbinCamSrv(x)

            if self.firstautostart or self.checkRunningCam():
                if SrvScript != '':
                    self.nameCamSrv = self.readSrvName(SrvScript)
                    self.typeScript = SrvScript
                    self.startCamSrvEvent(SrvScript, 0)
                    if self.CamScript != '':
                        self.startCamTimer1 = eTimer()
                        try:
                            self.startCamTimer1_conn = self.startCamTimer1.timeout.connect(self.startCam1)
                        except:
                            self.startCamTimer1.timeout.get().append(self.startCam1)
                        else:
                            self.startCamTimer1.start(15000, True)
                elif self.CamScript != '':
                    self.startCamSrvEvent(self.CamScript, 1)
        elif SrvScript != '':
            self.typeScript = SrvScript
            if not self.isAutoStartedCamSrv():
                self.startCamSrvEvent(SrvScript, 0)
        if self.CamScript != '':
            self.typeScript = self.CamScript
            if not self.isAutoStartedCamSrv():
                self.startCamSrvEvent(self.CamScript, 1)
        if not self.firstautostart:
            self.firstautostart = True
        self.startCamSrvTimer_UCM.startLongTimer(600)
        return

    def CheckbinCamSrv(self, what):
        try:
            f = open(GSU_PATH + 'Auto_start/' + what, 'r')
            for line in f.readlines():
                if line.startswith('SrvBin=') or line.startswith('CamBin='):
                    stmp = '/usr/UCM_CamSrv_bin/%s' % line.split('=')[1][:-1]
                    f.close()
                    if fileExists(stmp):
                        return what
                    self.startCamSrvEvent('clean.sh', 2)
                    return ''

            f.close()
        except:
            IOError

        self.startCamSrvEvent('clean.sh', 2)
        return ''

    def startCam1(self):
        self.startCamTimer1 = None
        self.startCamSrvEvent(self.CamScript, 1)
        return

    def startCamSrvEvent(self, script, sw):
        if sw == 1:
            self.nameCamSrv = self.readCamName(script)
            self.typeScript = self.CamScript
        if sw == 1 or sw == 0:
            cmd = GSU_PATH + 'Auto_start/%s start' % script
            if not self.firstautostart:
                self.isAutoStartedCamSrvTimer.start(9000, True)
        elif sw == 3:
            cmd = script
        else:
            cmd = GSU_PATH + 'Auto_start/%s' % script
        self.scriptexecuteAuto = eConsoleAppContainer()
        self.scriptexecuteAuto.execute(cmd)
        return

    def isAutoStartedCamSrv(self):
        self.isAutoStartedCamSrvTimer.stop()
        stmp = ''
        what = '/usr/UCM_CamSrv_script/%s' % self.typeScript
        try:
            f = open(what, 'r')
            c = f.readlines()
            f.close()
        except:
            c = ''

        for line in c:
            if line.startswith('SrvBin=') or line.startswith('CamBin='):
                stmp = '/usr/UCM_CamSrv_bin/%s' % line.split('=')[1][:-1]
                break

        stat = False
        if generatePS():
            f = open(A_TM, 'r')
            for z in f.readlines():
                proc = str(z)
                if stmp in proc:
                    stat = True
                    break

            f.close()
            system(RM_A_TMP)
        if self.firstautostart:
            return stat
        else:
            if stat:
                return
            cmd = '%s stop' % what
            self.startCamSrvEvent('clean.sh', 2)
            self.startCamSrvEvent(cmd, 3)
            return
        return

    def readSrvName(self, srv):
        try:
            f = open(GSU_PATH + 'Auto_start/' + srv, 'r')
            for line in f.readlines():
                if line.startswith('SrvName='):
                    stmp = line.split('=')[1][:-1]
                    stmp = stmp[:-1]
                    stmp = stmp[1:]
                    f.close()
                    return stmp

            f.close()
            return srv
        except:
            return 'None'

        return

    def readCamName(self, cam):
        try:
            f = open(GSU_PATH + 'Auto_start/' + cam, 'r')
            for line in f.readlines():
                if line.startswith('CamName='):
                    ctmp = line.split('=')[1][:-1]
                    ctmp = ctmp[:-1]
                    ctmp = ctmp[1:]
                    f.close()
                    return ctmp

            f.close()
            return cam
        except:
            return 'None'

        return

    def checkRunningCam(self):
        msg = True
        if generatePS():
            f = open(A_TM, 'r')
            for z in f.readlines():
                p = str(z).lower()
                if ('mpcs' in p or 'cam' in p or 'gbox' in p or 'mbox' in p or 'newcs' in p) and 'dreambox' not in p and '{' not in p and 'defunct' not in p:
                    if '/usr/ucm_camsrv_bin' in p:
                        msg = False
                        break
                    else:
                        msg = False
                        self.startCamSrvEvent('clean.sh', 2)
                        break

            f.close()
            system(RM_A_TMP)
        return msg


autocams = AutoCams()

class ipk_script_center(Screen):

    def __init__(self, session):
        self.skin = ipkScript_center
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.menuListAll = [('0', _('User scripts'), _('Starting user script, but have to be named: xxxx_user.sh and have to be placed in /usr/script')),
         (
          '1', _('IPK package install'), _('Installing ipk file, have to be placed in /tmp')),
         (
          '2', _('IPK package uninstall'), _('Uninstalling IPK package listed after autoscan all IPK packages')),
         (
          '3', _('TAR package install'), _('Installing GZ, BZ2 package, have to be placed in /tmp')),
         (
          '4', _('DEB package install'), _('Installing DEB file, have to be placed in /tmp')),
         (
          '5', _('DEB package uninstall'), _('Uninstalling DEB package listed after autoscan all DEB packages'))]
        self.status = {}
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['descriptions'] = Label()
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit), 
           'back': (self.exit)})
        self.onLayoutFinish.append(self.updatemenulist)
        return

    def selectedmenuitem(self):
        selectedItem = self['list'].getCurrent()[0]
        enabledItem = self.status.get(selectedItem)
        if enabledItem:
            if selectedItem == '0':
                self.session.open(script_center)
            elif selectedItem == '1':
                self.session.open(ipk_center)
            elif selectedItem in ('2', '5'):
                self.session.open(ipk_uninstall_center)
            elif selectedItem == '3':
                self.session.open(tar_center)
            elif selectedItem == '4':
                self.session.open(ipk_center, 'deb')
        return

    def updatemenulist(self):
        self.list = []
        icon_path = GSU_PATH + {3: 'uhd/icons/', 1.5: 'fhd/icons/', 1: 'icons/'}[FHD]
        for x in self.menuListAll:
            item = [
             x[0]]
            self.status[x[0]] = True
            if x[0] in ('4', '5') and not ENA_D or x[0] in ('1', '2') and ENA_D:
                self.status[x[0]] = False
            item = [
             x[0]]
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=x[1], color_sel=int({True: '0x00d100', False: '0xd10000'}[self.status.get(x[0])], 16), color=int({True: '0xffffff', False: '0x666666'}[self.status.get(x[0])], 16)))
            pix = LoadPixmap({True: (BP_ICO % 'green'), False: (BP_ICO % 'red')}[self.status.get(x[0])])
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(20), fhd(16)), png=pix))
            self.list.append(item)

        self['list'].l.setList(self.list)
        self.setTitle(_('IPK/DEB and User Scripts'))
        return

    def exit(self):
        self.close()
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            tmp2 = int(selection[0])
            tmp = str(self.menuListAll[tmp2][2])
            self['descriptions'].setText(tmp)
        return


class script_center(Screen):

    def __init__(self, session):
        self.skin = Script_center_scr
        Screen.__init__(self, session)
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['descriptions'] = Label()
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.updateList)
        return

    def selectedmenuitem(self):
        cmd = self['list'].getCurrent()[0]
        try:
            if cmd[0] != 'None':
                self.runCmd('/usr/script/' + cmd[0] + '_user.sh')
        except:
            pass

        return

    def updateList(self):
        del self.list[:]
        self.desc = {}
        f = listDir('/usr/script')
        if f:
            for x in f:
                if '_user.sh' in x:
                    (scriptName, description) = self.scriptNameDesc(x[:-8])
                    self.desc[scriptName] = (x[:-8], description)

            if len(self.desc) != 0:
                k = list(self.desc.keys())
                k.sort()
                for x in k:
                    item = [
                     (
                      self.desc[x][0], x)]
                    item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=x))
                    self.list.append(item)

        if len(self.list) == 0:
            self.desc['None'] = ('None', ' ')
            item = [('None', 'None')]
            item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=_('No Users Script Found')))
            self.list.append(item)
        self['list'].l.setList(self.list)
        self.setTitle(_('User scripts'))
        return

    def runCmd(self, cmd):
        if cmd is not None:
            self.session.open(Console, title=_('Executing script: ') + cmd, cmdlist=[cmd])
        return

    def scriptNameDesc(self, name):
        ll = {'Netstate': (_('Netstate')), 'Show Active Internet connections and Active UNIX domain sockets': (_('Show Active Internet connections and Active UNIX domain sockets')), 'Restore SD card': (_('Restore SD card')), 'Restore SD card /media/cf from /media/hdd/cf-backup.tar': (_('Restore SD card /media/cf from /media/hdd/cf-backup.tar')), 
           'Network Interfaces': (_('Network Interfaces')), 
           'Show Network Interfaces': (_('Show Network Interfaces')), 
           'Uptime': (_('Uptime')), 
           'Show Uptime your box': (_('Show Uptime your box')), 
           'Backup SD card': (_('Backup SD card')), 
           'Backup SD card /media/cf to /media/hdd/cf-backup.tar': (_('Backup SD card /media/cf to /media/hdd/cf-backup.tar')), 
           'Backup dir DATA': (_('Backup dir DATA')), 
           'Backup dir /data to /media/hdd/data-backup.tar': (_('Backup dir /data to /media/hdd/data-backup.tar')), 
           'Restore dir DATA': (_('Restore dir DATA')), 
           'Restore dir /data from /media/hdd/data-backup.tar': (_('Restore dir /data from /media/hdd/data-backup.tar'))}
        desc = '............................'
        try:
            f = open('/usr/script/' + name + '_user.sh', 'r')
            for line in f.readlines():
                if line.find('#scriptname=') >= 0 or line.find('#ScriptName=') >= 0:
                    name = line.split('=')[1].replace('\n', '').strip()
                if line.find('#description=') >= 0 or line.find('#DESCRIPTION=') >= 0:
                    desc = line.split('=')[1].replace('\n', '').strip()

            f.close()
            return (ll.get(name, name), ll.get(desc, desc))
        except:
            return (
             name, desc)

        return

    def reactivate(self):
        s = self['list'].getCurrent()[0]
        if s:
            self['descriptions'].setText(self.desc[s[1]][1])
        return


class ipk_center(Screen):

    def __init__(self, session, pkg_type='ipk'):
        self.skin = ipk_center_scr
        self.pkg_type = pkg_type
        Screen.__init__(self, session)
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit), 
           'back': (self.exit)})
        self.onLayoutFinish.append(self.updateList)
        return

    def selectedmenuitem(self):
        self.cmd = self['list'].getCurrent()[0]
        if self.cmd != 'None':
            msg = _('Do you want install package?') + '\n\n%s' % self.cmd
            self.session.openWithCallback(self.installIpk, MessageBox, msg, MessageBox.TYPE_YESNO)
        return

    def installIpk(self, answer):
        if answer:
            if ENA_D:
                cmd = 'dpkg -i --force-overwrite /tmp/%s.deb' % self.cmd
            else:
                cmd = 'opkg install --force-overwrite --force-downgrade /tmp/%s.ipk' % self.cmd
            self.session.openWithCallback(self.removeIpk, Console, title=_('Installing package'), cmdlist=[cmd])
        return

    def updateList(self):
        del self.list[:]
        f = listDir('/tmp')
        if f:
            for x in f:
                if '.' + self.pkg_type in x:
                    item = [
                     x[:-4]]
                    item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=x[:-4]))
                    self.list.append(item)

        if len(self.list) == 0:
            item = [
             'None']
            item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=_('No Files Found')))
            self.list.append(item)
        self['list'].l.setList(self.list)
        self.setTitle(_('Installing package'))
        return

    def exit(self):
        self.close()
        return

    def removeIpk(self):
        system('rm -rf /tmp/' + self.cmd + '.' + self.pkg_type)
        self.updateList()
        return


class ipk_uninstall_center(Screen):

    def __init__(self, session, what=''):
        self.skin = ipk_uninstall_scr
        Screen.__init__(self, session)
        self.what = what
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit), 
           'back': (self.exit)})
        self.onLayoutFinish.append(self.updateList)
        return

    def selectedmenuitem(self):
        self.cmd = self['list'].getCurrent()[0]
        if self.cmd != 'None':
            self.cmd = self.cmd.split(' ')[0]
            msg = _('Do you want to uninstall package?') + '\n\n%s' % self.cmd
            self.session.openWithCallback(self.uninstallIpk, MessageBox, msg, MessageBox.TYPE_YESNO)
        return

    def uninstallIpk(self, answer):
        if answer:
            if self.what != '':
                msg = ''
                f = listDir(GSU_PATH + 'Auto_start')
                if f:
                    for x in f:
                        if '_Cam.sh' in x:
                            msg = self.chckCamSrv(x)
                        elif '_Srv.sh' in x:
                            msg += self.chckCamSrv(x)

                if msg != '':
                    self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR, 6)
                    return
            if ENA_D:
                cmd = 'dpkg -r %s' % self.cmd
            else:
                cmd = '%spkg remove %s' % (PKGBIN, self.cmd)
            self.session.openWithCallback(self.updateList, Console, title=_('Uninstalling package'), cmdlist=[cmd])
        return

    def chckCamSrv(self, what):
        stmp = ''
        state = ''
        try:
            f = open(GSU_PATH + 'Auto_start/' + what, 'r')
            for line in f.readlines():
                if line.startswith('SrvBin=') or line.startswith('CamBin='):
                    stmp = line.split('=')[1][:-1]
                    f.close()
                    break

        except:
            state = _('Error reading script')

        if stmp != '':
            tmp = self.cmd.strip().split('.')[1]
            if tmp == stmp:
                state = tmp + ' ' + _('is in use, cannot be uninstalled')
        return state

    def setWindowTitle(self, titleName):
        self.setTitle(titleName)
        return

    def updateList(self):
        if self.what != '':
            self.setWindowTitle(_('Uninstall CAM/SRV menu'))
        else:
            self.setWindowTitle(_('Uninstalling package'))
        del self.list[:]
        contentInfo = chckPckgList()
        for line in contentInfo:
            if self.what != '':
                if line.startswith('glasssysutil-'):
                    item = [
                     line]
                    item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(860), fhd(25)), font=0, text=line))
                    led = 'yellow'
                    if '-srv.' in line:
                        led = 'blue'
                    pix = LoadPixmap(BP_ICO % led)
                    item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                    self.list.append(item)
            else:
                item = [
                 line]
                item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=line))
                self.list.append(item)

        if len(self.list) == 0:
            item = [
             'None']
            if self.what != '':
                txt = _('No CAM/SRV installed')
            else:
                txt = _('No Files Found')
            item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=txt))
            self.list.append(item)
        self['list'].l.setList(self.list)
        return

    def exit(self):
        self.close('1')
        return


class tar_center(Screen):

    def __init__(self, session):
        self.skin = tar_center_scr
        Screen.__init__(self, session)
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit), 
           'back': (self.exit)})
        self.onLayoutFinish.append(self.updateList)
        return

    def selectedmenuitem(self):
        self.cmd = self['list'].getCurrent()[0]
        if self.cmd != 'None':
            msg = _('Do you want install package?') + '\n\n%s' % self.cmd
            self.session.openWithCallback(self.installTar, MessageBox, msg, MessageBox.TYPE_YESNO)
        return

    def installTar(self, answer):
        if answer:
            if self.cmd.__contains__('gz'):
                self.runCmd('tar -xzf /tmp/' + self.cmd)
            else:
                self.runCmd('tar -xjf /tmp/' + self.cmd)
        return

    def updateList(self):
        del self.list[:]
        f = listDir('/tmp')
        if f:
            for x in f:
                if '.gz' in x or '.bz2' in x:
                    item = [
                     x]
                    item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=x))
                    self.list.append(item)

        if len(self.list) == 0:
            item = [
             'None']
            item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(860), fhd(25)), font=0, text=_('No Files Found')))
            self.list.append(item)
        self['list'].l.setList(self.list)
        self.setTitle(_('TAR package install'))
        return

    def runCmd(self, cmd):
        if cmd is not None:
            self.session.openWithCallback(self.removeTar, Console, title=_('Installing package'), cmdlist=[cmd])
        return

    def exit(self):
        self.close()
        return

    def removeTar(self):
        system('rm -rf /tmp/' + self.cmd)
        self.updateList()
        return


class oscamInfoChoiceServer(Screen):

    def __init__(self, session):
        self.skin = oscam_InfoChoiseServer
        self.session = session
        Screen.__init__(self, session)
        self.status = {}
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['server_detailed_labels'] = Label(_('Name') + ':\n' + _('Ip adress') + ':\n' + _('Port') + ':\n' + _('Login') + ':\n' + _('Pass') + ':')
        self['server_detailed_values'] = Label('')
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.choiseServer), 
           'ok': (self.choiseServer), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.readOScamServers)
        return

    def readOScamServers(self):
        item = []
        c = 0
        if fileExists('/etc/remote_servers.cfg'):
            try:
                f = open('/etc/remote_servers.cfg', 'r')
                content = f.read()
                f.close()
            except:
                content = ''
            else:
                contentInfo = content.split('\n')
                if content != '':
                    for line in contentInfo:
                        if line.startswith('O:'):
                            tmp = line.strip().split(' ')
                            if len(tmp) > 2:
                                loginName = passwordName = ''
                                if line.__contains__('127.0.0.1'):
                                    (line, url, loginName, passwordName) = readOscamCfg()
                                    line = line.replace('S: Local', 'O: %s' % tmp[1])
                                else:
                                    url = 'http://' + tmp[2] + '/'
                                    if len(tmp) > 4:
                                        if tmp[3] is not None and tmp[4] is not None and tmp[3] != '' and tmp[4] != '':
                                            loginName = tmp[3]
                                            passwordName = tmp[4]
                                self.status[line] = False
                                data = getUrlData(url, loginName, passwordName)
                                if isinstance(data, list):
                                    self.status[line] = True
                                c = c + 1
                                item = [line]
                                item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(35), fhd(22)), font=0, text=str(c) + '.'))
                                item.append(MultiContentEntryText(pos=(fhd(65), 0), size=(fhd(310), fhd(22)), font=0, text=tmp[1], color_sel=int({True: '0x00d100', False: '0xd10000'}[self.status.get(line)], 16), color=int({True: '0xffffff', False: '0x666666'}[self.status.get(line)], 16)))
                                pix = LoadPixmap({True: (BP_ICO % 'green'), False: (BP_ICO % 'red')}[self.status.get(line)])
                                item.append(MultiContentEntryPixmapAlphaTest(pos=(fhd(40), fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                                self.list.append(item)

                    self['list'].l.setList(self.list)
                    self.reactivate()
                    self.setTitle(_('Select Server'))
                else:
                    self.close()
        else:
            self.close()
        return

    def choiseServer(self):
        line = self['list'].getCurrent()[0]
        if self.status.get(line):
            tmp = line.strip().split(' ')
            url = 'http://' + tmp[2] + '/'
            loginName = passwordName = ''
            if len(tmp) > 4:
                if tmp[3] is not None and tmp[4] is not None and tmp[3] != '' and tmp[4] != '':
                    loginName = tmp[3]
                    passwordName = tmp[4]
            self.session.open(oscamInfo, url, tmp[1], loginName, passwordName)
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        serverName = serverPort = loginName = passwordName = '........'
        if selection:
            lineRq = selection[0]
            tmp = lineRq.strip().split(' ')
            serverName = tmp[2]
            if len(tmp) > 4:
                loginName = tmp[3]
                passwordName = tmp[4]
            server = tmp[2].split(':')
            if len(server) > 1:
                serverName = server[0]
                serverPort = server[1]
            self['server_detailed_values'].setText(tmp[1] + '\n' + serverName + '\n' + serverPort + '\n' + loginName + '\n' + passwordName)
        return


def getUrlData(url, login='', passwd=''):
    manager = urllibXX2.HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, url, login, passwd)
    opener = urllibXX2.build_opener(urllibXX2.HTTPDigestAuthHandler(manager), urllibXX2.HTTPBasicAuthHandler(manager))
    try:
        with opener.open(urllibXX2.Request(url), timeout=4) as response:
            raw = response.read(4*1024*1024+1)
        if len(raw) > 4*1024*1024:
            return None
        return raw.decode('utf-8', 'replace').split('\n')
    except (OSError, ValueError):
        return None


def readOscamCfg():
    candidates = []
    try:
        with open('/etc/remote_servers.cfg') as handle:
            for line in handle:
                if line.startswith('P:'):
                    fields = line.split()
                    if len(fields)>1:
                        candidates.append(os.path.join(fields[1], 'oscam.conf'))
    except OSError:
        pass
    for name in ('/tmp/.oscam/oscam.version', '/tmp/oscam.version'):
        try:
            with open(name) as handle:
                for line in handle:
                    if line.startswith('ConfigDir:'):
                        candidates.append(os.path.join(line.split(':',1)[1].strip(), 'oscam.conf'))
        except OSError:
            pass
    candidates.extend((os.path.join(config.plugins.GlassSysUtil.par17.value, 'oscam.conf'), '/etc/tuxbox/config/oscam.conf', '/etc/tuxbox/config/oscam/oscam.conf'))
    values = {}
    for name in candidates:
        try:
            section = ''
            with open(name) as handle:
                for raw in handle:
                    line=raw.strip()
                    if line.startswith('[') and line.endswith(']'):
                        section=line[1:-1].lower()
                    elif section=='webif' and '=' in line and not line.startswith(('#',';')):
                        key,value=line.split('=',1);values[key.strip().lower()]=value.strip()
            break
        except OSError:
            continue
    port=values.get('httpport','8888')
    scheme='https' if port.startswith('+') else 'http'
    port=port.lstrip('+')
    if not port.isdigit() or not 0<int(port)<65536:
        port='8888'
    login=values.get('httpuser','');password=values.get('httppwd','')
    url='%s://127.0.0.1:%s/' % (scheme,port)
    item='S: Local 127.0.0.1:%s' % port
    if login and password:
        item+=' '+login+' '+password
    return item,url,login,password


def readOscamWebInfo(data, what):
    if not isinstance(data, list):
        return data
    else:
        result = {}
        cnt = 0
        found = new = newVer = False
        if what == 'clients':
            SRCH = [
             '<TD class="statuscol2">c</TD>', '<TD CLASS="statuscol2">c</TD>', 'CLASS="c"', '\t\t\t<TD CLASS="statuscol4" TITLE="']
            SRCH_end = '</TR>'
        elif what == 'proxies':
            SRCH = [
             '<TD class="statuscol2">p</TD>', '<TD CLASS="statuscol2">p</TD>', 'CLASS="p"', '\t\t\t<TD CLASS="statuscol4" TITLE="']
            SRCH_end = '</TR>'
        elif what == 'readers':
            SRCH = [
             '<TD class="statuscol2">r</TD>', '<TD CLASS="statuscol2">r</TD>', 'CLASS="r"', '\t\t\t<TD CLASS="statuscol4" TITLE="']
            SRCH_end = '</TR>'
        elif what == 'log':
            result = {}
            result[cnt] = []
            for i in data:
                if new and i != '':
                    if 'log></oscam>' in i:
                        new = False
                    else:
                        result[cnt].append(i.strip())
                if not newVer and not new and (i.startswith('\t\t<span class="') or i.startswith('\t\t<SPAN CLASS="')):
                    result[cnt].append(i.replace('\t\t<span class=">', '').replace('">', ': ').replace('<SPAN CLASS="', '').replace('<span class="', '').replace('\t\t', '').replace('\t\t<SPAN CLASS=">', ''))
                elif not newVer and not new and '\t},"debug":"0"' in i:
                    newVer = True
                    found = True
                elif newVer and not new and i == '}':
                    found = False
                elif '<log><![CDATA[' in i:
                    new = True
                if newVer and found and not new and 'lines":[' in i:
                    tmp = i.strip().split('lines":[')[1].replace('{"id":"', '*').replace('","', ', ').replace('"', '').replace('},', '').replace('}]\t},', '')
                    tmp = tmp.strip().split('*')
                    for x in range(0, len(tmp)):
                        result[cnt].append(tmp[x].replace(', usr:', ' ').replace(', line:', ' ').replace('}]', '').replace('\t', '').replace('}', '').replace('&amp;', '/'))

            result[cnt].reverse()
            return result
        for i in data:
            if SRCH[0] in i or SRCH[1] in i:
                cnt += 1
                found = True
            elif SRCH[2] in i:
                new = True
                newVer = True
            elif new and SRCH[3] in i and '"><' in i and 'TITLE="' in i:
                cnt += 1
                found = True
                try:
                    m = i.strip().split('"><')[0].strip().split('TITLE="')[1]
                    result[cnt].append(m)
                except KeyError:
                    result[cnt] = []
                    result[cnt].append(m)

            elif SRCH_end not in i and found:
                m = i
                try:
                    if new and 'TITLE="Online:' in i and '">' in i:
                        m = i.strip().split('">')[0].strip().split('TITLE="Online:')[1]
                        m = m.replace('&#013;', '').replace('&#13;', '')
                    else:
                        m = re.search('>(.*)<', i).group(1)
                        m = m.replace('<SPAN TITLE="">', '').replace('</SPAN>', '')
                    if new:
                        if '<A HREF="entitl' in m:
                            pass
                        elif '<SPAN>' in m and 'tip">' in m:
                            m = m.strip().split('<SPAN>')[0].strip().split('tip">')[1]
                        elif '</A>' in m and '">' in m:
                            m = m.strip().replace('</A>', '').strip().split('">')[1]
                        else:
                            m = m.replace('<BR>', ' ')
                except:
                    pass
                else:
                    try:
                        result[cnt].append(m)
                    except KeyError:
                        result[cnt] = []
                        result[cnt].append(m)

            elif new and '</tbody>' in i:
                new = False
            else:
                found = False

        return (
         result, newVer)
    return


class ColorLabel(Label):

    def __init__(self, text=''):
        Label.__init__(self, text)
        return

    def colorWhite(self):
        if self.instance:
            self.instance.setForegroundColor(parseColor('#b2e0b4'))
        return

    def colorRed(self):
        if self.instance:
            self.instance.setForegroundColor(parseColor('#ff3300'))
        return

    def color1(self):
        if self.instance:
            self.instance.setForegroundColor(parseColor('#ffffff'))
        return

    def color2(self):
        if self.instance:
            self.instance.setForegroundColor(parseColor('#666666'))
        return

    def colorGreen(self):
        if self.instance:
            self.instance.setForegroundColor(parseColor('#00d100'))
        return

    def colorOrange(self):
        if self.instance:
            self.instance.setForegroundColor(parseColor('#ff9c00'))
        return


class oscamInfo(Screen):

    def __init__(self, session, url='http://127.0.0.1:8888/', srv_name='Box', login='', passwd=''):
        self.skin = oscam_Info
        self.session = session
        Screen.__init__(self, session)
        self.url = url
        self.srv_name = srv_name
        self.login = login
        self.passwd = passwd
        self.list = []
        self.menuListAll = [('summary', _('Summary Info')),
         (
          'readers', _('Servers Status')),
         (
          'users', _('Clients Status')),
         (
          'log', _('Log view')),
         (
          'files', _('Config Files'))]
        self.status = {}
        self['list'] = ListboxSys2(self.list)
        self['info'] = ColorLabel('')
        self['info'].hide()
        self['logo'] = Pixmap()
        self['server_name'] = Label('')
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self.warning_timer = eTimer()
        try:
            self.warning_timer_conn = self.warning_timer.timeout.connect(self.warning_Show)
        except:
            self.warning_timer.timeout.get().append(self.warning_Show)

        self.isRed = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit), 
           'back': (self.exit)})
        self.onLayoutFinish.append(self.updatemenulist)
        return

    def selectedmenuitem(self):
        selectedItem = self['list'].getCurrent()[0]
        enabledItem = self.status.get(selectedItem)
        if enabledItem:
            if selectedItem == 'summary':
                self.session.open(oscam_Summary, self.url, self.login, self.passwd)
            elif selectedItem == 'log':
                self.session.open(oscam_logInfo, self.url, self.login, self.passwd)
            elif selectedItem == 'readers':
                self.session.open(oscam_readers, self.url, self.login, self.passwd)
            elif selectedItem == 'users':
                self.session.open(oscam_Users, self.url, self.login, self.passwd)
            elif selectedItem == 'files':
                self.session.open(oscam_Files, self.url, self.login, self.passwd)
        return

    def updatemenulist(self):
        self.list = []
        tst = False
        infoline = startInfo = ''
        start = self.srv_name + '  (' + self.url[:-1] + ')'
        if self.url.__contains__('127.0.0.1'):
            loginName = passwordName = ''
            (line, self.url, self.login, self.passwd) = readOscamCfg()
            try:
                start = open('/etc/hostname', 'r').readline().strip()
            except:
                pass

        data = getUrlData(self.url, self.login, self.passwd)
        if isinstance(data, list):
            tst = True
            enaVer = True
            tmptxt = []
            for line in data:
                line = line.replace('<BR>', '\n')
                line = sub('<br(\\s+/)?>', '\n', line)
                line = sub('<(.*?)>', '', line)
                line = line.replace('\t', ' ')
                tmptxt.append(line)

            for line in tmptxt:
                if enaVer and 'oscam' in line.lower():
                    infoline = line.strip()
                    if 'r' in infoline:
                        tmp = infoline.strip().split('r')[1]
                        if ' ' in tmp:
                            tmp = tmp.strip().split(' ')[0]
                        infoline = 'OScam (' + tmp + ')'
                    enaVer = False
                    if line.__contains__('ymodv'):
                        tst = False
                if line.__contains__('UpTime:') or 'Start Time:' in line:
                    if 'Start Time:' in line:
                        try:
                            tmp = line.strip().split('Start Time:')[1].strip().split('.')
                            tt = tmp[2].split(' ')
                            if len(tt[0]) == 2:
                                tt[0] = '20' + tt[0]
                            tmp[2] = (' ').join(tt)
                            tmp = ('.').join(tmp)
                            startInfo = _('Start Time') + ': ' + tmp.replace('OSCam', '\n').replace('|', ' ').replace('Run Time', _('Uptime'))
                        except:
                            pass
                        else:
                            break
                    else:
                        tmp = line.strip().split(' ')
                        if len(tmp) > 10:
                            startInfo = _('Start Time') + ': ' + tmp[1] + '  ' + tmp[3] + '\n' + _('Uptime') + ': ' + tmp[6]
                        break

        for x in self.menuListAll:
            self.status[x[0]] = False
            if tst:
                self.status[x[0]] = True
            item = [
             x[0]]
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=x[1], color=int({True: '0xffffff', False: '0x666666'}[self.status.get(x[0])], 16)))
            pix = LoadPixmap({True: (BP_ICO % 'green'), False: (BP_ICO % 'red')}[self.status.get(x[0])])
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)

        self['list'].l.setList(self.list)
        self['server_name'].setText(start + '\n\n' + infoline + '\n\n' + startInfo)
        self.warning_timer.start(100)
        self['info'].colorWhite()
        self['info'].setText(_('Warning: in some version of the OScam, some function of OScam Info may be not work correctly, use it on own risk'))
        self['info'].show()
        return

    def warning_Show(self):
        self.warning_timer.stop()
        if self.isRed:
            self['info'].colorWhite()
            self.isRed = False
        else:
            self['info'].colorRed()
            self.isRed = True
        self.warning_timer.start(2000)
        return

    def exit(self):
        if self.warning_timer.isActive():
            self.warning_timer.stop()
        self.warning_timer = None
        self.close()
        return


class oscam_Files(Screen):

    def __init__(self, session, url, login, passwd):
        self.skin = oscam_Files_scr
        self.session = session
        self.url = url
        self.login = login
        self.passwd = passwd
        Screen.__init__(self, session)
        self.list = []
        self.menuListAll = [('oscam.version', 'oscam.version'), 
         ('oscam.dvbapi', 'oscam.dvbapi'), 
         ('oscam.conf', 'oscam.conf'), 
         ('oscam.user', 'oscam.user'), 
         ('oscam.server', 'oscam.server'), 
         ('oscam.services', 'oscam.services'), 
         ('oscam.srvid', 'oscam.srvid'), 
         ('oscam.provid', 'oscam.provid'), 
         ('oscam.tiers', 'oscam.tiers'), 
         ('oscam.retelimit', 'oscam.retelimit'), 
         ('oscam.whitelist', 'oscam.whitelist'), 
         ('logfile', 'logfile'), 
         ('userfile', 'userfile'), 
         ('anticasc', 'AC Log')]
        self['list'] = ListboxSys2(self.list)
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.updatemenulist)
        return

    def selectedmenuitem(self):
        selectedItem = self['list'].getCurrent()[0]
        selectedItem = selectedItem.strip().split('*')
        self.session.open(oscam_Files_detailed, self.url + 'files.html?file=' + selectedItem[0], self.login, self.passwd, selectedItem[1])
        return

    def updatemenulist(self):
        self.list = []
        for x in self.menuListAll:
            item = [
             x[0] + '*' + x[1]]
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=x[1]))
            pix = LoadPixmap(BP_ICO % 'green')
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)

        self['list'].l.setList(self.list)
        self.setTitle(_('Config Files'))
        return


class oscam_Files_detailed(Screen):

    def __init__(self, session, url, login, passwd, titleFile):
        self.skin = oscam_Files_scr2
        self.session = session
        self.url = url
        self.login = login
        self.passwd = passwd
        self.titleFile = titleFile
        Screen.__init__(self, session)
        self['red'] = Label(_('Exit'))
        self['file_info'] = ScrollLabel(_('No Files Found'))
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'left': (self.pageUp), 
           'right': (self.pageDown), 
           'down': (self.pageDown), 
           'up': (self.pageUp), 
           'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'cancel': (self.close), 
           'blue': (self.close), 
           'yellow': (self.close)}, -2)
        self.onLayoutFinish.append(self.loadfileInfo)
        return

    def setWindowTitle(self, titleName):
        self.setTitle(titleName)
        return

    def loadfileInfo(self):
        data = getUrlData(self.url, self.login, self.passwd)
        if not isinstance(data, list):
            self.close()
            return
        self.setWindowTitle(_('OScam File') + ': ' + self.titleFile)
        lineData = []
        ena = False
        for x in data:
            if '</TEXTAREA>' in x or '</textarea>' in x:
                break
            if ena:
                lineData.append(x)
            if (x.startswith('\t\t<textarea') or x.startswith('\t\t<TEXTAREA')) and '>' in x:
                idx = x.index('>')
                temp = x[idx + 1:]
                ena = True
                lineData.append(temp)

        if len(lineData) != 0:
            infoline = ''
            for i in range(0, len(lineData)):
                infoline += lineData[i] + '\n'

            self['file_info'].setText(infoline)
        return

    def pageUp(self):
        self['file_info'].pageUp()
        return

    def pageDown(self):
        self['file_info'].pageDown()
        return


class oscam_logInfo(Screen):

    def __init__(self, session, url, login, passwd):
        self.skin = oscam_logInfo_scr
        self.session = session
        self.url = url
        self.login = login
        self.passwd = passwd
        self.list = []
        Screen.__init__(self, session)
        self['log_info'] = ListboxSys2(self.list)
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.exit), 
           'ok': (self.exit), 
           'red': (self.exit), 
           'cancel': (self.exit), 
           'blue': (self.exit), 
           'yellow': (self.exit)}, -2)
        self.refreshTimer = eTimer()
        try:
            self.refreshTimer_conn = self.refreshTimer.timeout.connect(self.oscamLogInfo)
        except:
            self.refreshTimer.timeout.get().append(self.oscamLogInfo)

        self.onLayoutFinish.append(self.oscamLogInfo)
        return

    def oscamLogInfo(self):
        self.refreshTimer.stop()
        self.list = []
        item = []
        data = getUrlData(self.url, self.login, self.passwd)
        if not isinstance(data, list):
            self.exit()
            return
        parsedData = readOscamWebInfo(data, 'log')
        if not len(parsedData[0]) > 0:
            data = getUrlData(self.url + 'oscamapi.html?part=status&appendlog=1', self.login, self.passwd)
            if not isinstance(data, list):
                self.exit()
                return
            parsedData = readOscamWebInfo(data, 'log')
        if isinstance(parsedData, list):
            item = [
             '*']
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=_('No log info')))
            self.list.append(item)
        else:
            for i in range(len(parsedData[0])):
                txt = parsedData[0][i]
                clr = '0xb2e0b4'
                if 'found' in txt:
                    clr = '0x00d100'
                elif 'rejeted' in txt or 'timeout' in txt:
                    clr = '0xff3300'
                elif 'emmtype' in txt:
                    clr = '0x138aec'
                elif 'not found' in txt:
                    clr = '0xff9c00'
                item = [
                 txt]
                item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(1180), fhd(17)), font=1, text=txt, color=int(clr, 16)))
                self.list.append(item)

        self['log_info'].l.setList(self.list)
        self['log_info'].selectionEnabled(0)
        self.refreshTimer.startLongTimer(int(config.plugins.GlassSysUtil.par61.value))
        return

    def exit(self):
        if self.refreshTimer.isActive():
            self.refreshTimer.stop()
        self.refreshTimer = None
        self.close()
        return


class oscam_Summary(Screen):

    def __init__(self, session, url, login, passwd):
        self.skin = oscam_Summary_scr
        self.session = session
        self.url = url
        self.login = login
        self.passwd = passwd
        Screen.__init__(self, session)
        self['red'] = Label(_('Exit'))
        self['blue'] = Label(_('Restart'))
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['status_labels_0'] = Label('Label:\nAU:\nCrypted:\nAddress:\nPort:')
        self['status_values_0'] = Label('..........\n..........\n..........\n..........\n..........')
        self['status_labels_1'] = Label('Protocol:\nLogin:\nOnline:\nCAID:\nSRVID:')
        self['status_values_1'] = Label('..........\n..........\n..........\n..........\n..........')
        self['status_labels_2'] = Label('Channel:\nUsed:\nIdle:\nStatus:')
        self['status_values_2'] = Label('..........\n..........\n..........\n..........')
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.exit), 
           'ok': (self.exit), 
           'red': (self.exit), 
           'cancel': (self.exit), 
           'blue': (self.rstOsc), 
           'yellow': (self.exit)}, -2)
        self.refreshTimer = eTimer()
        self.typeV = False
        try:
            self.refreshTimer_conn = self.refreshTimer.timeout.connect(self.oscamStatus)
        except:
            self.refreshTimer.timeout.get().append(self.oscamStatus)

        self.onLayoutFinish.append(self.oscamStatus)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('Summary Info'))
        return

    def rstOsc(self):
        self.session.openWithCallback(self.restartAnswer, MessageBox, _('Do you want restart OScam now?'), MessageBox.TYPE_YESNO)
        return

    def restartAnswer(self, answer):
        if answer:
            data = getUrlData(self.url + 'shutdown.html?action=Restart', self.login, self.passwd)
            self.session.open(MessageBox, _('Restart finished'), MessageBox.TYPE_INFO, 6)
        return

    def oscamStatus(self):
        self.refreshTimer.stop()
        self.list = []
        data = getUrlData(self.url, self.login, self.passwd)
        if not isinstance(data, list):
            self.exit()
            return
        allWhat = ('Readers', 'Proxies', 'Clients')
        for what in allWhat:
            (parsedData, self.typeV) = readOscamWebInfo(data, what.lower())
            if self.typeV:
                start = 0
                end = 10
            else:
                start = 1
                end = 14
            stateItem = BP_ICO % 'white'
            item = ['*']
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=what + ':', color=int('0xffd700', 16)))
            pix = LoadPixmap(stateItem)
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)
            if isinstance(parsedData, dict):
                for i in list(parsedData.keys()):
                    infoline = tmp1 = ''
                    for x in range(start, end):
                        if self.typeV and (x == 2 or x == 5):
                            if x == 5:
                                infoline += '..........*..........*'
                            else:
                                infoline += '..........*'
                        if parsedData[i][x] == '':
                            parsedData[i][x] = '..........'
                        if parsedData[i][x].startswith('<a href="#"') or parsedData[i][x].startswith('<A HREF="#"'):
                            if parsedData[i][x].__contains__('ON'):
                                parsedData[i][x] = 'ON'
                            elif parsedData[i][x].__contains__('OFF'):
                                parsedData[i][x] = 'OFF'
                            elif parsedData[i][x].__contains__('ACTIVE'):
                                parsedData[i][x] = 'ACTIVE'
                            else:
                                parsedData[i][x] = '..........'
                        if parsedData[i][x].__contains__('<A HREF="'):
                            if parsedData[i][x].__contains__('count=') and parsedData[i][x].__contains__('reshare'):
                                tmp1 = parsedData[i][x].strip().split('count=')[1]
                                tmp1 = 'count: ' + tmp1.replace('<BR><BR>', '*').replace('<BR>', '*').replace('=', ': ').replace('</A>', '')
                                tmp1 = tmp1.replace('*', ', ')
                            parsedData[i][x] = parsedData[i][x].strip().split(' ')[0].replace('<BR><A', '')
                        if parsedData[i][x].__contains__('">'):
                            newDataTmp = parsedData[i][x]
                            idx = newDataTmp.index('>')
                            parsedData[i][x] = newDataTmp[idx + 1:]
                        if what != 'Clients':
                            if x != 11:
                                infoline += parsedData[i][x] + '*'
                            else:
                                infoline += '..........*'
                        else:
                            infoline += parsedData[i][x] + '*'

                    tmp = infoline.strip().split('*')
                    stateItem = BP_ICO % 'red'
                    if tmp[12] == 'OK' or tmp[12] == 'CONNECTED' or tmp[12] == 'CARDOK':
                        stateItem = BP_ICO % 'green'
                    item = [
                     infoline]
                    item.append(MultiContentEntryText(pos=(fhd(50), 0), size=(fhd(535), fhd(22)), font=0, text=tmp[0].replace('&#13;', ' ') + ' at ' + tmp[3]))
                    pix = LoadPixmap(stateItem)
                    item.append(MultiContentEntryPixmapAlphaTest(pos=(fhd(25), fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                    self.list.append(item)
                    if tmp1 != '':
                        item = [
                         '*']
                        item.append(MultiContentEntryText(pos=(fhd(50), 0), size=(fhd(920), fhd(19)), font=1, text=tmp1))
                        self.list.append(item)

            else:
                item = [
                 '*']
                item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text='*****   ' + _('None') + ' ' + what + '   *****'))
                self.list.append(item)

        self['list'].l.setList(self.list)
        self.reactivate()
        self.refreshTimer.start(15000, True)
        return

    def exit(self):
        if self.refreshTimer.isActive():
            self.refreshTimer.stop()
        self.refreshTimer = None
        self.close()
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            if lineRq != '*':
                try:
                    caid = srvid = '0000'
                    tmp = lineRq.strip().split('*')
                    caidSrvid = tmp[8].split(':')
                    if len(caidSrvid) > 1:
                        caid = caidSrvid[{True: 1, False: 0}['@' in tmp[8]]]
                        srvid = caidSrvid[{True: 0, False: 1}['@' in tmp[8]]]
                    if tmp[10].__contains__('&nbsp'):
                        tmp[10] = tmp[10].replace('&nbsp;', '')
                    if tmp[11].__contains__('</'):
                        idx = tmp[11].index('<')
                        tmp[11] = tmp[11][:idx]
                    if 'IDLE:' in tmp[11]:
                        idx = tmp[11].replace(' ', '').split('IDLE:')
                        if idx[0] != '':
                            tmp[7] = idx[0]
                        else:
                            tmp[7] = '..........'
                        tmp[11] = idx[1]
                    if 'ACTIVE' in tmp[1].upper():
                        tmp[1] = 'ACTIVE'
                    elif 'ON' in tmp[1].upper():
                        tmp[1] = 'ON'
                    if '<BR>' in tmp[2].upper():
                        tmp[2] = tmp[2].split('<BR>')[0]
                    if '(' in tmp[0] and ')' in tmp[0]:
                        tmp[0] = tmp[0].split('(')[0]
                    self['status_values_0'].setText(tmp[0].replace('&#13;', ' ') + '\n' + tmp[1] + '\n' + tmp[2] + '\n' + tmp[3] + '\n' + tmp[4])
                    self['status_values_1'].setText(tmp[5] + '\n' + tmp[6] + '\n' + tmp[7] + '\n' + caid + '\n' + srvid)
                    self['status_values_2'].setText(tmp[9] + '\n' + tmp[10] + '\n' + tmp[11] + '\n' + tmp[12])
                except:
                    pass

            else:
                self['status_values_0'].setText('..........\n..........\n..........\n..........\n..........')
                self['status_values_1'].setText('..........\n..........\n..........\n..........\n..........')
                self['status_values_2'].setText('..........\n..........\n..........\n..........')
        return


class oscam_readers(Screen):

    def __init__(self, session, url, login, passwd):
        self.skin = oscam_Readers_scr
        self.session = session
        self.url = url
        self.login = login
        self.passwd = passwd
        Screen.__init__(self, session)
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['status_labels_0'] = Label('EMM error (UK / G / S / UQ) :\nEMM written (UK / G / S / UQ):')
        self['status_values_0'] = Label('')
        self['status_labels_1'] = Label('EMM skipped (UK / G / S / UQ) :\nEMM blocked (UK / G / S / UQ):')
        self['status_values_1'] = Label('')
        self['blue_button'] = Label('')
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Entitlements'))
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.entitlements), 
           'ok': (self.entitlements), 
           'red': (self.exit), 
           'cancel': (self.exit), 
           'blue': (self.chngState), 
           'yellow': (self.exit)}, -2)
        self.refreshTimer = eTimer()
        try:
            self.refreshTimer_conn = self.refreshTimer.timeout.connect(self.oscamreaders)
        except:
            self.refreshTimer.timeout.get().append(self.oscamreaders)

        self.onLayoutFinish.append(self.oscamreaders)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('Servers Status'))
        return

    def exit(self):
        if self.refreshTimer.isActive():
            self.refreshTimer.stop()
        self.refreshTimer = None
        self.close()
        return

    def entitlements(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            tmp = lineRq.split('*')
            if not tmp[2].__contains__('newcamd') and not tmp[2].__contains__('camd3') and not tmp[2].__contains__('cs3'):
                tmp[1] = tmp[1].replace('+', '%2b').replace(' ', '+')
                self.session.open(oscam_entitlements, self.url, tmp[1], self.login, self.passwd)
            else:
                self.session.open(MessageBox, _('Protocol not allowed for entitlements'), MessageBox.TYPE_INFO, 4)
        return

    def oscamreaders(self):
        self.refreshTimer.stop()
        data = getUrlData(self.url + 'readers.html', self.login, self.passwd)
        if not isinstance(data, list):
            self.close()
            return
        self.list = []
        tmptxt = []
        state = []
        item = []
        num = 0
        cline = 0
        newV = ena = False
        for line in data:
            if '&amp;action=disable' in line or 'data-next-action="disable"' in line:
                state.append('green')
            elif '&amp;action=enable' in line or 'data-next-action="enable"' in line:
                state.append('red')
            if 'data-next-action="disable"' in line or 'data-next-action="enable"' in line:
                if not newV:
                    tmptxt = {}
                    newV = True
                cline += 1
                tmptxt[cline] = []
            if newV:
                if not ena and 'CLASS="readercol1"' in line:
                    ena = True
                elif '</TR>' in line:
                    ena = False
                if ena and 'CLASS="readercol' in line and 'CLASS="groups' not in line:
                    line = sub('<(.*?)>', '', line)
                    if line != '':
                        tmptxt[cline].append(line.replace('\t', ''))
            else:
                line = line.replace('<BR>', '\n')
                line = sub('<br(\\s+/)?>', '\n', line)
                line = sub('<(.*?)>', '', line)
                line = line.replace('\t', ' ')
                tmptxt.append(line)

        if not newV:
            enaRead = False
            for line in tmptxt:
                if line.__contains__('nbsp'):
                    break
                if line.__contains__('Action'):
                    enaRead = True
                if line.__contains__(' / ') and enaRead:
                    i = 0
                    infoline = ''
                    tmp22 = tmptxt[cline].split('/')
                    if not tmptxt[cline - 1].strip().__contains__('/') and len(tmp22) == 4:
                        infoline = str(num) + '*'
                        if tmptxt[cline - 1].strip().isdigit():
                            infoline += tmptxt[cline - 3].strip() + '*' + tmptxt[cline - 2].strip() + '*'
                        else:
                            infoline += tmptxt[cline - 2].strip() + '*' + tmptxt[cline - 1].strip() + '*'
                        while i < 4:
                            tmpInfo = tmptxt[cline + i].strip()
                            infoline += tmpInfo + '*'
                            i += 1

                        infoline += state[num]
                        tmp = infoline.split('*')
                        num += 1
                        item = [infoline]
                        item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=_('Name') + ': ' + tmp[1] + ', ' + _('used protocol') + ': ' + tmp[2]))
                        pix = LoadPixmap(BP_ICO % tmp[len(tmp) - 1])
                        item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                        self.list.append(item)
                cline += 1

        else:
            for i in list(tmptxt.keys()):
                aa = 0
                infoline = str(i) + '*'
                if tmptxt[i][5].replace(' ', '') == '0/0':
                    aa = 1
                for x in range(2 + aa, 6 + aa):
                    tmptxt[i][x - aa] = tmptxt[i][x + 3]

                tmptxt[i][6] = state[int(i) - 1]
                for x in range(0, 7):
                    infoline += tmptxt[i][x] + '*'

                tmp = infoline.strip().split('*')
                item = [infoline]
                item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=_('Name') + ': ' + tmp[1] + ', ' + _('used protocol') + ': ' + tmp[2]))
                pix = LoadPixmap(BP_ICO % tmp[7])
                item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                self.list.append(item)

            self['list'].l.setList(self.list)
            self.reactivate()
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            tmp = lineRq.split('*')
            self['status_values_0'].setText(tmp[3] + '\n' + tmp[4])
            self['status_values_1'].setText(tmp[5] + '\n' + tmp[6])
            if tmp[7] == 'green':
                self['blue_button'].setText(_('Disable'))
            else:
                self['blue_button'].setText(_('Enable'))
        return

    def chngState(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            tmp = lineRq.split('*')
            what = 'enable'
            if tmp[7] == 'green':
                what = 'disable'
            data = getUrlData(self.url + 'readers.html?label=' + tmp[1] + '&action=' + what, self.login, self.passwd)
            self.session.open(MessageBox, _('Reader/Proxies action finished'), MessageBox.TYPE_INFO, 6)
            self.refreshTimer.start(4000, True)
        return


class oscam_entitlements(Screen):

    def __init__(self, session, url, reader, login, passwd):
        self.skin = oscam_Entitlements_scr
        self.session = session
        self.url = url
        self.login = login
        self.passwd = passwd
        self.reader = reader
        Screen.__init__(self, session)
        self.allLabels = [
         'Host', 'CAID', 
         'System', 'Type', 
         'Share ID', 
         'Remote ID', 
         'Up', 'Re', 
         'Providers']
        self.allLabelsCRD = [
         'TypeCRD', 'CAIDcrd', 
         'ProvID', 'ID', 
         'Class', 
         'Start Date', 'Expire Date', 'Name']
        for x in self.allLabels:
            self[x] = Label()
            self[x].hide()

        for x in self.allLabelsCRD:
            self[x] = Label()
            self[x].hide()

        self['Crd_info'] = Label(_('No info about card detected'))
        self['Crd_system'] = Pixmap()
        self.list = []
        self['entitlements_list'] = ListboxSys2(self.list)
        self['red'] = Label(_('Exit'))
        self['blue'] = Label(_('Refresh entitlements'))
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'cancel': (self.close), 
           'blue': (self.refreshEntitl), 
           'yellow': (self.close)}, -2)
        self.refreshTimer = eTimer()
        try:
            self.refreshTimer_conn = self.refreshTimer.timeout.connect(self.oscamEntitlements)
        except:
            self.refreshTimer.timeout.get().append(self.oscamEntitlements)

        self.onLayoutFinish.append(self.oscamEntitlements)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('Entitlements'))
        return

    def refreshEntitl(self):
        data = getUrlData(self.url + 'readers.html?action=reread&label=' + self.reader, self.login, self.passwd)
        self.session.open(MessageBox, _('Refresh entitlements finished'), MessageBox.TYPE_INFO, 6)
        self.refreshTimer.start(6000, True)
        return

    def exit(self):
        if self.refreshTimer.isActive():
            self.refreshTimer.stop()
        self.refreshTimer = None
        self.close()
        return

    def oscamEntitlements(self):
        self.refreshTimer.stop()

        def appDataClean(dat):
            return dat.replace('<', '').replace('TR', '').replace('>', '').replace('TD', '').replace('\t', '').replace('/', '')

        data = getUrlData(self.url + 'entitlements.html?label=' + self.reader, self.login, self.passwd)
        if not isinstance(data, list):
            self.close()
            return
        self['Crd_system'].instance.setPixmapFromFile(BP_ICO % 'ca_small/Unknown-fs8')
        item = []
        self.list = []
        for x in self.allLabels:
            self[x].hide()

        for x in self.allLabelsCRD:
            self[x].hide()

        typeEnt = ''
        lineData = []
        for x in data:
            if x.__contains__('<TH>Class</TH><TH>Start Date</TH><TH>Expire Date</TH>') or x.__contains__('\t\t<TR><TH colspan="3">Cardsystem</TH><TH colspan="2">Valid To</TH>'):
                typeEnt = 'crd'
                break
            elif x.startswith('\t<TABLE CLASS="stats">'):
                typeEnt = 'cc_share'
            elif x.startswith('</TD><TD></TD><TD></TD></TR>\t</TABLE>') or typeEnt == 'cc_share' and '</TABLE>' in x:
                break
            if typeEnt == 'cc_share' and not x.__contains__('<H4 CLASS=') and x != '\t<TABLE CLASS="stats">':
                newData = x.replace('</TD><TD></TD><TD></TD></TR>\t\t<TR><TD>', '').replace('</TD><TD>', '*').replace('<BR>', '*')
                if newData.__contains__('Reshare'):
                    newData = newData.replace('\t<TABLE CLASS="stats">', '').replace('\t', '').replace('<TR><TD>', '')
                    newData = newData.replace('<TR><TH>Host</TH><TH>Caid</TH><TH>System</TH><TH>Type</TH><TH>Share id</TH><TH>Remote id</TH><TH>Uphops</TH><TH>Reshare</TH><TH>Providers</TH><TH>Nodes</TH><TH>Good sids</TH><TH>Bad sids</TH></TR>', '')
                    newData = newData.replace('<TR><TH>Host</TH><TH>Caid</TH><TH>System</TH><TH>Type</TH><TH>share id</TH><TH>remote id</TH><TH>Uphops</TH><TH>Reshare</TH><TH>Providers</TH><TH>Nodes</TH><TH>Good sids</TH><TH>Bad sids</TH></TR>', '')
                tmp = newData.split('*')
                if len(tmp) == 10:
                    lineData.append(appDataClean(newData))
                elif len(tmp) > 10:
                    try:
                        temp = ''
                        if tmp[0] == '':
                            if tmp[2].__contains__('</TD></TR>\t\t<TR><TD'):
                                temp = tmp[2]
                                temp = temp.replace('</TD></TR>\t\t<TR><TD', '')
                                idx = temp.index('>')
                                temp = temp[idx + 1:] + '*'
                                for y in range(3, 12):
                                    temp += tmp[y] + '*'

                            elif tmp[1].__contains__('</TD></TR>\t\t<TR><TD'):
                                temp = tmp[1]
                                temp = temp.replace('</TD></TR>\t\t<TR><TD', '')
                                idx = temp.index('>')
                                temp = temp[idx + 1:] + '*'
                                for y in range(2, 11):
                                    temp += tmp[y] + '*'

                        else:
                            for y in range(0, 10):
                                temp += tmp[y] + '*'

                            lineData.append(appDataClean(temp))
                    except:
                        pass

                elif newData.__contains__(':') or len(newData) != 18 and len(newData) != 17:
                    lineData.append(appDataClean('xFx********' + newData))

        if typeEnt == 'crd':
            lineData = []
            found = False
            SRCH = '</TH><TH>Start Date</TH><TH>Expire Date</TH>'
            SRCH_end = '\t</TABLE>'
            for i in data:
                if SRCH in i:
                    found = True
                elif SRCH_end not in i and found:
                    tmp = 'e_valid*'
                    if 'e_expired' in i:
                        tmp = 'e_expired*'
                    try:
                        m = re.search('>(.*)<', i).group(1)
                        m = m.replace('</TD><TD>', '*').replace('</TD>\t\t<TD>', '*').replace('</TD>', '').replace('<TD>', '')
                        m = tmp + m
                        lineData.append(m)
                    except:
                        pass

                else:
                    found = False

            item = []
            crdData = []
            found = False
            SRCH = '>Cardsystem</TH>'
            SRCH_end = '<TR><TH>Type<'
            for i in data:
                if SRCH in i:
                    found = True
                elif SRCH_end not in i and found:
                    if 'Serial' not in i:
                        m = re.sub('\\t*?<[^>]*?>', '?', i)
                        m = m.replace('??', '*').replace('&nbsp;', '').replace('?', '*')
                        crdData.append(m)
                else:
                    found = False

            atr = ''
            tmp1 = 'unknown'
            if len(crdData) > 1:
                tmp1 = crdData[0].strip().split('*')[1]
                allCaids = {'irdeto': 'Irdeto', 
                   'seca': 'Seca', 'nagra': 'Nagravision', 'panaccess': 'Panaccess', 'viaccess': 'Viaccess', 
                   'conax': 'Conax', 'tongfang': 'tongfang', 'cryptoworks': 'Cryptoworks', 
                   'videoguard1': 'Videoguard', 'videoguard': 'Videoguard', 'videoguard2': 'Videoguard', 
                   'dre': 'DRE-crypt', 'dgcrypt': 'DGCrypt', 'bulcrypt': 'Bulcrypt', 'griffin': 'Griffin'}
                if tmp1 in allCaids:
                    pngName = findPicon(allCaids.get(tmp1) + '-fs8', 'piconCam')
                    if pngName == '':
                        pngName = BP_ICO % 'ca_small/Unknown-fs8'
                    self['Crd_system'].instance.setPixmapFromFile(pngName)
                tmp = crdData[0].strip().split('*')
                provID = m = state1 = ''
                if len(tmp) > 5:
                    state1 = 'Valid to: ' + tmp[2] + ', IRD ID: ' + tmp[3]
                    provID += tmp[4].replace('Prv.ID: ', '') + ', '
                for i in range(1, len(crdData)):
                    tmp = crdData[i].strip().split('*')
                    xx = len(tmp)
                    if xx == 5 or xx == 6:
                        if tmp[2] == '':
                            m = 'ATR: ' + tmp[xx - 2].replace(' ', '') + ', Serial: ' + tmp[1]
                        else:
                            m = 'ATR: ' + tmp[xx - 2].replace(' ', '') + ', Serial: ' + tmp[1] + ', Rom: ' + tmp[2]
                        if xx == 6:
                            m += ', I2 SC-Ver-Rev-Patch: ' + tmp[3]
                    if not crdData[i].startswith('*'):
                        provID += crdData[i].replace('Prv.ID: ', '').replace('*', '') + ', '

                if provID != '':
                    provID = 'Prov ID: ' + provID[:-2]
                self['Crd_info'].setText(m.replace('\n', '') + '\n' + state1.replace('\n', '') + '\n' + provID)
            if tmp1 == 'unknown':
                item = [
                 0]
                item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(800), fhd(25)), font=1, text=_('No entitlements detected')))
                self.list.append(item)
            else:
                for x in self.allLabelsCRD:
                    self[x].show()

                for i in range(0, len(lineData)):
                    tmp = lineData[i].strip().split('*')
                    if len(tmp) > 8:
                        item = [
                         i]
                        if tmp[0].__contains__('expired'):
                            pix = LoadPixmap(BP_ICO % 'red')
                        else:
                            pix = LoadPixmap(BP_ICO % 'green')
                        item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                        item.append(MultiContentEntryText(pos=(fhd(30), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[1]))
                        item.append(MultiContentEntryText(pos=(fhd(125), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[2]))
                        item.append(MultiContentEntryText(pos=(fhd(200), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[3]))
                        item.append(MultiContentEntryText(pos=(fhd(300), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[4]))
                        item.append(MultiContentEntryText(pos=(fhd(500), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[5]))
                        item.append(MultiContentEntryText(pos=(fhd(650), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[6]))
                        item.append(MultiContentEntryText(pos=(fhd(805), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[7]))
                        tmp[8] = tmp[8].replace('amp;', '')
                        if len(tmp[8]) > 19:
                            tmp[8] = tmp[8][:16] + '...'
                        item.append(MultiContentEntryText(pos=(fhd(960), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[8]))
                        self.list.append(item)

                self['entitlements_list'].l.setList(self.list)
        elif typeEnt == 'cc_share':
            self['Crd_system'].instance.setPixmapFromFile(BP_ICO % 'ca_small/cccam')
            self['Crd_info'].setText(_('CCcam share for reader') + ': ' + self.reader)
            item = []
            if len(lineData) < 3:
                item = [
                 0]
                item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(800), fhd(25)), font=1, text=_('No entitlements detected')))
                self.list.append(item)
            else:
                for x in self.allLabels:
                    self[x].show()

                hostIP = '...'
                for i in range(0, len(lineData)):
                    tmp = lineData[i].strip().split('*')
                    if len(tmp) > 9:
                        if tmp[0] == 'xFx' and (tmp[8] == '' or 'UA_' in tmp[8] or '.' in tmp[8]):
                            if '.' in tmp[8]:
                                hostIP = tmp[8]
                        else:
                            item = [
                             i]
                            if tmp[0] == 'xFx':
                                item.append(MultiContentEntryText(pos=(fhd(20), 0), size=(fhd(300), fhd(25)), font=1, text=''))
                            elif 'UA_' in tmp[0] or tmp[0] == '':
                                item.append(MultiContentEntryText(pos=(fhd(20), 0), size=(fhd(300), fhd(25)), font=1, text=hostIP))
                            else:
                                item.append(MultiContentEntryText(pos=(fhd(20), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[0]))
                            item.append(MultiContentEntryText(pos=(fhd(300), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[1]))
                            item.append(MultiContentEntryText(pos=(fhd(350), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[2]))
                            item.append(MultiContentEntryText(pos=(fhd(460), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[3]))
                            item.append(MultiContentEntryText(pos=(fhd(500), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[4]))
                            item.append(MultiContentEntryText(pos=(fhd(600), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[5]))
                            item.append(MultiContentEntryText(pos=(fhd(700), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[6]))
                            item.append(MultiContentEntryText(pos=(fhd(730), 0), size=(fhd(300), fhd(25)), font=1, text=tmp[7]))
                            tx = tmp[8]
                            if len(tx) > 30:
                                tx = tx[:30] + '...'
                            item.append(MultiContentEntryText(pos=(fhd(760), 0), size=(fhd(330), fhd(25)), font=1, text=tx))
                            self.list.append(item)

                self['entitlements_list'].l.setList(self.list)
        return


class oscam_Users(Screen):

    def __init__(self, session, url, login, passwd):
        self.skin = oscam_Users_scr
        self.session = session
        self.url = url
        self.login = login
        self.passwd = passwd
        Screen.__init__(self, session)
        self['red'] = Label(_('Exit'))
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['status_labels_0'] = Label('Address:\nProtocol:\nChannel:\nCh_Time:\nIdle:')
        self['status_values_0'] = Label('..........\n..........\n..........\n..........\n..........')
        self['status_labels_1'] = Label('OK:\nNOK:\nIGN:\nTOUT:\nCW Cycle:')
        self['status_values_1'] = Label('..........\n..........\n..........\n..........\n..........')
        self['status_labels_2'] = Label('CACHE:\nTUN:\nLTIME:\nEOK:\nENOK:')
        self['status_values_2'] = Label('..........\n..........\n..........')
        self['blue_button'] = Label('')
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.exit), 
           'ok': (self.exit), 
           'red': (self.exit), 
           'cancel': (self.exit), 
           'blue': (self.chngState), 
           'yellow': (self.exit)}, -2)
        self.refreshTimer = eTimer()
        try:
            self.refreshTimer_conn = self.refreshTimer.timeout.connect(self.oscamUsers)
        except:
            self.refreshTimer.timeout.get().append(self.oscamUsers)

        self.onLayoutFinish.append(self.oscamUsers)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('Clients Status'))
        return

    def oscamUsers(self):

        def cleanMe(w):
            w = w.replace('<b>', '').replace('</b>', '').replace('<B>', '').replace('</B>', '')
            w = w.replace('<SPAN TITLE="">', '').replace('</SPAN>', '').replace(' title="No sleep defined">', '').replace('<SPAN>', '')
            return w.replace('<BR>', '')

        self.refreshTimer.stop()
        self.newV = False
        self.list = []
        data = getUrlData(self.url + 'userconfig.html', self.login, self.passwd)
        if not isinstance(data, list):
            self.exit()
            return
        result = {}
        cnt = 0
        typeEnt = enaRead = ena_new = False
        for x in data:
            if enaRead:
                if ('\t\t\t<TD class="usercol' in x or '\t\t\t<TD CLASS="usercol' in x) and not x.__contains__('<A HREF='):
                    newData = x.replace('\t\t\t<TD class="', '').replace('</TD>', '').replace('\t\t\t<TD CLASS="', '')
                    newData = newData.replace('<b>', '').replace('</b>', '').replace('<B>', '').replace('</B>', '')
                    newData = newData.replace('<SPAN TITLE="">', '').replace('</SPAN>', '').replace(' title="No sleep defined">', '').replace('<SPAN>', '')
                    for i in range(1, 23):
                        newData = newData.replace('usercol%s">' % i, '').replace('usercol%s" TITLE="">' % i, '').replace('usercol%s" title="">' % i, '').replace('usercol%s"' % i, '')

                    x.__contains__('="groups') or result[cnt].append(newData)
            elif ena_new and '\t<TD CLASS="usercol' in x:
                if '</TD>' in x and '">' in x and '<A class="' not in x and 'CLASS="groups"' not in x and '<A HREF="user_edit.' not in x:
                    cut = False
                    if ('\t<TD CLASS="usercol2' in x or '\t<TD CLASS="usercol3' in x) and '<BR>' in x:
                        cut = True
                    tpm = x.strip().split('</TD>')[0].strip().split('">')[1]
                    if cut:
                        cut = tpm.strip().split('<BR>')
                        tpm = cut[1]
                        result[cnt].append(cleanMe(cut[0]))
                    result[cnt].append(cleanMe(tpm))
            elif ena_new and '<TD CLASS="usercol23"><A HREF="' in x:
                ena_new = False
            elif x != '':
                enaRead = False
            if x.startswith('\t\t\t<TD class="usercol1"><SPAN TITLE="">') or x.startswith('\t\t\t<TD CLASS="usercol1"><SPAN TITLE="">'):
                typeEnt = True
                enaRead = True
                cnt += 1
                newData = x.replace('\t\t\t<TD class="usercol1"><SPAN TITLE="">', '').replace('\t\t\t<TD CLASS="usercol1"><SPAN TITLE="">', '')
                newData = newData.replace('</SPAN></TD>', '')
                for i in range(1, 30):
                    newData = newData.replace('</SPAN><SPAN CLASS="span_notifier">%s' % i, '')

                result[cnt] = []
                result[cnt].append(newData)
            elif '\t\t\t<TD CLASS="usercol1" data-sort' in x and '</A>' in x and '">' in x and '<A HREF="' in x:
                self.newV = True
                typeEnt = True
                ena_new = True
                cnt += 1
                result[cnt] = []
                result[cnt].append(x.strip().split('</A>')[0].strip().split('<A HREF="')[1].strip().split('">')[1])

        if typeEnt:
            if self.newV:
                for i in list(result.keys()):
                    try:
                        tmp = result[i][4]
                        result[i][4] = result[i][6]
                        result[i][6] = tmp
                        tmp = result[i][7]
                        for x in range(7, 11):
                            result[i][x] = result[i][x + 1]

                        result[i][11] = result[i][17]
                        result[i][14] = tmp
                    except:
                        pass

            for i in list(result.keys()):
                tmp = ''
                try:
                    for x in range(0, 22):
                        if result[i][x] == '':
                            result[i][x] = '..........'
                        tmp += result[i][x] + '*'

                except:
                    pass

                tmp1 = tmp.strip().split('*')
                if len(tmp1) == 21 or len(tmp1) == 22:
                    item = [
                     tmp]
                    item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=tmp1[0]))
                    stateItem = BP_ICO % 'red'
                    if 'disabled' in tmp1[1]:
                        stateItem = BP_ICO % 'blue'
                    elif tmp1[1] != 'offline':
                        stateItem = BP_ICO % 'green'
                    pix = LoadPixmap(stateItem)
                    item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                    self.list.append(item)

        else:
            item = [
             '*']
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text='***** ' + _('No User is defined') + ' *****'))
            self.list.append(item)
        self['list'].l.setList(self.list)
        self.reactivate()
        self.refreshTimer.start(8000, True)
        return

    def exit(self):
        if self.refreshTimer.isActive():
            self.refreshTimer.stop()
        self.refreshTimer = None
        self.close()
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            if lineRq != '*':
                tmp = lineRq.strip().split('*')
                self['status_values_0'].setText(tmp[2] + '\n' + tmp[3] + '\n' + tmp[4] + '\n' + tmp[5] + '\n' + tmp[6])
                self['status_values_1'].setText(tmp[7] + '\n' + tmp[8] + '\n' + tmp[9] + '\n' + tmp[10] + '\n' + tmp[11])
                self['status_values_2'].setText(tmp[12] + '\n' + tmp[13] + '\n' + tmp[14] + '\n' + tmp[15] + '\n' + tmp[16])
                if 'disabled' in tmp[1]:
                    self['blue_button'].setText(_('Enable'))
                else:
                    self['blue_button'].setText(_('Disable'))
        return

    def chngState(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            if lineRq != '*':
                tmp = lineRq.strip().split('*')
                what = 'disable'
                if 'disabled' in tmp[1]:
                    what = 'enable'
                data = getUrlData(self.url + 'userconfig.html?user=' + tmp[0] + '&action=' + what, self.login, self.passwd)
                self.session.open(MessageBox, _('User action finished'), MessageBox.TYPE_INFO, 6)
        return


class ECMInfo(Screen):

    def __init__(self, session):
        self.skin = Ecm_Info_scr
        self.session = session
        Screen.__init__(self, session)
        self['ecmValues'] = Label()
        self.e = 'CAM:\nSystem:\nCAID:\nProvider:\nProvID:\nPID:\nCW0:\nCW1:\nUsing:\nAddress:\nHops:\nShare:\nECM Time:'
        self['ecmlabels'] = Label(self.e)
        self['piccode'] = Pixmap()
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.exit), 
           'red': (self.exit), 
           'ok': (self.exit), 
           'cancel': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit)}, -2)
        self.runECMTimer = eTimer()
        try:
            self.runECMTimer_conn = self.runECMTimer.timeout.connect(self.readEcmInfo)
        except:
            self.runECMTimer.timeout.get().append(self.readEcmInfo)

        self.onLayoutFinish.append(self.startSearchInfo)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('ECM Information'))
        return

    def exit(self):
        if self.runECMTimer.isActive():
            self.runECMTimer.stop()
        self.runECMTimer = None
        self.close()
        return

    def startSearchInfo(self):
        service = self.session.nav.getCurrentService()
        info = service and service.info()
        if info:
            serviceinfo = service.info()
            if serviceinfo.getInfo(iServiceInformation.sIsCrypted):
                self.readEcmInfo()
            else:
                self['ecmlabels'].setText(self.e)
                self['ecmValues'].setText('..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n')
                self['piccode'].instance.setPixmapFromFile(BP_ICO % 'ca_small/Fta-fs8')
        return

    def readEcmInfo(self):
        self.runECMTimer.stop()
        (oscVer, typecam, system, caid, provider, provid, pid, using, adress, hops, share, ecmTime, coding, dcw0, dcw1) = ECMparser()
        if using == 'unsupported CAs\n':
            self['ecmlabels'].setText(self.e)
            self['ecmValues'].setText('..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n')
            self['piccode'].instance.setPixmapFromFile(BP_ICO % 'ca_small/Unknown-fs8')
        elif config.plugins.GlassSysUtil.par83.value != '':
            self['ecmlabels'].setText(self.e.replace(config.plugins.GlassSysUtil.par83.value, 'CHID:'))
        self['ecmValues'].setText(typecam.replace('\n', oscVer) + coding + '\n' + caid + provider + provid + pid + dcw0 + dcw1 + using + adress + hops + share + ecmTime)
        pngName = findPicon(coding + '-fs8', 'piconCam')
        if pngName == '':
            pngName = BP_ICO % 'ca_small/Unknown-fs8'
        self['piccode'].instance.setPixmapFromFile(pngName)
        self.runECMTimer.start(5000, True)
        return


class OnScreenEcmScreen(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.rollTimerText = eTimer()
        if config.plugins.GlassSysUtil.par3.value:
            self.skin = onScreenEcmBig_scr
            try:
                self.rollTimerText_conn = self.rollTimerText.timeout.connect(self.staticEcm)
            except:
                self.rollTimerText.timeout.get().append(self.staticEcm)
            else:
                self.e = 'CAID:\nProvID:\nPID:\nSID:\nUsing:\nTime:\nSystem:\nCAM:'
                self['ecm_items'] = Label(self.e)
                self['OSD_Ecm_info'] = Label('..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............')
        else:
            self.skin = onScreenEcm_scr
            try:
                self.rollTimerText_conn = self.rollTimerText.timeout.connect(self.rollText)
            except:
                self.rollTimerText.timeout.get().append(self.rollText)

            self['OSD_Ecm_info'] = Label('         *** Ready ***')
        self.runOSDECMTimer = eTimer()
        try:
            self.runOSDECMTimer_conn = self.runOSDECMTimer.timeout.connect(self.readEcmInfo)
        except:
            self.runOSDECMTimer.timeout.get().append(self.readEcmInfo)

        self.allInfos = {}
        self.status = 'end'
        self.rstInfos()
        self.ecmInfo_time = None
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={(iPlayableService.evStopped): (self.__endShow), (iPlayableService.evTunedIn): (self.__startSearchInfo)})
        self.onShow.append(self.firstRun)
        return

    def firstRun(self):
        if self.instance:
            self.instance.move(ePoint(config.plugins.GlassSysUtil.par1.value, config.plugins.GlassSysUtil.par2.value))
        self.__startSearchInfo()
        return

    def staticEcmStart(self, tmp=''):
        if not config.plugins.GlassSysUtil.par0.value:
            return
        if self.rollTimerText.isActive():
            self.rollTimerText.stop()
        self.status = 'start'
        if tmp != '':
            if config.plugins.GlassSysUtil.par83.value != '':
                self['ecm_items'].setText(self.e.replace(config.plugins.GlassSysUtil.par83.value, 'CHID:'))
            else:
                self['ecm_items'].setText(self.e)
            self['OSD_Ecm_info'].setText(tmp)
        self.rollTimerText.start(1000 * config.plugins.GlassSysUtil.par5.value)
        OnScreenEcm.makeShow('show')
        return

    def staticEcm(self):
        self.rollTimerText.stop()
        self.status = 'end'
        OnScreenEcm.makeShow('hide')
        self['OSD_Ecm_info'].setText('..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............')
        self.runOSDECMTimer.start(1000 * config.plugins.GlassSysUtil.par81.value, True)
        return

    def StartrollTextInfo(self, what):
        if not config.plugins.GlassSysUtil.par0.value:
            return
        if self.rollTimerText.isActive():
            self.rollTimerText.stop()
        self.x = len(what)
        self.idx = 0
        self.backtext = what
        self.status = 'start'
        self.rollTimerText.start(1500)
        OnScreenEcm.makeShow('show')
        return

    def rollText(self):
        self.rollTimerText.stop()
        if self.x > 0:
            txttmp = self.backtext[self.idx:]
            x = len(txttmp)
            self['OSD_Ecm_info'].setText(txttmp[:x])
            self.idx = self.idx + 1
            self.x = self.x - 1
        if self.x == 0:
            self.status = 'end'
            OnScreenEcm.makeShow('hide')
            self['OSD_Ecm_info'].setText('       ' + _('Found changes') + ':')
            if not self.backtext.__contains__('***    ' + _('Free To Air') + '    ***'):
                self.runOSDECMTimer.start(1000 * config.plugins.GlassSysUtil.par81.value, True)
        if self.status != 'end':
            self.rollTimerText.start(config.plugins.GlassSysUtil.par78.value)
        return

    def readEcmInfo(self):
        self.runOSDECMTimer.stop()
        if not config.plugins.GlassSysUtil.par0.value:
            return
        else:
            try:
                ecmInfo_time = os.stat('/tmp/ecm.info').st_mtime
            except:
                ecmInfo_time = None

            if ecmInfo_time == self.ecmInfo_time:
                if self.status == 'end':
                    self.runOSDECMTimer.start(1000 * config.plugins.GlassSysUtil.par81.value, True)
                return
                self.ecmInfo_time = ecmInfo_time
                (oscVer, typecam, system, caid, provider, provid, pid, using, adress, hops, share, ecmTime, coding, dcw0, dcw1) = ECMparser(10)
                if using == 'unsupported CAs\n':
                    config.plugins.GlassSysUtil.par3.value or self.StartrollTextInfo('                                           ' + '***    ' + _('Unsuported CA found, incorrect ECM info') + '    ***')
                else:
                    self.staticEcmStart('\n***    ' + _('Unsuported CA found, incorrect ECM info') + '    ***')
                return
            isneedShow = False
            tmpline = tmplineStatic = ''
            if caid != self.allInfos.get('caid'):
                self.allInfos['caid'] = caid
                tmpline += ' ... CAID: ' + caid[:-1]
                isneedShow = True
            tmplineStatic = caid
            if provider != self.allInfos.get('provider'):
                self.allInfos['provider'] = provider
                tmpline += ' ... Provider: ' + provider[:-1]
                if typecam == 'OScam\n':
                    isneedShow = True
            if provid != self.allInfos.get('provid'):
                self.allInfos['provid'] = provid
                tmpline += ' ... ProvID: ' + provid[:-1]
                if typecam != 'OScam\n':
                    isneedShow = True
            tmplineStatic += provid
            if pid != self.allInfos.get('pid'):
                self.allInfos['pid'] = pid
                tmpline += ' ... PID: ' + pid[:-1]
                isneedShow = True
            tmplineStatic += pid + str(self.sid) + '\n'
            if using != self.allInfos.get('using'):
                self.allInfos['using'] = using
                tmpline += ' ... Using: ' + using[:-1]
                isneedShow = True
            tmplineStatic += using
            if adress != self.allInfos.get('adress'):
                self.allInfos['adress'] = adress
                tmpline += ' ... Address: ' + adress[:-1]
            if hops != self.allInfos.get('hops'):
                self.allInfos['hops'] = hops
                tmpline += ' ... Hops: ' + hops[:-1]
            ecmOldtmp = self.allInfos.get('ecmTime')
            if ecmTime != ecmOldtmp:
                self.allInfos['ecmTime'] = ecmTime
                if ecmTime != '..............\n' and ecmOldtmp != '..............\n':
                    try:
                        ecmOldtmp = abs(float(ecmOldtmp[:-1]) - float(ecmTime[:-1]))
                        if len(ecmTime[:-1]) > 3:
                            ecmOldtmp *= 1000
                        if int(ecmOldtmp) > config.plugins.GlassSysUtil.par4.value:
                            tmpline += ' ... ECM Time: ' + ecmTime[:-1]
                            isneedShow = True
                    except:
                        tmpline += ' ... ECM Time: ' + ecmTime[:-1]
                        isneedShow = True

                else:
                    tmpline += ' ... ECM Time: ' + ecmTime[:-1]
                    isneedShow = True
            tmplineStatic += ecmTime
            if share != self.allInfos.get('share'):
                self.allInfos['share'] = share
                tmpline += ' ... Share: ' + share[:-1]
            if coding != self.allInfos.get('coding'):
                self.allInfos['coding'] = coding
                tmpline += ' ... System: ' + coding
                isneedShow = True
            tmplineStatic += coding + '\n'
            if '(' in typecam:
                typecam = typecam.split('(')[0]
            if typecam != self.allInfos.get('typecam'):
                self.allInfos['typecam'] = typecam
                tmpline += ' ... CAM: ' + typecam.replace('\n', oscVer)
                isneedShow = True
            tmplineStatic += typecam
            if config.plugins.GlassSysUtil.par3.value or tmpline != '':
                if config.plugins.GlassSysUtil.par83.value != '':
                    tmpline = tmpline.replace(config.plugins.GlassSysUtil.par83.value, 'CHID:')
                self.StartrollTextInfo('                                           ' + tmpline + '   ')
                return
            elif isneedShow:
                self.staticEcmStart(tmplineStatic)
                return
            self.runOSDECMTimer.start(1000 * config.plugins.GlassSysUtil.par81.value, True)
            return

    def rstInfos(self):
        Required = ['caid', 
         'provider', 'pid', 
         'using', 
         'adress', 
         'hops', 'share', 
         'ecmTime', 
         'coding', 
         'typecam', 'provid']
        for x in Required:
            self.allInfos[x] = '..............\n'

        return

    def __endShow(self):
        if config.plugins.GlassSysUtil.par0.value:
            self.rstInfos()
            self.status = 'end'
            if self.runOSDECMTimer.isActive():
                self.runOSDECMTimer.stop()
            if self.rollTimerText.isActive():
                self.rollTimerText.stop()
            OnScreenEcm.makeShow('hide')
        if not config.plugins.GlassSysUtil.par3.value:
            self['OSD_Ecm_info'].setText('         *** ' + _('Ready') + ' ***')
        else:
            self['OSD_Ecm_info'].setText('..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............')
        return

    def __startSearchInfo(self):
        if config.plugins.GlassSysUtil.par0.value:
            service = self.session.nav.getCurrentService()
            info = service and service.info()
            if info:
                serviceinfo = service.info()
                if serviceinfo.getInfo(iServiceInformation.sIsCrypted):
                    self.sid = '%0.4X' % serviceinfo.getInfo(iServiceInformation.sSID)
                    self.readEcmInfo()
                elif not config.plugins.GlassSysUtil.par3.value:
                    self.StartrollTextInfo('                                      ***    ' + _('Free To Air') + '    ***')
                else:
                    self.staticEcmStart()
        return


class OnScreenEcmMain():

    def __init__(self):
        self.dialog = None
        return

    def startShowOSD(self, session):
        self.dialog = session.instantiateDialog(OnScreenEcmScreen)
        self.makeShow()
        return

    def makeShow(self, whatDo='None'):
        if whatDo == 'None':
            if config.plugins.GlassSysUtil.par0.value:
                self.dialog.show()
            else:
                self.dialog.hide()
        elif whatDo == 'show':
            self.dialog.show()
        elif whatDo == 'hide':
            self.dialog.hide()
        return


OnScreenEcm = OnScreenEcmMain()

class OSD_ECM_Menu(Screen, ConfigListScreen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        if ENA_D:
            self.skin = OSD_ECM_Menu_scr.replace('<widget name="config" font="priveG;30"', '<widget name="config"').replace('<widget name="config" font="priveG;60"', '<widget name="config"')
        else:
            self.skin = OSD_ECM_Menu_scr
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Save'))
        self['info'] = Label('')
        self['info'].hide()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': (self.save), 
           'ok': (self.ActivateselectedFnc), 
           'red': (self.exitCancel), 
           'yellow': (self.exitCancel), 
           'blue': (self.exitCancel), 
           'cancel': (self.exitCancel)}, -2)
        self.list = []
        ConfigListScreen.__init__(self, self.list, session)
        self.onLayoutFinish.append(self.updatemenulist)
        self.onLayoutFinish.append(self.setNewTitle)
        self.old0 = config.plugins.GlassSysUtil.par0.value
        self.chckTimer = eTimer()
        try:
            self.chckTimer_conn = self.chckTimer.timeout.connect(self.chckWhite)
        except:
            self.chckTimer.timeout.get().append(self.chckWhite)

        self.chckTimer.start(1000, True)
        if config.plugins.GlassSysUtil.par3.value:
            config.plugins.GlassSysUtil.par80.value = '0'
        else:
            config.plugins.GlassSysUtil.par80.value = '1'
        self.osdType = config.plugins.GlassSysUtil.par80.value
        return

    def chckWhite(self):
        self.chckTimer.stop()
        t = self['config'].getCurrent()[1]
        if t == config.plugins.GlassSysUtil.par79:
            self['info'].setText(_('Press OK to activate'))
            self['info'].show()
        elif t == config.plugins.GlassSysUtil.par80 and self.osdType != config.plugins.GlassSysUtil.par80.value:
            self['info'].setText(_('Need restart GUI/E2 to activate change of type'))
            self['info'].show()
        else:
            self['info'].hide()
        self.chckTimer.start(1000, True)
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.chckSetup()
        return

    def chckSetup(self):
        t = self['config'].getCurrent()[1]
        if t in (config.plugins.GlassSysUtil.par0, config.plugins.GlassSysUtil.par80):
            self.updatemenulist()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.chckSetup()
        return

    def updatemenulist(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Enable OSD ECM Information'), config.plugins.GlassSysUtil.par0))
        if config.plugins.GlassSysUtil.par0.value != self.old0:
            self.old0 = config.plugins.GlassSysUtil.par0.value
            self.changeShow()
        if config.plugins.GlassSysUtil.par0.value:
            self.list.append(getConfigListEntry(_('Type'), config.plugins.GlassSysUtil.par80))
            self.list.append(getConfigListEntry(_('Threshold (1 - 2000 ms)'), config.plugins.GlassSysUtil.par4))
            self.list.append(getConfigListEntry(_('ECM Refresh Time (2 - 12 s)'), config.plugins.GlassSysUtil.par81))
            if config.plugins.GlassSysUtil.par80.value == '0':
                self.list.append(getConfigListEntry(_('Show Time (4 - 15 s)'), config.plugins.GlassSysUtil.par5))
            else:
                self.list.append(getConfigListEntry(_('Rolling text speed (50 - 450 ms)'), config.plugins.GlassSysUtil.par78))
            self.list.append(getConfigListEntry(_('Set position'), config.plugins.GlassSysUtil.par79))
        self['config'].list = self.list
        self['config'].setList(self.list)
        return

    def setNewTitle(self):
        self.setTitle(_('OSD ECM Information'))
        return

    def ActivateselectedFnc(self):
        self.t = self['config'].getCurrent()[1]
        if self.t == config.plugins.GlassSysUtil.par79:
            self.setPosition()
        return

    def save(self):
        if self.osdType != config.plugins.GlassSysUtil.par80.value:
            self.changeType()
        else:
            self.saveOnly()
        return

    def saveOnly(self, rst=False):
        for x in self['config'].list:
            x[1].save()

        configfile.save()
        if rst:
            Rst_E2(True)
        else:
            self.cleanExit()
        return

    def exitCancel(self):
        for x in self['config'].list:
            x[1].cancel()

        self.changeShow()
        self.cleanExit()
        return

    def cleanExit(self):
        self.chckTimer.stop()
        self.chckTimer_conn = None
        self.chckTimer = None
        self.close()
        return

    def changeShow(self):
        if OnScreenEcm.dialog is None:
            OnScreenEcm.startShowOSD(self.session)
        OnScreenEcm.makeShow()
        return

    def changeToBig(self, whatDo):
        if whatDo:
            if config.plugins.GlassSysUtil.par80.value == '1':
                config.plugins.GlassSysUtil.par3.value = False
            else:
                config.plugins.GlassSysUtil.par3.value = True
            config.plugins.GlassSysUtil.par3.save()
            self.saveOnly(True)
        return

    def changeType(self):
        self.session.openWithCallback(self.changeToBig, MessageBox, _('Do you want restart GUI to change type OSD ECM Info?'), MessageBox.TYPE_YESNO)
        return

    def setPosition(self):
        OnScreenEcm.dialog.hide()
        self.session.openWithCallback(self.restoreShow, SelectPosition)
        return

    def restoreShow(self, what='empty'):
        OnScreenEcm.makeShow()
        return


class SelectPosition(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        if config.plugins.GlassSysUtil.par3.value:
            self.skin = onScreenEcmBig_scr
            self['ecm_items'] = Label('CAID:\nProvID:\nPID:\nSID:\nUsing:\nTime:\nSystem:\nCAM:')
            self['OSD_Ecm_info'] = Label('..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............')
        else:
            self.skin = onScreenEcm_scr
            self['OSD_Ecm_info'] = Label('         *** ' + _('Ready') + ' ***')
        self['actions'] = ActionMap(['WizardActions'], {'left': (self.left), 
           'up': (self.up), 
           'right': (self.right), 
           'down': (self.down), 
           'ok': (self.ok), 
           'back': (self.exit)}, -1)
        self.moveTimer = eTimer()
        try:
            self.moveTimer_conn = self.moveTimer.timeout.connect(self.setNewPosition)
        except:
            self.moveTimer.callback.append(self.setNewPosition)

        self.moveTimer.start(80)
        return

    def setNewPosition(self):
        self.instance.move(ePoint(config.plugins.GlassSysUtil.par1.value, config.plugins.GlassSysUtil.par2.value))
        self.moveTimer.start(80)
        return

    def left(self):
        value = config.plugins.GlassSysUtil.par1.value
        value -= 5
        if value < 0:
            value = 0
        config.plugins.GlassSysUtil.par1.value = value
        return

    def up(self):
        value = config.plugins.GlassSysUtil.par2.value
        value -= 5
        if value < 0:
            value = 0
        config.plugins.GlassSysUtil.par2.value = value
        return

    def right(self):
        value = config.plugins.GlassSysUtil.par1.value
        value += 5
        if value > fhd(1180):
            value = fhd(1180)
        config.plugins.GlassSysUtil.par1.value = value
        return

    def down(self):
        value = config.plugins.GlassSysUtil.par2.value
        value += 5
        if value > fhd(700):
            value = fhd(700)
        config.plugins.GlassSysUtil.par2.value = value
        return

    def ok(self):
        config.plugins.GlassSysUtil.par1.save()
        config.plugins.GlassSysUtil.par2.save()
        self.moveTimer = None
        self.close()
        return

    def exit(self):
        config.plugins.GlassSysUtil.par1.cancel()
        config.plugins.GlassSysUtil.par2.cancel()
        self.moveTimer = None
        self.close()
        return


class mboxInfo(Screen):

    def __init__(self, session):
        self.skin = mbox_Main
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self.menuListAll = [
         (
          'pid.info', _('Pid info')),
         (
          'share.info', _('Share Information')),
         (
          'share.onl', _('Servers Status')),
         (
          'stat.info', _('Summary Info'))]
        self.status = {}
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Select'))
        self['list'] = ListboxSys2(self.list)
        self['info'] = Label(_('No Debug info'))
        self['server_name'] = Label('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.selectedmenuitem), 
           'ok': (self.selectedmenuitem), 
           'red': (self.exit), 
           'yellow': (self.exit), 
           'blue': (self.exit), 
           'back': (self.exit)})
        self.refreshTimer = eTimer()
        try:
            self.refreshTimer_conn = self.refreshTimer.timeout.connect(self.debugStatus)
        except:
            self.refreshTimer.timeout.get().append(self.debugStatus)

        self.onLayoutFinish.append(self.updatemenulist)
        return

    def selectedmenuitem(self):
        selectedItem = self['list'].getCurrent()[0]
        enabledItem = self.status.get(selectedItem)
        if enabledItem:
            if selectedItem == 'pid.info':
                self.session.open(m_pid)
            elif selectedItem == 'share.info':
                self.session.open(m_share)
            elif selectedItem == 'share.onl':
                self.session.open(m_servers)
            elif selectedItem == 'stat.info':
                self.session.open(m_stat)
        return

    def updatemenulist(self):
        self.list = []
        for x in self.menuListAll:
            self.status[x[0]] = False
            if fileExists('/tmp/' + x[0]):
                self.status[x[0]] = True
            item = [
             x[0]]
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(535), fhd(22)), font=0, text=x[1], color=int({True: '0xffffff', False: '0x666666'}[self.status.get(x[0])], 16)))
            pix = LoadPixmap({True: (BP_ICO % 'green'), False: (BP_ICO % 'red')}[self.status.get(x[0])])
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)

        self['list'].l.setList(self.list)
        if fileExists('/tmp/mbox.ver'):
            try:
                f = open('/tmp/mbox.ver', 'r').readline()
                f = f.strip()
                self['server_name'].setText(f)
            except:
                self['server_name'].setText(_('Unknown version'))

        else:
            self['server_name'].setText(_('Unknown version'))
        if fileExists('/tmp/debug.txt'):
            self.debugStatus()
        return

    def debugStatus(self):
        self.refreshTimer.stop()
        try:
            tmp = open('/tmp/debug.txt', 'r')
            content = tmp.read()
            tmp.close
        except:
            content = ''

        lines = content.split('\n')
        if content == '':
            return
        shoutline = []
        x = i = 0
        for line in lines:
            shoutline.append(line[:-1].strip())
            x += 1

        infoline = ''
        try:
            while i < 10:
                infoline += shoutline[x - 11 + i] + '\n'
                i += 1

        except:
            pass

        if infoline == '':
            infoline = _('No Debug info')
        self['info'].setText(infoline)
        self.refreshTimer.start(8000, True)
        return

    def exit(self):
        if self.refreshTimer.isActive():
            self.refreshTimer.stop()
        self.refreshTimer = None
        self.close()
        return


class m_pid(Screen):

    def __init__(self, session):
        self.skin = mbox_pid_scr
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['red'] = Label(_('Exit'))
        self['status_labels_0'] = Label('CAID:\nSystem:\nPID:')
        self['status_values_0'] = Label('')
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'cancel': (self.close), 
           'blue': (self.close), 
           'yellow': (self.close)}, -2)
        self.onLayoutFinish.append(self.showList)
        return

    def showList(self):
        self.list = []
        try:
            tmp = open('/tmp/pid.info', 'r')
            content = tmp.read()
            tmp.close
        except:
            content = ''

        lines = content.split('\n')
        if content == '':
            self.close()
            return
        item = []
        for line in lines:
            state = False
            if line.__contains__('ECM:'):
                if line.__contains__('*ECM:'):
                    state = True
                infoline = ''
                tmp = line[:-1].strip().split(' ')
                if len(tmp) > 8:
                    infoline = tmp[3][2:].strip() + '*' + tmp[4].strip() + '*' + tmp[len(tmp) - 1][2:].strip()
                    item = [infoline]
                    item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(700), fhd(22)), font=0, text=tmp[4]))
                    pix = LoadPixmap({True: (BP_ICO % 'green'), False: (BP_ICO % 'white')}[state])
                    item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                    self.list.append(item)

        self['list'].l.setList(self.list)
        self.reactivate()
        self.setTitle(_('PID Info'))
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            tmp = lineRq.strip().split('*')
            self['status_values_0'].setText(tmp[0] + '\n' + tmp[1] + '\n' + tmp[2])
        return


class m_servers(Screen):

    def __init__(self, session):
        self.skin = mbox_servers_scr
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['red'] = Label(_('Exit'))
        self['status_labels_0'] = Label('Ip:\nBoxId:\nVersion:')
        self['status_values_0'] = Label('')
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'cancel': (self.close), 
           'blue': (self.close), 
           'yellow': (self.close)}, -2)
        self.onLayoutFinish.append(self.showList)
        return

    def showList(self):
        self.list = []
        try:
            tmp = open('/tmp/share.onl', 'r')
            content = tmp.read()
            tmp.close
        except:
            content = ''

        lines = content.split('\n')
        if content == '':
            self.close()
            return
        item = []
        c = 0
        for line in lines:
            infoline = ''
            tmp = line[:-1].strip().split(' ')
            if len(tmp) > 4:
                c += 1
                infoline = tmp[2].strip() + '*' + tmp[3].strip() + '*' + tmp[4].strip()
                item = [infoline]
                item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(700), fhd(22)), font=0, text=tmp[1]))
                item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(22), fhd(22)), text=str(c) + '.'))
                self.list.append(item)

        self['list'].l.setList(self.list)
        self.reactivate()
        self.setTitle(_('Servers Status'))
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            tmp = lineRq.strip().split('*')
            self['status_values_0'].setText(tmp[0] + '\n' + tmp[1] + '\n' + tmp[2])
        return


class m_stat(Screen):

    def __init__(self, session):
        self.skin = mbox_netstat_scr
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['red'] = Label(_('Exit'))
        self['status_labels_0'] = Label('Connected:\nON/OFF/RE:\nECM D1-D8:\nInet Up:\nInet Down:')
        self['status_values_0'] = Label('')
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'cancel': (self.close), 
           'blue': (self.close), 
           'yellow': (self.close)}, -2)
        self.onLayoutFinish.append(self.showList)
        return

    def showList(self):
        self.list = []
        try:
            tmp = open('/tmp/stat.info', 'r')
            content = tmp.read()
            tmp.close
        except:
            content = ''

        lines = content.split('\n')
        if content == '':
            self.close()
            return
        item = []
        c = 0
        for line in lines:
            infoline = ''
            tmp = line[:-1].strip().split('|')
            if len(tmp) > 5:
                c += 1
                infoline = tmp[1].strip() + '*' + tmp[2].strip() + '*' + tmp[3].strip() + '*' + tmp[4].strip() + '*' + tmp[5].strip()
                item = [infoline]
                item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(700), fhd(22)), font=0, text=tmp[0]))
                item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(22), fhd(22)), text=str(c) + '.'))
                self.list.append(item)

        self['list'].l.setList(self.list)
        self.reactivate()
        self.setTitle(_('Summary Info'))
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            tmp = lineRq.strip().split('*')
            self['status_values_0'].setText(tmp[0] + '\n' + tmp[1] + '\n' + tmp[2] + '\n' + tmp[3] + '\n' + tmp[4])
        return


class m_share(Screen):

    def __init__(self, session):
        self.skin = mbox_share_scr
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['red'] = Label(_('Exit'))
        self['status_labels_0'] = Label('Type:\nType Id:\nSl:\nLevel:\nDistance:\nId:')
        self['status_values_0'] = Label('')
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'cancel': (self.close), 
           'blue': (self.close), 
           'yellow': (self.close)}, -2)
        self.onLayoutFinish.append(self.showList)
        return

    def showList(self):
        self.list = []
        try:
            tmp = open('/tmp/share.info', 'r')
            content = tmp.read()
            tmp.close
        except:
            content = ''

        lines = content.split('\n')
        if content == '':
            self.close()
            return
        item = []
        for line in lines:
            infoline = ''
            tmp = line[:-1].strip().split(' ')
            if len(tmp) > 9:
                infoline = tmp[4].strip() + '*' + tmp[5].strip() + '*' + tmp[6][3:].strip() + '*' + tmp[7][4:].strip() + '*' + tmp[8][5:].strip() + '*' + tmp[9][3:].strip()
                item = [infoline]
                item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(700), fhd(22)), font=0, text=tmp[0] + ' ' + tmp[1] + ' at ' + tmp[3]))
                self.list.append(item)

        self['list'].l.setList(self.list)
        self.reactivate()
        self.setTitle(_('Share Information'))
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            lineRq = selection[0]
            tmp = lineRq.strip().split('*')
            self['status_values_0'].setText(tmp[0] + '\n' + tmp[1] + '\n' + tmp[2] + '\n' + tmp[3] + '\n' + tmp[4] + '\n' + tmp[5])
        return


class swap_manager(Screen):

    def __init__(self, session):
        self.skin = swap_info
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self['red'] = Label(_('Exit'))
        self['yellow'] = Label(_('Delete'))
        self['green'] = Label(_('Add'))
        self['list'] = ListboxSys2(self.list)
        self['actions'] = ActionMap(['ColorActions', 'SetupActions', 'DirectionActions', 'WizardActions'], {'yellow': (self.swapDeleteQuestion), 
           'ok': (self.add), 
           'green': (self.add), 
           'red': (self.close), 
           'cancel': (self.close)})
        self.onLayoutFinish.append(self.readSwapInfo)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def add(self):
        self.session.openWithCallback(self.readSwapInfo, SwapCreate)
        return

    def setTitlenew(self):
        self.setTitle(_('Swap Management'))
        return

    def readSwapInfo(self, callback=None):
        self.list = []
        try:
            f = open('/proc/swaps')
            content = f.read()
            f.close()
        except:
            content = ''

        item = []
        if content != '':
            if '/' in content:
                contentInfo = content.split('\n')
                for line in contentInfo:
                    if line.startswith('/'):
                        tmp = str(line).strip()
                        tmp = tmp.replace('\t', ' ')
                        while tmp.find('  ') != -1:
                            tmp = tmp.replace('  ', ' ')

                        tmp = tmp.strip().split(' ')
                        item = [tmp[0]]
                        item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(380), fhd(20)), font=0, text=tmp[0]))
                        item.append(MultiContentEntryText(pos=(fhd(400), 0), size=(fhd(80), fhd(20)), font=0, text=tmp[1]))
                        item.append(MultiContentEntryText(pos=(fhd(490), 0), size=(fhd(100), fhd(20)), font=0, text=tmp[2]))
                        item.append(MultiContentEntryText(pos=(fhd(600), 0), size=(fhd(100), fhd(20)), font=0, text=tmp[3]))
                        item.append(MultiContentEntryText(pos=(fhd(690), 0), size=(fhd(40), fhd(20)), font=0, text=tmp[4]))
                        self.list.append(item)

        if len(self.list) == 0:
            item = [
             'No swapfile']
            item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(380), fhd(20)), font=0, text=_('No swapfile')))
            item.append(MultiContentEntryText(pos=(fhd(400), 0), size=(fhd(80), fhd(20)), font=0, text='****'))
            item.append(MultiContentEntryText(pos=(fhd(490), 0), size=(fhd(100), fhd(20)), font=0, text='****'))
            item.append(MultiContentEntryText(pos=(fhd(600), 0), size=(fhd(100), fhd(20)), font=0, text='****'))
            item.append(MultiContentEntryText(pos=(fhd(690), 0), size=(fhd(40), fhd(20)), font=0, text='****'))
            self.list.append(item)
        self['list'].l.setList(self.list)
        return

    def swapDeleteQuestion(self):
        selection = self['list'].getCurrent()[0]
        if str(selection) != 'No swapfile':
            self.session.openWithCallback(self.swapDelete, MessageBox, _('Really delete swap ?'))
        else:
            self.session.open(MessageBox, _('No swapfile for delete'), MessageBox.TYPE_INFO, 4)
            self.close()
        return

    def swapDelete(self, answer):
        if answer:
            selection = self['list'].getCurrent()[0]
            if selection:
                tmp = selection
                os.system('swapoff %s' % tmp)
                os.system('rm %s' % tmp)
                info = _('Delete swap') + ': ' + tmp
                deleteFstab(tmp)
                self.session.open(MessageBox, info, MessageBox.TYPE_INFO, 4)
                self.readSwapInfo()
        return


def deleteFstab(tmp):
    try:
        f = open('/etc/fstab', 'r')
        content = f.read()
        f.close()
    except:
        content = ''

    contentInfo = content.split('\n')
    allLines = ''
    if content != '':
        for line in contentInfo:
            if line != '' and tmp not in line:
                allLines += line + '\n'

    f = open('/etc/fstab', 'w')
    f.write(allLines)
    f.close()
    return


class SwapCreate(Screen, ConfigListScreen):

    def __init__(self, session):
        if ENA_D:
            self.skin = swap_create.replace('<widget name="config" font="priveG;30"', '<widget name="config"').replace('<widget name="config" font="priveG;60"', '<widget name="config"')
        else:
            self.skin = swap_create
        self.session = session
        Screen.__init__(self, session)
        self.list = []
        self['red'] = Label(_('Exit'))
        self['green'] = Label(_('Create'))
        ConfigListScreen.__init__(self, self.list, session)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': (self.SwapCreate), 
           'ok': (self.SwapCreate), 
           'red': (self.close), 
           'cancel': (self.close)}, -2)
        self.onLayoutFinish.append(self.SwapDefine)
        return

    def mountDevices(self):
        mountPoints = []
        mountPoints.append(_('None'))
        os.system('df -h > /tmp/tempinfo.tmp')
        if fileExists('/tmp/tempinfo.tmp'):
            f = open('/tmp/tempinfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == '/media/cf':
                    mountPoints.append('/media/cf')
                if parts[totsp] == '/media/sd':
                    mountPoints.append('/media/sd')
                if parts[totsp] == '/media/usb':
                    mountPoints.append('/media/usb')
                if parts[totsp] == '/media/ba':
                    mountPoints.append('/media/ba')
                if parts[totsp] == '/media/hdd':
                    mountPoints.append('/media/hdd')

            f.close()
            os.remove('/tmp/tempinfo.tmp')
        return mountPoints

    def SwapDefine(self):
        size = [
         _('None'), '32', '64', '128', '256', '512', '1024', '2048', '4096']
        selSize = ConfigSelection(default=size[0], choices=size)
        disk = self.mountDevices()
        selDisk = ConfigSelection(default=disk[0], choices=disk)
        name = ConfigText(str(time.time()).split('.')[0], False)
        self.list = []
        self.list.append(getConfigListEntry(_('Size') + ' (MB)', selSize))
        self.list.append(getConfigListEntry(_('Disk'), selDisk))
        self.list.append(getConfigListEntry(_('Name'), name))
        self['config'].list = self.list
        self['config'].l.setList(self.list)
        self.setTitle(_('Create'))
        return

    def SwapCreate(self):
        self['config'].setCurrentIndex(0)
        swapSize = self['config'].getCurrent()[1].getText()
        self['config'].setCurrentIndex(1)
        swapPlace = self['config'].getCurrent()[1].getText()
        self['config'].setCurrentIndex(2)
        name = self['config'].getCurrent()[1].getText()
        if swapPlace == _('None') or swapSize == _('None') or name == '':
            self.session.open(MessageBox, _('Please set all parameters') + ': ' + _('Size') + ', ' + _('Disk') + ', ' + _('Name'), MessageBox.TYPE_ERROR, 4)
        else:
            swapfileName = str(swapPlace) + '/swapfile_' + str(re.sub('\\W+', '', name))
            if os.path.isfile(swapfileName):
                self.session.open(MessageBox, swapfileName + ' ' + _('is already used as swapfile'), MessageBox.TYPE_ERROR, 4)
            else:
                os.system('dd if=/dev/zero of=%s bs=1M count=%s' % (swapfileName, swapSize))
                os.system('mkswap %s' % swapfileName)
                os.system('swapon %s' % swapfileName)
                writeFstab('%s swap swap defaults 0 0\n' % swapfileName)
                self.session.open(MessageBox, _('Create swapfile finished') + ': %s' % swapfileName, MessageBox.TYPE_INFO, 4)
        self.close()
        return


def checkDevices():
    try:
        devices = []
        for x in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', '1', '0']:
            if os.path.exists('/dev/sd%s' % x):
                i = checkHdd(x)
                if i == 1:
                    devices.append(('HDD%s' % x, _('HDD'), 'sd%s' % x, 'hdd.png'))
                elif i == 2:
                    devices.append(('SSD%s' % x, _('SSD'), 'sd%s' % x, 'hdd.png'))
                else:
                    devices.append(('USB%s' % x, _('USB device'), 'sd%s' % x, 'usb.png'))
            elif os.path.exists('/dev/mmcblk%s' % x):
                if not (x == '0' and ENA_D):
                    devices.append(('SD%s' % x, _('SD card'), 'mmcblk%s' % x, 'sd.png'))

        if devices:
            return devices
        return
    except:
        return

    return


def checkHdd(ww):
    system('hdparm -I /dev/sd%s | grep Model > %s' % (ww, F_TMP))
    try:
        file = open(F_TMP)
    except IOError:
        return 0
    else:
        for line in file.readlines():
            if line.__contains__('Model') and ';' not in line:
                system(RM_TMP)
                try:
                    tmp = open('/sys/block/sd%s/queue/rotational' % ww).readline()
                    if '0' in tmp:
                        return 2
                except:
                    pass

                return 1

    file.close()
    system(RM_TMP)
    return 0


def getMount(device):
    try:
        mounts = open('/proc/mounts')
        lines = mounts.readlines()
        mounts.close()
    except IOError:
        return
    else:
        for line in lines:
            if line.startswith('/dev/%s' % device):
                return line.strip().split(' ')[1]

    return


def setUnits(value):
    if value == -1:
        return 'N/A'
    if value >= 1048576:
        return '%.1f%s' % (float(value) / 1048576, ' TB')
    if value >= 1024:
        return '%.1f%s' % (float(value) / 1024, ' GB')
    return '%.1f%s' % (float(value), ' MB')


def getSpace(device_path):
    try:
        mounts = open('/proc/mounts')
        lines = mounts.readlines()
        mounts.close()
    except IOError:
        return -1
    else:
        for line in lines:
            parts = line.strip().split(' ')
            if path.realpath(parts[0]).startswith(device_path):
                try:
                    stat = statvfs(parts[1])
                except OSError:
                    continue

                return stat.f_bfree / 1024 * stat.f_bsize / 1024

    return -1


def getUSBinfo(x):
    ena = 0
    speed = man = prod = sn = man1 = prod1 = sn1 = 'N/A'
    err = True
    for i in ['', '/device']:
        link = '/sys/block/%s%s' % (x, i)
        if os.path.islink(link):
            system('readlink -v %s > /tmp/ii' % link)
            if os.path.isfile('/tmp/ii'):
                try:
                    myfile = open('/tmp/ii', 'r')
                    line = myfile.readline().strip()
                    if line.find('/host') != -1:
                        err = False
                except IOError:
                    err = True
                else:
                    break

    system('rm -rf /tmp/ii')
    if not err:
        info = line.strip().split('/host')[1].strip().split('/target')[0]
        if len(info) != 1 or not info.isdigit():
            err = True
    if not err:
        try:
            dev = open('/proc/scsi/usb-storage/%s' % info)
            lines = dev.readlines()
            dev.close()
        except IOError:
            err = True

    if not err:
        for i in lines:
            if i.find('Vendor') != -1:
                man = i.strip().split(':')[1].strip()
            elif i.find('Product') != -1:
                prod = i.strip().split(':')[1].strip()
            elif i.find('Model Number') != -1 or i.find('Serial Number') != -1:
                sn = i.strip().split(':')[1].strip()

    if sn != 'N/A' and not err:
        try:
            dev = open('/proc/bus/usb/devices')
            lines = dev.readlines()
            dev.close()
        except IOError:
            err = True
        else:
            if not err:
                for line in lines:
                    if line.startswith('T:') and line.find('Spd=') != -1:
                        ena = 1
                        speed = line.strip().split('Spd=')[1].strip().split(' ')[0]
                    if ena == 1:
                        if line.startswith('S:'):
                            if line.find('Manufacturer=') != -1:
                                man1 = line.strip().split('Manufacturer=')[1]
                            elif line.find('Product=') != -1:
                                prod1 = line.strip().split('Product=')[1]
                            elif line.find('SerialNumber=') != -1:
                                sn1 = line.strip().split('SerialNumber=')[1]
                        elif line.startswith('I:') and line.find('Driver=') != -1 and line.find('usb-storage') != -1:
                            if man == man1 and prod == prod1 and sn == sn1:
                                ena = 2
                            else:
                                ena = 0
                                speed = man1 = prod1 = sn1 = 'N/A'
                    if ena == 2:
                        break

            else:
                err = False
                try:
                    info = line.strip().split('/host')[0].strip().split('/usb')[1].strip().split('/')[1]
                    dev = open('/sys/bus/usb/devices/%s/serial' % info)
                    sn1 = dev.readline().replace('\n', '')
                    dev.close()
                    err = True
                except IOError:
                    pass
                else:
                    try:
                        if sn == sn1 or not err:
                            dev = open('/sys/bus/usb/devices/%s/speed' % info)
                            speed = dev.readline().replace('\n', '')
                            dev.close()
                            prod1 = prod
                            man1 = man
                            sn1 = sn
                    except IOError:
                        speed = man1 = prod1 = sn1 = 'N/A'

    return ', ' + _('Vendor') + ': ' + man1 + ', ' + _('Product') + ': %s' % prod1


def readUSBHDDInfo(what):
    info = ''
    try:
        file = open(what)
    except IOError:
        return ', ' + _('Vendor') + ': N/A, ' + _('Product') + ': N/A'
    else:
        for line in file.readlines():
            if line.__contains__('Vendor'):
                info += ', ' + _('Vendor') + ': ' + line.strip().split(':')[1].strip()
            elif line.__contains__('Product'):
                info += ', ' + _('Product') + ': ' + line.strip().split(':')[1].strip()
            elif line.__contains__('Model Number'):
                info += ', ' + _('Model') + ': ' + line.strip().split(':')[1].strip()

    file.close()
    if info == '':
        return ', ' + _('Vendor') + ': N/A, ' + _('Product') + ': N/A'
    else:
        return info
    return


def getUUID(dev):
    dev = '/dev/' + dev
    os.system(RM_TMP)
    os.system('blkid %s > %s' % (dev, F_TMP))
    uuid = None
    isExt4 = 'xxx'
    try:
        f = open(F_TMP)
    except IOError:
        return (
         uuid, isExt4)
    else:
        try:
            for line in f.readlines():
                if line.__contains__(dev + ':'):
                    if 'UUID="' in line:
                        uuid = line.strip().split(' UUID="')[1].strip().split('"')[0].strip()
                    if 'TYPE="' in line:
                        isExt4 = line.strip().split(' TYPE="')[1].strip().split('"')[0].strip()
                    break

        except:
            pass

    f.close()
    os.system(RM_TMP)
    return (uuid, isExt4)


def writeFstab(what):
    try:
        allLines = ''
        ena = what.__contains__('defaults') or what.__contains__('auto,nofail') or what.__contains__('username') or what.__contains__('rsize')
        r = open('/etc/fstab', 'r')
        for line in r.readlines():
            if ena or not line.__contains__(what):
                allLines += line

        r.close()
        if ena:
            if allLines[-1] == '\n':
                allLines += what
            else:
                allLines += '\n' + what
        r = open('/etc/fstab', 'w')
        r.write(allLines)
        r.close()
    except:
        pass

    return


def chckOscamScript():
    tmp = []
    ena = False
    try:
        r = open('/usr/UCM_CamSrv_script/Oscam_Srv.sh', 'r')
        for line in r.readlines():
            if line.startswith('SrvBin=oscam'):
                ena = True
            if ena and line.startswith('/usr/UCM_CamSrv_bin/$SrvBin '):
                tmp.append(line)

        r.close()
    except:
        tmp = []

    if len(tmp) == 2:
        if tmp[0] == tmp[1]:
            return tmp[0].replace('\n', '')
    return ''


def writeOscamCfgPath():
    x = [
     '/usr/UCM_CamSrv_script/Oscam_Srv.sh', GSU_PATH + 'Auto_start/Oscam_Srv.sh']
    num = ok = 0
    for i in x:
        if fileExists(i):
            num += 1
            try:
                allLines = ''
                r = open(i, 'r')
                for line in r.readlines():
                    if not line.startswith('/usr/UCM_CamSrv_bin/$SrvBin '):
                        allLines = allLines + line
                    else:
                        allLines = allLines + config.plugins.GlassSysUtil.par21.value + '\n'

                r.close()
                r = open(i, 'w')
                r.write(allLines)
                r.close()
                tmp = []
                r = open(i, 'r')
                for line in r.readlines():
                    if line.startswith('/usr/UCM_CamSrv_bin/$SrvBin '):
                        if line.replace('\n', '') == config.plugins.GlassSysUtil.par21.value:
                            tmp.append(line.replace('\n', ''))
                            if len(tmp) == 2:
                                if tmp[0] == tmp[1]:
                                    ok += 1
                                    break

                r.close()
            except:
                pass

    if num == ok and num != 0:
        return True
    return False


def partitionsChck(part):
    system('%s -l /dev/%s > %s' % (FDISKG, part, F_TMP))
    tmp = True
    try:
        file = open(F_TMP)
    except IOError:
        system(RM_TMP)
        return False
    else:
        for line in file.readlines():
            if 'partition' in line.lower() and 'doesn' in line.lower():
                tmp = False
                break

    file.close()
    system(RM_TMP)
    return tmp


class devMngMain(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skin = devices_management_main
        self.list = []
        self.listDevices = checkDevices()
        self['devices'] = ListboxSys3(self.list)
        self['devices'].onSelectionChanged.append(self.reactivate)
        self['button_bg'] = Label('')
        self['green'] = Label(_('Select'))
        self['red'] = Label(_('Exit'))
        self['yellow'] = Label(_('Add CIFS/NFS'))
        self.enaNet = False
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': (self.selection), 
           'green': (self.selection), 
           'yellow': (self.createNetmount), 
           'blue': (self.delNetmount), 
           'red': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.updateDevList)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('Devices Manager'))
        return

    def selection(self):
        selected = self['devices'].getCurrent()[0]
        if selected:
            if self.netMount[0] == 'nfs' or self.netMount[0] == 'cifs':
                self.createNetmount(selected)
            elif 'x' not in selected:
                sel = selected[len(selected) - 1]
                if sel in ('0', '1'):
                    self.partSeltoFix = 'mmcblk' + sel
                else:
                    self.partSeltoFix = 'sd' + sel
                if not partitionsChck(self.partSeltoFix):
                    self.session.openWithCallback(self.fixPartitions, MessageBox, _('Partition table entries are not in disk order, are you want to fix it? (all data will be destroyed)'), MessageBox.TYPE_YESNO)
                else:
                    self.session.openWithCallback(self.updateDevList, selectPartition, self.partSeltoFix, selected[:-1])
        return

    def fixPartitions(self, a):
        if a:
            a = '4'
            if HardwareInfo().get_device_name() == 'dm800':
                a = '3'
            system('{\necho y\n} | mkfs.ext%s /dev/%s' % (a, self.partSeltoFix))
            system('{\necho w\n} | %s /dev/%s' % (FDISKG, self.partSeltoFix))
            if partitionsChck(self.partSeltoFix):
                self.session.open(MessageBox, _('Partition table fixed'), MessageBox.TYPE_INFO, 6)
            else:
                self.session.open(MessageBox, _('Error while fixing of Partition table, please use external Partition manager to fix it'), MessageBox.TYPE_INFO, 6)
        return

    def updateDevList(self, answer=''):
        icon_path = GSU_PATH + {3: 'uhd/devices/', 1.5: 'fhd/devices/', 1: 'devices/'}[FHD]
        self.list = []
        if self.listDevices is not None:
            device_capacity = '  -  ( N/A )'
            device_info = _('Mounted') + ': N/A'
            info = ', ' + _('Vendor') + ': N/A, ' + _('Product') + ': N/A'
            system('%s -l | grep Disk > /tmp/tmpCap.tmp' % FDISKG)
            for x in self.listDevices:
                (cap, err) = self.getCapacity('/dev/%s' % x[2])
                device_capacity = ')  -  ( %s / %s )' % (setUnits(getSpace('/dev/%s' % x[2])), cap)
                device_info = _('Mounted') + ': ' + _(str(getMount(x[2])))
                if 'HDD' not in x[0] and 'SSD' not in x[0]:
                    info = getUSBinfo('sd' + x[0].replace('USB', ''))
                else:
                    system('hdparm -I /dev/%s | grep Model > %s' % (x[2], F_TMP))
                    info = readUSBHDDInfo(F_TMP)
                    system(RM_TMP)
                device_info += info
                txtx = self.numPart(x[0].replace('USB', ''))
                if txtx:
                    device_info += ', ' + _('blocked')
                elif err:
                    device_info += ', ' + _('probably damaged')
                if 'N/A / N/A' not in device_capacity:
                    item = [{False: (x[0]), True: 'x'}[txtx]]
                    item.append(MultiContentEntryText(pos=(fhd(60), fhd(10)), size=(fhd(720), fhd(50)), font=0, text=x[1] + ' (' + x[2] + device_capacity))
                    item.append(MultiContentEntryText(pos=(fhd(60), fhd(50)), size=(fhd(720), fhd(30)), font=1, text=device_info))
                    item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(10)), size=(fhd(40), fhd(80)), png=LoadPixmap(icon_path + x[3])))
                    item.append(MultiContentEntryText(pos=(0, fhd(78)), size=(fhd(760), fhd(1)), font=1, text=' ', backcolor=int('0x888888', 16)))
                    self.list.append(item)

            system('rm -rf /tmp/tmpCap.tmp')
        try:
            mounts = open('/proc/mounts')
            lines = mounts.readlines()
            mounts.close()
        except IOError:
            mounts = ''

        if mounts != '':
            for line in lines:
                if (line.__contains__('nfs') or line.__contains__('cifs')) and not line.__contains__('/proc/'):
                    try:
                        line = line.strip().split(' ')
                        line[2] = {False: 'cifs', True: 'nfs'}['nfs' in line[2]]
                        item = [line[2] + '*' + line[0] + '*' + line[1]]
                        item.append(MultiContentEntryText(pos=(fhd(60), fhd(10)), size=(fhd(720), fhd(50)), font=0, text=_('Network device') + ' - ' + line[2].upper()))
                        item.append(MultiContentEntryText(pos=(fhd(60), fhd(50)), size=(fhd(720), fhd(30)), font=1, text=_('Mounted') + ': ' + line[1] + ', ' + _('Source') + ': %s' % line[0]))
                        item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(10)), size=(fhd(40), fhd(80)), png=LoadPixmap(icon_path + line[2] + '.png')))
                        item.append(MultiContentEntryText(pos=(0, fhd(78)), size=(fhd(760), fhd(1)), font=1, text=' ', backcolor=int('0x888888', 16)))
                        self.list.append(item)
                    except:
                        pass

        if len(self.list) == 0:
            item = [
             'empty']
            item.append(MultiContentEntryText(pos=(fhd(60), fhd(10)), size=(fhd(720), fhd(50)), font=0, text=_('No USB device, HDD or NET mount is detected')))
            item.append(MultiContentEntryText(pos=(0, fhd(78)), size=(fhd(760), fhd(1)), font=1, text=' ', backcolor=int('0x888888', 16)))
            self.list.append(item)
        self['devices'].l.setList(self.list)
        return

    def numPart(self, part):
        if 'HDD' in part or 'SD' in part:
            return False
        dev = '/dev/sd%s' % part
        system('%s -l %s > %s' % (FDISKG, dev, F_TMP))
        try:
            file = open(F_TMP)
        except IOError:
            system(RM_TMP)
            return True
        else:
            tmp = False
            for line in file.readlines():
                if line.__contains__('Partition'):
                    tmp = True
                    break
                if line.startswith(dev):
                    part = line.strip().split(' ')[0]
                    if len(part) == 9 and 'Extended' in line:
                        tmp = True

        file.close()
        system(RM_TMP)
        return tmp

    def reactivate(self):
        selection = self['devices'].getCurrent()
        if selection:
            lineRq = selection[0]
            self.enaNet = False
            try:
                self.netMount = lineRq.strip().split('*')
                if self.netMount[0] == 'nfs' or self.netMount[0] == 'cifs':
                    self.enaNet = True
                    self['button_bg'].setText(_('Delete'))
                else:
                    self['button_bg'].setText('')
            except:
                self['green'].setText(_('Select'))
                self['button_bg'].setText('')

        return

    def getCapacity(self, what):
        info = 'N/A'
        error = False
        try:
            file = open('/tmp/tmpCap.tmp')
        except IOError:
            return (
             info, True)
        else:
            for line in file.readlines():
                if line.__contains__(what + ':') and ('GB' in line or 'MB' in line or 'TB' in line):
                    try:
                        info = line.strip().split(':')[1].strip().split(',')[0]
                    except:
                        error = True
                    else:
                        break

        file.close()
        return (info, error)

    def createNetmount(self, w=None):
        self.session.openWithCallback(self.updateDevList, createCifsNfs, w)
        return

    def delNetmount(self):
        if self.enaNet:
            self.session.openWithCallback(self.delAnswer, MessageBox, _('Are you sure to unmount?') + ' ' + self.netMount[2], MessageBox.TYPE_YESNO)
        return

    def delAnswer(self, answer):
        if answer:
            system('umount %s' % self.netMount[2])
            if not chckMount(self.netMount[2]):
                writeFstab(self.netMount[2])
                msg = _('Unmount finished correctly')
            else:
                msg = _('Unmount failed')
            self.session.openWithCallback(self.updateDevList, MessageBox, msg, MessageBox.TYPE_INFO, 6)
        return


class createCifsNfs(Screen, ConfigListScreen):

    def __init__(self, session, w):
        Screen.__init__(self, session)
        if ENA_D:
            self.skin = cifsNfsScr.replace('<widget name="config" font="priveG;30"', '<widget name="config"').replace('<widget name="config" font="priveG;60"', '<widget name="config"')
        else:
            self.skin = cifsNfsScr
        self.list = []
        self.w = w
        ConfigListScreen.__init__(self, self.list, session, on_change=self.changedEntry)
        self['green'] = Label(_('Mount'))
        self['red'] = Label(_('Exit'))
        self['yellow'] = Label(_('/etc/nfs_cifs.cfg'))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': (self.doNetmount), 
           'ok': (self.doNetmount), 
           'yellow': (self.fromFile), 
           'red': (self.exit), 
           'cancel': (self.exit)}, -2)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('CIFS/NFS'))
        if self.w:
            t = None
            try:
                self.w = self.w.replace('//', '').strip().split('*')
                config.plugins.GlassSysUtil.par6.value = self.w[0].upper()
                i = self.w[1].split('/')
                config.plugins.GlassSysUtil.par13.value = i[0]
                config.plugins.GlassSysUtil.par7.value = '/' + i[1]
                config.plugins.GlassSysUtil.par8.value = self.w[2]
                f = open('/etc/fstab')
                lines = f.readlines()
                f.close()
                for i in lines:
                    if i.__contains__(self.w[1]) and i.__contains__(self.w[0]) and i.__contains__(self.w[2]):
                        t = i
                        break

            except:
                pass
            else:
                self.w = None
                if t:
                    t = re.sub('\\s+', ' ', t)
                    if config.plugins.GlassSysUtil.par6.value == 'CIFS':
                        if 'username=' in t:
                            i = t.split('username=')[1]
                            if ',password=' in i:
                                i = i.split(',password=')[0]
                            else:
                                i = i.split(' ')[0]
                            config.plugins.GlassSysUtil.par9.value = i
                        if 'password=' in t:
                            config.plugins.GlassSysUtil.par10.value = t.split('password=')[1].split(' ')[0]
                    else:
                        if 'nolock' in t:
                            config.plugins.GlassSysUtil.par59.value = True
                        if config.plugins.GlassSysUtil.par59.value:
                            if 'udp,' in i or 'tcp,' in i:
                                if 'udp,' in i:
                                    i = 'udp'
                                if 'tcp,' in i:
                                    i = 'tcp'
                                config.plugins.GlassSysUtil.par82.value = i
                        if 'rsize=' in t:
                            i = t.split('rsize=')[1]
                            if ',wsize=' in i:
                                i = i.split(',wsize=')[0]
                            else:
                                i = i.split(' ')[0]
                            config.plugins.GlassSysUtil.par11.value = i
                        if 'wsize=' in t:
                            i = t.split('wsize=')[1]
                            if ',nolock' in i:
                                i = i.split(',nolock')[0]
                            else:
                                i = i.split(' ')[0]
                            config.plugins.GlassSysUtil.par12.value = i
        self.setMenu()
        return

    def setMenu(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Select type'), config.plugins.GlassSysUtil.par6))
        self.list.append(getConfigListEntry(_('Source IP'), config.plugins.GlassSysUtil.par13))
        self.list.append(getConfigListEntry(_('Source Dir'), config.plugins.GlassSysUtil.par7))
        self.list.append(getConfigListEntry(_('Destination'), config.plugins.GlassSysUtil.par8))
        if config.plugins.GlassSysUtil.par6.value == 'CIFS':
            self.list.append(getConfigListEntry(_('Username'), config.plugins.GlassSysUtil.par9))
            self.list.append(getConfigListEntry(_('Password'), config.plugins.GlassSysUtil.par10))
        else:
            self.list.append(getConfigListEntry(_('Use NFS mount cmd with "nolock" option'), config.plugins.GlassSysUtil.par59))
            if config.plugins.GlassSysUtil.par59.value:
                self.list.append(getConfigListEntry(_('Protocol'), config.plugins.GlassSysUtil.par82))
            self.list.append(getConfigListEntry(_('Set rsize'), config.plugins.GlassSysUtil.par11))
            self.list.append(getConfigListEntry(_('Set wsize'), config.plugins.GlassSysUtil.par12))
        self['config'].list = self.list
        self['config'].setList(self.list)
        return

    def changedEntry(self):
        t = self['config'].getCurrent()[1]
        if t in (config.plugins.GlassSysUtil.par6, config.plugins.GlassSysUtil.par59):
            self.setMenu()
        return

    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.changedEntry()
        return

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.changedEntry()
        return

    def doNetmount(self):
        msg = realizeNetmount(config.plugins.GlassSysUtil.par6.value, config.plugins.GlassSysUtil.par13.value, config.plugins.GlassSysUtil.par7.value, config.plugins.GlassSysUtil.par8.value, config.plugins.GlassSysUtil.par9.value, config.plugins.GlassSysUtil.par10.value, config.plugins.GlassSysUtil.par11.value, config.plugins.GlassSysUtil.par12.value)
        self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, 6)
        return

    def fromFile(self):
        msg = fromFile2()
        self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, 15)
        return

    def exit(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close()
        return


class HDD_USB_SD_Main(Screen):

    def __init__(self, session, what, isHDD, part=''):
        Screen.__init__(self, session)
        self.isHDD = isHDD
        self.host = what
        self.infoCmd = ''
        if self.isHDD in ('SSD', 'HDD'):
            self.host += part
            self.skin = usbhdd_management
            if self.isHDD == 'HDD':
                self.a = _('HDD Management')
            else:
                self.a = _('SSD Management')
            self.mountNew = '/media/hdd'
            self.infoCmd = 'hdparm -I /dev/%s' % self.host
        elif 'mmcblk' in self.host:
            self.skin = usbhdd_management.replace('hdd2.png', 'sd2.png')
            self.a = _('SD card Management')
            self.mountNew = '/media/cf'
            if part == '':
                self.host += part
            else:
                self.host += 'p' + part
        else:
            self.mountNew = '/media/usb'
            self.a = _('USB device Management')
            self.skin = usbhdd_management.replace('hdd2.png', 'usb2.png')
            self.host += part
            if getUSBinfo(self.host) != ', ' + _('Vendor') + ': N/A, ' + _('Product') + ': N/A':
                self.infoCmd = 'cat /proc/scsi/usb-storage/%s ' % {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6'}[self.host.replace('sd', '')]
        self.list = []
        self.status = {}
        self['green'] = Label(_('Select'))
        self['red'] = Label(_('Exit'))
        self['info'] = Label('')
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.reactivate)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': (self.selection), 
           'green': (self.selection), 
           'red': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.updateHddList)
        self.onLayoutFinish.append(self.setWindowTitle)
        return

    def setWindowTitle(self):
        self.setTitle(self.a + ': %s' % self.host)
        return

    def updateHddList(self, answer=''):
        mountCmdAs = '*'
        isMounted = True
        if getMount(self.host) is None:
            isMounted = False
        isPM = chckMount(self.mountNew)
        (self.uuid, self.isExt4) = getUUID(self.host)
        if self.uuid is not None:
            mountCmdAs = 'mount -t auto /dev/disk/by-uuid/%s ' % self.uuid
        self.menuListAll = [('0', _('Formating (ext3)'), '{\necho y\n} | mkfs.ext3 /dev/%s' % self.host, _('Formating (filesystem ext3), all data will be destroyed, available on unmounted device only')),
         (
          '1', _('Formating (ext4)'), '{\necho y\n} | mkfs.ext4 /dev/%s' % self.host, _('Formating (filesystem ext4), all data will be destroyed, available on unmounted device only')),
         (
          '2', _('Filesystem Check (ext3)'), 'fsck.ext3 -f -v -y -C 0 /dev/%s' % self.host, _('Filesystem checking (ext3), available on unmounted device only')),
         (
          '3', _('Filesystem Check (ext4)'), 'fsck.ext4 -f -v -y -C 0 /dev/%s' % self.host, _('Filesystem checking (ext4), available on unmounted device only')),
         (
          '4', _('Mount'), mountCmdAs, _('Mounting with standard option, available on unmounted device only') + ' (%s)' % self.mountNew),
         (
          '5', _('Mount as ...'), mountCmdAs, _('Mounting with user defined path')),
         (
          '6', _('Unmount'), 'umount /dev/%s' % self.host, _('Unmounting try unmount from all mounting paths of device')),
         (
          '7', _('All mount points'), 'cat /proc/mounts', _('Displaying all mounting points in system')),
         (
          '8', _('Extended info'), self.infoCmd, _('Displaying extended info about device'))]
        self.list = []
        for x in self.menuListAll:
            self.status[x[0]] = True
            if x[0] == '4' and isPM or x[0] in ('1', '3') and HardwareInfo().get_device_name() == 'dm800' or x[0] == '3' and self.isExt4 != 'ext4' or x[0] == '2' and self.isExt4 != 'ext3' or x[0] in ('2', '5', '6', '3', '4') and self.uuid is None or x[0] in ('0', '1', '2', '3', '4') and isMounted or x[0] == '6' and not isMounted or x[0] == '8' and self.infoCmd == '':
                self.status[x[0]] = False
            item = [
             x[0]]
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(300), fhd(22)), font=0, text=x[1], color=int({True: '0xffffff', False: '0x666666'}[self.status.get(x[0])], 16)))
            pix = LoadPixmap({True: (BP_ICO % 'green'), False: (BP_ICO % 'red')}[self.status.get(x[0])])
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)

        self['list'].l.setList(self.list)
        return

    def reactivate(self):
        selection = self['list'].getCurrent()
        if selection:
            tmp2 = int(selection[0])
            tmp = str(self.menuListAll[tmp2][3])
            self['info'].setText(tmp)
        return

    def selection(self):
        selectedItem = self['list'].getCurrent()[0]
        enabledItem = self.status.get(selectedItem)
        if enabledItem:
            tmp2 = int(selectedItem)
            cmd = str(self.menuListAll[tmp2][2])
            cmdTitle = str(self.menuListAll[tmp2][1])
            if selectedItem in ('0', '1'):
                msg = _('All data will be destroyed, do you wish to continue?')
                self.session.openWithCallback(self.formatAnswer, MessageBox, msg, MessageBox.TYPE_YESNO)
            elif selectedItem == '4':
                self.mountAnswer(self.mountNew.replace('/media/', ''))
            elif selectedItem == '6':
                system(cmd)
                if getMount(self.host) is None:
                    deleteFstab(self.uuid)
                    deleteFstab(self.host)
                    msg = _('Unmount finished correctly')
                else:
                    msg = _('Unmount failed')
                self.session.openWithCallback(self.updateHddList, MessageBox, msg, MessageBox.TYPE_INFO, 6)
            elif selectedItem in ('2', '7', '8', '3'):
                self.session.open(Console, title=cmdTitle, cmdlist=[cmd])
            elif selectedItem == '5':
                self.session.openWithCallback(self.mountAnswer, InputBox, title=_('Please enter name for target') + ': ', text='dir_name            ', maxSize=30, type=Input.TEXT)
        return

    def mountAnswer(self, answer):
        if answer is None:
            return
        else:
            answer = answer.strip()
            mountNew = '/media/' + answer
            if os.path.exists(mountNew):
                if chckMount(mountNew):
                    self.session.open(MessageBox, answer + ' ' + _('is mounted, please, select another'), MessageBox.TYPE_INFO, 6)
                    return
            else:
                system('mkdir /media/' + answer)
            selectedItem = self['list'].getCurrent()[0]
            tmp2 = int(selectedItem)
            cmd = str(self.menuListAll[tmp2][2]) + mountNew
            state = False
            if '*' not in cmd:
                system(cmd)
                if chckMount(mountNew):
                    writeFstab('/dev/disk/by-uuid/%s\t%s\tauto\tauto,nofail\t0\t0\n' % (self.uuid, mountNew))
                    state = True
                else:
                    system('mount -t auto /dev/%s %s' % (self.host, mountNew))
                    if chckMount(mountNew):
                        writeFstab('/dev/%s %s auto defaults 0 0\n' % (self.host, mountNew))
                        state = True
            if state:
                if self.isHDD in ('HDD', 'SSD') and answer == 'hdd':
                    if not os.path.exists(mountNew + '/movie'):
                        system('mkdir %s/movie' % mountNew)
                msg = _('Mount finished correctly')
            else:
                msg = _('Mount failed')
            self.session.openWithCallback(self.updateHddList, MessageBox, msg, MessageBox.TYPE_INFO, 6)
            return

    def formatAnswer(self, answer):
        if answer:
            selectedItem = self['list'].getCurrent()[0]
            tmp2 = int(selectedItem)
            cmd = str(self.menuListAll[tmp2][2])
            cmdTitle = str(self.menuListAll[tmp2][1])
            self.session.openWithCallback(self.updateHddList, Console, title=cmdTitle, cmdlist=[cmd])
        return


class selectPartition(Screen):

    def __init__(self, session, device, typeDev):
        Screen.__init__(self, session)
        self.skin = select_Partition
        if 'mmcblk' in device:
            self.devPart = 'p'
        else:
            self.devPart = ''
        self.device = device
        self.typeDev = typeDev
        self.ena = True
        self.list = []
        self['green'] = Label(_('Select'))
        self['green'].hide()
        self['red'] = Label(_('Exit'))
        self['yellow'] = Label(_('Add'))
        self['blue'] = Label(_('Delete'))
        self['blue'].hide()
        self['part'] = Label(_('Name'))
        self['mnt'] = Label(_('Mounted') + ':')
        self['start'] = Label(_('Beginning') + ':')
        self['end'] = Label(_('End') + ':')
        self['size'] = Label(_('Size') + ':')
        self['id'] = Label(_('ID') + ':')
        self['fstype'] = Label(_('Type') + ':')
        self['list'] = ListboxSys2(self.list)
        self['list'].onSelectionChanged.append(self.enaSelection)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': (self.selection), 
           'yellow': (self.addPartition), 
           'blue': (self.delPartition), 
           'green': (self.selection), 
           'red': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.showPartition)
        self.onShow.append(self.setWindowTitle)
        return

    def enaSelection(self):
        s = self['list'].getCurrent()[0]
        if s:
            if '*x' in s:
                self['green'].hide()
            else:
                self['green'].show()
        return

    def setWindowTitle(self):
        self.setTitle(_('Partitions management') + ' (%s/%s)' % (self.typeDev, self.device))
        return

    def showPartition(self, s=''):
        self.list = []
        self.ena = True
        dptmp = '/tmp/dp'
        system('%s -l /dev/%s > %s' % (FDISKG, self.device, dptmp))
        try:
            f = open(dptmp, 'r').read()
            if f.find('heads') != -1:
                f = open(dptmp)
                self.ena = False
        except IOError:
            pass

        self.numParts = 0
        if not self.ena:
            self.allItems = []
            for x in range(1, 5):
                item1 = [
                 str(x)]
                item1.append('0')
                item1.append('0')
                self.allItems.append(item1)

            for line in f.readlines():
                if line.__contains__('heads'):
                    line = line.strip().split(',')
                    heads = line[0].strip().split(' ')[0]
                    sectors = line[1].strip().split(' ')[0]
                    self.maxCylinders = int(line[2].strip().split(' ')[0])
                    self.geoConstant = int(heads) * int(sectors) * 512
                i = 0
                while i != 5:
                    i += 1
                    if line.__contains__(self.device + self.devPart + str(i)):
                        self.numParts += 1
                        line = line.strip().split('/')
                        line = line[2].replace('*', '')
                        line = line.strip().split(' ')
                        tmp = ''
                        for x in range(len(line)):
                            if line[x] != '':
                                tmp += line[x] + '-'

                        tmp = tmp.strip().split('-')
                        tmp1 = getMount(self.device + self.devPart + str(i))
                        if tmp1 is None:
                            tmp1 = '----------'
                        item = [
                         str(i) + '*' + tmp1]
                        item.append(MultiContentEntryText(pos=(fhd(2), 2), size=(fhd(40), fhd(25)), font=0, text=str(i) + '.'))
                        item.append(MultiContentEntryText(pos=(fhd(40), 2), size=(fhd(130), fhd(25)), font=0, text=line[0]))
                        item.append(MultiContentEntryText(pos=(fhd(190), 2), size=(fhd(200), fhd(25)), font=0, text=tmp1))
                        item.append(MultiContentEntryText(pos=(fhd(430), 2), size=(fhd(200), fhd(25)), font=0, text=tmp[1]))
                        item.append(MultiContentEntryText(pos=(fhd(600), 2), size=(fhd(200), fhd(25)), font=0, text=tmp[2]))
                        item.append(MultiContentEntryText(pos=(fhd(770), 2), size=(fhd(120), fhd(25)), font=0, text=self.sizePart((int(tmp[2]) - int(tmp[1]) + 1) * self.geoConstant)))
                        item.append(MultiContentEntryText(pos=(fhd(890), 2), size=(fhd(50), fhd(25)), font=0, text=tmp[4]))
                        item.append(MultiContentEntryText(pos=(fhd(940), 2), size=(fhd(120), fhd(25)), font=0, text=tmp[5]))
                        self.list.append(item)
                        self.allItems[i - 1][1] = tmp[1]
                        self.allItems[i - 1][2] = tmp[2]

            f.close()
        system('rm -rf %s' % dptmp)
        if self.numParts == 0:
            self['blue'].hide()
            if not self.ena:
                item = [
                 '*']
                tmp = '***  ' + _('No partitions detected') + '  ***'
                detMount = getMount(self.device)
                if detMount is not None:
                    tmp = '***   ' + self.device + ' ' + _('have no partions, but is mounted to') + ' ' + detMount + '   ***'
            else:
                item = [
                 '*x']
                tmp = '***  ' + _('Partitions detetection failed, device cannot be managed') + '  ***'
            item.append(MultiContentEntryText(pos=(fhd(2), 2), size=(fhd(800), fhd(25)), font=0, text=tmp))
            self.list.append(item)
        else:
            self['blue'].show()
        self['list'].l.setList(self.list)
        return

    def sizePart(self, value):
        if value >= 1099511627776:
            return '%.1f%s' % (float(value) / 1099511627776, ' TB')
        if value >= 1073741824:
            return '%.1f%s' % (float(value) / 1073741824, ' GB')
        return '%.1f%s' % (float(value) / 1048576, ' MB')

    def selection(self):
        partition = self['list'].getCurrent()[0]
        if '*x' in partition:
            return
        if partition != '*':
            partition = partition.strip().split('*')[0]
            self.session.openWithCallback(self.showPartition, HDD_USB_SD_Main, self.device, self.typeDev, partition)
        else:
            self.session.openWithCallback(self.noPartAnswer, MessageBox, self.device + ' - ' + _('have no partitions, do you want manage device without using partition?'), MessageBox.TYPE_YESNO)
        return

    def noPartAnswer(self, answer):
        if answer:
            self.session.openWithCallback(self.showPartition, HDD_USB_SD_Main, self.device, self.typeDev)
        return

    def addPartition(self):
        if self.ena:
            return
        else:
            if self.numParts == 0:
                detMount = getMount(self.device)
                if detMount is not None:
                    self.session.open(MessageBox, self.device + ' ' + _('device is mounted to') + ' ' + detMount + ' ' + _('unmount first'), MessageBox.TYPE_INFO, 6)
                    return
            if self.numParts == 4:
                self.session.open(MessageBox, _('Max of available partitions is in use, delete one or more partition(s) first'), MessageBox.TYPE_INFO, 6)
                return
            space = 0
            for x in range(0, 4):
                sub = int(self.allItems[x][2]) - int(self.allItems[x][1])
                if sub != 0:
                    space += sub + 1

            if space == self.maxCylinders:
                self.session.open(MessageBox, _('No more space to create of any partition'), MessageBox.TYPE_INFO, 6)
            elif (self.maxCylinders - space) * self.geoConstant < 300000000:
                self.session.open(MessageBox, _('Too little space to create of any partition (less than 300MB)'), MessageBox.TYPE_INFO, 6)
            else:
                self.session.openWithCallback(self.numAddPartition, InputBox, title=_('Partition') + ': ', text='1', maxSize=1, type=Input.NUMBER)
            return

    def numAddPartition(self, num):
        if num is not None:
            if self.allItems[int(num) - 1][1] == '0' and self.allItems[int(num) - 1][2] == '0':
                self.cmdItems = str(num) + '*'
                minCylinders = int(300000000 / self.geoConstant)
                if num == '1':
                    self.firstFreeCyl = 1
                    self.direct = True
                    if self.allItems[1][1] == '0':
                        if self.allItems[2][1] == '0':
                            if self.allItems[3][1] == '0':
                                self.lastFreeCyl = self.maxCylinders
                            else:
                                self.lastFreeCyl = int(self.allItems[3][1]) - 1
                        else:
                            self.lastFreeCyl = int(self.allItems[2][1]) - 1
                    else:
                        self.lastFreeCyl = int(self.allItems[1][1]) - 1
                elif num == '2':
                    if self.allItems[0][1] == '0':
                        self.firstFreeCyl = 1
                        self.direct = False
                    else:
                        self.firstFreeCyl = int(self.allItems[0][2]) + 1
                        self.direct = True
                    if self.allItems[2][1] == '0':
                        if self.allItems[3][1] == '0':
                            self.lastFreeCyl = self.maxCylinders
                        else:
                            self.lastFreeCyl = int(self.allItems[3][1]) - 1
                    else:
                        self.lastFreeCyl = int(self.allItems[2][1]) - 1
                elif num == '3':
                    if self.allItems[1][1] == '0':
                        if self.allItems[0][1] == '0':
                            self.firstFreeCyl = 1
                        else:
                            self.firstFreeCyl = int(self.allItems[0][2]) + 1
                    else:
                        self.firstFreeCyl = int(self.allItems[1][2]) + 1
                    if self.allItems[3][1] == '0':
                        self.lastFreeCyl = self.maxCylinders
                        self.direct = True
                    else:
                        self.lastFreeCyl = int(self.allItems[3][1]) - 1
                        self.direct = False
                elif num == '4':
                    self.lastFreeCyl = self.maxCylinders
                    self.direct = False
                    if self.allItems[2][1] == '0':
                        if self.allItems[1][1] == '0':
                            if self.allItems[0][1] == '0':
                                self.firstFreeCyl = 1
                            else:
                                self.firstFreeCyl = int(self.allItems[0][2]) + 1
                        else:
                            self.firstFreeCyl = int(self.allItems[1][2]) + 1
                    else:
                        self.firstFreeCyl = int(self.allItems[2][2]) + 1
                else:
                    self.session.open(MessageBox, _('Number of the partitions have to be in the range (1-4)'), MessageBox.TYPE_INFO, 6)
                    return
                if self.lastFreeCyl - self.firstFreeCyl < minCylinders:
                    self.session.open(MessageBox, _('Too little space to create of the partition') + ': %s' % num, MessageBox.TYPE_INFO, 6)
                    return
                self.maxSpace = float((self.lastFreeCyl - self.firstFreeCyl) * self.geoConstant / 1048576)
                if self.maxSpace >= 1048576:
                    showMaxfree = '%.1f%s' % (float(self.maxSpace) / 1048576, 'TB')
                elif self.maxSpace >= 1024:
                    showMaxfree = '%.1f%s' % (float(self.maxSpace) / 1024, 'GB')
                else:
                    showMaxfree = '%.1f%s' % (float(self.maxSpace), 'MB')
                self.session.openWithCallback(self.sizeAddPartition, InputBox, title='000MB = max(' + showMaxfree + '), ' + _('or') + ' 300MB-%s' % showMaxfree, text='000MB', maxSize=5, type=Input.TEXT)
            else:
                self.session.open(MessageBox, _('Partition is in use, please, select another'), MessageBox.TYPE_INFO, 6)
        return

    def sizeAddPartition(self, size):
        if size is not None:
            msg = ''
            if size == '000MB':
                self.cmdItems += str(self.firstFreeCyl) + '*' + str(self.lastFreeCyl)
            else:
                if 'MB' in size:
                    try:
                        reqSize = int(size.strip().split('M')[0])
                    except:
                        self.session.open(MessageBox, _('Entered wrong data, have to be: XXXMB, where XXX is Number'), MessageBox.TYPE_INFO, 6)
                        return

                elif 'GB' in size:
                    if '.' in size:
                        try:
                            tmp = size.strip().split('G')[0]
                            tmp = tmp.strip().split('.')
                            if len(tmp[0]) != 1 and len(tmp[1]) != 1:
                                self.session.open(MessageBox, _('Entered wrong data, have to be: X.XGB, where X.X is Number'), MessageBox.TYPE_INFO, 6)
                                return
                            reqSize = int(tmp[0]) * 1024 + int(tmp[1]) * 100
                        except:
                            self.session.open(MessageBox, _('Entered wrong data, have to be: X.XGB, where X.X is Number'), MessageBox.TYPE_INFO, 6)
                            return

                    else:
                        try:
                            reqSize = int(size.strip().split('G')[0]) * 1024
                        except:
                            self.session.open(MessageBox, _('Entered wrong data, have to be: XXXGB, where XXX is Number'), MessageBox.TYPE_INFO, 6)
                            return

                elif 'TB' in size:
                    if '.' in size:
                        try:
                            tmp = size.strip().split('T')[0]
                            tmp = tmp.strip().split('.')
                            if len(tmp[0]) != 1 and len(tmp[1]) != 1:
                                self.session.open(MessageBox, _('Entered wrong data, have to be: X.XTB, where X.X is Number'), MessageBox.TYPE_INFO, 6)
                                return
                            reqSize = int(tmp[0]) * 1048576 + int(tmp[1]) * 102400
                        except:
                            self.session.open(MessageBox, _('Entered wrong data, have to be: X.XTB, where X.X is Number'), MessageBox.TYPE_INFO, 6)
                            return

                    else:
                        try:
                            reqSize = int(size.strip().split('T')[0]) * 1048576
                        except:
                            self.session.open(MessageBox, _('Entered wrong data, have to be: XTB, where X is Number'), MessageBox.TYPE_INFO, 6)
                            return

                else:
                    self.session.open(MessageBox, _('Entered wrong data, TB, GB or MB is missing'), MessageBox.TYPE_INFO, 6)
                    return
                if reqSize < self.maxSpace and reqSize > int(300000000 / 1048576):
                    cylinders = int(reqSize * 1024 * 1024 / self.geoConstant)
                    if self.direct:
                        self.cmdItems += str(self.firstFreeCyl) + '*' + str(self.firstFreeCyl + cylinders)
                    else:
                        self.cmdItems += str(self.lastFreeCyl - cylinders) + '*' + str(self.lastFreeCyl)
                else:
                    self.session.open(MessageBox, _('Entered wrong data, size out of range'), MessageBox.TYPE_INFO, 6)
                    return
            self.cmdItems = self.cmdItems.strip().split('*')
            system('{\necho n\necho p\necho %s\necho %s\necho %s\necho w\n} | %s /dev/%s' % (self.cmdItems[0], self.cmdItems[1], self.cmdItems[2], FDISKG, self.device))
            system('%s -l /dev/%s > %s' % (FDISKG, self.device, F_TMP))
            try:
                file = open(F_TMP)
            except IOError:
                system(RM_TMP)
                self.session.open(MessageBox, _('Error reading partition info'), MessageBox.TYPE_INFO, 6)
                return
            else:
                for line in file.readlines():
                    if line.__contains__('/dev/%s%s%s' % (self.device, self.devPart, self.cmdItems[0])):
                        self.session.openWithCallback(self.rstAnswer, MessageBox, _('Partition created, formating of the partition is needed before using') + '\n' + _('Restart enigma2/GUI is recommended to get correct device mounting by UUID, restart now? '), MessageBox.TYPE_YESNO)
                        return

                self.session.open(MessageBox, _('Creating the partition failed'), MessageBox.TYPE_INFO, 6)
        return

    def rstAnswer(self, a):
        Rst_E2(a)
        self.showPartition()
        return

    def delPartition(self):
        if self.ena:
            return
        partition = self['list'].getCurrent()[0]
        if partition != '*':
            partDev = partition.strip().split('*')[0]
            isMounted = partition.strip().split('*')[1]
            if '*x' in partition or isMounted == '----------':
                msg = _('All data will be destroyed, do you wish to continue?')
                self.session.openWithCallback(self.delAnswer, MessageBox, msg, MessageBox.TYPE_YESNO)
            else:
                msg = _('Mounted partition can not be deleted') + '\n(' + self.device + partDev + ' ' + _('is mounted as') + ' %s)' % isMounted
                self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, 6)
        return

    def delAnswer(self, answer):
        if answer:
            partition = self['list'].getCurrent()[0]
            partDev = partition.strip().split('*')[0]
            system('{\necho d\necho %s\necho w\n} | %s /dev/%s' % (partDev, FDISKG, self.device))
            msg = _('Partition deleted')
            self.session.openWithCallback(self.showPartition, MessageBox, msg, MessageBox.TYPE_INFO, 6)
        return


class autoInstallMain(Screen, ConfigListScreen):

    def __init__(self, session):
        Screen.__init__(self, session)
        if ENA_D:
            self.skin = autoInst_cfg.replace('<widget name="config" font="priveG;30"', '<widget name="config"').replace('<widget name="config" font="priveG;60"', '<widget name="config"')
        else:
            self.skin = autoInst_cfg
        self['green'] = Label(_('Save'))
        self['red'] = Label(_('Exit'))
        self['yellow'] = Label(_('Status'))
        self['blue'] = Label(_('Install'))
        self['white'] = Label(_('Press OK to select dir'))
        self['white'].hide()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': (self.save), 
           'ok': (self.ActivateselectedFnc), 
           'blue': (self.doItnow), 
           'yellow': (self.showState), 
           'red': (self.exitCancel), 
           'cancel': (self.exitCancel)}, -2)
        self.list = []
        ConfigListScreen.__init__(self, self.list, session)
        self.onLayoutFinish.append(self.runSetup)
        self.onLayoutFinish.append(self.setNewtitle)
        self.old = config.plugins.GlassSysUtil.par15
        self.chckTimer = eTimer()
        try:
            self.chckTimer_conn = self.chckTimer.timeout.connect(self.chckWhite)
        except:
            self.chckTimer.timeout.get().append(self.chckWhite)

        self.chckTimer.start(1000, True)
        return

    def chckWhite(self):
        self.chckTimer.stop()
        t = self['config'].getCurrent()[1]
        if self.old != t:
            self.old = t
            if t == config.plugins.GlassSysUtil.par14:
                self['white'].show()
            else:
                self['white'].hide()
        self.chckTimer.start(1000, True)
        return

    def setNewtitle(self):
        self.setTitle(_('AutoInstall'))
        return

    def runSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Enable AutoInstall (when E2 is started)'), config.plugins.GlassSysUtil.par15))
        self.list.append(getConfigListEntry(_('AutoInstall dir(full path)'), config.plugins.GlassSysUtil.par14))
        self['config'].list = self.list
        self['config'].setList(self.list)
        return

    def ActivateselectedFnc(self):
        t = self['config'].getCurrent()[1]
        if t == config.plugins.GlassSysUtil.par14:
            self.session.openWithCallback(self.dirSelected, dirBrowser, config.plugins.GlassSysUtil.par14.value)
        return

    def dirSelected(self, answer):
        if answer is not None:
            config.plugins.GlassSysUtil.par14.value = answer
            self.runSetup()
        return

    def doItnow(self):
        self.session.openWithCallback(self.doItnowAnswer, MessageBox, _('Do you want to install files from') + ': %s' % config.plugins.GlassSysUtil.par14.value, MessageBox.TYPE_YESNO)
        return

    def doItnowAnswer(self, answer):
        if answer:
            autoInstallMng.autoInstMain()
        return

    def showState(self):
        if self.trySavePath():
            self.session.open(autoInstStatus)
        return

    def trySavePath(self):
        tmp = config.plugins.GlassSysUtil.par14.value[:-1]
        os.path.exists(tmp) or system('mkdir ' + tmp)
        if not os.path.exists(tmp):
            self.session.open(MessageBox, tmp + ' ' + _('cannot be created, please, select another'), MessageBox.TYPE_INFO, 5)
            return False
            config.plugins.GlassSysUtil.par14.save()
            return True
        else:
            config.plugins.GlassSysUtil.par14.save()
            return True
        return

    def save(self):
        if self.trySavePath():
            for x in self['config'].list:
                x[1].save()

            configfile.save()
            self.close()
        return

    def exitCancel(self):
        self.chckTimer.stop()
        self.chckTimer = None
        self.chckTimer_conn = None
        for x in self['config'].list:
            x[1].cancel()

        self.close()
        return


class autoInstallMngMain():

    def __init__(self):
        self.cmd = ''
        return

    def autoInstallStart(self, session):
        self.session = session
        self.startTimer = eTimer()
        try:
            self.startTimer_conn = self.startTimer.timeout.connect(self.autoInstMain)
        except:
            self.startTimer.timeout.get().append(self.autoInstMain)

        if config.plugins.GlassSysUtil.par15.value:
            self.startTimer.start(60000, True)
        else:
            self.startTimer = None
        return

    def autoInstMain(self):
        if self.startTimer is not None:
            self.startTimer.stop()
            self.startTimer = None
            self.startTimer_conn = None
        ipk_list = self.autoInstIpkList()
        if len(ipk_list) == 0:
            return
        else:
            for ipk in ipk_list:
                if fileExists(config.plugins.GlassSysUtil.par14.value + ipk + '.' + PKG):
                    if ENA_D:
                        self.cmd = 'dpkg -i --force-overwrite %s%s.deb > %s' % (PKGBIN, config.plugins.GlassSysUtil.par14.value, ipk, F_TMP)
                    else:
                        self.cmd = '%spkg install --force-overwrite --force-downgrade %s%s.ipk > %s' % (PKGBIN, config.plugins.GlassSysUtil.par14.value, ipk, F_TMP)
                    x = self.InstIpk(ipk)

            return

    def InstIpk(self, ipk):
        system(self.cmd)
        try:
            allLines = ''
            error = False
            r = open(F_TMP, 'r')
            for line in r.readlines():
                if line.__contains__('error'):
                    error = True
                    break

            r.close()
            system(RM_TMP)
            r = open(GSU_PATH + 'autoInstall_status', 'r')
            for line in r.readlines():
                if line.__contains__(ipk):
                    if error:
                        allLines = allLines + PKG + ': ' + ipk + '*error\n'
                    else:
                        allLines = allLines + PKG + ': ' + ipk + '*ok\n'
                else:
                    allLines = allLines + line

            r.close()
            r = open(GSU_PATH + 'autoInstall_status', 'w')
            r.write(allLines)
            r.close()
        except:
            pass

        return True

    def autoInstIpkList(self):
        result = []
        allLines = ''
        status_file = GSU_PATH + 'autoInstall_status'
        try:
            f = listDir(config.plugins.GlassSysUtil.par14.value[:-1])
            if f:
                for x in f:
                    if '.' + PKG in x:
                        tmp = x[:-4]
                        r = open(status_file, 'r')
                        founded = False
                        for line in r.readlines():
                            if line.__contains__(tmp):
                                if line.__contains__('*error') or line.__contains__('*new'):
                                    result.append(tmp)
                                allLines = allLines + line
                                founded = True
                                break

                        if not founded:
                            allLines = allLines + PKG + ': ' + tmp + '*new\n'
                            result.append(tmp)
                        r.close()

                r = open(status_file, 'w')
                r.write(allLines)
                r.close()
        except:
            pass

        return result


autoInstallMng = autoInstallMngMain()

class autoInstStatus(Screen):

    def __init__(self, session):
        self.skin = autoInstStatus_scr
        self.session = session
        Screen.__init__(self, session)
        self.status = {}
        self.list = []
        self['list'] = ListboxSys2(self.list)
        self['red'] = Label(_('Exit'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': (self.close), 
           'ok': (self.close), 
           'red': (self.close), 
           'yellow': (self.close), 
           'blue': (self.close), 
           'back': (self.close)})
        self.onLayoutFinish.append(self.readStatus)
        return

    def readStatus(self):
        item = []
        c = 0
        status_file = GSU_PATH + 'autoInstall_status'
        ipk_list = autoInstallMng.autoInstIpkList()
        try:
            f = open(status_file, 'r')
            content = f.read()
            f.close()
        except:
            content = ''

        contentInfo = content.split('\n')
        if content != '':
            item = [
             '***']
            item.append(MultiContentEntryText(pos=(fhd(25), 0), size=(fhd(150), fhd(22)), font=0, text='- ' + _('new')))
            pix = LoadPixmap(BP_ICO % 'yellow')
            item.append(MultiContentEntryPixmapAlphaTest(pos=(0, fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            item.append(MultiContentEntryText(pos=(fhd(210), 0), size=(fhd(250), fhd(22)), font=0, text='- ' + _('error while installing')))
            pix = LoadPixmap(BP_ICO % 'red')
            item.append(MultiContentEntryPixmapAlphaTest(pos=(fhd(185), fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            item.append(MultiContentEntryText(pos=(fhd(530), 0), size=(fhd(150), fhd(22)), font=0, text='- ' + _('installed')))
            pix = LoadPixmap(BP_ICO % 'green')
            item.append(MultiContentEntryPixmapAlphaTest(pos=(fhd(505), fhd(3)), size=(fhd(15), fhd(16)), png=pix))
            self.list.append(item)
            for line in contentInfo:
                if line.startswith(PKG + ': '):
                    tmp = line.strip().split(' ')[1]
                    tmp = tmp.strip().split('*')
                    if len(tmp) > 1:
                        c = c + 1
                        item = [line]
                        item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(35), fhd(22)), font=0, text=str(c) + '.'))
                        item.append(MultiContentEntryText(pos=(fhd(65), 0), size=(fhd(695), fhd(22)), font=0, text=tmp[0]))
                        ico = 'blue'
                        if tmp[1] == 'error':
                            ico = 'red'
                        elif tmp[1] == 'new':
                            ico = 'yellow'
                        elif tmp[1] == 'ok':
                            ico = 'green'
                        pix = LoadPixmap(BP_ICO % ico)
                        item.append(MultiContentEntryPixmapAlphaTest(pos=(fhd(40), fhd(3)), size=(fhd(15), fhd(16)), png=pix))
                        self.list.append(item)

        if len(item) == 0:
            item = [
             '*']
            item.append(MultiContentEntryText(pos=(0, 0), size=(fhd(350), fhd(22)), font=0, text=_('No files detected')))
            self.list.append(item)
        self['list'].l.setList(self.list)
        self.setTitle(_('Status'))
        return


class UCMPanel():
    __module__ = __name__

    def __init__(self):
        self['UCMPanel'] = ActionMap(['InfobarExtensions'], {'UCM_conect': (self.UCM_Open)})
        return

    def UCM_Open(self):
        self.session.open(univCamMng)
        return


def fill(a, b, c=5):
    d = ''
    if c == 0:
        d = ' '
    for i in range(c, len(b) - 1):
        a += b[i] + d

    if c == 0:
        return a[:-1]
    return a


class cronMng(Screen):

    def __init__(self, session):
        self.skin = cronMng_scr
        self.session = session
        Screen.__init__(self, session)
        self.Console = CompConsole()
        self.crond_autostart = False
        self.crond_state = False
        self['key_ok'] = Label(_('(OK) - Edit'))
        self['key_green'] = Label(_('Add'))
        self['key_red'] = Label(_('Delete'))
        self['key_yellow'] = Label(_('Start'))
        self['key_blue'] = Label(_('Enable Autostart'))
        self.list = []
        self['list'] = ListboxSys(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'MenuActions'], {'ok': (self.info), 'back': (self.close), 
           'green': (self.addtocron), 
           'red': (self.delcron), 
           'yellow': (self.CrondStart), 
           'blue': (self.autostart)})
        self.onLayoutFinish.append(self.updateList)
        return

    def CrondStart(self):
        if self.crond_state == False:
            self.Console.ePopen('/etc/init.d/busybox-cron start')
            sleep(3)
            self.updateList()
        elif self.crond_state == True:
            self.Console.ePopen('/etc/init.d/busybox-cron stop')
            sleep(3)
            self.updateList()
        return

    def autostart(self):
        a = self.symUnlink('/etc/init.d/busybox-cron', '/etc/rc0.d/K20busybox-cron')
        a = self.symUnlink('/etc/init.d/busybox-cron', '/etc/rc1.d/K20busybox-cron')
        a = self.symUnlink('/etc/init.d/busybox-cron', '/etc/rc2.d/S20busybox-cron')
        a = self.symUnlink('/etc/init.d/busybox-cron', '/etc/rc3.d/S20busybox-cron')
        a = self.symUnlink('/etc/init.d/busybox-cron', '/etc/rc4.d/S20busybox-cron')
        a = self.symUnlink('/etc/init.d/busybox-cron', '/etc/rc5.d/S20busybox-cron')
        a = self.symUnlink('/etc/init.d/busybox-cron', '/etc/rc6.d/K20busybox-cron')
        self.updateList()
        return

    def symUnlink(self, b, a):
        try:
            if path.exists(a):
                unlink(a)
            else:
                symlink(b, a)
        except:
            pass

        return True

    def addtocron(self):
        self.session.openWithCallback(self.updateList, SetupCronConf)
        return

    def delcron(self):
        selection = self['list'].getCurrent()
        if selection:
            line = str(selection[0])
            if line != '***':
                box = self.session.openWithCallback(self.doDelCron, MessageBox, _('Do you want delete?') + '\n\n %s' % str(selection[2][7]), MessageBox.TYPE_YESNO)
                box.setTitle(_('Delete ?'))
        return

    def doDelCron(self, answer):
        if answer:
            selection = self['list'].getCurrent()
            if selection:
                line = str(selection[0])
                if line != '***':
                    open('/etc/cron/crontabs/temp.tmp', 'w').writelines([l for l in open('/etc/cron/crontabs/root').readlines() if line not in l])
                    rename('/etc/cron/crontabs/temp.tmp', '/etc/cron/crontabs/root')
                    system('crontab /etc/cron/crontabs/root -c /etc/cron/crontabs')
                    self.updateList()
        return

    def info(self):
        selection = self['list'].getCurrent()
        if selection:
            line = str(selection[0])
            if line != '***':
                self.session.openWithCallback(self.updateList, SetupCronConf, line)
        return

    def updateList(self):
        self.crond_autostart = False
        self.crond_state = False
        state = _('Crond Status') + ': ' + _('Stopped') + ', ' + _('Autostart') + ': ' + _('Disabled')
        if generatePS():
            f = open(A_TM, 'r')
            for line in f.readlines():
                if 'crond' in line:
                    self.crond_state = True
                    state = state.replace(_('Stopped'), _('Running'))

            f.close()
            system(RM_A_TMP)
        if path.exists('/etc/rc3.d/S20busybox-cron'):
            self.crond_autostart = True
            state = state.replace(_('Disabled'), _('Enabled'))
        if self.crond_state:
            self['key_yellow'].setText(_('Stop'))
        else:
            self['key_yellow'].setText(_('Start'))
        if self.crond_autostart:
            self['key_blue'].setText(_('Disable Autostart'))
        else:
            self['key_blue'].setText(_('Enable Autostart'))
        self.setTitle(state)
        self.list = []
        item = []
        if path.exists('/etc/cron/crontabs/root'):
            f = open('/etc/cron/crontabs/root', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts:
                    txt = ''
                    ena = False
                    for x in range(0, len(parts) - 1):
                        if not parts[x].isdigit() and parts[x] != '*':
                            ena = True
                            break

                    if ena or '* * * * * ' in line:
                        txt = _('Time Definition') + ': ' + fill(txt, parts, 0)
                    elif parts[1] == '*':
                        txt = _('Hourly') + ':' + _(' Min') + ' ' + parts[0] + fill(txt, parts)
                    elif parts[2] == '*' and parts[4] == '*':
                        txt = _('Daily') + ': ' + parts[1] + ':' + parts[0].zfill(2) + ' ' + fill(txt, parts)
                    elif parts[3] == '*':
                        if parts[4] == '*':
                            txt = _('Monthly') + ': ' + _('Day') + ' ' + parts[2] + '  ' + parts[1] + ':' + parts[0].zfill(2) + ' ' + fill(txt, parts)
                        week = _('Weekly') + ': '
                        day = ''
                        if str(parts[4]).find('0') >= 0:
                            day = _('Sunday') + ' '
                        if str(parts[4]).find('1') >= 0:
                            day += _('Monday') + ' '
                        if str(parts[4]).find('2') >= 0:
                            day += _('Tuesday') + ' '
                        if str(parts[4]).find('3') >= 0:
                            day += _('Wednesday') + ' '
                        if str(parts[4]).find('4') >= 0:
                            day += _('Thursday') + ' '
                        if str(parts[4]).find('5') >= 0:
                            day += _('Friday') + ' '
                        if str(parts[4]).find('6') >= 0:
                            day += _('Saturday') + ' '
                        if day:
                            txt = week + day + parts[1] + ':' + parts[0].zfill(2) + ' ' + fill(txt, parts)
                    if txt != '':
                        item = [
                         line]
                        item.append(MultiContentEntryText(pos=(0, fhd(6)), size=(fhd(455), fhd(30)), font=1, text=txt, color=int('0xffffff', 16)))
                        item.append(MultiContentEntryText(pos=(fhd(460), fhd(6)), size=(fhd(540), fhd(30)), font=1, text=parts[len(parts) - 1], color=int('0xffcc00', 16)))
                        self.list.append(item)

            f.close()
        if len(self.list) == 0:
            item = [
             '***']
            item.append(MultiContentEntryText(pos=(fhd(0), fhd(6)), size=(fhd(1000), fhd(30)), font=1, text='***     ' + _('None Cron command/script detected') + '     ***', color=int('0xff3300', 16)))
            self.list.append(item)
        self['list'].l.setList(self.list)
        return


class SetupCronConf(Screen, ConfigListScreen):

    def __init__(self, session, line=None):
        Screen.__init__(self, session)
        if ENA_D:
            self.skin = cronScr.replace('<widget name="config" font="priveG;30"', '<widget name="config"').replace('<widget name="config" font="priveG;60"', '<widget name="config"')
        else:
            self.skin = cronScr
        self.list = []
        self.l = line
        ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
        self['key_green'] = Label(_('Save'))
        self['key_red'] = Label(_('Cancel'))
        self['key_txt'] = Label(_('TXT'))
        self['actions'] = ActionMap(['WizardActions',
         'ColorActions',
         'VirtualKeyboardActions',
         'MenuActions'], {'green': (self.chcknewCron), 'back': (self.close), 
           'red': (self.close), 
           'ok': (self.chcknewCron), 
           'showVirtualKeyboard': (self.KeyText)})
        self.createSetup(self.l)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        if self.l:
            self.setTitle(_('Edit'))
        else:
            self.setTitle(_('Add'))
        return

    def createSetup(self, l=None):
        predefinedlist = []
        f = listDir('/usr/script')
        if f:
            for line in f:
                parts = line.split()
                path = '/usr/script/'
                pkg = parts[0]
                description = path + parts[0]
                if pkg.find('.sh') >= 0:
                    predefinedlist.append((description, pkg))

            predefinedlist.sort()
        else:
            predefinedlist.append(('None', _('None')))
        config.plugins.GlassSysUtil.par46 = NoSave(ConfigSelection(choices=predefinedlist))
        if l:
            l = l.replace('\n', '')
            tmp = l.strip().split()
            ena = False
            for x in range(0, len(tmp) - 1):
                if not tmp[x].isdigit() and tmp[x] != '*':
                    ena = True
                    break

            if ena or '* * * * * ' in l:
                config.plugins.GlassSysUtil.par43.value = '0'
                config.plugins.GlassSysUtil.par76.value = fill('', tmp, 0)
            else:
                config.plugins.GlassSysUtil.par77.value = int(tmp[0])
                if ' * * * * ' in l:
                    config.plugins.GlassSysUtil.par43.value = 'Hourly'
                else:
                    config.plugins.GlassSysUtil.par41.value = int(tmp[1])
                    if ' * * * ' in l:
                        config.plugins.GlassSysUtil.par43.value = 'Daily'
                    elif ' * * 0 ' in l or ' * * 1 ' in l or ' * * 2 ' in l or ' * * 3 ' in l or ' * * 4 ' in l or ' * * 5 ' in l or ' * * 6 ' in l:
                        config.plugins.GlassSysUtil.par43.value = 'Weekly'
                        if ' * * 0 ' in l:
                            config.plugins.GlassSysUtil.par44.value = 'Sunday'
                        elif ' * * 1 ' in l:
                            config.plugins.GlassSysUtil.par44.value = 'Monday'
                        elif ' * * 2 ' in l:
                            config.plugins.GlassSysUtil.par44.value = 'Tuesday'
                        elif ' * * 3 ' in l:
                            config.plugins.GlassSysUtil.par44.value = 'Wednesday'
                        elif ' * * 4 ' in l:
                            config.plugins.GlassSysUtil.par44.value = 'Thursday'
                        elif ' * * 5 ' in l:
                            config.plugins.GlassSysUtil.par44.value = 'Friday'
                        elif ' * * 6 ' in l:
                            config.plugins.GlassSysUtil.par44.value = 'Saturday'
                    elif ' * * ' in l:
                        config.plugins.GlassSysUtil.par45.value = int(tmp[2])
                        config.plugins.GlassSysUtil.par43.value = 'Monthly'
            tmp = tmp[len(tmp) - 1].strip()
            ena = False
            for x in range(0, len(predefinedlist)):
                if predefinedlist[x][0] == tmp:
                    ena = True
                    break

            if ena:
                config.plugins.GlassSysUtil.par46.value = tmp
                config.plugins.GlassSysUtil.par42.value = 'None'
                config.plugins.GlassSysUtil.par47.value = '/usr/script'
            else:
                config.plugins.GlassSysUtil.par47.value = 'User'
                config.plugins.GlassSysUtil.par42.value = tmp
        self.finishSetup()
        return

    def finishSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('When') + ': ', config.plugins.GlassSysUtil.par43))
        if config.plugins.GlassSysUtil.par43.value == '0':
            self.list.append(getConfigListEntry(_('Time Definition') + ': ', config.plugins.GlassSysUtil.par76))
        elif config.plugins.GlassSysUtil.par43.value != 'Hourly':
            self.list.append(getConfigListEntry(_('Hour') + ': ', config.plugins.GlassSysUtil.par41))
        self.list.append(getConfigListEntry(_('Minute') + ': ', config.plugins.GlassSysUtil.par77))
        if config.plugins.GlassSysUtil.par43.value == 'Weekly':
            self.list.append(getConfigListEntry(_('Day of Week') + ': ', config.plugins.GlassSysUtil.par44))
        if config.plugins.GlassSysUtil.par43.value == 'Monthly':
            self.list.append(getConfigListEntry(_('Day of Month') + ': ', config.plugins.GlassSysUtil.par45))
        self.list.append(getConfigListEntry(_('Command Type') + ': ', config.plugins.GlassSysUtil.par47))
        if config.plugins.GlassSysUtil.par47.value == 'User':
            self.list.append(getConfigListEntry(_('Command to Run') + ': ', config.plugins.GlassSysUtil.par42))
        else:
            self.list.append(getConfigListEntry(_('Command to Run') + ': ', config.plugins.GlassSysUtil.par46))
        self['config'].list = self.list
        self['config'].setList(self.list)
        return

    def changedEntry(self):
        t = self.getCurrentEntry()
        if t == _('When') + ': ' or t == _('Command Type') + ': ':
            self.finishSetup()
        return

    def getCurrentEntry(self):
        return self['config'].getCurrent()[0]

    def KeyText(self):
        sel = self['config'].getCurrent()
        if sel:
            self.vkvar = sel[0]
            if sel[0] == _('Command to Run') + ': ' and config.plugins.GlassSysUtil.par47.value == 'User' or sel[0] == _('Time Definition') + ': ':
                from Screens.VirtualKeyBoard import VirtualKeyBoard
                self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self.getCurrentEntry(), text=self['config'].getCurrent()[1].getValue())
        return

    def VirtualKeyBoardCallback(self, callback=None):
        if callback is not None and len(callback):
            self['config'].getCurrent()[1].setValue(callback)
            self['config'].invalidate(self['config'].getCurrent())
        return

    def chcknewCron(self):
        msg = ''
        if config.plugins.GlassSysUtil.par47.value == '/usr/script' and config.plugins.GlassSysUtil.par46.value == 'None' or config.plugins.GlassSysUtil.par47.value == 'User' and config.plugins.GlassSysUtil.par42.value == '':
            msg = _('Please set at least one Command')
        if msg:
            self.session.open(MessageBox, msg, MessageBox.TYPE_ERROR)
        else:
            self.save()
        return

    def save(self):
        hour = '%s' % config.plugins.GlassSysUtil.par41.value
        minutes = '%s' % config.plugins.GlassSysUtil.par77.value
        if config.plugins.GlassSysUtil.par47.value == '/usr/script' and config.plugins.GlassSysUtil.par46.value != 'None':
            command = config.plugins.GlassSysUtil.par46.value
        else:
            command = config.plugins.GlassSysUtil.par42.value
        if config.plugins.GlassSysUtil.par43.value == 'Hourly':
            newcron = minutes + ' ' + ' * * * * '
        elif config.plugins.GlassSysUtil.par43.value == 'Daily':
            newcron = minutes + ' ' + hour + ' * * * '
        elif config.plugins.GlassSysUtil.par43.value == 'Weekly':
            if config.plugins.GlassSysUtil.par44.value == 'Sunday':
                newcron = minutes + ' ' + hour + ' * * 0 '
            elif config.plugins.GlassSysUtil.par44.value == 'Monday':
                newcron = minutes + ' ' + hour + ' * * 1 '
            elif config.plugins.GlassSysUtil.par44.value == 'Tuesday':
                newcron = minutes + ' ' + hour + ' * * 2 '
            elif config.plugins.GlassSysUtil.par44.value == 'Wednesday':
                newcron = minutes + ' ' + hour + ' * * 3 '
            elif config.plugins.GlassSysUtil.par44.value == 'Thursday':
                newcron = minutes + ' ' + hour + ' * * 4 '
            elif config.plugins.GlassSysUtil.par44.value == 'Friday':
                newcron = minutes + ' ' + hour + ' * * 5 '
            elif config.plugins.GlassSysUtil.par44.value == 'Saturday':
                newcron = minutes + ' ' + hour + ' * * 6 '
        elif config.plugins.GlassSysUtil.par43.value == 'Monthly':
            newcron = minutes + ' ' + hour + ' ' + str(config.plugins.GlassSysUtil.par45.value) + ' * * '
        else:
            newcron = config.plugins.GlassSysUtil.par76.value + ' '
        newcron += command.strip() + '\n'
        if not os.path.exists('/etc/cron/crontabs'):
            system('mkdir /etc/cron')
            system('mkdir /etc/cron/crontabs')
        if self.l:
            if self.l != newcron:
                tmp = ''
                for l in open('/etc/cron/crontabs/root').readlines():
                    if self.l in l:
                        tmp += newcron
                    else:
                        tmp += l

                open('/etc/cron/crontabs/temp.tmp', 'w').writelines(tmp)
                rename('/etc/cron/crontabs/temp.tmp', '/etc/cron/crontabs/root')
        else:
            out = open('/etc/cron/crontabs/root', 'a')
            out.write(newcron)
            out.close()
        system('crontab /etc/cron/crontabs/root -c /etc/cron/crontabs')
        config.plugins.GlassSysUtil.par46.value = 'None'
        config.plugins.GlassSysUtil.par42.value = 'None'
        config.plugins.GlassSysUtil.par43.value = 'Daily'
        config.plugins.GlassSysUtil.par44.value = 'Monday'
        config.plugins.GlassSysUtil.par45.value = 1
        config.plugins.GlassSysUtil.par41.value = 1
        config.plugins.GlassSysUtil.par77.value = 1
        config.plugins.GlassSysUtil.par76.value = 'None'
        self.close()
        return


class TxtEditor(Screen):

    def __init__(self, session, filename):
        if ENA_D:
            self.skin = txtEdScr.replace('<widget name="txt" font="priveG;30"', '<widget name="txt"').replace('<widget name="txt" font="priveG;60"', '<widget name="txt"')
        else:
            self.skin = txtEdScr
        self.session = session
        Screen.__init__(self, session)
        self.file_name = filename
        self.list = []
        self['txt'] = MenuList(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': (self.editLine), 
           'green': (self.editLine), 
           'yellow': (self.exitAndSave), 
           'red': (self.close), 
           'back': (self.close)})
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('Edit line'))
        self['key_yellow'] = Label(_('Save and Exit'))
        self.selectedLine = None
        self.oldLine = None
        self.isChanged = False
        self.Gettxt(filename)
        return

    def exitAndSave(self):
        if self.isChanged:
            updTitle = self.session.openWithCallback(self.SaveEditedFile, MessageBox, self.file_name + ' ' + _('have been changed! Do you want to save it?'), MessageBox.TYPE_YESNO)
            updTitle.setTitle(_('Text Editor'))
        else:
            self.close()
        return

    def Gettxt(self, filename):
        try:
            flines = open(filename, 'r')
            for line in flines:
                self.list.append(line)

            flines.close()
            self.setTitle(filename)
        except:
            pass

        return

    def editLine(self):
        self.selectedLine = None
        self.oldLine = None
        try:
            self.selectedLine = self['txt'].getSelectionIndex()
            self.oldLine = self.list[self.selectedLine]
        except:
            pass

        if self.selectedLine is None or self.oldLine is None:
            self.session.open(MessageBox, _('This line is not editable'), MessageBox.TYPE_ERROR, 6)
        else:
            self.session.openWithCallback(self.writeEditLine, editInputBox, title=self.oldLine, windowTitle=_('Edited line') + ': ', text=self.oldLine[:-1], type=Input.TEXT)
        return

    def writeEditLine(self, newline):
        if newline is not None:
            newline += '\n'
            if newline != self.oldLine:
                self.isChanged = True
            self.list[self.selectedLine] = newline
        self.selectedLine = None
        self.oldLine = None
        return

    def SaveEditedFile(self, answer):
        if answer is True:
            try:
                f = open(self.file_name, 'w')
                for x in self.list:
                    f.writelines(x)

                f.close()
            except:
                pass
            else:
                self.close()
        else:
            self.close()
        return


class cfgGsuScreen(Screen, ConfigListScreen):

    def __init__(self, session):
        Screen.__init__(self, session)
        if ENA_D:
            self.skin = cfgScreen.replace('<widget name="config" font="priveG;30"', '<widget name="config"').replace('<widget name="config" font="priveG;60"', '<widget name="config"')
        else:
            self.skin = cfgScreen
        self['green'] = Label(_('Save'))
        self['red'] = Label(_('Exit'))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': (self.save), 
           'ok': (self.save), 
           'red': (self.exitCancel), 
           'cancel': (self.exitCancel)}, -2)
        self.tmp = config.plugins.GlassSysUtil.par51.value
        self.tmp1 = config.plugins.GlassSysUtil.par52.value
        self.tmp2 = config.plugins.GlassSysUtil.par53.value
        self.tmp3 = config.plugins.GlassSysUtil.par54.value
        self.tmp4 = config.plugins.GlassSysUtil.par55.value
        self.tmp5 = config.plugins.GlassSysUtil.par56.value
        self.tmp6 = config.plugins.GlassSysUtil.par57.value
        self.tmp7 = config.plugins.GlassSysUtil.par60.value
        self.tmp8 = config.plugins.GlassSysUtil.par62.value
        CfgConfigList = []
        CfgConfigList.append(getConfigListEntry(_('Show GSU in main menu'), config.plugins.GlassSysUtil.par51))
        CfgConfigList.append(getConfigListEntry(_('Show GSU in extensions list'), config.plugins.GlassSysUtil.par52))
        CfgConfigList.append(getConfigListEntry(_('Show System Information in extensions list'), config.plugins.GlassSysUtil.par53))
        CfgConfigList.append(getConfigListEntry(_('Show Channel Information in extensions list'), config.plugins.GlassSysUtil.par54))
        if MNG_DEV:
            CfgConfigList.append(getConfigListEntry(_('Show Devices Manager in extensions list'), config.plugins.GlassSysUtil.par55))
        CfgConfigList.append(getConfigListEntry(_('Show CAM/SRV Manager in extensions list'), config.plugins.GlassSysUtil.par56))
        CfgConfigList.append(getConfigListEntry(_('Show Oscam Info in extensions list'), config.plugins.GlassSysUtil.par60))
        CfgConfigList.append(getConfigListEntry(_('Enable autocheck of mounts CIFS/NFS'), config.plugins.GlassSysUtil.par57))
        CfgConfigList.append(getConfigListEntry(_('Refresh time of autocheck (CIFS/NFS) (min)'), config.plugins.GlassSysUtil.par58))
        CfgConfigList.append(getConfigListEntry(_('OScam info - log refresh time'), config.plugins.GlassSysUtil.par61))
        CfgConfigList.append(getConfigListEntry(_('Enable GSU localization'), config.plugins.GlassSysUtil.par62))
        ConfigListScreen.__init__(self, CfgConfigList, session)
        self.onLayoutFinish.append(self.setTitlenew)
        return

    def setTitlenew(self):
        self.setTitle(_('GSU Configuration'))
        return

    def save(self):
        ena = False
        if self.tmp8 != config.plugins.GlassSysUtil.par62.value or self.tmp7 != config.plugins.GlassSysUtil.par60.value or self.tmp6 != config.plugins.GlassSysUtil.par57.value or self.tmp5 != config.plugins.GlassSysUtil.par56.value or self.tmp4 != config.plugins.GlassSysUtil.par55.value or self.tmp3 != config.plugins.GlassSysUtil.par54.value or self.tmp != config.plugins.GlassSysUtil.par51.value or self.tmp1 != config.plugins.GlassSysUtil.par52.value or self.tmp2 != config.plugins.GlassSysUtil.par53.value:
            ena = True
        for x in self['config'].list:
            x[1].save()

        configfile.save()
        self.close(ena)
        return

    def exitCancel(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close(False)
        return


class dirBrowser(Screen):

    def __init__(self, session, dd, files=False):
        Screen.__init__(self, session)
        self.skin = filebrowser
        self.files = files
        self.inhibitDirs = None
        if not self.files:
            self.inhibitDirs = [
             '/autofs', '/bin', '/boot', '/dev', '/opt', 
             '/lib', '/proc', '/sbin', '/sys', '/tmp', '/home', 
             '/run']
        self.filelist = FileList(dd, showDirectories=True, showFiles=self.files, inhibitDirs=self.inhibitDirs)
        self['filelist'] = self.filelist
        self['actions'] = ActionMap(['SetupActions', 'DirectionActions', 'ColorActions'], {'ok': (self.ok), 
           'cancel': (self.cancel), 
           'left': (self.left), 
           'right': (self.right), 
           'up': (self.up), 
           'down': (self.down), 
           'green': (self.green), 
           'red': (self.cancel)}, -1)
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('Select'))
        self.onLayoutFinish.append(self.updTitle)
        return

    def updTitle(self):
        a = self['filelist'].getCurrentDirectory()
        if a is not None:
            if a.startswith('/') and a.endswith('/'):
                aa = a.split('/')
                b = len(aa)
                if b > 5:
                    a = '.../' + aa[b - 4] + '/' + aa[b - 3] + '/' + aa[b - 2] + '/'
            self.setTitle(a)
        return

    def cancel(self):
        if not self.files:
            self.close(None)
        else:
            self.close()
        return

    def green(self):
        if self.files:
            a = self['filelist'].getCurrentDirectory()
            b = self['filelist'].getFilename()
            if a is None or b is None:
                self.session.open(MessageBox, _('Incorrect selected file'), MessageBox.TYPE_ERROR, 6)
            elif os.path.isfile(a + b) and os.path.getsize(a + b) < 50000:
                self.session.open(TxtEditor, a + b)
            else:
                self.session.open(MessageBox, _('Too big file to editing! (max 50kB)'), MessageBox.TYPE_ERROR, 6)
        else:
            ret = self['filelist'].getSelection()[0]
            if self['filelist'].getSelection()[1]:
                if ret is not None and not ret.endswith('/'):
                    ret += '/'
                self.close(ret)
        return

    def up(self):
        self['filelist'].up()
        return

    def down(self):
        self['filelist'].down()
        return

    def left(self):
        self['filelist'].pageUp()
        return

    def right(self):
        self['filelist'].pageDown()
        return

    def ok(self):
        if self['filelist'].canDescent():
            self['filelist'].descent()
            self.updTitle()
        return
