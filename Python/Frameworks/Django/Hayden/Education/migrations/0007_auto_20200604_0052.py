# Generated by Django 3.0.3 on 2020-06-04 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Education', '0006_auto_20200603_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credit',
            name='subject',
            field=models.CharField(blank=True, choices=[('Capstone', 'Capstone'), ('Fine Arts', 'Fine Arts'), ('Language Arts', 'Language Arts'), ('Mathematics', 'Mathematics'), ('Outdoor Education', 'Outdoor Education'), ('Physical Education', 'Physical Education'), ('Science', 'Science'), ('Social Studies', 'Social Studies'), ('Technology', 'Technology'), ('World Languages', 'World Languages')], max_length=18),
        ),
    ]
