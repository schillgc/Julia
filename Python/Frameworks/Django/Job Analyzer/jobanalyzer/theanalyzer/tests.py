"""Access-control and configuration tests for private Job Analyzer records."""

import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Company, Position


class JobAnalyzerAccessControlTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Example Employer",
            industry="Technology",
        )
        self.position = Position.objects.create(
            title="Senior Data Analyst",
            company=self.company,
            active=True,
            applied=True,
            interviewed=False,
        )
        self.staff_user = get_user_model().objects.create_user(
            username="job-analyzer-staff",
            email="job-analyzer-staff@example.test",
            is_staff=True,
        )

    def protected_urls(self):
        return (
            reverse("theanalyzer:position_list"),
            reverse("theanalyzer:position_detail", kwargs={"the_slug": self.position.slug}),
            reverse("theanalyzer:company_list"),
            reverse("theanalyzer:company_detail", kwargs={"pk": self.company.pk}),
        )

    def test_anonymous_users_cannot_view_private_job_search_records(self):
        for url in self.protected_urls():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith("/admin/login/"))

    def test_authenticated_non_staff_users_cannot_view_private_job_search_records(self):
        user = get_user_model().objects.create_user(
            username="job-analyzer-non-staff",
            email="job-analyzer-non-staff@example.test",
        )
        self.client.force_login(user)

        for url in self.protected_urls():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith("/admin/login/"))

    def test_staff_users_can_view_position_and_company_records(self):
        self.client.force_login(self.staff_user)

        for url in self.protected_urls():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_ci_database_environment_override_is_used(self):
        database_path = os.environ.get("JOB_ANALYZER_DJANGO_DB_NAME")
        if database_path:
            self.assertEqual(settings.DATABASES["default"]["NAME"], database_path)
