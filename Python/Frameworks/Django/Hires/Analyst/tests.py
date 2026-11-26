"""Tests for the Hires job-list application."""
from django.test import TestCase

from Analyst.models import Job


class HiresViewTests(TestCase):
    def test_index_view_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Analyst/index.html")

    def test_index_view_returns_an_empty_job_list_without_records(self):
        response = self.client.get("/")
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
