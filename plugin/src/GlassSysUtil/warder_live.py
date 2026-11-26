"""Read-only live sampling; history is bounded, no persistent background task."""
from time import monotonic
from .warder_tools import Probe
from .warder_telemetry import cpu_counters,cpu_percent,memory_values,network_counters,network_rates,History

def used(total,free):
    if total is None or free is None or total<=0 or not 0<=free<=total:return None
    return 100*(total-free)/total

class Sampler:
    def __init__(self,probe=None,clock=monotonic):
        self.probe=probe or Probe()
        self.clock=clock
        self.history=History(seconds=60,capacity=61,clock=clock)
        self.previous=None
    def reset(self):
        self.previous=None
    def sample(self):
        p=self.probe
        now=self.clock()
        cpu=cpu_counters(p.text('/proc/stat',16384))
        memory=memory_values(p.text('/proc/meminfo',16384))
        net=network_counters(p.text('/proc/net/dev',32768))
        net.pop('lo',None)
        values={'cpu':None,'ram':used(memory['ram_total'],memory['ram_available']),
                'swap':used(memory['swap_total'],memory['swap_free']),
                'rx':None,'tx':None}
        if self.previous is not None:
            stamp,old_cpu,old_net=self.previous
            values['cpu']=cpu_percent(old_cpu,cpu)
            rates=network_rates(old_net,net,now-stamp)
            # Interface changes/reset make aggregate rates incomplete.
            if rates and set(rates)==set(net)==set(old_net):
                values['rx']=sum(v[0] for v in rates.values())
                values['tx']=sum(v[1] for v in rates.values())
        self.previous=(now,cpu,net)
        self.history.append(values)
        return values

def statistics(samples,key):
    values=[v.get(key) for _,v in samples if v.get(key) is not None]
    return (min(values),max(values),sum(values)/len(values)) if values else (None,None,None)
