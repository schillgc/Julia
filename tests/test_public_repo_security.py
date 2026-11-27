"""Regression checks for source-control privacy and configuration boundaries."""

import ast
import os
import unittest
import re
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
DJANGO_SETTINGS = [
    ("Python/Frameworks/Django/Hayden/Hayden/settings.py", "HAYDEN"),
    ("Python/Frameworks/Django/Hires/Hires/settings.py", "HIRES"),
    ("Python/Frameworks/Django/Inventory/summit/summit/settings.py", "INVENTORY"),
    ("Python/Frameworks/Django/Job Analyzer/jobanalyzer/jobanalyzer/settings.py", "JOB_ANALYZER"),
    ("Python/Frameworks/Django/KDF/KDF/settings.py", "KDF"),
    ("Python/Frameworks/Django/Polls/mysite/mysite/settings.py", "POLLS"),
    ("Python/Frameworks/Django/UICalendar/ui_calendar/ui_calendar/settings.py", "UI_CALENDAR"),
    ("Python/Frameworks/Django/Vintage Print and Distribution/automation/automation/settings.py", "VINTAGE_AUTOMATION"),
    ("Python/Frameworks/Django/semmLaw/semmlaw/semmlaw/settings.py", "SEMMLAW"),
    ("Python/Frameworks/Django/Gymkhana Stampede/KDF/KDF/settings.py", "GYMKHANA"),
    ("Python/Frameworks/Django/Men's Outfit Predictor/OutfitPredictor/OutfitPredictor/settings.py", "OUTFIT_PREDICTOR_FRAMEWORK"),
    ("Python/Console Apps/Utilities/Men's Outfit Predictor/OutfitPredictor/OutfitPredictor/settings.py", "OUTFIT_PREDICTOR"),
]


class PublicRepositorySecurityTests(unittest.TestCase):
    def test_vintage_address_records_require_staff_and_route_parameters_match(self):
        project = "Python/Frameworks/Django/Vintage Print and Distribution/automation/"
        settings = (ROOT / project / "automation/settings.py").read_text(encoding="utf-8")
        urls = (ROOT / project / "file_converter/urls.py").read_text(encoding="utf-8")
        views = (ROOT / project / "file_converter/views.py").read_text(encoding="utf-8")

        self.assertRegex(
            settings,
            r"'file_converter\.apps\.FileConverterConfig',\s*'django\.contrib\.admin',",
        )
        self.assertIn("path('<int:address_id>/', views.demographics", urls)
        self.assertIn("def demographics(request, address_id):", views)
        self.assertIn('@staff_member_required(login_url="/admin/login/")', views)
        self.assertIn('"file_converter/address.html"', views)

    def load_project_required_env(self, relative_path):
        """Execute only the project's environment helper without importing Django."""
        source = (ROOT / relative_path).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=relative_path)
        function = next(
            node for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "_required_env"
        )
        module = ast.Module(body=[function], type_ignores=[])
        ast.fix_missing_locations(module)
        namespace = {"os": os, "ImproperlyConfigured": ValueError}
        exec(compile(module, relative_path, "exec"), namespace)
        return namespace["_required_env"]

    def test_all_project_signing_key_helpers_enforce_minimum_strength(self):
        for relative_path, prefix in DJANGO_SETTINGS:
            required_env = self.load_project_required_env(relative_path)
            variable = f"{prefix}_DJANGO_SECRET_KEY"
            with self.subTest(path=relative_path, weakness="short"):
                with patch.dict(os.environ, {variable: "short-secret"}):
                    with self.assertRaisesRegex(ValueError, "at least 50 characters"):
                        required_env(variable)
            with self.subTest(path=relative_path, weakness="low-diversity"):
                weak_key = ("A" * 59) + "b"
                with patch.dict(os.environ, {variable: weak_key}):
                    with self.assertRaisesRegex(ValueError, "5 distinct characters"):
                        required_env(variable)
            with self.subTest(path=relative_path, weakness="valid"):
                valid_key = (
                    f"portfolio-test-{prefix.lower()}-key-with-at-least-fifty-characters-"
                    "and-varied-alphabet-2026"
                )
                self.assertGreaterEqual(len(valid_key), 50)
                self.assertGreaterEqual(len(set(valid_key)), 5)
                with patch.dict(os.environ, {variable: valid_key}):
                    self.assertEqual(required_env(variable), valid_key)

    def test_django_settings_fail_closed_and_use_project_specific_environment(self):
        for relative_path, prefix in DJANGO_SETTINGS:
            with self.subTest(path=relative_path):
                source = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(f'SECRET_KEY = _required_env("{prefix}_DJANGO_SECRET_KEY")', source)
                self.assertIn(f'DEBUG = _env_bool("{prefix}_DJANGO_DEBUG", default=False)', source)
                self.assertIn(f'ALLOWED_HOSTS = _env_csv("{prefix}_DJANGO_ALLOWED_HOSTS")', source)
                self.assertIn("len(value) < 50", source)
                self.assertIn("len(set(value)) < 5", source)
                self.assertNotRegex(source, r"(?m)^SECRET_KEY\s*=\s*['\"]")
                self.assertNotRegex(source, r"(?m)^DEBUG\s*=\s*True\s*$")
                self.assertNotRegex(source, r"AIza[0-9A-Za-z_-]{30,}")

    def test_oauth_tokens_and_client_files_are_not_tracked(self):
        self.assertFalse((ROOT / "Python/Console Apps/Utilities/Google Calendar API/credentials.json").exists())
        self.assertFalse((ROOT / "Python/Console Apps/Utilities/Google Calendar API/token.pickle").exists())
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in ("**/credentials.json", "**/client_secrets.json", "**/token.pickle", "**/token.json"):
            self.assertIn(pattern, ignore)

    def test_python_credential_modules_and_private_keys_are_ignored(self):
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in (
            "**/credentials.py",
            "**/secrets.py",
            "**/*_credentials.py",
            "**/*_secrets.py",
            "**/*.pem",
            "**/*.key",
            "**/*.p12",
            "**/*.pfx",
        ):
            with self.subTest(pattern=pattern):
                self.assertIn(pattern, ignore)

        policy = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("Ignore rules do not remove files that are already tracked", policy)
        self.assertIn("Oxford Dictionary", policy)
        credential_module = (
            ROOT / "Python/Console Apps/Utilities/Oxford Dictionary/credentials.py"
        ).read_text(encoding="utf-8")
        self.assertIn('os.environ.get("OXFORD_DICTIONARIES_APP_ID", "")', credential_module)
        self.assertIn('os.environ.get("OXFORD_DICTIONARIES_APP_KEY", "")', credential_module)
        self.assertNotRegex(credential_module, r"AIza[0-9A-Za-z_-]{30,}")

    def test_external_api_samples_do_not_embed_keys(self):
        paths = [
            "Python/Console Apps/Utilities/Oxford Dictionary/credentials.py",
            "Python/Console Apps/Utilities/Oxford Dictionary/oxford_dictionary.cs",
            "Python/Console Apps/Utilities/MailChimp API/mailchimp-api.py",
            "Python/Frameworks/Django/semmLaw/semmlaw/semmlaw/settings.py",
            "Python/Console Apps/Utilities/Code Describer/config.py",
        ]
        for relative_path in paths:
            with self.subTest(path=relative_path):
                source = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertNotRegex(source, r"AIza[0-9A-Za-z_-]{30,}")
                self.assertNotRegex(source, r'''(?i)(?:app_key|api_key|client_secret)\s*[:=]\s*['"][^'"]{12,}['"]''')

    def test_url_calculator_does_not_embed_a_development_server(self):
        relative_path = "Python/Console Apps/Utilities/URL Calculator/url_calculator.py"
        source = (ROOT / relative_path).read_text(encoding="utf-8")
        module = ast.parse(source, filename=relative_path)
        run_calls = [
            node for node in ast.walk(module)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "app"
            and node.func.attr == "run"
        ]

        self.assertEqual(run_calls, [])
        self.assertNotIn("0.0.0.0", source)
        self.assertNotIn("debug=True", source)
    def test_job_search_mailchimp_utility_uses_environment_credentials(self):
        template = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("JOB_SEARCH_MAILCHIMP_API_KEY=", template)
        self.assertIn("JOB_SEARCH_MAILCHIMP_USERNAME=", template)

        script = (
            ROOT / "Python/Console Apps/Utilities/Job Search/job_search.py"
        ).read_text(encoding="utf-8")
        self.assertIn('os.environ.get("JOB_SEARCH_MAILCHIMP_API_KEY"', script)
        self.assertIn('os.environ.get("JOB_SEARCH_MAILCHIMP_USERNAME"', script)
        self.assertIn('if __name__ == "__main__":', script)
        self.assertNotIn("from credentials import", script)

    def test_oxford_dictionary_examples_use_environment_credentials(self):
        template = (ROOT / ".env.example").read_text(encoding="utf-8")
        self.assertIn("OXFORD_DICTIONARIES_APP_ID=", template)
        self.assertIn("OXFORD_DICTIONARIES_APP_KEY=", template)

        for relative_path in (
            "Python/Console Apps/Utilities/Oxford Dictionary/oxford_dictionary.py",
            "Python/Console Apps/Utilities/Oxford Dictionary/oxford_dictionary_2.py",
        ):
            with self.subTest(path=relative_path):
                source = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn('os.environ.get("OXFORD_DICTIONARIES_APP_ID"', source)
                self.assertIn('os.environ.get("OXFORD_DICTIONARIES_APP_KEY"', source)
                self.assertIn("timeout=(5, 20)", source)
                self.assertIn('if __name__ == "__main__":', source)
                self.assertNotIn("from credentials import", source)

    def test_mailchimp_credentials_are_environment_driven_and_never_hardcoded(self):
        settings = (
            ROOT / "Python/Frameworks/Django/semmLaw/semmlaw/semmlaw/settings.py"
        ).read_text(encoding="utf-8")
        sample = (
            ROOT / "Python/Console Apps/Utilities/MailChimp API/mailchimp-api.py"
        ).read_text(encoding="utf-8")
        template = (ROOT / ".env.example").read_text(encoding="utf-8")

        self.assertRegex(
            settings,
            r'MAILCHIMP_API_KEY\s*=\s*os\.environ\.get\("SEMMLAW_MAILCHIMP_API_KEY",\s*""\)',
        )
        self.assertIn("MAILCHIMP_TRANSACTIONAL_API_KEY", sample)
        self.assertRegex(
            sample,
            r'os\.environ\.get\("MAILCHIMP_TRANSACTIONAL_API_KEY",\s*""\)',
        )
        self.assertIn("SEMMLAW_MAILCHIMP_API_KEY=", template)
        self.assertIn("MAILCHIMP_TRANSACTIONAL_API_KEY=", template)
        for source in (settings, sample):
            self.assertNotRegex(
                source,
                r"(?i)(?:[a-f0-9]{32}-us\d+|mc-[a-f0-9]{30,})",
            )

    def test_personal_financial_values_are_loaded_at_runtime(self):
        paths = [
            "Python/Console Apps/Utilities/BCforward Budget/financials/assets.py",
            "Python/Console Apps/Utilities/BCforward Budget/financials/expenses.py",
            "Python/Console Apps/Utilities/Job Analysis/Base/Income/external.py",
            "Python/Console Apps/Utilities/Job Analysis/Positions/Local/MHS/senior_power_bi_developer.py",
        ]
        for relative_path in paths:
            with self.subTest(path=relative_path):
                source = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn("os.environ", source)

    def test_sensitive_environment_template_contains_no_actual_credentials(self):
        source = (ROOT / ".env.example").read_text(encoding="utf-8")
        for line in source.splitlines():
            if "=" not in line or line.lstrip().startswith("#"):
                continue
            key, value = line.split("=", 1)
            if any(part in key for part in ("SECRET_KEY", "API_KEY", "APP_KEY")):
                self.assertEqual(value, "", msg=f"{key} must remain an empty placeholder")

    def test_cell_biller_private_inputs_are_not_tracked_or_embedded(self):
        biller = ROOT / "Python/Frameworks/Streamlit/Cell Phone Biller"
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in (
            "**/tmobile_config.json",
            "**/bills.xlsx",
            "**/tmobile_bills.csv",
            "**/tmobile_bills.xlsx",
        ):
            self.assertIn(pattern, ignore)
        self.assertFalse((biller / "tmobile_config.json").exists())
        self.assertFalse((biller / "bills.xlsx").exists())

        app_source = (biller / "app.py").read_text(encoding="utf-8")
        readme = (biller / "README.md").read_text(encoding="utf-8")
        for source in (app_source, readme):
            self.assertNotRegex(source, r"\(\d{3}\)\s*\d{3}-\d{4}")
            self.assertNotIn("354.37", source)
        self.assertIn('os.environ.get("TMOBILE_CONFIG_FILE"', app_source)
        self.assertIn('"expected_total_bill": None', app_source)
        self.assertIn("legacy_tmobile_perk_members", app_source)
        self.assertIn("line_on_us_members", app_source)
        self.assertIn("io.BytesIO()", app_source)
        self.assertNotIn("EXPECTED_TOTAL_BILL", app_source)

    def test_changed_python_files_compile(self):
        paths = [path for path, _ in DJANGO_SETTINGS] + [
            "Python/Frameworks/Django/Vintage Print and Distribution/automation/automation/settings.py",
            "Python/Frameworks/Django/Vintage Print and Distribution/automation/file_converter/urls.py",
            "Python/Frameworks/Django/Vintage Print and Distribution/automation/file_converter/views.py",
            "Python/Console Apps/Utilities/URL Calculator/url_calculator.py",
            "Python/Console Apps/Utilities/Job Search/job_search.py",
            "Python/Console Apps/Utilities/Google Calendar API/quickstart.py",
            "Python/Console Apps/Utilities/Oxford Dictionary/credentials.py",
            "Python/Console Apps/Utilities/Oxford Dictionary/oxford_dictionary.py",
            "Python/Console Apps/Utilities/Oxford Dictionary/oxford_dictionary_2.py",
            "Python/Console Apps/Utilities/MailChimp API/mailchimp-api.py",
            "Python/Console Apps/Utilities/Code Describer/config.py",
            "Python/Frameworks/Django/semmLaw/semmlaw/marketing/views.py",
            "Python/Console Apps/Utilities/BCforward Budget/financials/assets.py",
            "Python/Console Apps/Utilities/BCforward Budget/financials/expenses.py",
            "Python/Console Apps/Utilities/BCforward Budget/calculator.py",
            "Python/Console Apps/Utilities/Job Analysis/Base/Income/external.py",
            "Python/Console Apps/Utilities/Job Analysis/Positions/Local/MHS/senior_power_bi_developer.py",
            "Python/Console Apps/Utilities/YouTube API/youtube.py",
            "Python/Frameworks/Streamlit/Cell Phone Biller/app.py",
        ]
        for relative_path in paths:
            with self.subTest(path=relative_path):
                source = (ROOT / relative_path).read_text(encoding="utf-8")
                compile(source, relative_path, "exec")


if __name__ == "__main__":
    unittest.main()
