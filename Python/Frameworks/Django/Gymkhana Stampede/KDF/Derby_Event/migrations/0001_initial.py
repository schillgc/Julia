# Generated by Django 2.0.6 on 2018-06-05 17:26

from django.db import migrations, models
import geoposition.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checkpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', geoposition.fields.GeopositionField(max_length=42)),
                ('photograph', models.ImageField(upload_to='')),
                ('information', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('time', models.DateTimeField()),
                ('location', geoposition.fields.GeopositionField(max_length=42)),
                ('point_value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_total', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email_address', models.EmailField(max_length=254)),
                ('birthday', models.DateField()),
                ('location', geoposition.fields.GeopositionField(max_length=42)),
                ('proof', models.ImageField(upload_to='')),
            ],
        ),
    ]
