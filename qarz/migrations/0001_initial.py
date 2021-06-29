# Generated by Django 3.2.4 on 2021-06-29 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QarzUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnic', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.BigIntegerField()),
                ('type', models.CharField(choices=[('', 'Choose user type'), ('DONOR', 'DONOR'), ('LOANER', 'LOANER')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('donation_or_loan', models.BooleanField(default=True)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('qarz_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qarz.qarzuser')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_date', models.DateTimeField(blank=True, null=True)),
                ('total_donated', models.IntegerField(blank=True, null=True)),
                ('total_loan', models.IntegerField(blank=True, null=True)),
                ('remaining_loan', models.IntegerField(blank=True, null=True)),
                ('report_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qarz.qarzuser')),
            ],
        ),
    ]