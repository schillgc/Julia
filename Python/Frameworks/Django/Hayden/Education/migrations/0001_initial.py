# Generated by Django 4.1.6 on 2023-02-09 14:06

import address.models
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('grade_level', models.CharField(choices=[('6th Grade', '6th Grade'), ('7th Grade', '7th Grade'), ('8th Grade', '8th Grade'), ('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'), ('Junior', 'Junior'), ('Senior', 'Senior'), ('Graduate', 'Graduate School')], max_length=9, verbose_name='Grade Level')),
                ('subject', models.CharField(blank=True, choices=[('Capstone', 'Capstone'), ('Fine Arts', 'Fine Arts'), ('Language Arts', 'Language Arts'), ('Mathematics', 'Mathematics'), ('Outdoor Education', 'Outdoor Education'), ('Physical Education', 'Physical Education'), ('Religion', 'Religious Studies'), ('Science', 'Science'), ('Social Studies', 'Social Studies'), ('Technology', 'Technology'), ('World Languages', 'World Languages')], max_length=18, verbose_name='Subject')),
                ('required_exam', models.CharField(blank=True, choices=[('AP', 'Advanced Placement'), ('CLEP', 'College Level Examination Program'), ('PLTW', 'Project Lead the Way')], max_length=4, verbose_name='Required Exam for College Credit')),
                ('registered', models.BooleanField(default=False)),
                ('raw_score_grade', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5, verbose_name='Raw Class Grade Percentage')),
                ('letter_grade', models.CharField(blank=True, max_length=2, verbose_name='Letter Grade')),
                ('class_weight', models.CharField(blank=True, choices=[('Semester', 0.5), ('Year', 1)], max_length=9, verbose_name='Class Weight')),
                ('course_weighted_grade_point_average', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, verbose_name='Weighted Grade Point Average (GPA)')),
            ],
            options={
                'verbose_name': 'Graduation Credit',
                'verbose_name_plural': 'Graduation Credits',
                'ordering': ['school', 'grade_level', 'subject', 'required_exam', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Name of the School')),
                ('next_year_full_tuition_currency', djmoney.models.fields.CurrencyField(choices=[('CAN', 'Canadian Dollars'), ('EUR', 'Euros'), ('USD', 'US Dollars')], default='USD', editable=False, max_length=3)),
                ('next_year_full_tuition', djmoney.models.fields.MoneyField(decimal_places=0, default_currency='USD', max_digits=7)),
                ('headmaster', models.CharField(max_length=250, verbose_name="Head of School's Name")),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('fax_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('admissions_director', models.CharField(blank=True, max_length=250, verbose_name="Admissions Director's Name")),
                ('website', models.URLField(blank=True)),
                ('application_received', models.BooleanField(default=False)),
                ('application_submitted', models.BooleanField(default=False)),
                ('toured', models.BooleanField(default=False)),
                ('teacher_recommendations_requested', models.BooleanField(default=False)),
                ('teacher_recommendations_submitted', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('financial_aid_requested', models.BooleanField(default=False)),
                ('financial_aid_awarded_currency', djmoney.models.fields.CurrencyField(choices=[('CAN', 'Canadian Dollars'), ('EUR', 'Euros'), ('USD', 'US Dollars')], default='USD', editable=False, max_length=3)),
                ('financial_aid_awarded', djmoney.models.fields.MoneyField(decimal_places=0, default_currency='USD', max_digits=7)),
                ('description', models.TextField(blank=True, default='', max_length=10000)),
                ('address', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, to='address.address', verbose_name="Institution's Address")),
            ],
            options={
                'verbose_name': 'Educational Institution',
                'verbose_name_plural': 'Educational Institutions',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=125, verbose_name="Instructor's First Name")),
                ('last_name', models.CharField(blank=True, max_length=125, verbose_name="Instructor's Last Name")),
                ('email_address_of_instructor', models.EmailField(blank=True, max_length=254, verbose_name="Instructor's Email Address")),
                ('phone_number_of_instructor', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name="Instructor's Telephone Number")),
                ('course', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Education.credit', verbose_name='Name of School Credit')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Education.institution', verbose_name='School Name')),
            ],
            options={
                'verbose_name': 'Teaching Instructor',
                'verbose_name_plural': 'Teaching Instructors',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.AddField(
            model_name='credit',
            name='school',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Education.institution', verbose_name='Name of Institution'),
        ),
    ]
