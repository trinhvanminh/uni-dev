# Generated by Django 3.2.7 on 2021-10-28 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iob_demo', '0005_auto_20211028_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iob',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
