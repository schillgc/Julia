from django.db import models


# Create your models here.
class Calendar(models.Model):
    start_date = models.DateField()
    number_of_days = models.SmallIntegerField()
    country_code = models.CharField(max_length=2)
