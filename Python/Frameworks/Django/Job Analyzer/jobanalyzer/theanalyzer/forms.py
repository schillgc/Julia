from django import forms

from .models import Benefit, Company, Position, Recruiter


class BenefitForm(forms.ModelForm):
    class Meta:
        model = Benefit
        fields = ['name', 'amount']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'industry', 'logo', 'website']


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class PositionForm(forms.ModelForm):
    model = Position
    fields = ['title', 'pay', 'duration', 'classification', 'remote', 'company', 'benefit', 'recruiter', 'city',
              'state', 'active', 'applied', 'interviewed', 'start_date', 'slug']


class RecruiterForm(forms.ModelForm):
    model = Recruiter
    fields = ['first_name', 'last_name', 'company', 'title', 'phone_number', 'email_address']
