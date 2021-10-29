# Generated by Django 3.2.7 on 2021-10-27 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckTakeIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('take_in', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CheckTakeOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('take_out', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TakeOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('take_out_no', models.CharField(max_length=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('code', models.CharField(max_length=100)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('unit', models.CharField(max_length=5)),
                ('price', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('take_out', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iob_demo.checktakeout')),
            ],
            options={
                'unique_together': {('client', 'code', 'date')},
            },
        ),
        migrations.CreateModel(
            name='TakeIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('invoice_no', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=100)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('unit', models.CharField(max_length=5)),
                ('price', models.IntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('cd_no', models.CharField(blank=True, max_length=50, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('take_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iob_demo.checktakein')),
            ],
            options={
                'unique_together': {('client', 'code', 'date')},
            },
        ),
    ]