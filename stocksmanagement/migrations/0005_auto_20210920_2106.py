# Generated by Django 3.2.7 on 2021-09-20 21:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocksmanagement', '0004_alter_ecus_registered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='a42',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='b13',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='e21',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='e52',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='ecus',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='fg_stock',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='rm_stock',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='balance',
            name='wip_stock',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bom',
            name='bom',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bom',
            name='finish_product',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bom',
            name='finish_product_convert',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bom',
            name='finish_product_exchange',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bom',
            name='finish_product_inventory',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bom',
            name='loss',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='goods_no',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='nt_value',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='registered_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 9, 20, 21, 6, 44, 244203), null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='tax_cost',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='tax_rate',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='total',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='total_2',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='total_value',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='unit_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='ecus',
            name='unit_price_taxed',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='begin_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='begin_quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='di_sale_issue_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='di_sale_issue_quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='mr_production_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='mr_production_quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='oi_unplanned_issue_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='oi_unplanned_issue_quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='or_unplanned_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='or_unplanned_quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pi_issue_production_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pi_issue_production_quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pr_purchase_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pr_purchase_quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_transfer_issue_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_transfer_issue_quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_transfer_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_transfer_quantity',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
