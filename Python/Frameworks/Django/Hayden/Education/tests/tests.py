"""Django tests for Hayden's education and careers subprojects."""
from django.test import TestCase
from django.urls import reverse
from moneyed import Money

from Education.models import Credit, Instructor, School
from Job.models import Career


class HaydenHomeViewTests(TestCase):
    def test_home_page_loads_with_an_empty_credit_list(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertEqual(list(response.context["credit_list"]), [])


class EducationModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.school = School.objects.create(
            name="Example School",
            slug="example-school",
            headmaster="Example Headmaster",
            next_year_full_tuition=Money(10000, "USD"),
            registration_fee=Money(500, "USD"),
            student_activity_fee=Money(250, "USD"),
        )
        cls.instructor = Instructor.objects.create(
            first_name="Taylor",
            last_name="Teacher",
            email="teacher@example.test",
            phone="+12025550100",
            title="Class Instructor",
            slug="taylor-teacher",
        )
        cls.credit = Credit.objects.create(
            school=cls.school,
            name="Biology",
            grade_level="Senior",
            subject=Credit.Subject.SCIENCE,
            course_number=101,
            section=1,
            track="Honors",
            grade_percentage=95,
            term="Semester",
            slug="biology-101",
        )
        cls.credit.instructor.add(cls.instructor)

    def test_school_string_representation(self):
        self.assertEqual(str(self.school), "Example School")

    def test_instructor_string_representation(self):
        self.assertEqual(str(self.instructor), "Taylor Teacher")

    def test_credit_gpa_and_term_weight_calculations(self):
        self.assertEqual(self.credit.unweighted_gpa, 4.0)
        self.assertAlmostEqual(self.credit.weighted_gpa, 5.2)
        self.assertEqual(self.credit.class_weight, 0.5)
        self.assertEqual(self.credit.weighted_grade_equivalence, "A+")


class CareerModelAndViewTests(TestCase):
    def setUp(self):
        self.career = Career.objects.create(
            profession="Software Engineer",
            average_salary=Money(95000, "USD"),
            required_education="Bachelor's Degree",
        )

    def test_career_model_fields_and_string(self):
        self.assertEqual(str(self.career), "Software Engineer")
        self.assertEqual(self.career.average_salary, Money(95000, "USD"))

    def test_career_list_view(self):
        response = self.client.get(reverse("Job:career-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Software Engineer")

    def test_career_detail_view(self):
        response = self.client.get(
            reverse("Job:career-detail", args=[self.career.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Software Engineer")
