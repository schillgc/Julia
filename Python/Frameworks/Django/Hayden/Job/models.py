from django.db import models
from djmoney.models.fields import MoneyField


class Career(models.Model):
    profession = models.CharField(
        verbose_name="Profession",
        max_length=250,
    )

    average_salary = MoneyField(max_digits=6, decimal_places=0, default_currency='USD')

    MINIMUM_AGE = "Minimum Age"
    HIGH_SCHOOL_DIPLOMA = "High School Diploma"
    ASSOCIATES = "Associate's Degree"
    BACHELORS = "Bachelor's Degree"
    MBA = "Master's of Business Administration"
    JD = "Doctor of Jurisprudence"
    LLM = "Master of Laws"
    MD = "Doctor of Medicine"
    PHD = "Doctor of Philosophy"
    FELLOW = "Fellowship"

    DEGREE_CHOICES = [
        (MINIMUM_AGE, "Minimum Age"),
        (HIGH_SCHOOL_DIPLOMA, "High School Diploma"),
        (ASSOCIATES, "Associate's Degree"),
        (BACHELORS, "Bachelor's Degree"),
        (MBA, "Master's of Business Administration"),
        (JD, "Doctor of Jurisprudence"),
        (LLM, "Master of Laws"),
        (MD, "Doctor of Medicine"),
        (PHD, "Doctor of Philosophy"),
        (FELLOW, "Fellowship"),
    ]

    required_education = models.CharField(
        verbose_name="Required Education",
        max_length=35,
        choices=DEGREE_CHOICES,
        blank=False,
    )

    def __str__(self):
        return self.profession

    class Meta:
        ordering = ['required_education', 'average_salary', 'profession']
