# Generated by Django 3.2.7 on 2021-09-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hscode', '0002_auto_20210922_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heading',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subheading',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]