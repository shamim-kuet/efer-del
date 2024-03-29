# Generated by Django 4.1.1 on 2022-09-28 05:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referral_code', models.CharField(max_length=30)),
                ('referral_discount', models.DecimalField(decimal_places=2, default=10.0, max_digits=7)),
                ('is_percent', models.BooleanField(default=True)),
                ('total_referral', models.IntegerField(default=0)),
                ('total_referral_income', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('purchase_limit_per_user', models.IntegerField(default=3)),
                ('minimum_purchase_per_user', models.DecimalField(decimal_places=2, default=1.0, max_digits=7)),
                ('number_of_referral_confirmed_purchase', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referrer_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReferredPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referred_person_name', models.CharField(max_length=50)),
                ('referred_person_id', models.CharField(max_length=50)),
                ('referred_person_last_order_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('total_purchase_time', models.IntegerField(default=0)),
                ('total_purchase_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('referral', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referral_user', to='referral.referral')),
            ],
        ),
    ]
