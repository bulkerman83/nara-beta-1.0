# Generated by Django 4.2.10 on 2024-02-19 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0004_auto_20240216_1443"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="profile_image",
        ),
    ]
