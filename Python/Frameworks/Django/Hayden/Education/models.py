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
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    ]

    grade_level = models.CharField(
        verbose_name="Grade Level",
        max_length=9,
        choices=YEAR_IN_SCHOOL_CHOICES,
        blank=False,
    )

    ENGLISH = 'English'
    ENRICHMENT = 'Enrichment'
    FINE_ARTS_AND_HUMANITIES = 'Fine Arts & Humanities'
    HEALTH_AND_PHYSICAL_EDUCATION = 'Health & Physical Education'
    MATHEMATICS = 'Mathematics'
    SCIENCE = 'Science'
    SOCIAL_STUDIES = 'Social Studies'
    BUSINESS_AND_TECHNOLOGY = 'Business & Technology'
    THEOLOGY = 'Theology'
    WORLD_LANGUAGES = 'World Languages'

    SUBJECT_CHOICES = [
        (BUSINESS_AND_TECHNOLOGY, 'Business & Technology'),
        (ENGLISH, 'English'),
        (ENRICHMENT, 'Enrichment'),
        (FINE_ARTS_AND_HUMANITIES, 'Fine Arts & Humanities'),
        (MATHEMATICS, 'Mathematics'),
        (HEALTH_AND_PHYSICAL_EDUCATION, 'Health & Physical Education'),
        (SCIENCE, 'Science'),
        (SOCIAL_STUDIES, 'Social Studies'),
        (THEOLOGY, 'Theology'),
        (WORLD_LANGUAGES, 'World Languages'),
    ]

    subject = models.CharField(
        verbose_name="Subject",
        max_length=27,
        choices=SUBJECT_CHOICES,
        blank=True,
    )

    TRADITIONAL = 'Traditional'
    ACADEMIC = 'Academic'
    HONORS = 'Honors'
    ADVANCED = 'Advanced'
    ADVANCED_PLACEMENT = 'AP'

    TRACK_CHOICES = [
        (TRADITIONAL, 'Traditional'),
        (ACADEMIC, 'Academic'),
        (HONORS, 'Honors'),
        (ADVANCED, 'Advanced'),
        (ADVANCED_PLACEMENT, 'AP'),
    ]

    track = models.CharField(
        verbose_name="Course Track",
        max_length=18,
        choices=TRACK_CHOICES,
        blank=True,
    )

    clep_exam = models.BooleanField(verbose_name="College-Level Examination Program®", default=False)

    registered = models.BooleanField(default=False)

    A_PLUS = 'A+'
    A = 'A'
    A_MINUS = 'A-'
    B_PLUS = 'B+'
    B = 'B'
    B_MINUS = 'B-'
    C_PLUS = 'C+'
    C = 'C'
    C_MINUS = 'C-'
    D_PLUS = 'D+'
    D = 'D'
    D_MINUS = 'D-'
    F = 'F'

    LETTER_GRADE_CHOICES = [
        (A_PLUS, 'A+'),
        (A, 'A'),
        (A_MINUS, 'A-'),
        (B_PLUS, 'B+'),
        (B, 'B'),
        (B_MINUS, 'B-'),
        (C_PLUS, 'C+'),
        (C, 'C'),
        (C_MINUS, 'C-'),
        (D_PLUS, 'D+'),
        (D, 'D'),
        (D_MINUS, 'D-'),
        (F, 'F'),
    ]

    letter_grade = models.CharField(
        verbose_name="Letter Grade",
        max_length=7,
        choices=LETTER_GRADE_CHOICES,
        blank=True,
    )

    SEMESTER = 'Semester'
    YEAR = 'Year'

    TERM_CHOICES = [
        (SEMESTER, 'Semester'),
        (YEAR, 'Full-Year'),
    ]

    term = models.CharField(
        verbose_name="Class Weight",
        max_length=9,
        choices=TERM_CHOICES,
        blank=True,
    )

    class Meta:
        ordering = ['school', 'grade_level', 'subject', 'track', 'name']
        verbose_name = "Graduation Credit"
        verbose_name_plural = "Graduation Credits"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('credit-detail', kwargs={'pk': self.pk})

    @property
    def class_gpa(self):
        class_gpa = 0
        if self.track:
            if self.track == "Traditional":
                class_gpa += 0
            elif self.track == "Academic":
                class_gpa += 0.8
            elif self.track == "Honors":
                class_gpa += 1.2
            elif self.track == "Advanced":
                class_gpa += 1.6
            elif self.track == "AP":
                class_gpa += 2
        if self.letter_grade:
            if self.letter_grade == "A+" or self.letter_grade == "A":
                class_gpa += 4
            elif self.letter_grade == "A-":
                class_gpa += (3 + (2 / 3))
            elif self.letter_grade == "B+":
                class_gpa += (3 + (1 / 3))
            elif self.letter_grade == "B":
                class_gpa += 3
            elif self.letter_grade == "B-":
                class_gpa += (2 + (2 / 3))
            elif self.letter_grade == "C+":
                class_gpa += (2 + (1 / 3))
            elif self.letter_grade == "C":
                class_gpa += 2
            elif self.letter_grade == "C-":
                class_gpa += (1 + (2 / 3))
            elif self.letter_grade == "D+":
                class_gpa += (1 + (1 / 3))
            elif self.letter_grade == "D":
                class_gpa += 1
            elif self.letter_grade == "F":
                class_gpa += 0
        return class_gpa


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
