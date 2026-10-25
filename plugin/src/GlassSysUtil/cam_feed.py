"""CAM catalogue from the receiver's existing opkg sources, outside the GUI."""
import re
import shutil
import subprocess
from .softcam_feed_setup import ensure_softcam_feed, finish_refresh

_NAME=re.compile(r'^[a-z0-9][a-z0-9+._-]*$')
_CAM=re.compile(r'^(?:oscam|cccam|ncam|doscam|mgcamd|gbox|mbox|newcs|osemu)(?:$|[-_.0-9])')


def is_cam_package(name):
    if not _NAME.fullmatch(name):return False
    for prefix in ('enigma2-plugin-softcams-','enigma2-plugin-cams-'):
        if name.startswith(prefix):return len(name)>len(prefix)
    if name.startswith('softcam-'):name=name[len('softcam-'):]
    return bool(_CAM.match(name))


def parse_catalogue(text):
    packages={}
    for line in text.splitlines():
        fields=line.split(' - ',2)
        if len(fields)<2:continue
        name,version=fields[:2]
        if not is_cam_package(name):continue
        record=packages.setdefault(name,{'name':name,'versions':[],'description':fields[2].strip() if len(fields)>2 else ''})
        if version not in record['versions']:record['versions'].append(version)
    return [packages[name] for name in sorted(packages)]


def read_catalogue(refresh=True):
    opkg=shutil.which('opkg')
    if not opkg:raise OSError('opkg is unavailable')
    warning=False
    if refresh:
        setup=ensure_softcam_feed()
        try:
            update=subprocess.run([opkg,'update'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=45,check=False)
            warning=update.returncode != 0
        except (OSError,subprocess.TimeoutExpired):warning=True
        if warning and setup.get('requires_refresh'):
            raise OSError('Migrated feed must refresh successfully before offering packages.')
        if not warning:finish_refresh(setup)
    result=subprocess.run([opkg,'list'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=15,check=False)
    if result.returncode:raise OSError('Package catalogue could not be read')
    return {'packages':parse_catalogue(result.stdout.decode('utf-8','replace')),'warning':warning}
