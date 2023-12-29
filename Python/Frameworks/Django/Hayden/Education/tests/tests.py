import pytest
import unittest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from test_models import Credit, Instructor, Institution

# @pytest.fixture
# def credit():
#     return CreditFactory()
#
#
# @pytest.fixture
# def institution():
#     return InstitutionFactory()
#
#
# @pytest.fixture
# def instructor():
#     return InstructorFactory()


def test_credit_model(Credit):
    assert Credit.school
    assert Credit.name
    assert Credit.grade_level
    assert Credit.subject
    assert Credit.course_number
    assert Credit.section
    assert Credit.track
    assert Credit.clep_exam
    assert Credit.registered
    assert Credit.grade_percentage
    assert Credit.term
    assert Credit.instructor.all()


def test_credit_model_str(Credit):
    assert str(Credit)


def test_credit_model_get_absolute_url(Credit):
    assert reverse('Education/credit_detail', kwargs={'pk': Credit.pk})


def test_credit_model_unweighted_gpa(Credit):
    assert Credit.unweighted_gpa


def test_credit_model_weighted_gpa(Credit):
    assert Credit.weighted_gpa


def test_credit_model_class_weight(Credit):
    assert Credit.class_weight


def test_credit_model_grade_equivalence(Credit):
    assert Credit.grade_equivalence


def test_institution_model(Institution):
    assert Institution.name
    assert Institution.next_year_full_tuition
    assert Institution.registration_fee
    assert Institution.student_activity_fee
    assert Institution.headmaster
    assert Institution.address
    assert Institution.phone_number
    assert Institution.fax_number
    assert Institution.admissions_director
    assert Institution.website
    assert Institution.application_received
    assert Institution.application_submitted
    assert Institution.toured
    assert Institution.teacher_recommendations_requested
    assert Institution.teacher_recommendations_submitted
    assert Institution.accepted
    assert Institution.financial_aid_requested
    assert Institution.financial_aid_awarded
    assert Institution.description
    assert Institution.slug


def test_institution_model_str(Institution):
    assert str(Institution)


def test_institution_model_get_absolute_url(Institution):
    assert reverse('Education/institution_detail', kwargs={'pk': Institution.pk})


def test_instructor_model(Instructor):
    assert Instructor.first_name
    assert Instructor.last_name
    assert Instructor.email
    assert Instructor.phone
    assert Instructor.title
    assert Instructor.slug


def test_instructor_model_str(Instructor):
    assert str(Instructor)


def test_instructor_model_get_absolute_url(Instructor):
    assert reverse('Education/instructor_detail', kwargs={'pk': Instructor.pk})


def test_credit_model_school_foreign_key(Credit):
    with pytest.raises(ValidationError):
        Credit.school = None
        Credit.full_clean()


def test_credit_model_name_max_length(Credit):
    with pytest.raises(ValidationError):
        Credit.name = 'a' * 101
        Credit.full_clean()


def test_credit_model_grade_level_choices(Credit):
    with pytest.raises(ValidationError):
        Credit.grade_level = 'Freshman'
        Credit.full_clean()


def test_credit_model_subject_choices(Credit):
    with pytest.raises(ValidationError):
        Credit.subject = 'a'
        Credit.full_clean()


def test_credit_model_course_number_max_length(Credit):
    with pytest.raises(ValidationError):
        Credit.course_number = 'a' * 11
        Credit.full_clean()


def test_credit_model_section_max_length(Credit):
    with pytest.raises(ValidationError):
        Credit.section = 'a' * 4
        Credit.full_clean()


def test_credit_model_track_choices(Credit):
    with pytest.raises(ValidationError):
        Credit.track = 'a' * 19
        Credit.full_clean()


def test_credit_model_term_choices(Credit):
    with pytest.raises(ValidationError):
        Credit.term = 'a' * 13
        Credit.full_clean()


def test_credit_model_instructor_many_to_many(Credit):
    with pytest.raises(IntegrityError):
        Credit.instructor.add(Instructor)


def test_institution_model_name_max_length(Institution):
    with pytest.raises(ValidationError):
        Institution.name = 'a' * 251
        Institution.full_clean()


def test_institution_model_next_year_full_tuition_max_length(Institution):
    with pytest.raises(ValidationError):
        Institution.next_year_full_tuition = 'a' * 8
        Institution.full_clean()


def test_institution_model_registration_fee_max_length(Institution):
    with pytest.raises(ValidationError):
        Institution.registration_fee = 'a' * 4
        Institution.full_clean()


def test_institution_model_student_activity_fee_max_length(Institution):
    with pytest.raises(ValidationError):
        Institution.student_activity_fee = 'a' * 4
        Institution.full_clean()


def test_institution_model_headmaster_max_length(Institution):
    with pytest.raises(ValidationError):
        Institution.headmaster = 'a' * 251
        Institution.full_clean()


def test_institution_model_address_model_foreign_key(Institution):
    with pytest.raises(ValidationError):
        Institution.address = None
        Institution.full_clean()


def test_institution_model_phone_number_model_foreign_key(Institution):
    with pytest.raises(ValidationError):
        Institution.phone_number = None
        Institution.full_clean()


def test_institution_model_fax_number_model_foreign_key(Institution):
    with pytest.raises(ValidationError):
        Institution.fax_number = None
        Institution.full_clean()


def test_institution_model_admissions_director_max_length(Institution):
    with pytest.raises(ValidationError):
        Institution.admissions_director = 'a' * 251
        Institution.full_clean()


def test_institution_model_website_url(Institution):
    with pytest.raises(ValidationError):
        Institution.website = 'a' * 251
        Institution.full_clean()


def test_institution_model_application_received_boolean(Institution):
    with pytest.raises(ValidationError):
        Institution.application_received = 'a'
        Institution.full_clean()


def test_institution_model_application_submitted_boolean(Institution):
    with pytest.raises(ValidationError):
        Institution.application_submitted = 'a'
        Institution.full_clean()


def test_institution_model_toured_boolean(Institution):
    with pytest.raises(ValidationError):
        Institution.toured = 'a'
        Institution.full_clean()


def test_institution_model_teacher_recommendations_requested_boolean(Institution):
    with pytest.raises(ValidationError):
        Institution.teacher_recommendations_requested = 'a'
        Institution.full_clean()


def test_institution_model_teacher_recommendations_submitted_boolean(Institution):
    with pytest.raises(ValidationError):
        Institution.teacher_recommendations_submitted = 'a'
        Institution.full_clean()


def test_institution_model_accepted_boolean(Institution):
    with pytest.raises(ValidationError):
        Institution.accepted = 'a'
        Institution.full_clean()


def test_institution_model_financial_aid_requested_boolean(Institution):
    with pytest.raises(ValidationError):
        Institution.financial_aid_requested = 'a'
        Institution.full_clean()


def test_institution_model_financial_aid_awarded_max_length(Institution):
    with pytest.raises(ValidationError):
        Institution.financial_aid_awarded = 'a' * 8
        Institution.full_clean()


def test_institution_model_description_max_length(Institution):
    with pytest.raises(ValidationError):
        Institution.description = 'a' * 10001
        Institution.full_clean()


def test_instructor_model_first_name_max_length(Instructor):
    with pytest.raises(ValidationError):
        Instructor.first_name = 'a' * 51
        Instructor.full_clean()


class CreditModelTests(TestCase):
    def setUp(self):
        self.credit1 = Credit(
            student_name='John Doe',
            course_name='Calculus',
            institution_name='MIT',
            grade='A',
            total_classes=12
        )
        self.credit1.save()

    def test_credit_model_can_be_created(self):
        credit = Credit.objects.get(id=self.credit1.id)
        self.assertIsNotNone(credit)

    def test_credit_model_has_fields(self):
        credit_fields = [
            'student_name',
            'course_name',
            'institution_name',
            'grade',
            'total_classes'
        ]
        credit = Credit.objects.get(id=self.credit1.id)
        for field in credit_fields:
            self.assertIn(field, credit.__dict__)

    def test_credit_model_can_be_queried(self):
        credit = Credit.objects.get(student_name='John Doe')
        self.assertIsNotNone(credit)


class InstitutionModelTests(TestCase):
    def setUp(self):
        self.institution1 = Institution(
            name='MIT',
            next_year_full_tuition=50000,
            financial_aid_awarded=10000
        )
        self.institution1.save()

    def test_institution_model_can_be_created(self):
        institution = Institution.objects.get(id=self.institution1.id)
        self.assertIsNotNone(institution)

    def test_institution_model_has_fields(self):
        institution_fields = [
            'name',
            'full_tuition',
            'financial_aid_awarded'
        ]
        institution = Institution.objects.get(id=self.institution1.id)
        for field in institution_fields:
            self.assertIn(field, institution.__dict__)

    def test_institution_model_can_be_queried(self):
        institution = Institution.objects.get(name='MIT')
        self.assertIsNotNone(institution)


class InstructorModelTests(TestCase):
    def setUp(self):
        self.instructor1 = Instructor(
            first_name='Harry',
            last_name='Potter'
        )
        self.instructor1.save()

    def test_instructor_model_can_be_created(self):
        instructor = Instructor.objects.get(id=self.instructor1.id)
        self.assertIsNotNone(instructor)

    def test_instructor_model_has_fields(self):
        instructor_fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'title',
        ]
        instructor = Instructor.objects.get(id=self.instructor1.id)
        for field in instructor_fields:
            self.assertIn(field, instructor.__dict__)

    def test_instructor_model_can_be_queried(self):
        instructor = Instructor.objects.get(last_name='Potter')
        self.assertIsNotNone(instructor)
