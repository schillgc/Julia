from address.models import Locality, State
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.text import slugify
from djmoney.models.fields import MoneyField
from phone_field import PhoneField


class Benefit(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    amount = MoneyField(max_digits=5, decimal_places=0, default_currency='USD', blank=True, null=True)

    def __str__(self):
        return f"{ self.name }"


class Company(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    industry = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to="upload/")
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{ self.name }"

    class Meta:
        verbose_name_plural = "companies"
        ordering = ['name']


class Recruiter(models.Model):
    first_name = models.CharField(verbose_name="Recruiter's First Name", max_length=200)
    last_name = models.CharField(verbose_name="Recruiter's Last Name", max_length=200, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Recruiter's Professional Title", max_length=200, blank=True, null=True)
    phone_number = PhoneField(verbose_name="Recruiter's Phone Number", blank=True, null=True)
    email_address = models.EmailField(verbose_name="Recruiter's Email Address", blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} { self.last_name }"

    class Meta:
        ordering = ['last_name', 'first_name']


class Position(models.Model):
    title = models.CharField(verbose_name="Position Title", max_length=200)
    pay = MoneyField(max_digits=6, decimal_places=0, default_currency='USD', blank=True, null=True)

    MONTHLY = '1-month'
    BI_MONTHLY = '2-months'
    QUARTERLY = '3-months'
    TRIMESTER = '4-months'
    FIVE_MONTHS = '5-months'
    SEMI_ANNUALLY = '6-months'
    SEVEN_MONTHS = '7-months'
    BI_TRIMESTER = '8-months'
    GESTATIONAL = '9-months'
    TEN_MONTHS = '10-months'
    ELEVEN_MONTHS = '11-months'
    ANNUALLY = '12-months'
    DURATION = [
        (MONTHLY, 'occurring on a Monthly basis'),
        (BI_MONTHLY, 'occurring on a Bi-Monthly basis'),
        (QUARTERLY, 'occurring on a Quarterly basis'),
        (TRIMESTER, 'occurring on a Annual Trimester basis'),
        (FIVE_MONTHS, 'occurring on a 5-Month duration period'),
        (SEMI_ANNUALLY, 'occurring on a Semi-Annual basis'),
        (SEVEN_MONTHS, 'occurring on a 7-Month duration period'),
        (BI_TRIMESTER, 'occurring on a Bi-Trimester basis'),
        (GESTATIONAL, 'occurring on a Gestational term basis'),
        (TEN_MONTHS, 'occurring on a 10-Month duration period'),
        (ELEVEN_MONTHS, 'occurring on an 11-Month duration period'),
        (ANNUALLY, 'occurring on an Annual basis'),
    ]
    duration = models.CharField(
        max_length=40,
        choices=DURATION,
        default=ANNUALLY,
        blank=True,
        null=True,
    )

    W2 = 'Employee Wages (W-2)'
    CONTRACT = 'Contract'
    C2H = 'Contract-to-Hire'
    C2C = 'Corp-to-Corp'
    CLASSIFICATION = [
        (W2, 'Employee Wages (W-2)'),
        (CONTRACT, 'Contract'),
        (C2H, 'Contract-to-Hire'),
        (C2C, 'Corp-to-Corp')
    ]
    classification = models.CharField(
        max_length=20,
        choices=CLASSIFICATION,
        default=W2,
        blank=True,
        null=True,
    )

    remote = models.BooleanField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    benefit = models.ManyToManyField(Benefit, blank=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, blank=True, null=True)
    city = Locality.name
    state = State.code
    slug = models.SlugField(unique=True)

    active = models.BooleanField(default=True)
    applied = models.BooleanField(default=False)
    interviewed = models.BooleanField(default=False)
    start_date = models.DateField(verbose_name="Start Date", blank=True, null=True)

    def __str__(self):
        return f"{ self.title } @ { self.company }"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + self.company)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['pay']
