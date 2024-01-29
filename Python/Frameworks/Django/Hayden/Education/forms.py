from address.forms import AddressField
from django import forms

from .models import Credit


class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['school', 'name', 'grade_level', 'subject', 'course_number', 'section', 'track', 'clep_exam',
                  'registered', 'grade_percentage', 'term', 'instructor']


class PersonForm(forms.Form):
    address = AddressField()
