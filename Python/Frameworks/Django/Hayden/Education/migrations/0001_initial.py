# Generated by Django 3.0.3 on 2020-05-21 23:01

import address.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0002_auto_20160213_1726'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=250)),
                ('next_year_full_tuition', models.DecimalField(decimal_places=2, max_digits=7)),
                ('headmaster', models.CharField(max_length=250)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('fax_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('director_of_admissions', models.CharField(max_length=250)),
                ('application_received', models.BooleanField()),
                ('teacher_recommendations_requested', models.BooleanField()),
                ('application_submitted', models.BooleanField()),
                ('teacher_recommendations_submitted', models.BooleanField()),
                ('financial_aid_requested', models.BooleanField()),
                ('financial_aid_awarded', models.DecimalField(decimal_places=2, max_digits=7)),
                ('description', models.TextField(max_length=10000, null=True)),
                ('address', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, to='address.Address')),
            ],
            options={
                'verbose_name': 'Middle School',
                'verbose_name_plural': 'Middle Schools',
            },
        ),
        migrations.CreateModel(
            name='Credits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_level', models.CharField(choices=[('6G', '6th Grade'), ('7G', '7th Grade'), ('8G', '8th Grade'), ('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate School')], max_length=2)),
                ('subject', models.CharField(max_length=50)),
                ('class_name', models.CharField(max_length=100)),
                ('required_exam', models.CharField(blank=True, choices=[('AP', 'Advanced Placement'), ('CL', 'College Level Examination Program'), ('CO', 'Taken @ College')], max_length=2)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Education.School')),
            ],
        ),
    ]
