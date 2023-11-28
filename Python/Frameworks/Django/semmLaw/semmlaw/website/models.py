from address.models import AddressField
from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from .services import validate_academic_institution


class Education(models.Model):
    academic_institution_name = models.CharField(verbose_name="Name of the Academic Institution", max_length=255)
    address = AddressField(null=True)


class Attorney(models.Model):
    # Bio. Information
    first_name = models.CharField(verbose_name="Lawyer's First Name", max_length=255)
    last_name = models.CharField(verbose_name="Lawyer's Last Name", max_length=255)

    # Contact Information
    phone_number = PhoneNumberField(verbose_name="Work Phone Number", blank=True)
    fax_number = PhoneNumberField(verbose_name="Work Fax Number", blank=True)

    # Academics
    academic_institution_details = validate_academic_institution(request="academic_institution_details")
    degree = models.CharField(verbose_name="Degree", max_length=255, blank=True, null=True)
    graduated_with_honors = models.BooleanField(verbose_name="Graduated with Honors", blank=True, null=True)
    graduation_year = models.PositiveSmallIntegerField(verbose_name="Year of Graduation", blank=True, null=True)

    # Other
    image = models.ImageField(verbose_name="Picture of Attorney", blank=True)
    slug = models.SlugField(max_length=255, unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.first_name, self.last_name)
        super(Attorney, self).save(*args, **kwargs)


class Newsfeed(models.Model):
    news = models.TextField()
