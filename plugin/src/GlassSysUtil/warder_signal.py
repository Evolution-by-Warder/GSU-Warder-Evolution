"""Read the active decoder's frontend without allocating, tuning or stopping it."""
import csv
import os
import tempfile
from .warder_telemetry import History


def number(data, key, low, high, factor=1):
    value = data.get(key)
    if type(value) is int and low <= value <= high:
        return value / factor
    return None


def measurements(status):
    status = status if isinstance(status, dict) else {}
    lock = status.get('tuner_locked')
    return {
        'snr': number(status, 'tuner_signal_quality', 0, 65535, 655.35),
        'agc': number(status, 'tuner_signal_power', 0, 65535, 655.35),
        'db': number(status, 'tuner_signal_quality_db', -5000, 10000, 100),
        'ber': number(status, 'tuner_bit_error_rate', 0, 0xffffffff),
        'lock': int(lock) if type(lock) in (int, bool) and lock in (0, 1) else None,
    }


class SignalMonitor:
    def __init__(self, nav):
        self.nav = nav
        self.history = History()
        self.identity = None

    def sample(self):
        ref = self.nav.getCurrentlyPlayingServiceReference()
        identity = ref.toString() if ref is not None else None
        if identity != self.identity:
            self.history.samples.clear()
            self.identity = identity
        service = self.nav.getCurrentService()
        frontend = service.frontendInfo() if service else None
        status = frontend.getFrontendStatus() if frontend else None
        values = measurements(status)
        self.history.append(values)
        return values


def lock_losses(samples):
    previous = None
    losses = 0
    for _, values in samples:
        lock = values.get('lock')
        if previous == 1 and lock == 0:
            losses += 1
        previous = lock
    return losses


def export(samples, directory='/tmp'):
    # Indices and measurements only. Service references may contain IPTV credentials.
    keys = ('snr', 'agc', 'db', 'ber', 'lock')
    with tempfile.NamedTemporaryFile(mode='w', encoding='ascii', newline='', dir=directory,
                                     prefix='gsu-signal-', suffix='.csv', delete=False) as out:
        try:
            writer = csv.writer(out)
            writer.writerow(('elapsed_s', 'SNR_percent', 'AGC_percent', 'dB', 'BER', 'LOCK'))
            for stamp, values in samples:
                writer.writerow([round(stamp-samples[0][0], 3)] + [values.get(key) for key in keys])
            return out.name
        except BaseException:
            os.unlink(out.name)
            raise


def satellite_identity(screen):
    """Recognized native 15-field satellite tuple, never a service URL."""
    raw=getattr(screen,'transponder',None)
    if not isinstance(raw,(list,tuple)) or len(raw)!=15:return None
    import re
    def integer(v):
        if type(v) is int:return v
        if isinstance(v,str) and re.fullmatch(r'-?\d{1,9}',v):return int(v)
        raise ValueError('unknown parameter')
    try:
        tp=tuple(integer(v) for v in raw)
        selector=getattr(screen,'satfinder_scan_nims',None)
        if selector is None:selector=getattr(screen,'scan_nims',None)
        slot=integer(selector.value)
    except (ValueError,TypeError,AttributeError):return None
    if not (0<=slot<256 and 3000<=tp[0]<=30000 and 1<=tp[1]<=100000
            and 0<=tp[2]<=3 and 0<=tp[5]<3600):return None
    return slot,tp


def measurement_record(identity,samples,stamp):
    """Save only observed measurements; unlocked values do not enter averages."""
    from .warder_live import statistics
    if identity is None:return None
    locked=[(t,v) for t,v in samples if v.get('lock')==1 and v.get('snr') is not None]
    if len(locked)<3:return None
    return {'identity':identity,'stamp':stamp,'duration':round(samples[-1][0]-samples[0][0],1),
            'count':len(samples),'locked':len(locked),'losses':lock_losses(samples),
            'stats':{key:statistics(locked,key) for key in ('snr','agc','db','ber')}}


def comparison_text(records,tr):
    def shown(v):return '—' if v is None else '%.1f'%v
    lines=[]
    for index,record in enumerate(records,1):
        slot,tp=record['identity']
        pos=tp[5];orbital=(3600-pos)/10 if pos>1800 else pos/10
        lines.extend(('%d.  %.1f° %s   ·   %d %s   ·   %d kS/s   ·   Tuner %d'%(
            index,orbital,'W' if pos>1800 else 'E',tp[0],('H','V','L','R')[tp[2]],tp[1],slot),
            record['stamp']+'   ·   %.1f s'%record['duration'],
            'LOCK + SNR   %d/%d   ·   %s %d'%(record['locked'],record['count'],tr('Lock losses'),record['losses']),
            '%s / %s / %s'%(tr('Minimum'),tr('Maximum'),tr('Average'))))
        for key,label,unit in (('snr','SNR','%'),('agc','AGC','%'),('db','SNR','dB'),('ber','BER','')):
            lines.append(label+' '+unit+'   '+ ' / '.join(shown(v) for v in record['stats'][key]))
        # Include native parameters so distinct MIS/PLS/FEC settings are visible.
        lines.extend(('FEC / SYS / MOD   %d / %d / %d'%(tp[3],tp[6],tp[7]),
                      'MIS / PLS / T2-MI   %d / %d:%d / %d:%d'%(tp[10],tp[11],tp[12],tp[13],tp[14]),''))
    return '\n'.join(lines).strip() or tr('Unavailable')
