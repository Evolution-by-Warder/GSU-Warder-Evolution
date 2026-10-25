"""Warder plugin release checks and verified IPK installation (Python 3)."""

import hashlib
import io
import json
import pathlib
import re
import ssl
import subprocess
import tarfile
import tempfile
from dataclasses import dataclass, field
from urllib.request import Request, urlopen

REPOSITORY = "Evolution-by-Warder/Glass-System-Utility-Warder-Evolution"
PACKAGE_ID = "enigma2-plugin-glasssysutil"
# The recovered runtime has its own feed; production dashboards never enter it.
FEED_URL = "https://raw.githubusercontent.com/" + REPOSITORY + "/original-python314/restoration/update/candidate.json"
MAX_IPK_BYTES = 128 * 1024 * 1024


class UpdateError(ValueError):
    pass


def version_key(value):
    if not isinstance(value, str):
        raise UpdateError("Invalid plugin version")
    match = re.fullmatch(r"(\d+)\.(\d+)-r(\d+)", value)
    if not match:
        raise UpdateError("Invalid restoration version")
    return tuple(int(part) for part in match.groups())


@dataclass(frozen=True)
class Release:
    version: str
    url: str
    sha256: str
    bytes: int
    notes: str = ""
    notes_i18n: dict = field(default_factory=dict)


def parse_release(payload, current_version):
    """Return a newer published release, never a work commit or downgrade."""
    current = version_key(current_version)
    try:
        document = json.loads(payload)
    except (ValueError, TypeError, UnicodeError) as exc:
        raise UpdateError("Invalid release manifest") from exc
    if not isinstance(document, dict) or type(document.get("schema")) is not int or document["schema"] != 1:
        raise UpdateError("Unsupported release manifest")
    if document.get("product") != "Glass System Utility Warder Evolution" or document.get("channel") != "original-python314":
        raise UpdateError("Wrong update product or channel")
    if "release" not in document:
        raise UpdateError("Missing release entry")
    item = document["release"]
    if item is None:
        return None
    if not isinstance(item, dict):
        raise UpdateError("Invalid release entry")
    remote = version_key(item.get("version"))
    tag = item.get("tag")
    if tag not in (item["version"], "v" + item["version"]):
        raise UpdateError("Release tag does not match version")
    expected = "https://github.com/" + REPOSITORY + "/releases/download/" + tag + "/" + PACKAGE_ID + "_" + item["version"] + "_all.ipk"
    if item.get("url") != expected:
        raise UpdateError("Unexpected plugin package URL")
    digest, size, notes = item.get("sha256"), item.get("bytes"), item.get("notes", "")
    if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise UpdateError("Missing package SHA256")
    if type(size) is not int or not 0 < size <= MAX_IPK_BYTES:
        raise UpdateError("Invalid package size")
    if not isinstance(notes, str) or len(notes) > 8192:
        raise UpdateError("Invalid release notes")
    translated_notes = item.get("notes_i18n", {})
    if (not isinstance(translated_notes, dict) or len(translated_notes) > 32 or
            any(not isinstance(k, str) or not re.fullmatch(r"[a-z]{2,3}", k) or
                not isinstance(v, str) or len(v) > 8192 for k,v in translated_notes.items())):
        raise UpdateError("Invalid translated release notes")
    if remote <= current:
        return None
    return Release(item["version"], expected, digest, size, notes, translated_notes)


def _open(url, timeout=6):
    request = Request(url, headers={"User-Agent": "Glass-System-Utility-Warder-Evolution", "Cache-Control": "no-cache"})
    # Explicit context remains verified even when another legacy plugin changes
    # urllib's process-wide default SSL context.
    return urlopen(request, timeout=timeout, context=ssl.create_default_context())


def check_release(current_version, opener=_open):
    with opener(FEED_URL) as response:
        payload = response.read(65537)
    if len(payload) > 65536:
        raise UpdateError("Release manifest is too large")
    return parse_release(payload, current_version)


def download_release(release, destination, opener=_open):
    """Write only to the private staging area; validate before invoking opkg."""
    path = pathlib.Path(destination)
    digest, count, created = hashlib.sha256(), 0, False
    try:
        with path.open("xb") as target:
            created = True
            with opener(release.url, timeout=15) as response:
                while True:
                    data = response.read(128 * 1024)
                    if not data:
                        break
                    count += len(data)
                    if count > release.bytes:
                        raise UpdateError("Package exceeds published size")
                    digest.update(data)
                    target.write(data)
        if count != release.bytes or digest.hexdigest() != release.sha256:
            raise UpdateError("Package size or SHA256 mismatch")
        return path
    except Exception:
        if created:
            path.unlink(missing_ok=True)
        raise


def _control_archive(path):
    """Read the control member of either common IPK container, without extraction."""
    with path.open("rb") as source:
        if source.read(8) == b"!<arch>\n":
            while True:
                header = source.read(60)
                if not header:
                    break
                if len(header) != 60 or header[58:] != b"`\n":
                    raise UpdateError("Invalid IPK header")
                try:
                    size = int(header[48:58])
                    name = header[:16].decode("ascii").strip().rstrip("/")
                except (ValueError, UnicodeError) as exc:
                    raise UpdateError("Invalid IPK member") from exc
                if size < 0 or source.tell() + size > path.stat().st_size:
                    raise UpdateError("Truncated IPK member")
                if name in ("control.tar.gz", "control.tar.xz", "control.tar.bz2", "control.tar"):
                    if size > 4 * 1024 * 1024:
                        raise UpdateError("IPK control archive is too large")
                    return source.read(size)
                source.seek(size + (size % 2), 1)
    try:
        with tarfile.open(path, "r:*") as outer:
            for item in outer:
                if item.name.removeprefix("./") in ("control.tar.gz", "control.tar.xz", "control.tar.bz2", "control.tar"):
                    if not item.isfile() or item.size > 4 * 1024 * 1024:
                        raise UpdateError("Invalid IPK control archive")
                    return outer.extractfile(item).read()
    except tarfile.TarError as exc:
        raise UpdateError("Invalid IPK archive") from exc
    raise UpdateError("IPK control archive is missing")


def validate_ipk(path, release):
    try:
        with tarfile.open(fileobj=io.BytesIO(_control_archive(path)), mode="r:*") as control:
            members = [m for m in control if m.name.removeprefix("./") == "control"]
            if len(members) != 1 or not members[0].isfile() or members[0].size > 65536:
                raise UpdateError("Invalid IPK control metadata")
            text = control.extractfile(members[0]).read(65537).decode("utf-8")
    except (tarfile.TarError, UnicodeError) as exc:
        raise UpdateError("Invalid IPK control metadata") from exc
    fields = {}
    for line in text.splitlines():
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            if key in fields:
                raise UpdateError("Duplicate IPK control field")
            fields[key] = value.strip()
    if fields.get("Package") != PACKAGE_ID or fields.get("Version") != release.version or fields.get("Architecture") != "all":
        raise UpdateError("IPK package identity, version or architecture mismatch")


def install_release(release, opener=_open, runner=subprocess.run):
    """Called only after the UI accepts installation; never force or reboot."""
    with tempfile.TemporaryDirectory(prefix="gsu-plugin-update-") as temporary:
        path = download_release(release, pathlib.Path(temporary) / "update.ipk", opener)
        validate_ipk(path, release)
        result = runner(["opkg", "install", str(path)], stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True, timeout=300)
        if result.returncode != 0:
            raise UpdateError("opkg failed (%s): %s" % (result.returncode, result.stdout[-2000:]))
    return release.version

