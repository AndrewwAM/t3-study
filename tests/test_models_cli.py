"""Exercise the portable CLI from nested course folders, with no real providers."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ModelsCLITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="t3-study-cli-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "study workspace ü"
        (self.root / "skills/t3-study").mkdir(parents=True)
        (self.root / "skills/t3-study/SKILL.md").write_text("Test skill.", encoding="utf-8")
        (self.root / "scripts").mkdir()
        self.script = self.root / "scripts/study_models.py"
        shutil.copy2(ROOT / "scripts/study_models.py", self.script)
        self.course = self.root / "ramos/course with spaces"
        self.course.mkdir(parents=True)
        self.catalog = Path(self.temp.name) / "catalog.json"
        self.catalog.write_text(json.dumps({"providers": []}), encoding="utf-8")

    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(self.script), *args],
                              cwd=self.course, capture_output=True, text=True,
                              encoding="utf-8", timeout=10)

    def test_missing_profile_does_not_create_notes_or_config_in_course(self):
        result = self.run_cli("check", "--environment", "new-machine", "--catalog", str(self.catalog))
        self.assertEqual(result.returncode, 2, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "setup_required")
        self.assertEqual(data["config"], str(self.root / "study-models.json"))
        self.assertEqual(list(self.course.iterdir()), [])
        self.assertFalse((self.root / "study-models.json").exists())
        self.assertFalse((self.root / "notas").exists())

    def test_explicit_parent_profile_roundtrips_without_provider_or_service(self):
        profile = {"label": "Equipo de Lucía", "roles": {
            role: {"mode": "parent"}
            for role in ("study_researcher", "study_mermaid_maker", "study_visual_maker")
        }}
        path = Path(self.temp.name) / "profile.json"
        path.write_text(json.dumps(profile, ensure_ascii=False), encoding="utf-8")
        saved = self.run_cli("set", "--environment", "machine-a", "--catalog", str(self.catalog),
                             "--profile", str(path))
        self.assertEqual(saved.returncode, 0, saved.stderr)
        self.assertEqual(json.loads(saved.stdout)["targets"], {})
        shown = self.run_cli("show", "--environment", "machine-a")
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertEqual(json.loads(shown.stdout)["profile"], profile)
        self.assertFalse((self.course / "study-models.json").exists())
        self.assertFalse((self.root / "notas").exists())

    def test_bad_json_is_reported_without_traceback_or_replacement(self):
        config = self.root / "study-models.json"
        config.write_text("{ broken", encoding="utf-8")
        result = self.run_cli("show")
        self.assertEqual(result.returncode, 1)
        self.assertIn("error", json.loads(result.stderr))
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(config.read_text(encoding="utf-8"), "{ broken")


if __name__ == "__main__":
    unittest.main()
