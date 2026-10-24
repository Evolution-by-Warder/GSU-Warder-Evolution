#!/usr/bin/env python3
"""Apply explicit Python 3.14 / current OpenATV compatibility edits, not a UI rewrite."""
import ast
import pathlib
import sys


def port(source):
    replacements = []
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    def replace(node, text):
        replacements.append((node.lineno-1, node.end_lineno, text.rstrip()+'\n'))
    def function(name, text):
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
        replace(node, text)
    # Python 3 uses unicode text and its standard networking modules directly.
    for node in tree.body:
        if isinstance(node, ast.If) and isinstance(node.test, ast.Name) and node.test.id == 'ISP38':
            assign = next(n for n in node.body if isinstance(n, ast.Assign))
            ftp = ''.join(lines[assign.lineno-1:assign.end_lineno]).strip()
            replace(node, 'from urllib import request as urllibXX\nfrom urllib import request as urllibXX2\n'+ftp+"\nDG = '\u00b0'")
        if isinstance(node, ast.If) and isinstance(node.test, ast.Call) and any(isinstance(n,ast.Constant) and n.value=='/usr/bin/about1.png' for n in ast.walk(node.test)):
            replace(node, '# Architecture-specific helpers stay private; no mutation of /usr/bin on import.')
    # libc / libcrypto SONAMEs are ABI boundaries, never copies of another ABI.
    function('cpLibCr', 'def cpLibCr():\n    return False')
    function('chckPckg', '''def chckPckg():
    if shutil.which('opkg'):
        return ('o', 'mipsel', 'ipk', '-')
    if shutil.which('dpkg'):
        return ('dpkg -i /tmp/%s', 'debpkg', 'deb', '-')
    return ('o', 'mipsel', 'ipk', '-')''')
    function('generatePS', '''def generatePS():
    try:
        rows = []
        for pid in os.listdir('/proc'):
            if not pid.isdigit():
                continue
            try:
                with open('/proc/%s/cmdline' % pid, 'rb') as handle:
                    command = handle.read(8192).replace(b'\\x00', b' ').decode('utf-8', 'replace').strip()
                if not command:
                    with open('/proc/%s/comm' % pid) as handle:
                        command = handle.read().strip()
                rows.append('%s %s' % (pid, command))
            except OSError:
                continue
        with open(A_TM, 'w') as handle:
            handle.write('\\n'.join(rows)+'\\n')
        return bool(rows)
    except OSError:
        return False''')
    function('oscamRunning', '''def oscamRunning(osemu=False):
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
    return False''')
    function('getUrlData', '''def getUrlData(url, login='', passwd=''):
    manager = urllibXX2.HTTPPasswordMgrWithDefaultRealm()
    manager.add_password(None, url, login, passwd)
    opener = urllibXX2.build_opener(urllibXX2.HTTPDigestAuthHandler(manager), urllibXX2.HTTPBasicAuthHandler(manager))
    try:
        with opener.open(urllibXX2.Request(url), timeout=4) as response:
            raw = response.read(4*1024*1024+1)
        if len(raw) > 4*1024*1024:
            return None
        return raw.decode('utf-8', 'replace').split('\\n')
    except (OSError, ValueError):
        return None''')
    function('readOscamCfg', '''def readOscamCfg():
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
    return item,url,login,password''')
    for start,end,text in sorted(replacements,reverse=True):
        lines[start:end]=[text]
    source=''.join(lines)
    source=source.replace('import gettext\n','import gettext\nimport builtins\nimport platform\nimport shutil\n_ = getattr(builtins, "_", lambda value: value)\n',1)
    source=source.replace("gettext.Catalog('gsu', GSU_PATH + 'locale', gsu_language)","gettext.translation('gsu', GSU_PATH + 'locale', languages=gsu_language, fallback=True)")
    source=source.replace("FDISKG = 'fdisk'\nif os.path.isfile('/usr/bin/fdisk_g'):\n    FDISKG = '/usr/bin/fdisk_g'\nMNG_DEV = False\nif os.path.exists('/sbin/fdisk') or os.path.isfile('/usr/bin/fdisk_g'):\n    MNG_DEV = True", "FDISKG = shutil.which('fdisk') or 'fdisk'\nMNG_DEV = bool(shutil.which('fdisk'))")
    # Python 2's file alias was not translated by lib2to3.
    source=source.replace("file('/etc/cron/", "open('/etc/cron/")
    # The 2.6 LIST_APPEND temporary is not a source-level variable. The 3.12
    # implementation appends the original line, as verified in its bytecode.
    source=source.replace("[_[1] for l in open('/etc/cron/crontabs/root').readlines() if line not in l]", "[l for l in open('/etc/cron/crontabs/root').readlines() if line not in l]")
    # Keep original native helpers private, resolving their ABI at runtime.
    marker="GSU_PATH = PYTHONPATH + 'Plugins/Extensions/GlassSysUtil/'"
    helper='''
_MACHINE = platform.machine().lower()
_HELPER_ARCH = 'arm' if _MACHINE.startswith('arm') else 'aarch64' if _MACHINE in ('aarch64','arm64') else 'mips' if _MACHINE.startswith('mips') else 'sh4'
def _gsu_helper(name):
    system_path=shutil.which(name)
    if system_path:
        return system_path
    bundled=os.path.join(GSU_PATH,'bin',_HELPER_ARCH,name)
    return bundled if os.path.isfile(bundled) else name
'''
    source=source.replace(marker,marker+'\n'+helper)
    source=source.replace("fileExists('/usr/bin/bitgenerator')", "os.path.isfile(_gsu_helper('bitgenerator'))")
    source=source.replace("cmd = 'bitgenerator %s%s %s %s' % (a, str(demux), str(vpid), str(apid))", "cmd = '%s %s%s %s %s' % (_gsu_helper('bitgenerator'), a, str(demux), str(vpid), str(apid))")
    source=source.replace("system('unrar_bin x /tmp/%s.rar /tmp' % self.zipFileOS)", "system('%s x /tmp/%s.rar /tmp' % (_gsu_helper('unrar_bin'),self.zipFileOS))")
    source=source.replace("system('/usr/bin/unrar_bin x -p%s /tmp/%s /tmp' % (PWDV, self.fileName))", "system('%s x -p%s /tmp/%s /tmp' % (_gsu_helper('unrar_bin'),PWDV,self.fileName))")
    for suffix in (' -q -n /dev/sd%s > %s', ' -q -n -w /dev/sd%s > %s'):
        source=source.replace(repr('/usr/bin/hdd_temp_g'+suffix), "(_gsu_helper('hdd_temp_g') + "+repr(suffix)+")")
    source=source.replace("    cpu = open('/proc/cpuinfo', 'r').read()", "    with open('/proc/cpuinfo', 'r') as _cpu_file:\n        cpu = _cpu_file.read()")
    source=source.replace("self['blue'] = Label(_('Update'))", "self['blue'] = Label('')", 1)
    # Preserve class and method signatures; no placeholder function bodies.
    compile(source, 'plugin.py', 'exec')
    return source


if __name__=='__main__':
    pathlib.Path(sys.argv[2]).write_text(port(pathlib.Path(sys.argv[1]).read_text()))
