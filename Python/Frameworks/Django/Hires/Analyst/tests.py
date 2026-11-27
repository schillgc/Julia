"""Tests for the Hires job-list application."""
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from Analyst.models import Job


class HiresViewTests(TestCase):
    def setUp(self):
        self.staff_user = get_user_model().objects.create_user(
            username="hires-staff",
            email="hires-staff@example.test",
            is_staff=True,
        )
        self.job = Job.objects.create(
            company="Private Example Employer",
            title="Senior Engineer",
        )

    def test_anonymous_users_cannot_view_the_job_list(self):
        response = self.client.get(reverse("Analyst:index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/admin/login/"))

    def test_anonymous_users_cannot_view_job_details(self):
        response = self.client.get(
            reverse("Analyst:detail", kwargs={"slug": self.job.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/admin/login/"))

    def test_authenticated_non_staff_users_cannot_view_job_records(self):
        user = get_user_model().objects.create_user(
            username="hires-non-staff",
            email="hires-non-staff@example.test",
            password="test-only-password",
            is_staff=False,
        )
        self.client.force_login(user)
        for url in (
            reverse("Analyst:index"),
            reverse("Analyst:detail", kwargs={"slug": self.job.slug}),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith("/admin/login/"))

    def test_staff_can_view_the_job_list_and_job_details(self):
        self.client.force_login(self.staff_user)
        index_response = self.client.get(reverse("Analyst:index"))
        detail_response = self.client.get(
            reverse("Analyst:detail", kwargs={"slug": self.job.slug})
        )
        self.assertEqual(index_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(index_response, "Private Example Employer")
        self.assertContains(detail_response, "Private Example Employer")

    def test_staff_list_view_returns_an_empty_list_when_no_jobs_exist(self):
        Job.objects.all().delete()
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse("Analyst:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["job_list"]), [])

    def test_new_job_generates_a_human_readable_slug_and_detail_url(self):
        job = Job.objects.create(company="Acme Labs", title="Senior Engineer")
        self.assertEqual(job.slug, "acme-labs-senior-engineer")
        self.assertEqual(job.get_absolute_url(), "/job/acme-labs-senior-engineer/")

    def test_duplicate_job_titles_receive_distinct_slugs(self):
        first = Job.objects.create(company="Acme Labs", title="Engineer")
        second = Job.objects.create(company="Acme Labs", title="Engineer")
        self.assertEqual(first.slug, "acme-labs-engineer")
        self.assertEqual(second.slug, "acme-labs-engineer-2")

    def test_ci_database_override_is_used_when_configured(self):
        database_path = os.environ.get("HIRES_DJANGO_DB_NAME")
        if database_path:
            self.assertEqual(settings.DATABASES["default"]["NAME"], database_path)
