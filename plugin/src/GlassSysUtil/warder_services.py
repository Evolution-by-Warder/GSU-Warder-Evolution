"""Preview the native database for the current transponder and export a new bouquet."""
import os
import re
import tempfile

DVB = re.compile(r'^1:0:([0-9a-fA-F]+):(?:[0-9a-fA-F]+:){7}$')


def services(nav, center, ref_type):
    current = nav.getCurrentlyPlayingServiceReference()
    if current is None or not DVB.fullmatch(current.toString()):
        return []
    namespace, tsid, onid = (current.getUnsignedData(i) for i in (4, 2, 3))
    if not any((namespace, tsid, onid)):
        return []
    query = '1:7:1:0:0:0:0:0:0:0:(channelID == %08x%04x%04x) ORDER BY name' % (namespace, tsid, onid)
    listing = center.list(ref_type(query))
    if listing is None:
        return []
    found, seen = [], set()
    for _ in range(512):
        ref = listing.getNext()
        if not ref.valid():
            break
        ident = ref.toString()
        match = DVB.fullmatch(ident)
        if not match or ident in seen:
            continue
        if tuple(ref.getUnsignedData(i) for i in (4,2,3)) != (namespace, tsid, onid):
            continue
        seen.add(ident)
        info = center.info(ref)
        name = info.getName(ref) if info else ''
        name = ' '.join(str(name or '').split())[:128]
        # Audio and television lists are separate on Enigma2.
        found.append(('radio' if int(match[1],16) in (2,10) else 'tv',ident,name))
    return found


def export(rows, kind, directory='/tmp'):
    selected = [row for row in rows if row[0]==kind and DVB.fullmatch(row[1])]
    if not selected or kind not in ('tv','radio'):
        return None
    # Standalone user-named files never replace an existing bouquet or lamedb.
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=directory,delete=False,
                                     prefix='userbouquet.gsu-',suffix='.'+kind) as out:
        try:
            out.write('#NAME GSU · Transponder\n')
            for _,ident,name in selected:
                out.write('#SERVICE '+ident+'\n')
                if name:
                    out.write('#DESCRIPTION '+' '.join(name.split())+'\n')
            return out.name
        except BaseException:
            os.unlink(out.name)
            raise


def display(rows, tr):
    """Group database services by type; the export keeps original references."""
    sections=[]
    for kind, label in (('tv','TV'),('radio','Radio')):
        group=[name or ident for media,ident,name in rows if media==kind]
        sections.append('%s  ·  %d'%(tr(label),len(group)))
        sections.extend('    %s'%name for name in group)
        sections.append('')
    return '\n'.join(sections).rstrip() if rows else tr('Unavailable')
