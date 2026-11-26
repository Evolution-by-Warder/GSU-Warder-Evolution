"""Measure the actual read-only sampler on the machine running this command."""
import json
from pathlib import Path
import platform
import resource
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'plugin/src'))
from GlassSysUtil.warder_live import Sampler


def main():
    sampler = Sampler()
    elapsed = []
    cpu_start = time.process_time()
    rss_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    for _ in range(30):
        start = time.monotonic()
        sampler.sample()
        elapsed.append(1000*(time.monotonic()-start))
        time.sleep(0.02)
    result = {'platform':platform.machine(), 'python':platform.python_version(),'samples':len(elapsed),
              'mean_ms':round(sum(elapsed)/len(elapsed),3),'max_ms':round(max(elapsed),3),
              'cpu_ms':round(1000*(time.process_time()-cpu_start),3),
              'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'initial_peak_rss_kib':rss_start}
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
