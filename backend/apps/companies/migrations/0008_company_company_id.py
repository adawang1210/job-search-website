# Generated by Django 5.0.2 on 2025-05-23 11:16

from django.db import migrations, models
from django.utils.text import slugify
import uuid

def generate_company_ids(apps, schema_editor):
    Company = apps.get_model('companies', 'Company')
    for company in Company.objects.all():
        base_slug = slugify(company.name, allow_unicode=True)
        unique_id = str(uuid.uuid4())[:8]
        company.company_id = f"{base_slug}-{unique_id}"
        company.save()

class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0007_alter_companymedia_logo_alter_companyphoto_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="company_id",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.RunPython(generate_company_ids),
        migrations.AlterField(
            model_name="company",
            name="company_id",
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
