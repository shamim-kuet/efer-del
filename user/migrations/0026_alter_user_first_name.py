# Generated by Django 4.1.1 on 2023-02-15 05:13

from django.db import migrations
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_alter_ehubpurchaseperson_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=user.models.StrippedCharField(blank=True, max_length=225, null=True),
        ),
    ]
