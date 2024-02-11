# Generated by Django 5.0.1 on 2024-01-29 21:33

import address.models
import django.core.validators
import django.db.models.deletion
import djmoney.models.fields
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0003_auto_20200830_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name="Instructor's First Name")),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name="Instructor's Last Name")),
                ('email', models.EmailField(blank=True, max_length=254, validators=[django.core.validators.EmailValidator], verbose_name="Instructor's Email Address")),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name="Instructor's Telephone Number")),
                ('title', models.CharField(choices=[('Advisor', 'Academic Advisor'), ('Counselor', 'School Counselor'), ('Mentor', 'Life Mentor'), ('Nurse', 'School Nurse'), ('Sponsor', 'Club Faculty Sponsor'), ('Teacher', 'Class Instructor')], max_length=20, verbose_name='Professional Role Title')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Teaching Instructor',
                'verbose_name_plural': 'Teaching Instructors',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Education.department')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name of the School')),
                ('next_year_full_tuition_currency', djmoney.models.fields.CurrencyField(choices=[('CAN', 'Canadian Dollars'), ('EUR', 'Euros'), ('USD', 'US Dollars')], default='USD', editable=False, max_length=3)),
                ('next_year_full_tuition', djmoney.models.fields.MoneyField(decimal_places=0, max_digits=7)),
                ('registration_fee_currency', djmoney.models.fields.CurrencyField(choices=[('CAN', 'Canadian Dollars'), ('EUR', 'Euros'), ('USD', 'US Dollars')], default='USD', editable=False, max_length=3)),
                ('registration_fee', djmoney.models.fields.MoneyField(decimal_places=0, max_digits=3)),
                ('student_activity_fee_currency', djmoney.models.fields.CurrencyField(choices=[('CAN', 'Canadian Dollars'), ('EUR', 'Euros'), ('USD', 'US Dollars')], default='USD', editable=False, max_length=3)),
                ('student_activity_fee', djmoney.models.fields.MoneyField(decimal_places=0, max_digits=3)),
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
                ('financial_aid_awarded', djmoney.models.fields.MoneyField(decimal_places=2, max_digits=10)),
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
                ('track', models.CharField(blank=True, choices=[('Traditional', 'Traditional'), ('Academic', 'Academic'), ('Honors', 'Honors'), ('Advanced', 'Advanced'), ('Advanced Placement', 'AP')], max_length=18, verbose_name='Course Track')),
                ('undertaking', models.BooleanField(default=False, verbose_name='Course Undertaking')),
                ('clep_exam', models.BooleanField(default=False, verbose_name='College-Level Examination Program®')),
                ('registered', models.BooleanField(default=False)),
                ('grade_percentage', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Raw Course Grade Percentage')),
                ('term', models.CharField(blank=True, choices=[('Semester', 'Semester'), ('Summer', 'Summer'), ('Full Year', 'Full Year')], max_length=12, verbose_name='Class Weight')),
                ('slug', models.SlugField(unique=True)),
                ('instructor', models.ManyToManyField(blank=True, to='Education.instructor', verbose_name='Course Teacher(s)')),
                ('school', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Education.school', verbose_name='Name of Institution')),
            ],
            options={
                'verbose_name': 'Graduation Credit',
                'verbose_name_plural': 'Graduation Credits',
                'ordering': ['school', 'grade_level', 'subject', 'track', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Education.major')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Education.school')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.CharField(max_length=2)),
                ('credit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Education.credit')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Education.student')),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('graduation_date', models.DateField()),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Education.major')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Education.student')),
            ],
        ),
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=255)),
                ('grade', models.CharField(max_length=2)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Education.student')),
            ],
        ),
    ]
