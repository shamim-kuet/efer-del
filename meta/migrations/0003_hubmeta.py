# Generated by Django 4.1.1 on 2022-11-16 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0002_address_is_hub'),
    ]

    operations = [
        migrations.CreateModel(
            name='HubMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('three_years_store_price', models.IntegerField(blank=True, null=True)),
                ('four_years_store_price', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
