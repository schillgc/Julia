from address.models import AddressField
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
    )

    phone = PhoneNumberField(
        verbose_name="Instructor's Telephone Number",
        blank=True,
    )

    def __str__(self):
        return self.last_name + ", " + self.first_name

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
        FRESHMAN = 'FRESHMAN', 'Freshman'
        SOPHOMORE = 'SOPHOMORE', 'Sophomore'
        JUNIOR = 'JUNIOR', 'Junior'
        SENIOR = 'SENIOR', 'Senior'

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
        TRADITIONAL = 'TRADITIONAL', 'Traditional'
        ACADEMIC = 'ACADEMIC', 'Academic'
        HONORS = 'HONORS', 'Honors'
        ADVANCED = 'ADVANCED', 'Advanced'
        ADVANCED_PLACEMENT = 'ADVANCED_PLACEMENT', 'AP'

    track = models.CharField(
        verbose_name="Course Track",
        max_length=18,
        choices=Track.choices,
        blank=True,
    )

    clep_exam = models.BooleanField(verbose_name="College-Level Examination Program®", default=False)

    registered = models.BooleanField(default=False)

    class LetterGrade(TextChoices):
        A_PLUS = 'A_PLUS', 'A+'
        A = 'A', 'A'
        A_MINUS = 'A_MINUS', 'A-'
        B_PLUS = 'B_PLUS', 'B+'
        B = 'B', 'B'
        B_MINUS = 'B_MINUS', 'B-'
        C_PLUS = 'C_PLUS', 'C+'
        C = 'C', 'C'
        C_MINUS = 'C_MINUS', 'C-'
        D_PLUS = 'D_PLUS', 'D+'
        D = 'D', 'D'
        D_MINUS = 'D_MINUS', 'D-'
        F = 'F', 'F'

    letter_grade = models.CharField(
        verbose_name="Letter Grade",
        max_length=7,
        choices=LetterGrade.choices,
        blank=True,
    )

    class Term(TextChoices):
        SEMESTER = 'SEMESTER', 'Semester'
        SUMMER = 'SUMMER', 'Summer'
        YEAR = 'YEAR', 'Full Year'

    term = models.CharField(
        verbose_name="Class Weight",
        max_length=9,
        choices=Term.choices,
        blank=True,
    )

    teacher = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        verbose_name="Course Teacher",
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
            if self.letter_grade == "A+":
                class_gpa += (4 + (1 / 3))
            elif self.letter_grade == "A":
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

    @property
    def class_weight(self):
        global class_weight
        if self.term:
            if self.term == "Semester" or Credit.term == "Summer":
                class_weight = 0.5
            elif self.term == "Full Year":
                class_weight = 1
        return class_weight
