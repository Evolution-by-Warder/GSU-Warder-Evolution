"""Test real released IPKs in isolated opkg roots. Never invoke a host package manager."""
import hashlib
import io
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'plugin/tools'))
import build_ipk

LEGACY = 'enigma2-plugin-glasssysutil'
PACKAGE = build_ipk.PACKAGE
PINS = {
    '13.40-r93': '5f4d969f0253dfcf530e5a26037f7200033d262e36810d2c583635ded0025ee1',
    '13.41-r4': '48d8f90a6f1665f28e777b615f4dd25b1b8afc0b85128685965d44b66134acb2',
    '13.41-r5': '17de1b2624dd90b77d2c8c05ceba997e683c2d66d888212dda21e31233ef7085',
    '13.41-r6': 'a8e79609147666b27f18460b3340e099bb013664478a787746bcf56bb28052e2',
}


def ipk_parts(path):
    data = path.read_bytes()
    assert data.startswith(b'!<arch>\n')
    pos = 8
    members = {}
    while pos < len(data):
        header = data[pos:pos+60]
        assert header[58:] == b'`\n'
        size = int(header[48:58])
        name = header[:16].decode().strip(' /')
        assert name not in members and len(data) >= pos+60+size
        members[name] = data[pos+60:pos+60+size]
        pos += 60+size+size%2
    return members


def prerequisite(path, control):
    with tarfile.open(fileobj=io.BytesIO(control)) as tar:
        fields = tar.extractfile('./control').read().decode().splitlines()
    deps = next(l.split(': ',1)[1] for l in fields if l.startswith('Depends:'))
    metadata = ('Package: gsu-ci-receiver-dependencies\nVersion: 1\nArchitecture: all\nProvides: '+deps+'\nDescription: offline migration dependencies\n').encode()
    parts = [('debian-binary', b'2.0\n'), ('control.tar.gz', build_ipk.archive([('control',metadata,0o644)])), ('data.tar.gz',build_ipk.archive([]))]
    with path.open('wb') as out:
        out.write(b'!<arch>\n')
        for name, raw in parts:
            out.write(('%-16s%-12s%-6s%-6s%-8s%-10s`\n' % (name+'/',0,0,0,'100644',len(raw))).encode())
            out.write(raw + b'\n'*(len(raw)%2))


def allocated_bytes(root, listed):
    """Measure filesystem allocation of actual installed files, once per inode."""
    import stat
    seen = set()
    blocks = 0
    for line in listed.splitlines():
        if not line.startswith('/'):
            continue
        path = Path(line)
        if not path.is_relative_to(root):
            path = root / line.lstrip('/')
        if not path.exists():
            continue
        info = path.lstat()
        identity=(info.st_dev,info.st_ino)
        if stat.S_ISREG(info.st_mode) and identity not in seen:
            seen.add(identity)
            blocks += info.st_blocks
    assert seen and blocks
    return blocks*512


def main(opkg, archive, current, report=None):
    routes = {}
    paths = {}
    for version, digest in PINS.items():
        prefix = LEGACY if version.endswith('r93') else 'enigma2-plugin-extensions-gsu'
        path = archive/(prefix+'_'+version+'_all.ipk')
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        paths[version] = path
    feed = (ROOT/'plugin/update/stable.json').read_bytes()
    assert json.loads(feed)['release']['sha256'] == PINS['13.41-r6']
    tag = 'v0.41.5'
    url = 'https://github.com/Evolution-by-Warder/GSU-Warder-Evolution/releases/download/'+tag+'/'+current.name
    modern = json.dumps({'schema':1,'channel':'stable-modern','product':'Glass System Utility Warder Evolution',
                         'release':{'version':'0.41.5','tag':tag,'url':url,'sha256':hashlib.sha256(current.read_bytes()).hexdigest(),'bytes':current.stat().st_size}})
    for version in ('13.40-r93','13.41-r4','13.41-r5'):
        with tempfile.TemporaryDirectory() as directory:
            work=Path(directory)
            root=work/'root'
            (root/'var/lock').mkdir(parents=True)
            (root/'usr/lib/opkg').mkdir(parents=True)
            config=work/'opkg.conf'
            config.write_text('dest root /\narch all 10\n')
            def run(*args):
                result=subprocess.run([str(opkg),'-f',str(config),'-o',str(root),*map(str,args)],text=True,capture_output=True,timeout=40)
                assert result.returncode==0,(args,result.stdout,result.stderr)
                return result.stdout
            prereq=work/'prerequisites.ipk'
            prerequisite(prereq,ipk_parts(current)['control.tar.gz'])
            run('install',prereq)
            run('install',paths[version])
            settings=root/'etc/enigma2/settings'
            settings.parent.mkdir(parents=True,exist_ok=True)
            settings.write_bytes(b'config.plugins.GlassSysUtil.par62=True\n')
            runtime=root/build_ipk.PLUGIN
            updater=runpy.run_path(str(runtime/'plugin_update.py'))
            offered=updater['parse_release'](feed,version)
            updater['validate_ipk'](paths['13.41-r6'],offered)
            if version.endswith('r93'):
                run('remove',LEGACY)
            run('install',paths['13.41-r6'])
            assert PACKAGE+' - 13.41-r6' in run('list-installed')
            assert (runtime/'version').read_text().strip()=='13.41-r6'
            updater=runpy.run_path(str(runtime/'plugin_update.py'))
            accepted=updater['parse_release'](modern,'13.41-r6','stable-modern')
            updater['validate_ipk'](current,accepted)
            run('install',current)
            assert PACKAGE+' - 1:0.41.5' in run('list-installed')
            assert LEGACY+' - ' not in run('list-installed')
            assert (runtime/'version').read_text().strip()=='0.41.5'
            assert settings.read_bytes()==b'config.plugins.GlassSysUtil.par62=True\n'
            allocation=allocated_bytes(root,run('files',PACKAGE))
            routes[version]=allocation
            print(version,'-> 13.41-r6 -> 1:0.41.5 verified; allocated package file bytes:',allocation)
    if report:
        report.write_text(json.dumps({'allocated_installed_package_file_bytes':routes},indent=2)+'\n')


if __name__ == '__main__':
    main(Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve(),Path(sys.argv[3]).resolve(),Path(sys.argv[4]) if len(sys.argv)>4 else None)
