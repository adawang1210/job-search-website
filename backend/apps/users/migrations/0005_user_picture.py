# Generated by Django 5.0.2 on 2025-05-26 09:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_userskill_user_userskillpackage_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="picture",
            field=models.ImageField(
                blank=True, upload_to="profile_pictures/", verbose_name="頭像"
            ),
        ),
    ]
