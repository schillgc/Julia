from django.forms import ModelForm, ValidationError
from django.core.validators import EMPTY_VALUES
from .models import Account


class AccountForm(ModelForm):
    class Meta:
        model = Account

    def clean(self):
        is_leased = self.cleaned_data.get('is_leased', False)
        if is_leased:
            monthly_phone_cost = self.cleaned_data.get('monthly_phone_cost', None)
            if monthly_phone_cost in EMPTY_VALUES:
                raise ValidationError(
                    'Monthly phone cost cannot be empty.',
                )
            return self.cleaned_data
