from address.models import AddressField
from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField


class Institution(models.Model):
    name = models.CharField(
        verbose_name="Name of the School",
        max_length=250
    )

    next_year_full_tuition = MoneyField(max_digits=7, decimal_places=0, default_currency='USD')

    headmaster = models.CharField(
        verbose_name="Head of School's Name",
        max_length=250,
    )
    address = AddressField(
        on_delete=models.CASCADE,
        verbose_name="Institution's Address",
    )
    phone_number = PhoneNumberField()
    fax_number = PhoneNumberField(blank=True)

    admissions_director = models.CharField(
        verbose_name="Admissions Director's Name",
        max_length=250,
        blank=True,
    )

    website = models.URLField(blank=True)

    application_received = models.BooleanField(default=False)
    application_submitted = models.BooleanField(default=False)

    toured = models.BooleanField(default=False)

    teacher_recommendations_requested = models.BooleanField(default=False)
    teacher_recommendations_submitted = models.BooleanField(default=False)

    accepted = models.BooleanField(default=False)

    financial_aid_requested = models.BooleanField(default=False)
    financial_aid_awarded = MoneyField(max_digits=7, decimal_places=0, default_currency='USD')

    description = models.TextField(
        max_length=10000,
        blank=True,
        default='',
    )

    class Meta:
        verbose_name = "Educational Institution"
        verbose_name_plural = "Educational Institutions"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('institution-detail', kwargs={'pk': self.pk})


class Credit(models.Model):
    school = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        verbose_name="Name of Institution",
        blank=True,
    )

    name = models.CharField(max_length=100)

    SIXTH_GRADE = '6th Grade'
    SEVENTH_GRADE = '7th Grade'
    EIGHTH_GRADE = '8th Grade'
    FRESHMAN = 'Freshman'
    SOPHOMORE = 'Sophomore'
    JUNIOR = 'Junior'
    SENIOR = 'Senior'
    GRADUATE = 'Graduate'

    YEAR_IN_SCHOOL_CHOICES = [
        (SIXTH_GRADE, '6th Grade'),
        (SEVENTH_GRADE, '7th Grade'),
        (EIGHTH_GRADE, '8th Grade'),
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate School'),
    ]

    grade_level = models.CharField(
        verbose_name="Grade Level",
        max_length=9,
        choices=YEAR_IN_SCHOOL_CHOICES,
        blank=False,
    )

    CAPSTONE = 'Capstone'
    FINE_ARTS = 'Fine Arts'
    LANGUAGE_ARTS = 'Language Arts'
    MATHEMATICS = 'Mathematics'
    OUTDOOR_EDUCATION = 'Outdoor Education'
    PHYSICAL_EDUCATION = 'Physical Education'
    RELIGION = 'Religion'
    SCIENCE = 'Science'
    SOCIAL_STUDIES = 'Social Studies'
    TECHNOLOGY = 'Technology'
    WORLD_LANGUAGES = 'World Languages'

    SUBJECT_CHOICES = [
        (CAPSTONE, 'Capstone'),
        (FINE_ARTS, 'Fine Arts'),
        (LANGUAGE_ARTS, 'Language Arts'),
        (MATHEMATICS, 'Mathematics'),
        (OUTDOOR_EDUCATION, 'Outdoor Education'),
        (PHYSICAL_EDUCATION, 'Physical Education'),
        (RELIGION, 'Religious Studies'),
        (SCIENCE, 'Science'),
        (SOCIAL_STUDIES, 'Social Studies'),
        (TECHNOLOGY, 'Technology'),
        (WORLD_LANGUAGES, 'World Languages'),
    ]

    subject = models.CharField(
        verbose_name="Subject",
        max_length=18,
        choices=SUBJECT_CHOICES,
        blank=True,
    )

    AP = 'AP'
    CLEP = 'CLEP'
    PLTW = 'PLTW'

    EXAM_CHOICES = [
        (AP, 'Advanced Placement'),
        (CLEP, 'College Level Examination Program'),
        (PLTW, 'Project Lead the Way'),
    ]

    required_exam = models.CharField(
        verbose_name="Required Exam for College Credit",
        max_length=4,
        choices=EXAM_CHOICES,
        blank=True,
    )

    registered = models.BooleanField(default=False)

    raw_score_grade = models.DecimalField(
        verbose_name="Raw Class Grade Percentage",
        max_digits=5,
        decimal_places=2,
        blank=True,
        default=0.00,
    )

    letter_grade = models.CharField(
        verbose_name="Letter Grade",
        max_length=2,
        blank=True,
    )

    course_weighted_grade_point_average = models.DecimalField(
        verbose_name="Weighted Grade Point Average (GPA)",
        max_digits=3,
        decimal_places=2,
        blank=True,
        default=0.00,
    )

    class Meta:
        ordering = ['school', 'grade_level', 'subject', 'required_exam', 'name']
        verbose_name = "Graduation Credit"
        verbose_name_plural = "Graduation Credits"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('credit-detail', kwargs={'pk': self.pk})


class Instructor(models.Model):
    school = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        verbose_name="School Name",
    )

    course = models.ForeignKey(
        Credit,
        on_delete=models.CASCADE,
        blank=True,
        verbose_name="Name of School Credit",
    )

    first_name = models.CharField(
        verbose_name="Instructor's First Name",
        blank=True,
        max_length=125,
    )

    last_name = models.CharField(
        verbose_name="Instructor's Last Name",
        blank=True,
        max_length=125,
    )

    email_address_of_instructor = models.EmailField(
        verbose_name="Instructor's Email Address",
        blank=True,
    )

    phone_number_of_instructor = PhoneNumberField(
        verbose_name="Instructor's Telephone Number",
        blank=True,
    )

    def __str__(self):
        return self.last_name, self.first_name

    class Meta:
        verbose_name = "Teaching Instructor"
        verbose_name_plural = "Teaching Instructors"
        ordering = ['last_name', 'first_name']
