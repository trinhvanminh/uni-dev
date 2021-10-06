# Generated by Django 3.2.7 on 2021-09-17 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocksmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='a42',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='b13',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='e21',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='e52',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='ecus',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='fg_stock',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='rm_stock',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='wip_stock',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bom',
            name='finish_product',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='goods_no',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='begin_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='di_sale_issue_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='mr_production_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='oi_unplanned_issue_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='or_unplanned_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pi_issue_production_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pr_purchase_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_transfer_issue_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_transfer_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]