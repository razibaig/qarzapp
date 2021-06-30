# Generated by Django 3.2.4 on 2021-06-30 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qarz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='donation_or_loan',
        ),
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('', 'Transaction type'), ('DONATION', 'DONATION'), ('LOAN', 'LOAN'), ('RETURN', 'RETURN')], default='DONATION', max_length=20),
        ),
    ]
