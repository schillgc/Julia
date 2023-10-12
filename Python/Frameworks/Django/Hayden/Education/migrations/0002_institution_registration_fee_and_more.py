# Generated by Django 4.2.5 on 2023-09-11 00:43

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Education', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='registration_fee',
            field=djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal('100'), default_currency='USD', max_digits=3),
        ),
        migrations.AddField(
            model_name='institution',
            name='registration_fee_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CAN', 'Canadian Dollars'), ('EUR', 'Euros'), ('USD', 'US Dollars')], default='USD', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='institution',
            name='student_activity_fee',
            field=djmoney.models.fields.MoneyField(decimal_places=0, default=Decimal('125'), default_currency='USD', max_digits=3),
        ),
        migrations.AddField(
            model_name='institution',
            name='student_activity_fee_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('CAN', 'Canadian Dollars'), ('EUR', 'Euros'), ('USD', 'US Dollars')], default='USD', editable=False, max_length=3),
        ),
    ]