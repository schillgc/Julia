"""Tests for the Hires job-list application."""
from django.test import TestCase


class HiresViewTests(TestCase):
    def test_index_view_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Analyst/index.html")

    def test_index_view_returns_an_empty_job_list_without_records(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["job_list"]), [])
