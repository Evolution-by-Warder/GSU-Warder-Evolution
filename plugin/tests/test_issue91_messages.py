"""Issue #91: pure source/hook checks; no IPK build and no receiver changes."""
import ast
import os
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/build_ipk.py"
PREINST = ROOT / "control/preinst"
BAR = "*" * 66


def hooks():
    source = BUILDER.read_text(encoding="utf-8")
    tree = ast.parse(source)
    found = {"preinst": PREINST.read_text(encoding="utf-8")}
    for item in ast.walk(tree):
        if not isinstance(item, ast.Assign):
            continue
        for target in item.targets:
            if not isinstance(target, ast.Name) or target.id not in ("postinst", "prerm", "postrm"):
                continue
            value = item.value
            if isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute) and value.func.attr == "encode":
                value = value.func.value
            if isinstance(value, ast.Constant) and isinstance(value.value, (str, bytes)):
                found[target.id] = value.value.decode() if isinstance(value.value, bytes) else value.value
    return found, source


def run(script, event, stage=False):
    env = os.environ.copy()
    if stage:
        env["D"] = "/tmp/warder-issue91-staging"
    else:
        env.pop("D", None)
    return subprocess.run(["sh", "-c", script, "warder-hook", event],
                          env=env, text=True, capture_output=True, timeout=8, check=True).stdout


class WarderGSUMessages(unittest.TestCase):
    def test_hooks_parse_and_use_uniform_banner(self):
        found, builder = hooks()
        self.assertEqual(set(found), {"preinst", "postinst", "prerm", "postrm"})
        compile(builder, str(BUILDER), "exec")
        for name, script in found.items():
            with self.subTest(name=name):
                self.assertTrue(script.startswith("#!/bin/sh\n"))
                self.assertIn('echo "' + BAR + '"', script)
                subprocess.run(["sh", "-n"], input=script, text=True, check=True)
        self.assertIn("('postrm',postrm,0o755)", builder)

    def test_upgrade_is_never_called_uninstall(self):
        found, _ = hooks()
        self.assertEqual(run(found["postrm"], "upgrade"), "")
        self.assertEqual(run(found["postrm"], "failed-upgrade"), "")
        self.assertEqual(run(found["prerm"], "upgrade"), "")
        self.assertEqual(run(found["preinst"], "install", stage=True), "")
        self.assertEqual(run(found["postrm"], "remove", stage=True), "")

    def test_completion_follows_original_integrity_check(self):
        found, _ = hooks()
        script = found["postinst"]
        self.assertLess(script.index('install_health.py" --files-only'),
                        script.index("Install/upgrade/reinstall finished"))
        self.assertIn("Existing GSU settings", script)
        self.assertIn("Please restart GUI to activate changes.", script)
        self.assertIn("package-rename-in-progress", found["prerm"])
        self.assertIn("package-rename-in-progress", found["postrm"])
        self.assertIn("--restore-all", found["prerm"])
        self.assertIn("verified 13.20", PREINST.read_text(encoding="utf-8"))

    def test_real_post_remove_message_is_non_destructive(self):
        found, _ = hooks()
        if not Path("/var/lib/warder-gsu/package-rename-in-progress").exists():
            msg = run(found["postrm"], "remove")
            self.assertIn("Removal finished: GSU Warder Evolution", msg)
            self.assertIn("settings and custom configuration", msg)
            self.assertTrue(msg.startswith(BAR + "\n"))


if __name__ == "__main__":
    unittest.main()
