from address.forms import AddressField
from django import forms


class PersonForm(forms.Form):
    address = AddressField()
