from address.models import AddressField
from django.core.validators import EmailValidator
from django.db import models
from django.db.models import TextChoices
from django.urls import reverse
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField


class Institution(models.Model):
    name = models.CharField(
        verbose_name="Name of the School",
        max_length=250
    )

    next_year_full_tuition = MoneyField(max_digits=7, decimal_places=0, default_currency='USD')
    registration_fee = MoneyField(max_digits=3, decimal_places=0, default_currency='USD')
    student_activity_fee = MoneyField(max_digits=3, decimal_places=0, default_currency='USD')

    headmaster = models.CharField(
        verbose_name="Head of School's Name",
        max_length=250,
    )
    address = AddressField(
        on_delete=models.CASCADE,
        verbose_name="Institution's Address",
    )
    phone_number = PhoneNumberField(
        verbose_name="School's Main Phone Number",
        blank=True,
    )
    fax_number = PhoneNumberField(
        verbose_name="School's Main Fax Number",
        blank=True,
    )

    admissions_director = models.CharField(
        verbose_name="Admissions Director's Name",
        max_length=250,
        blank=True,
    )

    website = models.URLField(
        verbose_name="School Website",
        blank=True,
    )

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
    )

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
    first_name = models.CharField(
        verbose_name="Instructor's First Name",
        blank=True,
        max_length=50,
    )

    last_name = models.CharField(
        verbose_name="Instructor's Last Name",
        blank=True,
        max_length=50,
    )

    email = models.EmailField(
        verbose_name="Instructor's Email Address",
        blank=True,
        validators=[EmailValidator],
    )

    phone = PhoneNumberField(
        verbose_name="Instructor's Telephone Number",
        blank=True,
    )

    class Title(TextChoices):
        ADVISOR = 'Academic Advisor'
        MENTOR = 'Mentor'
        NURSE = 'School Nurse'
        SPONSOR = 'Club Faculty Sponsor'
        TEACHER = 'Class Instructor'

    title = models.CharField(
        verbose_name="Professional Role Title",
        max_length=20,
        choices=Title.choices,
        blank=False,
    )

    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    class Meta:
        verbose_name = "Teaching Instructor"
        verbose_name_plural = "Teaching Instructors"
        ordering = ['last_name', 'first_name']


class Credit(models.Model):
    school = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        verbose_name="Name of Institution",
        blank=True,
    )

    name = models.CharField(max_length=100)

    class YearInSchool(TextChoices):
        FRESHMAN = 'Freshman', 'Freshman'
        SOPHOMORE = 'Sophomore', 'Sophomore'
        JUNIOR = 'Junior', 'Junior'
        SENIOR = 'Senior', 'Senior'

    grade_level = models.CharField(
        verbose_name="Grade Level",
        max_length=9,
        choices=YearInSchool.choices,
        blank=False,
    )

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

    subject = models.CharField(
        verbose_name="Subject",
        max_length=1,
        choices=Subject.choices,
        blank=True,
    )

    course_number = models.IntegerField(verbose_name="Course Number", blank=True)
    section = models.IntegerField(verbose_name="Section", blank=True, default='001')

    class Track(TextChoices):
        TRADITIONAL = 'Traditional', 'Traditional'
        ACADEMIC = 'Academic', 'Academic'
        HONORS = 'Honors', 'Honors'
        ADVANCED = 'Advanced', 'Advanced'
        ADVANCED_PLACEMENT = 'AP', 'AP'

    track = models.CharField(
        verbose_name="Course Track",
        max_length=18,
        choices=Track.choices,
        blank=True,
    )

    clep_exam = models.BooleanField(verbose_name="College-Level Examination Program®", default=False)

    registered = models.BooleanField(default=False)

    grade_percentage = models.PositiveSmallIntegerField(verbose_name="Raw Course Grade Percentage", null=True,
                                                        blank=True)

    class Term(TextChoices):
        FIRST_SEMESTER = '1st Semester', '1st Semester'
        SECOND_SEMESTER = '2nd Semester', '2nd Semester'
        SUMMER = 'Summer', 'Summer'
        YEAR = 'Full Year', 'Full Year'

    term = models.CharField(
        verbose_name="Class Weight",
        max_length=12,
        choices=Term.choices,
        blank=True,
    )

    teacher = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        verbose_name="Course Teacher",
        blank=True,
    )

    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['school', 'grade_level', 'subject', 'track', 'name']
        verbose_name = "Graduation Credit"
        verbose_name_plural = "Graduation Credits"

    def __str__(self):
        return (f"{self.term} {self.grade_level} {self.track} {self.name} - {self.teacher} - Course GPA:"
                f" {self.class_gpa} - Academic Credit(s): {self.class_weight}")

    def get_absolute_url(self):
        return reverse('credit-detail', kwargs={'pk': self.pk})

    @property
    def class_gpa(self):
        class_gpa = float()

        if self.track:
            if self.track == "Traditional" or self.track == "TRADITIONAL":
                class_gpa += 0
            elif self.track == "Academic" or self.track == "ACADEMIC":
                class_gpa += 0.8
            elif self.track == "Honors" or self.track == "HONORS":
                class_gpa += 1.2
            elif self.track == "Advanced" or self.track == "ADVANCED":
                class_gpa += 1.6
            elif self.track == "AP" or self.track == "ADVANCED_PLACEMENT":
                class_gpa += 2

        if self.grade_percentage:
            if int(self.grade_percentage) >= 90:
                class_gpa += 4.0
            elif int(self.grade_percentage) == 89:
                class_gpa += 3.9
            elif int(self.grade_percentage) == 88:
                class_gpa += 3.8
            elif int(self.grade_percentage) == 87:
                class_gpa += 3.7
            elif int(self.grade_percentage) == 86:
                class_gpa += 3.5
            elif int(self.grade_percentage) == 85:
                class_gpa += 3.4
            elif int(self.grade_percentage) == 84:
                class_gpa += 3.3
            elif int(self.grade_percentage) == 83:
                class_gpa += 3.0
            elif int(self.grade_percentage) == 82:
                class_gpa += 2.9
            elif int(self.grade_percentage) == 81:
                class_gpa += 2.8
            elif int(self.grade_percentage) == 80:
                class_gpa += 2.7
            elif int(self.grade_percentage) == 79:
                class_gpa += 2.5
            elif int(self.grade_percentage) == 78:
                class_gpa += 2.4
            elif int(self.grade_percentage) == 77:
                class_gpa += 2.3
            elif int(self.grade_percentage) == 76:
                class_gpa += 2.1
            elif int(self.grade_percentage) == 75:
                class_gpa += 1.9
            elif int(self.grade_percentage) == 74:
                class_gpa += 1.8
            elif int(self.grade_percentage) == 73:
                class_gpa += 1.7
            elif int(self.grade_percentage) == 72:
                class_gpa += 1.5
            elif int(self.grade_percentage) == 71:
                class_gpa += 1.4
            elif int(self.grade_percentage) == 70:
                class_gpa += 1.3
            elif int(self.grade_percentage) <= 69:
                class_gpa += 0
        return class_gpa

    @property
    def class_weight(self):
        class_weight = float()
        if self.term:
            if (self.term == "1st Semester" or self.term == "FIRST_SEMESTER" or self.term == "2nd Semester" or
                    self.term == "SECOND_TERM" or self.term == "Summer" or self.term == "Spring" or
                    self.term == "SUMMER"):
                class_weight = 0.5
            elif self.term == "Full Year" or self.term == "YEAR":
                class_weight = 1
        return class_weight

    def grade_equivalence(self):
        if self.class_gpa >= 4.33:
            grade_equivalence = 'A+'
        elif self.class_gpa >= 4.00:
            grade_equivalence = 'A'
        elif self.class_gpa >= 3+(2/3):
            grade_equivalence = 'A-'
        elif self.class_gpa >= 3+(1/3):
            grade_equivalence = 'B+'
        elif self.class_gpa >= 3.00:
            grade_equivalence = 'B'
        elif self.class_gpa >= 2+(2/3):
            grade_equivalence = 'B-'
        elif self.class_gpa >= 2+(1/3):
            grade_equivalence = 'C+'
        elif self.class_gpa >= 2.00:
            grade_equivalence = 'C'
        elif self.class_gpa >= 1+(2/3):
            grade_equivalence = 'C-'
        elif self.class_gpa >= 1+(1/3):
            grade_equivalence = 'D+'
        elif self.class_gpa >= 1.00:
            grade_equivalence = 'D'
        else:
            grade_equivalence = 'F'
