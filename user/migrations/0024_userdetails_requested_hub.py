# Generated by Django 4.1.1 on 2022-12-21 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_rename_address_useraddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='requested_hub',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
