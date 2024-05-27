from django.db import models
from djmoney.models.fields import MoneyField


DEGREE_CHOICES = (
  ("Minimum Age", "Minimum Age"),
  ("High School Diploma", "High School Diploma"),
  ("Associate's Degree", "Associate's Degree"),
  ("Bachelor's Degree", "Bachelor's Degree"),
  ("Master's of Business Administration", "Master's of Business Administration"),
  ("Doctor of Jurisprudence", "Doctor of Jurisprudence"),
  ("Master of Laws", "Master of Laws"),
  ("Doctor of Medicine", "Doctor of Medicine"),
  ("Doctor of Philosophy", "Doctor of Philosophy"),
  ("Fellowship", "Fellowship")
)


class Career(models.Model):
    profession = models.CharField(max_length=250)

    average_salary = MoneyField(
        max_digits=6,
        decimal_places=0,
        default_currency='USD'
    )

    required_education = models.CharField(
        max_length=35,
        choices=DEGREE_CHOICES,
        blank=True
    )

    def __str__(self):
        return self.profession

    class Meta:
        ordering = ["required_education", "average_salary", "profession"]
