import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = REPO_ROOT / "scripts" / "install_resolve_user.ps1"
ENTRY_SOURCE = REPO_ROOT / "scripts" / "Fusion" / "ResolveNodeKit_Arrange.py"


def run_installer(fusion_root, extra=()):
    cmd = [
        "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", str(INSTALLER), "-FusionRoot", str(fusion_root),
        "-RepoRoot", str(REPO_ROOT), *extra,
    ]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120)


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_package_files():
    root = REPO_ROOT / "src" / "resolve_node_kit"
    found = []
    for path in sorted(root.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        found.append(path)
    return found


class InstallerSandboxTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="rnk-install-"))
        self.fusion = self.work / "Fusion"
        (self.fusion / "Scripts" / "Comp").mkdir(parents=True)
        self.sibling = self.fusion / "Scripts" / "Comp" / "OtherTool.py"
        self.sibling.write_text("# unrelated user script", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.work, ignore_errors=True)

    def test_install_and_verify(self):
        result = run_installer(self.fusion)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("INSTALL VERIFIED", result.stdout)
        entry = self.fusion / "Scripts" / "Comp" / "ResolveNodeKit_Arrange.py"
        self.assertTrue(entry.is_file())
        self.assertEqual(sha256_of(entry), sha256_of(ENTRY_SOURCE))
        manifest_path = self.fusion / "ResolveNodeKit" / "install_manifest.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["tool"], "ResolveNodeKit Semantic Arrange")
        for item in manifest["files"]:
            target = self.fusion / "ResolveNodeKit" / Path(item["path"])
            self.assertTrue(target.is_file(), item["path"])
            self.assertEqual(sha256_of(target), item["sha256"])
        self.assertEqual(self.sibling.read_text(encoding="utf-8"), "# unrelated user script")

    def test_reinstall_is_idempotent_without_backup(self):
        self.assertEqual(run_installer(self.fusion).returncode, 0)
        self.assertEqual(run_installer(self.fusion).returncode, 0)
        backup_root = self.fusion / "ResolveNodeKit" / "backup"
        self.assertFalse(backup_root.exists())

    def test_repair_backs_up_and_restores(self):
        self.assertEqual(run_installer(self.fusion).returncode, 0)
        entry = self.fusion / "Scripts" / "Comp" / "ResolveNodeKit_Arrange.py"
        entry.write_text(entry.read_text(encoding="utf-8") + chr(10) + "# drifted line", encoding="utf-8")
        result = run_installer(self.fusion)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(sha256_of(entry), sha256_of(ENTRY_SOURCE))
        backups = list((self.fusion / "ResolveNodeKit" / "backup").rglob("ResolveNodeKit_Arrange.py"))
        self.assertEqual(len(backups), 1)
        self.assertIn("# drifted line", backups[0].read_text(encoding="utf-8"))

    def test_uninstall_removes_only_owned(self):
        self.assertEqual(run_installer(self.fusion).returncode, 0)
        result = run_installer(self.fusion, extra=("-Uninstall",))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UNINSTALL DONE", result.stdout)
        self.assertFalse((self.fusion / "Scripts" / "Comp" / "ResolveNodeKit_Arrange.py").exists())
        self.assertFalse((self.fusion / "ResolveNodeKit").exists())
        self.assertTrue(self.sibling.is_file())
        again = run_installer(self.fusion, extra=("-Uninstall",))
        self.assertEqual(again.returncode, 0)

    def test_foreign_entry_refuses(self):
        foreign = self.fusion / "Scripts" / "Comp" / "ResolveNodeKit_Arrange.py"
        foreign.write_text("# someone else script", encoding="utf-8")
        result = run_installer(self.fusion)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(foreign.read_text(encoding="utf-8"), "# someone else script")


STUB_INIT = "__all__ = []\n"
STUB_FUSION = (
    "print(\"STUB PACKAGE LOADED\")\n"
    "class FusionHostError(RuntimeError):\n"
    "    pass\n"
    "class ArrangeDialogState:\n"
    "    def __init__(self, include_unselected=False, ungroup=False):\n"
    "        self.include_unselected = include_unselected\n"
    "        self.ungroup = ungroup\n"
    "    @classmethod\n"
    "    def from_askuser(cls, result):\n"
    "        return None\n"
    "def arrange_comp(*args, **kwargs):\n"
    "    raise AssertionError(\"arrange must not run without a comp\")\n"
    "def ask_arrange_options(*args, **kwargs):\n"
    "    raise AssertionError(\"dialog must not run without a comp\")\n"
)


def write_stub_package(src_root):
    package = Path(src_root) / "resolve_node_kit"
    fusion = package / "fusion"
    fusion.mkdir(parents=True, exist_ok=True)
    (package / "__init__.py").write_text(STUB_INIT, encoding="utf-8")
    (fusion / "__init__.py").write_text(STUB_FUSION, encoding="utf-8")


class ScriptBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="rnk-bootstrap-"))

    def tearDown(self):
        shutil.rmtree(self.work, ignore_errors=True)

    def run_script(self, script_path, env_extra=None):
        env = dict(os.environ)
        env.pop("RNK_SUPPORT_ROOT", None)
        env.update(env_extra or {})
        return subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True, text=True, timeout=60, cwd=str(self.work), env=env,
        )

    def test_env_override_uses_installed_tree(self):
        fake = self.work / "support"
        write_stub_package(fake / "ResolveNodeKit" / "src")
        result = self.run_script(ENTRY_SOURCE, {"RNK_SUPPORT_ROOT": str(fake)})
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("STUB PACKAGE LOADED", result.stdout)
        self.assertIn("no active Fusion composition", result.stdout)

    def test_upward_search_prefers_installed_tree(self):
        fake_fusion = self.work / "Fusion"
        write_stub_package(fake_fusion / "ResolveNodeKit" / "src")
        comp_dir = fake_fusion / "Scripts" / "Comp"
        comp_dir.mkdir(parents=True)
        installed_copy = comp_dir / "ResolveNodeKit_Arrange.py"
        shutil.copyfile(ENTRY_SOURCE, installed_copy)
        result = self.run_script(installed_copy)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("STUB PACKAGE LOADED", result.stdout)
        self.assertIn("no active Fusion composition", result.stdout)
