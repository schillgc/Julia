from django.db import models

from address.models import AddressField


# Create your models here.
class File(models.Model):
    file = models.FileField
    path = models.FilePathField


class Demographics(models.Model):
    address = AddressField()

    CORPORATE = 'corp'
    INDIVIDUAL = 'individual'
    CATEGORIZATION_CHOICES = (
        CORPORATE,
        INDIVIDUAL
    )
    categorization = models.CharField(
        max_length=10,
        choices=CATEGORIZATION_CHOICES,
        default="Please Select"
    )
