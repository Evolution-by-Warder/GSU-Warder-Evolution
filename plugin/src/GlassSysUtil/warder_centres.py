"""Canonical navigation ownership; legacy IDs remain stable."""
CENTRES = (
    ("system", "System centre", ("system-overview", "system-live", "system-processes", "system-log", "0")),
    ("reception", "Reception centre", ("signal-live", "1", "tuner-details", "tuner-native")),
    ("storage", "Memory and storage", ("storage-overview", "storage-categories", "9")),
    ("network", "Network centre", ("network-overview", "network-test")),
    ("cam", "CAM / ECM centre", ("2", "3", "4", "6", "7", "8")),
    ("service", "Service centre", ("service-health", "service-ipk", "forum-report", "17")),
    ("warder", "Warder Evolution centre", ("projects", "16")),
)

# Titles and descriptions belong to the same catalogue used by the remote UI.
DIAGNOSTICS = {
    "network-overview": ("Network overview", "Network link"),
    "system-overview": ("System health check", "Available memory"),
    "system-processes": ("Process Info", "CPU / RAM"),
    "system-log": ("Log view", "Dmesg Info"),
    "system-live": ("Live monitoring", "CPU · RAM · RX/TX"),
    "signal-live": ("Signal history", "SNR · AGC · BER · LOCK"),
    "tuner-details": ("Tuner interfaces", "Transponder"),
    "tuner-native": ("Tuner setup", "DiSEqC · USALS"),
    "storage-overview": ("Memory and storage", "SMART · RAM · HDD · USB"),
    "storage-categories": ("Space by category", "Picon storage"),
    "network-test": ("Connection test", "HTTPS · RTT"),
    "service-health": ("Installation check", "Crash logs"),
    "forum-report": ("Forum report", "JSON"),
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
