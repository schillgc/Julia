# Generated by Django 4.1 on 2022-08-29 11:47

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['make', 'model'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('expires', models.DateTimeField(blank=True, null=True)),
                ('users', models.ManyToManyField(to='biller.user')),
            ],
            options={
                'ordering': ['expires', 'name', 'amount'],
            },
        ),
        migrations.CreateModel(
            name='AdditionalTaxOrFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('users', models.ManyToManyField(to='biller.user')),
            ],
            options={
                'ordering': ['name', 'amount'],
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_insured', models.BooleanField(default=True)),
                ('cost_of_insurance', models.IntegerField(default=0, null=True)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biller.phone')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biller.user')),
            ],
            options={
                'ordering': ['is_active', 'user', 'phone'],
            },
        ),
    ]