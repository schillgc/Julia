from address.models import AddressField
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import TextChoices
from django.urls import reverse
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField


class Institution(models.Model):
    name = models.CharField(verbose_name="Name of the School", max_length=250)
    next_year_full_tuition = MoneyField(max_digits=7, decimal_places=0, default_currency='USD')
    registration_fee = MoneyField(max_digits=3, decimal_places=0, default_currency='USD')
    student_activity_fee = MoneyField(max_digits=3, decimal_places=0, default_currency='USD')
    headmaster = models.CharField(verbose_name="Head of School's Name", max_length=250)
    address = AddressField(verbose_name="Institution's Address")
    phone_number = PhoneNumberField(verbose_name="School's Main Phone Number", blank=True)
    fax_number = PhoneNumberField(verbose_name="School's Main Fax Number", blank=True)
    admissions_director = models.CharField(verbose_name="Admissions Director's Name", max_length=250, blank=True)
    website = models.URLField(verbose_name="School Website", blank=True)
    application_received = models.BooleanField(default=False)
    application_submitted = models.BooleanField(default=False)
    toured = models.BooleanField(default=False)
    teacher_recommendations_requested = models.BooleanField(default=False)
    teacher_recommendations_submitted = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    financial_aid_requested = models.BooleanField(default=False)
    financial_aid_awarded = MoneyField(max_digits=7, decimal_places=0, default_currency='USD')
    description = models.TextField(max_length=10000, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Educational Institution"
        verbose_name_plural = "Educational Institutions"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('institution-detail', kwargs={'pk': self.pk})


class Instructor(models.Model):
    first_name = models.CharField(verbose_name="Instructor's First Name", max_length=50, blank=True)
    last_name = models.CharField(verbose_name="Instructor's Last Name", max_length=50, blank=True)
    email = models.EmailField(verbose_name="Instructor's Email Address", blank=True, validators=[EmailValidator])
    phone = PhoneNumberField(verbose_name="Instructor's Telephone Number", blank=True)

    class Title(TextChoices):
        ADVISOR = 'Academic Advisor'
        COUNSELOR = 'Counselor'
        MENTOR = 'Mentor'
        NURSE = 'School Nurse'
        SPONSOR = 'Club Faculty Sponsor'
        TEACHER = 'Class Instructor'

    title = models.CharField(verbose_name="Professional Role Title", max_length=20, choices=Title.choices, blank=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    class Meta:
        verbose_name = "Teaching Instructor"
        verbose_name_plural = "Teaching Instructors"
        ordering = ['last_name', 'first_name']


class Credit(models.Model):
    class Subject(TextChoices):
        BUSINESS_AND_TECHNOLOGY = 'B', 'Business & Technology'
        ENGLISH = 'E', 'English'
        ENRICHMENT = 'Q', 'Enrichment'
        FINE_ARTS_AND_HUMANITIES = 'A', 'Fine Arts & Humanities'
        MATHEMATICS = 'M', 'Mathematics'
        HEALTH_AND_PHYSICAL_EDUCATION = 'P', 'Health & Physical Education'
        SCIENCE = 'C', 'Science'
        SOCIAL_STUDIES = 'T', 'Social Studies'
        THEOLOGY = 'R', 'Theology'
        CHINESE = 'H', 'Chinese'
        FRENCH = 'F', 'French'
        GERMAN = 'G', 'German'
        SPANISH = 'S', 'Spanish'

    class Track(TextChoices):
        TRADITIONAL = 'Traditional', 'Traditional'
        ACADEMIC = 'Academic', 'Academic'
        HONORS = 'Honors', 'Honors'
        ADVANCED = 'Advanced', 'Advanced'
        ADVANCED_PLACEMENT = 'AP', 'AP'

    class Term(TextChoices):
        SEMESTER = 'Semester', 'Semester'
        SUMMER = 'Summer', 'Summer'
        YEAR = 'Full Year', 'Full Year'

    class YearInSchool(TextChoices):
        FRESHMAN = 'Freshman', 'Freshman'
        SOPHOMORE = 'Sophomore', 'Sophomore'
        JUNIOR = 'Junior', 'Junior'
        SENIOR = 'Senior', 'Senior'

    school = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name="Name of Institution", blank=True)
    name = models.CharField(max_length=100)
    grade_level = models.CharField(verbose_name="Grade Level", max_length=9, choices=YearInSchool.choices, blank=False)
    subject = models.CharField(verbose_name="Subject", max_length=1, choices=Subject.choices, blank=True)
    course_number = models.IntegerField(verbose_name="Course Number", blank=True)
    section = models.IntegerField(verbose_name="Section", blank=True, default='001')
    track = models.CharField(verbose_name="Course Track", max_length=18, choices=Track.choices, blank=True)
    clep_exam = models.BooleanField(verbose_name="College-Level Examination Program®", default=False)
    registered = models.BooleanField(default=False)
    grade_percentage = models.PositiveSmallIntegerField(verbose_name="Raw Course Grade Percentage", null=True,
                                                        blank=True)
    term = models.CharField(verbose_name="Class Weight", max_length=12, choices=Term.choices, blank=True)
    instructor = models.ManyToManyField(Instructor, verbose_name="Course Teacher", blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['school', 'grade_level', 'subject', 'track', 'name']
        verbose_name = "Graduation Credit"
        verbose_name_plural = "Graduation Credits"

    def __str__(self):
        return (f"{self.term} of {self.track} {self.grade_level} {self.name} - Course GPA:"
                f" {self.weighted_gpa} - Academic Credit(s): {self.class_weight}")

    def get_absolute_url(self):
        return reverse('credit-detail', kwargs={'pk': self.pk})

    @property
    def unweighted_gpa(grade_percentage):
        unweighted_gpa = 0.0
        unweighted_gpa += min((grade_percentage - 50) / 10, 4.0)

        return unweighted_gpa

    @property
    def weighted_gpa(self):
        weighted_gpa = 0.0
        unweighted_gpa = 0.0

        if self.track == "Traditional":
            weighted_gpa += 0 + unweighted_gpa
        elif self.track == "Academic":
            weighted_gpa += 0.8 + unweighted_gpa
        elif self.track == "Honors":
            weighted_gpa += 1.2 + unweighted_gpa
        elif self.track == "Advanced":
            weighted_gpa += 1.6 + unweighted_gpa
        elif self.track == "AP":
            weighted_gpa += 2.0 + unweighted_gpa

        if self.grade_percentage:
            weighted_gpa += min((self.grade_percentage - 50) / 10, 4.0)

        return weighted_gpa

    @property
    def class_weight(self):
        if self.term in ["Semester", "Summer"]:
            return 0.5
        elif self.term == "Full Year":
            return 1.0
        else:
            return 0.0

    @property
    def grade_equivalence(self):
        weighted_gpa = self.weighted_gpa
        if weighted_gpa >= 4 + (1 / 3):
            return 'A+'
        elif weighted_gpa >= 4:
            return 'A'
        elif weighted_gpa >= 3 + (2 / 3):
            return 'A-'
        elif weighted_gpa >= 3 + (1 / 3):
            return 'B+'
        elif weighted_gpa >= 3:
            return 'B'
        elif weighted_gpa >= 2 + (2 / 3):
            return 'B-'
        elif weighted_gpa >= 2 + (1 / 3):
            return 'C+'
        elif weighted_gpa >= 2:
            return 'C'
        elif weighted_gpa >= 1 + (2 / 3):
            return 'C-'
        elif weighted_gpa >= 1 + (1 / 3):
            return 'D+'
        elif weighted_gpa >= 1:
            return 'D'
        else:
            return 'F'
