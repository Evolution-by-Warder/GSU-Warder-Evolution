"""Bounded text-only transport for the original CCcam WebInfo screens."""
from io import StringIO
from urllib.parse import unquote, urlsplit, urlunsplit
from urllib.request import HTTPBasicAuthHandler, HTTPDigestAuthHandler, HTTPPasswordMgrWithDefaultRealm, Request, build_opener

LIMIT = 4 * 1024 * 1024


def open_text(url):
    parts = urlsplit(url)
    if parts.scheme not in ('http', 'https') or not parts.hostname:
        raise OSError('Invalid CCcam WebInfo URL')
    clean = urlunsplit((parts.scheme, parts.netloc.rsplit('@', 1)[-1], parts.path, parts.query, ''))
    manager = HTTPPasswordMgrWithDefaultRealm()
    if parts.username is not None:
        manager.add_password(None, clean, unquote(parts.username), unquote(parts.password or ''))
    opener = build_opener(HTTPDigestAuthHandler(manager), HTTPBasicAuthHandler(manager))
    with opener.open(Request(clean), timeout=4) as response:
        raw = response.read(LIMIT + 1)
        charset = response.headers.get_content_charset() or 'utf-8'
    if len(raw) > LIMIT:
        raise OSError('CCcam WebInfo response too large')
    try:
        text = raw.decode(charset, 'replace')
    except LookupError:
        text = raw.decode('utf-8', 'replace')
    return StringIO(text)
