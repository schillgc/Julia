from Analyst.models import Job
from django import template

register = template.Library()


def pay(rate_per_hour, number_of_hours_per_week, number_of_weeks):
    rate_per_hour * number_of_hours_per_week * number_of_weeks
