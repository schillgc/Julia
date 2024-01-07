# tests/test_models.py
from django.test import TestCase
from djmoney.models.fields import Money

from Education.models import Institution, Instructor, Credit


class TestInstitution(TestCase):
    def setUp(self):
        self.institution = Institution(
            name='Test Institution',
            next_year_full_tuition=Money(10000, 'USD'),
            registration_fee=Money(500, 'USD'),
            student_activity_fee=Money(250, 'USD'),
            headmaster='Test Headmaster',
            address='Test Address',
            phone_number='555-555-5555',
            fax_number='555-555-5556',
            admissions_director='Test Admissions Director',
            website='http://example.com',
            application_received=True,
            application_submitted=True,
            toured=True,
            teacher_recommendations_requested=True,
            teacher_recommendations_submitted=True,
            accepted=True,
            financial_aid_requested=True,
            financial_aid_awarded=Money(5000, 'USD'),
            description='Test Description',
            slug='test-institution'
        )

    def test_str(self):
        self.assertEqual(str(self.institution), 'Test Institution')


class TestInstructor(TestCase):
    def setUp(self):
        self.instructor = Instructor(
            first_name='Test',
            last_name='Instructor',
            email='<EMAIL>',
            phone='555-555-5555',
            title=Instructor.Title.TEACHER,
            slug='test-instructor'
        )

    def test_str(self):
        self.assertEqual(str(self.instructor), 'Instructor, Test')


class TestCredit(TestCase):
    def setUp(self):
        self.credit = Credit(
            school=Institution.objects.first(),
            name='Test Credit',
            grade_level=Credit.YearInSchool.SENIOR,
            subject=Credit.Subject.SCIENCE,
            course_number=100,
            section='001',
            track=Credit.Track.ACADEMIC,
            clep_exam=False,
            registered=True,
            grade_percentage=90,
            term=Credit.Term.SEMESTER,
            slug='test-credit'
        )