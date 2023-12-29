# filters.py
import django_filters
from django import forms
from .models import Credit

class CreditFilter(django_filters.FilterSet):
    class_weight = django_filters.NumberFilter(
        field_name='class_weight',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Class Weight',
        help_text='Class Weight is Semester, Summer, Full Year',
        error_messages={'invalid': 'Class weight must be either the number 0.5 and 1'},
    )

    grade_level = django_filters.ChoiceFilter(
        choices=Credit.GRADE_LEVEL_CHOICES,  # Assuming GRADE_LEVEL_CHOICES is defined in the Credit model
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Grade Level',
        help_text='Grade Level is Freshman, Sophomore, Junior, or Senior',
    )

    school = django_filters.ModelChoiceFilter(
        queryset=School.objects.all(),  # Assuming School model is related to Credit model
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='School',
        help_text='School is the name of the school that the credit is for.',
    )

    class Meta:
        model = Credit
        fields = []  # No need to specify fields here as they are defined as individual filters above