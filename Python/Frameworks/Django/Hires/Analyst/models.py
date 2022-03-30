from address.models import Locality, State
from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from phone_field import PhoneField


def pay(rate_per_hour, number_of_hours_per_week, number_of_weeks):
    rate_per_hour * number_of_hours_per_week * number_of_weeks


class Job(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name="Job Title",
                             blank=True)
    company = models.CharField(max_length=200,
                               verbose_name="Company Name",
                               blank=True)
    slug = models.SlugField(default=str(company) + "_" + str(title),
                            null=True)

    job_sight_city = Locality.name
    job_sight_state = State.code
    remote = models.BooleanField(verbose_name="Remote",
                                 default=False)
    active = models.BooleanField(verbose_name="Actively Seeking This Position",
                                 default=True)
    applied = models.BooleanField(verbose_name="Applied",
                                  default=False)

    ''' Recruiting Information '''
    recruiting_company = models.CharField(max_length=200,
                                          verbose_name="Recruiting Company",
                                          blank=True)
    recruiter = models.CharField(max_length=500,
                                 verbose_name="Recruiter's Name",
                                 blank=True)
    email_of_recruiter = models.EmailField(verbose_name="Recruiter's Email Address",
                                           blank=True)
    phone_number_of_recruiter = PhoneField(blank=True,
                                           help_text="Recruiter's Phone Number")
    screened = models.BooleanField(verbose_name="Screened By Recruiter",
                                   default=False)
    thanked = models.BooleanField(verbose_name="Thanked",
                                  default=False)

    ''' Company Contact Information '''
    company_contact = models.CharField(max_length=500,
                                       verbose_name="Company Contact's Name",
                                       blank=True)
    email_of_contact = models.EmailField(verbose_name="Company Contact's Email Address",
                                         blank=True)
    phone_number_of_contact = PhoneField(blank=True,
                                         help_text="Company Contact's Phone Number")
    interviewed = models.BooleanField(verbose_name="Interviewed",
                                      default=False)
    accepted = models.BooleanField(verbose_name="Accepted",
                                   default=False)

    rate_per_hour = MoneyField(max_digits=5,
                               decimal_places=2,
                               default_currency="USD",
                               verbose_name="Pay Rate / Hour",
                               null=True,
                               blank=True)
    number_of_hours_per_week = models.DecimalField(max_digits=5,
                                                   decimal_places=2,
                                                   verbose_name="# of Hours / Week",
                                                   null=True,
                                                   blank=True)
    number_of_weeks = models.DecimalField(max_digits=4,
                                          decimal_places=2,
                                          verbose_name="# of Weeks",
                                          null=True,
                                          blank=True)

    ''' Research Information '''
    website = models.URLField(verbose_name="Application Website",
                              blank=True)

    def __str__(self):
        if self.title and self.recruiting_company and self.company and self.rate_per_hour:
            return self.title + " @ " + self.company + " via " + self.recruiting_company + " for " + str(
                self.rate_per_hour) + " per hour"
        elif self.title and self.recruiting_company and self.company:
            return self.title + " @ " + self.company + " via " + self.recruiting_company
        elif self.title and self.recruiting_company:
            return self.title + " via " + self.recruiting_company
        elif self.title and self.company:
            return self.title + " @ " + self.company
        else:
            return "Unknown"

    def get_absolute_url(self):
        return reverse('job_detail', kwargs={'slug': self.slug})
