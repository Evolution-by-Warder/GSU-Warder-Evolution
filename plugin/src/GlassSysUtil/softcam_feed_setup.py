"""Add only the external feed configuration requested by the user.

Derived from the supplied softcam-feed-universal 4.8-r0 configuration scheme;
no legacy installer, file cleanup, binary, or CAM activation is executed here.
"""
import ast
import gzip
import io
import urllib.request
import os
import re
import shlex
import tempfile
from pathlib import Path

BASE_FEED='http://updates.mynonpublic.com/oea'


def feed_parameters(metadata):
    if metadata.get('distro','').lower()!='openatv':
        raise OSError('Automatic SoftCAM feed setup requires OpenATV.')
    version=metadata.get('oe','').removeprefix('OE-Alliance ').strip()
    arch=metadata.get('architecture','').strip()
    if not re.fullmatch(r'[0-9]+(?:\.[0-9]+){1,2}',version):
        raise OSError('Cannot determine the OE-Alliance version.')
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*',arch) or arch in ('all','unknown','arm'):
        raise OSError('Cannot determine the package architecture.')
    # Compatibility mapping used by the original feed provider.
    if arch=='cortexa7hf':arch='cortexa7hf-vfp'
    if tuple(map(int,version.split('.'))) < (3,4):
        raise OSError('This image is too old for the SoftCAM feed.')
    return arch,version,BASE_FEED+'/'+version+'/'+arch


def read_metadata(path):
    result={}
    for line in Path(path).read_text().splitlines():
        key,separator,value=line.partition('=')
        key=key.strip()
        if separator and key in ('distro','oe','architecture'):
            try:parsed=ast.literal_eval(value.strip())
            except (SyntaxError,ValueError):parsed=value.strip()
            if isinstance(parsed,str):result[key]=parsed
    return result


def existing_feed(directory):
    for path in sorted(Path(directory).glob('*.conf')):
        for line in path.read_text().splitlines():
            try:fields=shlex.split(line,comments=True)
            except ValueError:continue
            if len(fields)!=3 or fields[0] not in ('src','src/gz'):continue
            source,url=fields[1:]
            if 'softcam' in source.lower() or 'secret-feed' in source.lower() or url.startswith(BASE_FEED+'/'):
                return path
    return None


def verify_feed(url,arch):
    # Validate metadata, never execute a remote installer or CAM binary.
    with urllib.request.urlopen(url+'/Packages.gz',timeout=10) as response:
        compressed=response.read(2*1024*1024+1)
    if len(compressed)>2*1024*1024:raise OSError('SoftCAM feed index is too large.')
    with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as stream:
        data=stream.read(4*1024*1024+1)
    if len(data)>4*1024*1024:raise OSError('SoftCAM feed index is too large.')
    for block in data.decode('utf-8','replace').split('\n\n'):
        fields=dict(line.split(': ',1) for line in block.splitlines() if ': ' in line)
        if fields.get('Package','').startswith('enigma2-plugin-softcams-') and fields.get('Architecture')==arch:return
    raise OSError('No compatible CAM packages in the selected feed.')


def finish_refresh(result):
    marker=result.get('marker')
    if marker:Path(marker).unlink(missing_ok=True)


def ensure_softcam_feed(directory='/etc/opkg',metadata_path='/usr/lib/enigma.info'):
    directory=Path(directory)
    configured=existing_feed(directory)
    if configured:
        original=configured.read_text()
        lines=original.splitlines(keepends=True)
        known=[]
        for index,line in enumerate(lines):
            try:fields=shlex.split(line,comments=True)
            except ValueError:continue
            if len(fields)==3 and fields[0] in ('src','src/gz') and re.fullmatch(re.escape(BASE_FEED)+r'/[0-9.]+/[a-z0-9_-]+/?',fields[2]):
                known.append((index,fields))
        # Custom providers are user configuration; keep them unchanged.
        if not known:return {'created':False,'path':str(configured)}
        if len(known)!=1:raise OSError('Multiple SoftCAM feed entries need review.')
        arch,version,url=feed_parameters(read_metadata(metadata_path))
        index,fields=known[0]
        marker=Path(str(configured)+'.warder-refresh-pending')
        if fields[2].rstrip('/')==url:
            return {'created':False,'updated':False,'path':str(configured),'requires_refresh':marker.exists(),'marker':str(marker) if marker.exists() else None}
        verify_feed(url,arch)
        # Keep the original file once and mark old cached lists unusable until
        # a successful opkg update. Both sidecars are ignored by opkg (*.conf).
        backup=Path(str(configured)+'.warder-backup')
        try:
            with backup.open('x') as handle:
                os.fchmod(handle.fileno(),configured.stat().st_mode & 0o777)
                handle.write(original)
        except FileExistsError:pass
        marker.write_text(url+'\n');marker.chmod(0o600)
        lines[index]=fields[0]+' '+fields[1]+' '+url+'\n'
        fd,temporary=tempfile.mkstemp(prefix='.warder-softcam-',suffix='.tmp',dir=directory)
        try:
            with os.fdopen(fd,'w') as handle:
                handle.write(''.join(lines));handle.flush();os.fsync(handle.fileno())
            os.chmod(temporary,configured.stat().st_mode & 0o777)
            if configured.read_text()!=original:raise OSError('Feed configuration changed during setup.')
            os.replace(temporary,configured)
        finally:
            if os.path.exists(temporary):os.unlink(temporary)
        return {'created':False,'updated':True,'path':str(configured),'requires_refresh':True,'marker':str(marker)}
    arch,version,url=feed_parameters(read_metadata(metadata_path))
    verify_feed(url,arch)
    target=directory/(arch+'-3rdparty-secret-feed.conf')
    directory.mkdir(parents=True,exist_ok=True)
    fd,temporary=tempfile.mkstemp(prefix='.warder-softcam-',suffix='.tmp',dir=directory)
    try:
        with os.fdopen(fd,'w') as handle:
            handle.write('src/gz '+arch+'-3rdparty-secret-feed '+url+'\n')
            handle.flush();os.fsync(handle.fileno())
        os.chmod(temporary,0o644)
        try:os.link(temporary,target)
        except FileExistsError:
            return {'created':False,'path':str(target)}
    finally:
        os.unlink(temporary)
    return {'created':True,'path':str(target)}
