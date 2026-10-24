"""Read-only DVB PID rate sampler, isolated from the Enigma GUI process.

Linux DVB demux UAPI: DMX_OUT_TSDEMUX_TAP delivers filtered TS packets
from the demux fd, including packets a legacy PES reader cannot deliver.
Rates include transport headers. No decoder filters or receiver settings change.
"""
import errno
import fcntl
import os
import platform
import select
import struct
import sys
import time

DMX_SET_BUFFER_SIZE = (0x20000000 if platform.machine().startswith('mips') else 0) | 0x6f2d
DMX_SET_PES_FILTER = (0x80000000 if platform.machine().startswith('mips') else 0x40000000) | (20 << 16) | 0x6f2c


def open_reader(adapter, demux, pid):
    if not 0 <= pid < 0x1fff:
        return None
    fd = os.open('/dev/dvb/adapter%d/demux%d' % (adapter, demux), os.O_RDONLY | os.O_NONBLOCK)
    try:
        fcntl.ioctl(fd, DMX_SET_BUFFER_SIZE, 1024 * 1024)
        # pid, input=FRONTEND, output=TSDEMUX_TAP, pes_type=OTHER,
        # flags=IMMEDIATE_START; explicit padding matches the 20-byte UAPI.
        fcntl.ioctl(fd, DMX_SET_PES_FILTER, struct.pack('=H2xIIII', pid, 0, 3, 20, 4))
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_ready(fd):
    total = 0
    for _ in range(8):
        try:
            data = os.read(fd, 256 * 1024)
        except BlockingIOError:
            break
        except OSError as error:
            if error.errno == errno.EOVERFLOW:
                continue
            raise
        if not data:
            break
        total += len(data)
    return total


class Statistics:
    def __init__(self):
        self.minimum = None
        self.maximum = 0
        self.total = 0
        self.elapsed = 0.0

    def observe(self, count, elapsed):
        rate = int(count * 8 / (1000 * elapsed))
        self.minimum = rate if self.minimum is None else min(self.minimum, rate)
        self.maximum = max(self.maximum, rate)
        self.total += count
        self.elapsed += elapsed
        average = int(self.total * 8 / (1000 * self.elapsed))
        return self.minimum, self.maximum, average, rate


def main(arguments):
    if len(arguments) != 4:
        raise ValueError('expected adapter demux video_pid audio_pid')
    adapter, demux, vpid, apid = map(int, arguments)
    if not 0 <= adapter <= 255 or not 0 <= demux <= 255:
        raise ValueError('invalid DVB device')
    readers = {}
    counters = [0, 0]
    stats = [Statistics(), Statistics()]
    try:
        for index, pid in enumerate((vpid, apid)):
            try:
                fd = open_reader(adapter, demux, pid)
                if fd is not None:
                    readers[fd] = index
            except OSError as error:
                print('reader pid=%d failed errno=%s' % (pid, error.errno), file=sys.stderr, flush=True)
        if not readers:
            return 1
        last = time.monotonic()
        while readers:
            ready, _, _ = select.select(list(readers), [], [], max(0, 1 - (time.monotonic() - last)))
            for fd in ready:
                try:
                    counters[readers[fd]] += read_ready(fd)
                except OSError as error:
                    print('read failed errno=%s' % error.errno, file=sys.stderr, flush=True)
                    os.close(fd)
                    del readers[fd]
            now = time.monotonic()
            elapsed = now - last
            if elapsed >= 1:
                for index in range(2):
                    print('%d %d %d %d' % stats[index].observe(counters[index], elapsed), flush=True)
                    counters[index] = 0
                last = now
    finally:
        for fd in readers:
            os.close(fd)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv[1:]))
    except (OSError, ValueError) as error:
        print('bitrate sampler failed: %s' % error, file=sys.stderr)
        sys.exit(1)
