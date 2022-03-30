from django import forms
from address.forms import AddressField


class EducationForm(forms.Form):
    location = AddressField()
