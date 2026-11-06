"""Profiles use real catalog semantics without running models or writing notes."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import tempfile
import unittest

PACK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("study_models", PACK / "scripts/study_models.py")
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)


class ModelProfilesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="study-model-test-")
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name) / "study workspace ü"
        (self.workspace / "skills/t3-study").mkdir(parents=True)
        (self.workspace / "skills/t3-study/SKILL.md").write_text("Test skill.")
        self.catalog = {
            "inheritedProviderInstanceId": "provider-a",
            "runtimeMode": "full-access",
            "providers": [{
                "providerInstanceId": "provider-b",
                "canRunChildTask": True, "canRunCrossProviderChildTask": True,
                "runtimeModes": ["full-access"],
                "models": [{"id": "verified-model", "options": [
                    {"id": "effort", "values": ["low", "high"]},
                    {"id": "fastMode", "values": [False, True]},
                ]}],
            }],
        }
        self.profile = {"label": "Test machine", "roles": {
            role: {"providerInstanceId": "provider-b", "model": "verified-model",
                   "options": {"effort": "high", "fastMode": False}}
            for role in models.ROLES
        }}

    def test_new_environment_needs_setup_without_writing_any_files(self):
        result = models.check(self.workspace, "new-machine", self.catalog)
        self.assertEqual(result["status"], "setup_required")
        self.assertEqual(result["targets"], {})
        self.assertFalse(models.config_path(self.workspace).exists())
        self.assertFalse((self.workspace / "notas").exists())

    def test_saved_choices_preserve_other_machines_and_exact_target_options(self):
        models.save_profile(self.workspace, "one", self.profile, self.catalog)
        second = deepcopy(self.profile)
        second["roles"]["study_mermaid_maker"] = {"mode": "parent"}
        result = models.save_profile(self.workspace, "two", second, self.catalog)
        self.assertEqual(result["status"], "ready")
        self.assertNotIn("study_mermaid_maker", result["targets"])
        self.assertEqual(result["targets"]["study_researcher"], self.profile["roles"]["study_researcher"])
        config = models.load_config(self.workspace)
        self.assertEqual(config["environments"]["one"], self.profile)
        self.assertEqual(config["environments"]["two"], second)
        self.assertEqual(models.check(self.workspace, "third-machine", self.catalog)["status"], "setup_required")
        self.assertFalse((self.workspace / "notas").exists())

    def test_disabled_or_incompatible_provider_never_overwrites_saved_profile(self):
        models.save_profile(self.workspace, "one", self.profile, self.catalog)
        before = models.config_path(self.workspace).read_bytes()
        for field, value in [("canRunChildTask", False), ("canRunCrossProviderChildTask", False),
                             ("runtimeModes", ["approval-required"])]:
            with self.subTest(field=field):
                catalog = deepcopy(self.catalog)
                catalog["providers"][0][field] = value
                self.assertEqual(models.check(self.workspace, "one", catalog)["status"], "needs_attention")
                with self.assertRaises(models.StudyError):
                    models.save_profile(self.workspace, "one", self.profile, catalog)
                self.assertEqual(models.config_path(self.workspace).read_bytes(), before)

    def test_unsupported_options_and_unlisted_model_are_not_assumed_valid(self):
        invalid = [
            {"model": "not-in-short-catalog"},
            {"options": {"reasoningEffort": "high"}},
            {"options": {"effort": "ultra"}},
            {"options": {"fastMode": 1}},
        ]
        for change in invalid:
            with self.subTest(change=change):
                profile = deepcopy(self.profile)
                profile["roles"]["study_researcher"].update(change)
                with self.assertRaises(models.StudyError):
                    models.save_profile(self.workspace, "one", profile, self.catalog)
        self.assertFalse(models.config_path(self.workspace).exists())

    def test_partial_profiles_require_attention_instead_of_inheriting_implicitly(self):
        del self.profile["roles"]["study_visual_maker"]
        with self.assertRaises(models.StudyError):
            models.save_profile(self.workspace, "one", self.profile, self.catalog)

    def test_malformed_config_is_preserved(self):
        path = models.config_path(self.workspace)
        path.write_text('{"schema_version":1, malformed')
        original = path.read_bytes()
        with self.assertRaises(models.StudyError):
            models.save_profile(self.workspace, "one", self.profile, self.catalog)
        self.assertEqual(path.read_bytes(), original)

    def test_user_can_choose_parent_for_all_roles(self):
        profile = {"roles": {role: {"mode": "parent"} for role in models.ROLES}}
        result = models.save_profile(self.workspace, "one", profile, self.catalog)
        self.assertEqual(result["status"], "ready")
        self.assertEqual(result["targets"], {})


if __name__ == "__main__":
    unittest.main()
