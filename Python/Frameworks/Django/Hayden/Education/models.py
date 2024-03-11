"""
File: models.py
Author: Gavin Schilling

This file defines the Credit, Institution, Instructor models for the Django project.
"""

from django.db import models
from django.db.models import TextChoices
from django.core.validators import EmailValidator, MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField
from address.models import AddressField


class School(models.Model):
    """
    A model representing an educational institution.

    Attributes:
        name (str): The name of the institution.
        next_year_full_tuition (djmoney.models.fields.MoneyField): The full tuition for the next school year.
        registration_fee (djmoney.models.fields.MoneyField): The registration fee for new students.
        student_activity_fee (djmoney.models.fields.MoneyField): The fee for student activities.
        headmaster (str): The name of the headmaster.
        address (address.models.AddressField): The address of the institution.
        phone_number (phonenumber_field.modelfields.PhoneNumberField): The main phone number of the institution.
        fax_number (phonenumber_field.modelfields.PhoneNumberField): The main fax number of the institution.
        admissions_director (str): The name of the admissions director.
        website (str): The website of the institution.
        application_received (bool): A boolean indicating whether the application has been received.
        application_submitted (bool): A boolean indicating whether the application has been submitted.
        toured (bool): A boolean indicating whether the campus has been toured.
        teacher_recommendations_requested (bool): A boolean indicating whether teacher recommendations have been requested.
        teacher_recommendations_submitted (bool): A boolean indicating whether teacher recommendations have been submitted.
        accepted (bool): A boolean indicating whether the institution has been accepted.
        financial_aid_requested (bool): A boolean indicating whether financial aid has been requested.
        financial_aid_awarded (djmoney.models.fields.MoneyField): The amount of financial aid awarded.
        description (str): A description of the institution.
        slug (str): A unique slug for the institution.
    """

    name = models.CharField(verbose_name="Name of the School", max_length=255, unique=True)
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
    financial_aid_awarded = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    description = models.TextField(max_length=10000, blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Educational Institution"
        verbose_name_plural = "Educational Institutions"
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def net_cost(self):
        return self.next_year_full_tuition - self.financial_aid_awarded



class Instructor(models.Model):
    """
    A model representing a teaching instructor.

    Attributes:
        first_name (str): The instructor's first name.
        last_name (str): The instructor's last name.
        email (str): The instructor's email address.
        phone (str): The instructor's phone number.
        title (str): The instructor's professional role title.
        slug (str): A unique slug for the instructor.

    Methods:
        __str__(self): Returns the instructor's full name.

    """

    first_name = models.CharField(verbose_name="Instructor's First Name", max_length=255, blank=True)
    last_name = models.CharField(verbose_name="Instructor's Last Name", max_length=255, blank=True)
    email = models.EmailField(verbose_name="Instructor's Email Address", blank=True, validators=[EmailValidator])
    phone = PhoneNumberField(verbose_name="Instructor's Telephone Number", blank=True)

    TITLE_CHOICES = [
        ('Academic Advisor', 'Academic Advisor'),
        ('Academic Dean', 'Academic Dean'),
        ('Class Instructor', 'Class Instructor'),
        ('College Counselor', 'College Counselor'),
        ('Faculty Sponsor', 'Faculty Sponsor'),
        ('Learning Support Coordinator', 'Learning Support Coordinator'),
        ('Life Mentor', 'Life Mentor'),
        ('School Nurse', 'School Nurse'),
        ('Personal/Academic Counselor', 'Personal/Academic Counselor'),
    ]

    title = models.CharField(verbose_name="Professional Role Title", max_length=28, choices=TITLE_CHOICES, blank=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Teaching Instructor"
        verbose_name_plural = "Teaching Instructors"
        ordering = ['last_name', 'first_name']


class Credit(models.Model):
    """
    A model representing a graduation credit.

    Attributes:
        school (School): The institution that offers the credit.
        name (str): The name of the credit.
        grade_level (str): The grade level of the credit.
        subject (str): The subject of the credit.
        course_number (int): The course number of the credit.
        section (int): The section of the credit.
        track (str): The track of the credit.
        clep_exam (bool): A boolean indicating whether the credit is a CLEP exam.
        registered (bool): A boolean indicating whether the credit is registered.
        undertaking (bool): A boolean indicating whether the credit is undertaking.
        grade_percentage (int): The raw course grade percentage.
        term (str): The term of the credit.
        instructor (list): A list of instructors for the credit.
        slug (str): A unique slug for the credit.

    Methods:
        __str__(self): Returns the name of the credit.
        unweighted_gpa(grade_percentage): Returns the unweighted GPA.
        weighted_gpa(self): Returns the weighted GPA.
        class_weight(self): Returns the class weight.
        grade_equivalence(self): Returns the grade equivalence.

    """

    GRADE_LEVEL_CHOICES = [
        ('Freshman', 'Freshman'),
        ('Sophomore', 'Sophomore'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
    ]

    TERM_CHOICES = [
        ('Semester', 'Semester'),
        ('Summer', 'Summer'),
        ('Full Year', 'Full Year'),
    ]

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

    TRACK_CHOICES = [
        ('Traditional', 'Traditional'),
        ('Academic', 'Academic'),
        ('Honors', 'Honors'),
        ('Advanced', 'Advanced'),
        ('Advanced Placement', 'AP'),
    ]


    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="Name of Institution", blank=True)
    name = models.CharField(max_length=100)
    grade_level = models.CharField(verbose_name="Grade Level", max_length=9, choices=GRADE_LEVEL_CHOICES, blank=False)
    subject = models.CharField(verbose_name="Subject", max_length=1, choices=Subject.choices, blank=True)
    course_number = models.IntegerField(verbose_name="Course Number", blank=True)
    section = models.IntegerField(verbose_name="Section", blank=True, default='001')
    track = models.CharField(verbose_name="Course Track", max_length=18, choices=TRACK_CHOICES, blank=True)
    undertaking = models.BooleanField(verbose_name="Course Undertaking", default=False)
    clep_exam = models.BooleanField(verbose_name="College-Level Examination Program®", default=False)
    registered = models.BooleanField(default=False)
    grade_percentage = models.PositiveSmallIntegerField(verbose_name="Raw Course Grade Percentage", null=True,
                                                        blank=True)
    term = models.CharField(verbose_name="Class Weight", max_length=12, choices=TERM_CHOICES, blank=True)
    instructor = models.ManyToManyField(Instructor, verbose_name="Course Teacher(s)", blank=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['school', 'grade_level', 'subject', 'track', 'name']
        verbose_name = "Graduation Credit"
        verbose_name_plural = "Graduation Credits"

    def __str__(self):
        return (f"{self.term} of {self.track} {self.grade_level} {self.name} - Course GPA:"
                f" {self.weighted_gpa} - Academic Credit(s): {self.class_weight}")

    @property
    def unweighted_gpa(self):
        if self.grade_percentage is not None:
            unweighted_gpa_table = {
                100.00: 4.00,
                99.00: 4.00,
                98.00: 4.00,
                97.00: 4.00,
                96.00: 4.00,
                95.00: 4.00,
                94.00: 4.00,
                93.00: 4.00,
                92.00: 4.00,
                91.00: 4.00,
                90.00: 4.00,
                89.00: 3.90,
                88.00: 3.80,
                87.00: 3.70,
                86.00: 3.50,
                85.00: 3.40,
                84.00: 3.30,
                83.00: 3.00,
                82.00: 2.90,
                81.00: 2.80,
                80.00: 2.70,
                79.00: 2.50,
                78.00: 2.40,
                77.00: 2.30,
                76.00: 2.10,
                75.00: 1.90,
                74.00: 1.80,
                73.00: 1.70,
                72.00: 1.50,
                71.00: 1.40,
                70.00: 1.30,
                69.00: 0.00,
            }
            return max(min(unweighted_gpa_table.get(self.grade_percentage, 0.0), 4.0), 0.0)
        return None  # or raise an exception, depending on your desired behavior

    @property
    def weighted_gpa(self):
        if self.grade_percentage is not None:
            unweighted_gpa = self.unweighted_gpa
            track_weights = {
                "Traditional": 0,
                "Academic": 0.8,
                "Honors": 1.2,
                "Advanced": 1.6,
                "AP": 2.0
            }
            weighted_gpa = unweighted_gpa + track_weights.get(self.track, 0)
            return max(min(weighted_gpa, 5.0), 0.0)
        # return None  # or raise an exception, depending on your desired behavior

    @property
    def class_weight(self):
        """
        Returns the class weight.

        Returns:
            float: The class weight.

        """

        if self.term in ["Semester", "Summer"]:
            return 0.5
        elif self.term == "Full Year":
            return 1.0
        else:
            return 0.0

    @property
    def unweighted_grade_equivalence(self):
        """
        Returns the unweighted grade equivalence.

        Returns:
            str: The unweighted grade equivalence.

        """
        if self.grade_percentage is not None:
            unweighted_gpa_table = {
                100.00: 'A+',
                99.00: 'A+',
                98.00: 'A+',
                97.00: 'A+',
                96.00: 'A+',
                95.00: 'A+',
                94.00: 'A',
                93.00: 'A',
                92.00: 'A',
                91.00: 'A',
                90.00: 'A',
                89.00: 'A-',
                88.00: 'A-',
                87.00: 'A-',
                86.00: 'B+',
                85.00: 'B+',
                84.00: 'B+',
                83.00: 'B',
                82.00: 'B-',
                81.00: 'B-',
                80.00: 'B-',
                79.00: 'C+',
                78.00: 'C+',
                77.00: 'C+',
                76.00: 'C',
                75.00: 'C-',
                74.00: 'C-',
                73.00: 'C-',
                72.00: 'D+',
                71.00: 'D+',
                70.00: 'D+',
                69.00: 'F',
            }
            return unweighted_gpa_table.get(self.grade_percentage, 'F')
        return None  # or raise an exception, depending on your desired behavior

    @property
    def weighted_grade_equivalence(self):
        """
        Returns the weighted grade equivalence.

        Returns:
            str: The weighted grade equivalence.

        """
        if self.grade_percentage is not None:
            weighted_gpa = self.weighted_gpa
            # Grade equivalences based on weighted GPA
            if weighted_gpa >= 4.3:
                return 'A+'
            elif weighted_gpa >= 4:
                return 'A'
            elif weighted_gpa >= 3.7:
                return 'A-'
            elif weighted_gpa >= 3.3:
                return 'B+'
            elif weighted_gpa >= 3:
                return 'B'
            elif weighted_gpa >= 2.7:
                return 'B-'
            elif weighted_gpa >= 2.3:
                return 'C+'
            elif weighted_gpa >= 2:
                return 'C'
            elif weighted_gpa >= 1.7:
                return 'C-'
            elif weighted_gpa >= 1.3:
                return 'D+'
            else:
                return 'F'
        return None  # or raise an exception, depending on your desired behavior




class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Major(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student} - {self.credit} - {self.grade}"


class Degree(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    graduation_date = models.DateField()

    def __str__(self):
        return f"{self.student} - {self.major} - {self.graduation_date}"


class Transcript(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.CharField(max_length=255)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student} - {self.course} - {self.grade}"
