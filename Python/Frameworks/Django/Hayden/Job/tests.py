from django.test import TestCase
from django.urls import reverse
from moneyed import Money

# Use a relative import for models within the same app
from Job.models import Career


class CareerModelTests(TestCase):
    """
    Tests for the Career model.
    """

    def setUp(self):
        """
        Set up a sample Career object for use in all test methods.
        This method is run before each test.
        """
        self.career = Career.objects.create(
            profession="Software Engineer",
            average_salary=Money(95000, 'USD'),
            required_education="Bachelor's Degree"
        )

    def test_career_creation(self):
        """Test that a Career instance can be created with the correct attributes."""
        self.assertIsInstance(self.career, Career)
        self.assertEqual(self.career.profession, "Software Engineer")
        self.assertEqual(self.career.average_salary, Money(95000, 'USD'))
        self.assertEqual(self.career.required_education, "Bachelor's Degree")

    def test_str_representation(self):
        """Test the model's __str__ method."""
        self.assertEqual(str(self.career), "Software Engineer")

    def test_meta_ordering(self):
        """Test the model's Meta ordering option."""
        # Create a few more objects to test ordering
        Career.objects.create(
            profession="Doctor",
            average_salary=Money(200000, 'USD'),
            required_education="Doctor of Medicine"
        )
        Career.objects.create(
            profession="Accountant",
            average_salary=Money(70000, 'USD'),
            required_education="Bachelor's Degree"
        )

        # The order should be by required_education, then average_salary, then profession
        careers = Career.objects.all()
        self.assertEqual(careers[0].profession, "Accountant")
        self.assertEqual(careers[1].profession, "Software Engineer")
        self.assertEqual(careers[2].profession, "Doctor")


class CareerViewTests(TestCase):
    """
    Tests for the views related to the Career model.
    Assumes you have a 'career-list' and 'career-detail' URL name.
    """

    def setUp(self):
        """Set up a sample career for view tests."""
        self.career = Career.objects.create(
            profession="Data Scientist",
            average_salary=Money(110000, 'USD')
        )

    def test_career_list_view(self):
        """Test the list view for careers."""
        # Use the namespaced URL name 'Job:career-list'
        url = reverse('Job:career-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Data Scientist")
        # ASSUMPTION: You have a template at 'Job/career_list.html'
        self.assertTemplateUsed(response, 'Job/career_list.html')

    def test_career_detail_view(self):
        """Test the detail view for a single career."""
        # Use the namespaced URL name 'Job:career-detail'
        url = reverse('Job:career-detail', args=[self.career.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Data Scientist")

    def test_career_detail_view_not_found(self):
        """Test that the detail view returns a 404 for an invalid career ID."""
        url = reverse('Job:career-detail', args=[999])  # An ID that doesn't exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
