"""Explain measured resource pressure without treating missing data as healthy."""
def resource_check(name, total, available, warning=15, critical=5):
    if type(total) not in (int,float) or type(available) not in (int,float) or not 0 <= available <= total or total <= 0:
        return dict(name=name,state="unknown",available_percent=None)
    percent=100.0*available/total
    state="critical" if percent<critical else "warning" if percent<warning else "ok"
    return dict(name=name,state=state,available_percent=percent,warning=warning,critical=critical)

def health_summary(checks):
    checks=tuple(checks)
    known=[c for c in checks if c["state"] in ("ok","warning","critical")]
    counts={state:sum(c["state"]==state for c in checks) for state in ("ok","warning","critical","unknown")}
    # Resource thresholds are indicative, not predictions of hardware failure.
    points={"ok":100,"warning":50,"critical":0}
    score=round(sum(points[c["state"]] for c in known)/len(known)) if known else None
    status=("critical" if counts["critical"] else "warning" if counts["warning"] else
            "unknown" if counts["unknown"] or not known else "ok")
    return dict(score=score,coverage=(len(known),len(checks)),state=status,counts=counts)
