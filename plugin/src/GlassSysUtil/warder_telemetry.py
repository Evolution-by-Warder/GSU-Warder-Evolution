"""Bounded, read-only telemetry primitives; no GUI or worker ownership."""
from collections import deque
from math import isfinite
from time import monotonic

def cpu_line(fields):
    try:
        values=[int(v) for v in fields[1:9]]
        if len(values)<4 or min(values)<0:return None
        return sum(values),values[3]+(values[4] if len(values)>4 else 0)
    except ValueError:return None


def cpu_counters(text):
    for line in text.splitlines():
        fields=line.split()
        if fields and fields[0]=='cpu':return cpu_line(fields)
    return None


def core_counters(text):
    result={}
    for line in text.splitlines():
        fields=line.split()
        if fields and fields[0].startswith('cpu') and fields[0][3:].isdigit():
            number=int(fields[0][3:])
            if number<256:result[number]=cpu_line(fields)
    return result

def cpu_percent(previous, current):
    if previous is None or current is None:
        return None
    total, idle = (current[i] - previous[i] for i in range(2))
    if total <= 0 or not 0 <= idle <= total:
        return None
    return 100.0 * (total-idle)/total

def memory_values(text):
    values = {}
    for line in text.splitlines():
        key, sep, value = line.partition(":")
        parts = value.split()
        if sep and len(parts) == 2 and parts[1] == "kB":
            try:
                number = int(parts[0])
                if number >= 0:
                    values[key] = number * 1024
            except ValueError:
                pass
    total = values.get("MemTotal")
    available = values.get("MemAvailable")
    basis = "MemAvailable"
    if available is None:
        available = values.get("MemFree")
        basis = "MemFree"
    swap_total, swap_free = values.get("SwapTotal"), values.get("SwapFree")
    return {"ram_total": total, "ram_available": available if total is not None and available is not None and available <= total else None,
            "ram_basis": basis if available is not None else None,
            "swap_total": swap_total, "swap_free": swap_free if swap_total is not None and swap_free is not None and swap_free <= swap_total else None}

def network_counters(text):
    result = {}
    for line in text.splitlines():
        name, sep, body = line.partition(":")
        if not sep:
            continue
        name = name.strip()
        try:
            fields = [int(v) for v in body.split()]
            if name and len(fields) >= 16 and min(fields) >= 0:
                result[name] = (fields[0], fields[8])
        except ValueError:
            continue
    return result

def network_rates(previous, current, elapsed):
    if not isfinite(elapsed) or elapsed <= 0:
        return {}
    result = {}
    for name in previous.keys() & current.keys():
        delta = tuple(b-a for a,b in zip(previous[name],current[name]))
        if min(delta) >= 0:
            result[name] = tuple(v/elapsed for v in delta)
    return result

class History:
    """Time and count bounds, no timers; caller owns sampling lifecycle."""
    def __init__(self, seconds=60, capacity=61, clock=monotonic):
        if not 0 < seconds <= 3600 or not 1 <= capacity <= 3601:
            raise ValueError("history bounds")
        self.seconds, self.clock = seconds, clock
        self.samples = deque(maxlen=capacity)
    def append(self, values):
        now = self.clock()
        if self.samples and now < self.samples[-1][0]:
            self.samples.clear()
        self.samples.append((now, dict(values)))
        self.prune(now)
    def prune(self, now=None):
        now = self.clock() if now is None else now
        while self.samples and now-self.samples[0][0] > self.seconds:
            self.samples.popleft()
    def snapshot(self):
        self.prune()
        return tuple((t, dict(v)) for t,v in self.samples)
