from address.forms import AddressField
from django import forms


class EducationForm(forms.Form):
    location = AddressField()
