# Generated by Django 4.1.1 on 2022-12-21 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_ehubpurchaseperson_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='hub_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
