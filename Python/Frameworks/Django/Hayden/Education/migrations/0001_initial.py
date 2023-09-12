# Generated by Django 4.2.5 on 2023-09-10 21:53

import address.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0003_auto_20200830_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name="Instructor's First Name")),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name="Instructor's Last Name")),
                ('email', models.EmailField(blank=True, max_length=254, validators=[django.core.validators.EmailValidator], verbose_name="Instructor's Email Address")),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name="Instructor's Telephone Number")),
                ('title', models.CharField(choices=[('Academic Advisor', 'Advisor'), ('Mentor', 'Mentor'), ('School Nurse', 'Nurse'), ('Club Faculty Sponsor', 'Sponsor'), ('Class Instructor', 'Teacher')], max_length=20, verbose_name='Professional Role Title')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Teaching Instructor',
                'verbose_name_plural': 'Teaching Instructors',
                'ordering': ['last_name', 'first_name'],
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
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name="School's Main Phone Number")),
                ('fax_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name="School's Main Fax Number")),
                ('admissions_director', models.CharField(blank=True, max_length=250, verbose_name="Admissions Director's Name")),
                ('website', models.URLField(blank=True, verbose_name='School Website')),
                ('application_received', models.BooleanField(default=False)),
                ('application_submitted', models.BooleanField(default=False)),
                ('toured', models.BooleanField(default=False)),
                ('teacher_recommendations_requested', models.BooleanField(default=False)),
                ('teacher_recommendations_submitted', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('financial_aid_requested', models.BooleanField(default=False)),
                ('financial_aid_awarded_currency', djmoney.models.fields.CurrencyField(choices=[('CAN', 'Canadian Dollars'), ('EUR', 'Euros'), ('USD', 'US Dollars')], default='USD', editable=False, max_length=3)),
                ('financial_aid_awarded', djmoney.models.fields.MoneyField(decimal_places=0, default_currency='USD', max_digits=7)),
                ('description', models.TextField(blank=True, max_length=10000)),
                ('slug', models.SlugField(unique=True)),
                ('address', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, to='address.address', verbose_name="Institution's Address")),
            ],
            options={
                'verbose_name': 'Educational Institution',
                'verbose_name_plural': 'Educational Institutions',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('grade_level', models.CharField(choices=[('Freshman', 'Freshman'), ('Sophomore', 'Sophomore'), ('Junior', 'Junior'), ('Senior', 'Senior')], max_length=9, verbose_name='Grade Level')),
                ('subject', models.CharField(blank=True, choices=[('B', 'Business & Technology'), ('E', 'English'), ('Q', 'Enrichment'), ('A', 'Fine Arts & Humanities'), ('M', 'Mathematics'), ('P', 'Health & Physical Education'), ('C', 'Science'), ('T', 'Social Studies'), ('R', 'Theology'), ('H', 'Chinese'), ('F', 'French'), ('G', 'German'), ('S', 'Spanish')], max_length=1, verbose_name='Subject')),
                ('course_number', models.IntegerField(blank=True, verbose_name='Course Number')),
                ('section', models.IntegerField(blank=True, default='001', verbose_name='Section')),
                ('track', models.CharField(blank=True, choices=[('Traditional', 'Traditional'), ('Academic', 'Academic'), ('Honors', 'Honors'), ('Advanced', 'Advanced'), ('AP', 'AP')], max_length=18, verbose_name='Course Track')),
                ('clep_exam', models.BooleanField(default=False, verbose_name='College-Level Examination Program®')),
                ('registered', models.BooleanField(default=False)),
                ('grade_percentage', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Raw Course Grade Percentage')),
                ('term', models.CharField(blank=True, choices=[('1st Semester', '1st Semester'), ('2nd Semester', '2nd Semester'), ('Summer', 'Summer'), ('Full Year', 'Full Year')], max_length=12, verbose_name='Class Weight')),
                ('slug', models.SlugField(unique=True)),
                ('school', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Education.institution', verbose_name='Name of Institution')),
                ('teacher', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Education.instructor', verbose_name='Course Teacher')),
            ],
            options={
                'verbose_name': 'Graduation Credit',
                'verbose_name_plural': 'Graduation Credits',
                'ordering': ['school', 'grade_level', 'subject', 'track', 'name'],
            },
        ),
    ]
