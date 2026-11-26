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
