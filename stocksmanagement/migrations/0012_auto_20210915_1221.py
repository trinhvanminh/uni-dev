# Generated by Django 3.2.7 on 2021-09-15 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocksmanagement', '0011_auto_20210915_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecus',
            name='bill_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='contract_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='registered_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
