from django.db import models
from django.contrib.auth.models import User

from geoposition.fields import GeopositionField
from localflavor.us.models import USStateField, USZipCodeField
from cities.models import City


class BiographicInformation(models.Model):
    birthday = models.DateField()
    city = City
    date_joined = User.date_joined
    email_address = User.email
    first_name = User.first_name
    groups = User.groups
    is_active = User.is_active
    is_staff = User.is_staff
    is_superuser = User.is_superuser
    last_login = User.last_login
    last_name = User.last_name
    location = GeopositionField()
    password = User.password
    permissions = User.user_permissions
    proof = models.ImageField()
    state = USStateField
    username = User.username
    zip_code = USZipCodeField

    def __str__(self):
        return self.email_address


class Checkpoint(models.Model):
    name = models.CharField(max_length=500)
    location = GeopositionField()
    photograph = models.ImageField()
    information = models.TextField()
    isValid = models.BooleanField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    time = models.DateTimeField()
    location = GeopositionField()
    point_value = models.IntegerField()

    def __str__(self):
        return self.name


class Reward(models.Model):
    point_total = models.IntegerField()

    def __str__(self):
        return self.point_total
