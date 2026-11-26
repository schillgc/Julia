"""Remove the invalid field-object slug default without touching existing rows."""
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Analyst", "0003_alter_job_rate_per_hour_currency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]
