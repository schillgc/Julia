"""Regression checks for source-control privacy and configuration boundaries."""

import unittest
from pathlib import Path


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
    def test_django_settings_fail_closed_and_use_project_specific_environment(self):
        for relative_path, prefix in DJANGO_SETTINGS:
            with self.subTest(path=relative_path):
                source = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(f'SECRET_KEY = _required_env("{prefix}_DJANGO_SECRET_KEY")', source)
                self.assertIn(f'DEBUG = _env_bool("{prefix}_DJANGO_DEBUG", default=False)', source)
                self.assertIn(f'ALLOWED_HOSTS = _env_csv("{prefix}_DJANGO_ALLOWED_HOSTS")', source)
                self.assertNotRegex(source, r"(?m)^SECRET_KEY\s*=\s*['\"]")
                self.assertNotRegex(source, r"(?m)^DEBUG\s*=\s*True\s*$")
                self.assertNotRegex(source, r"AIza[0-9A-Za-z_-]{30,}")

    def test_oauth_tokens_and_client_files_are_not_tracked(self):
        self.assertFalse((ROOT / "Python/Console Apps/Utilities/Google Calendar API/credentials.json").exists())
        self.assertFalse((ROOT / "Python/Console Apps/Utilities/Google Calendar API/token.pickle").exists())
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for pattern in ("**/credentials.json", "**/client_secrets.json", "**/token.pickle", "**/token.json"):
            self.assertIn(pattern, ignore)

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

    def test_changed_python_files_compile(self):
        paths = [path for path, _ in DJANGO_SETTINGS] + [
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
        ]
        for relative_path in paths:
            with self.subTest(path=relative_path):
                source = (ROOT / relative_path).read_text(encoding="utf-8")
                compile(source, relative_path, "exec")


if __name__ == "__main__":
    unittest.main()
