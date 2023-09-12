import django_filters
from django import forms

from .models import Credit


class CreditFilter(django_filters.FilterSet):

    category = django_filters.ModelChoiceField(
        queryset=Credit.objects.all(),
        empty_label="All Credits",
        label="Credits",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Credit
        fields = ['class_weight', 'grade_level', 'school']
