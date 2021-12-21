# Generated by Django 3.0.5 on 2020-06-27 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=250, verbose_name='Profession')),
                ('average_salary', models.DecimalField(decimal_places=0, max_digits=6)),
                ('required_education', models.CharField(choices=[('Minimum Age', 'Minimum Age'), ('High School Diploma', 'High School Diploma'), ("Associate's Degree", "Associate's Degree"), ("Bachelor's Degree", "Bachelor's Degree"), ("Master's Degree", "Master's Degree"), ('PhD', 'PhD')], max_length=19, verbose_name='Required Education')),
            ],
        ),
    ]
