"""Canonical navigation ownership; legacy IDs remain stable."""
CENTRES = (
    ("system", "System centre", ("system-overview", "system-processes", "system-log", "0")),
    ("reception", "Reception centre", ("1",)),
    ("storage", "Memory and storage", ("9",)),
    ("network", "Network centre", ("network-overview",)),
    ("cam", "CAM / ECM centre", ("2", "3", "4", "6", "7", "8")),
    ("service", "Service centre", ("17",)),
    ("warder", "Warder Evolution centre", ("16",)),
)

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
