# Generated by Django 4.1.1 on 2022-10-03 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('referral', '0002_referralreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referrer_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
