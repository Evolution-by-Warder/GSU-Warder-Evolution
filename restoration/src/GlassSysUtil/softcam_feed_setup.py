"""Add only the external feed configuration requested by the user.

Derived from the supplied softcam-feed-universal 4.8-r0 configuration scheme;
no legacy installer, file cleanup, binary, or CAM activation is executed here.
"""
import ast
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


def ensure_softcam_feed(directory='/etc/opkg',metadata_path='/usr/lib/enigma.info'):
    directory=Path(directory)
    configured=existing_feed(directory)
    if configured:return {'created':False,'path':str(configured)}
    arch,version,url=feed_parameters(read_metadata(metadata_path))
    target=directory/(arch+'-3rdparty-secret-feed.conf')
    # Atomic, no-clobber publication. Unrelated feeds and CAM files stay intact.
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
