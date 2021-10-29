# Generated by Django 3.2.7 on 2021-10-28 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iob_demo', '0003_auto_20211027_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='takeout',
            name='item',
        ),
        migrations.RemoveField(
            model_name='iob',
            name='take_in',
        ),
        migrations.RemoveField(
            model_name='iob',
            name='take_out',
        ),
        migrations.AddField(
            model_name='itemstakein',
            name='iob',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='take_ins', to='iob_demo.iob'),
        ),
        migrations.AddField(
            model_name='itemstakein',
            name='take_in',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='itemstakeout',
            name='iob',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='take_outs', to='iob_demo.iob'),
        ),
        migrations.AddField(
            model_name='itemstakeout',
            name='take_out',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='TakeIn',
        ),
        migrations.DeleteModel(
            name='TakeOut',
        ),
    ]