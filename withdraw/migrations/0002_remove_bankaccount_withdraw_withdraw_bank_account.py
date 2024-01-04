# Generated by Django 4.1.1 on 2022-10-02 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('withdraw', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='withdraw',
        ),
        migrations.AddField(
            model_name='withdraw',
            name='bank_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='withdraw.bankaccount'),
        ),
    ]
