"""Canonical navigation ownership; legacy IDs remain stable."""
CENTRES = (
    ("system", "System centre", ("system-overview", "system-live", "system-cpu", "system-processes", "system-log", "0")),
    ("reception", "Reception centre", ("signal-quick", "signal-live", "1", "tuner-details", "transponder-services", "tuner-native")),
    ("storage", "Memory and storage", ("storage-overview", "storage-memory", "storage-categories", "storage-activity", "9")),
    ("network", "Network centre", ("network-overview", "network-interfaces", "network-statistics", "network-test", "network-mounts", "network-services")),
    ("cam", "CAM / ECM centre", ("2", "3", "4", "6", "7", "8")),
    ("service", "Service centre", ("service-smart", "service-health", "service-crashes", "service-plugins", "service-ipk", "forum-report", "17")),
    ("warder", "Warder Evolution centre", ("projects", "16")),
)

# Titles and descriptions belong to the same catalogue used by the remote UI.
DIAGNOSTICS = {
    "network-overview": ("Network overview", "Network link"),
    "system-overview": ("System health check", "Available memory"),
    "system-processes": ("Process Info", "CPU / RAM"),
    "system-cpu": ("CPU details", "CPU · MHz"),
    "system-log": ("Log view", "Dmesg Info"),
    "system-live": ("Live monitoring", "CPU · RAM · RX/TX"),
    "signal-live": ("Signal history", "SNR · AGC · BER · LOCK"),
    "tuner-details": ("Tuner interfaces", "Transponder"),
    "tuner-native": ("Tuner setup", "DiSEqC · USALS"),
    "storage-overview": ("Memory and storage", "SMART · RAM · HDD · USB"),
    "storage-categories": ("Space by category", "Picon storage"),
    "storage-memory": ("Memory details", "RAM · Swap"),
    "storage-activity": ("Disk activity", "R/W · IOPS"),
    "network-test": ("Connection test", "HTTPS · RTT"),
    "network-interfaces": ("Network interfaces", "LAN · Wi-Fi"),
    "network-statistics": ("Network statistics", "RX/TX"),
    "network-mounts": ("Network mounts", "NFS · CIFS"),
    "network-services": ("Network services", "TCP · UDP"),
    "service-health": ("Installation check", "Crash logs"),
    "service-smart": ("Smart Diagnostics", "System health check"),
    "service-crashes": ("Crash logs", "Logs"),
    "service-plugins": ("Installed plugin packages", "Package manager"),
    "forum-report": ("Forum report", "JSON"),
    "signal-quick": ("Quick signal", "SNR · dB · LOCK"),
    "transponder-services": ("Transponder services", "TV / Radio → /tmp"),
    "service-ipk": ("IPK · /tmp", "Package manager"),
    "projects": ("Stable releases", "Warder Evolution"),
}


def legacy_routes(entries):
    """Return grouped original menu entries, preserving labels and action IDs.
    Unknown future entries remain reachable in a separate fallback group.
    """
    items = tuple(entries)
    ids = [entry[0] for entry in items]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate menu ID")
    by_id = dict(zip(ids, items))
    used = set()
    groups = []
    for key, label, members in CENTRES:
        group = tuple(by_id[i] for i in members if i in by_id)
        used.update(item[0] for item in group)
        groups.append((key, label, group))
    rest = tuple(item for item in items if item[0] not in used)
    if rest:
        groups.append(("other", "Other", rest))
    return tuple(groups)


# User-facing descriptions are independent of route labels and stable IDs.
# Technical acronyms are left intact; all explanatory sentences are localized.
TOPICS = {
    'network-overview': ('Network link','IP','Default gateway','DNS configuration','Network mounts'),
    'system-log': ('Logs','System Information','Dmesg Info'),
    'system-cpu': ('CPU','MHz','Uptime'),
    'system-live': ('CPU','RAM','Swap','Temperature','RX/TX'),
    'signal-live': ('SNR','AGC','BER','dB','LOCK','Minimum','Maximum','Average','Lock losses'),
    'tuner-details': ('Tuner interfaces','Transponder','Recordings','Channel Information'),
    'storage-overview': ('RAM','Swap','HDD / SSD / USB','Total:','Free:','SMART'),
    'storage-categories': ('Picons','Skins','Plugins','EPG','Cache','Logs'),
    'storage-memory': ('RAM','Swap','Cache','swappiness'),
    'storage-activity': ('HDD / SSD / USB','R/W','IOPS'),
    'network-test': ('Default gateway','Packet loss','RTT','HTTPS','warder-evolution.eu'),
    'network-interfaces': ('Network link','IP','MAC','LAN','Wi-Fi'),
    'network-statistics': ('RX/TX','Packets','Errors','Dropped packets'),
    'network-mounts': ('NFS','CIFS','read-only'),
    'network-services': ('FTP','Telnet','VPN','Samba','NFS','Local ports'),
    'service-health': ('Check installed files','Package dependencies','Crash logs'),
    'service-smart': ('Resource score','Network link','Temperature','Installation check'),
    'service-crashes': ('Crash logs','Check plugin dependencies','Check image compatibility'),
    'service-plugins': ('Package manager','Installed version','Architecture'),
    'forum-report': ('Preview anonymous report','System Information','Crash logs'),
    'signal-quick': ('Signal','SNR','dB','LOCK','Audio:'),
    'transponder-services': ('Transponder','TV / Radio','/tmp'),
    'service-ipk': ('IPK','Package manager','Version','Architecture','Package dependencies','Scripts'),
    'projects': ('Installed version','Stable version','Package dependencies','Open plugin'),
}

def description(ident,tr,default=''):
    if ident=='system-overview':
        return tr('This view provides an overview of: %s.') % tr('CPU load, RAM and swap usage, free flash and disk space, temperature and resource status')
    if ident=='system-processes':
        return tr('Running processes with PID, state, CPU and memory use. Sort by CPU or RAM.')
    if ident=='tuner-native' or ident.startswith('native:'):
        return tr('A channel backup is created before active tuning; live TV may stop.')
    if ident in TOPICS:
        return tr('Use this tool to inspect: %s.') % ', '.join(tr(key).rstrip(':') for key in TOPICS[ident])
    return default
