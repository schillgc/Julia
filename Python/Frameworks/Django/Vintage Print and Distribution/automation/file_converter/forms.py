from django import forms

from address.forms import AddressField


class DemographicsForm(forms.Form):
    address = AddressField()
