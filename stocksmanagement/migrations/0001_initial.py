<<<<<<< HEAD
# Generated by Django 3.2.7 on 2021-10-06 20:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
=======
# Generated by Django 3.2.7 on 2021-09-17 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
>>>>>>> 2a2cb229b4c727c4212802a7b390e8e05b1ecf3b


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, choices=[('Finished Goods(제품)', 'Finished Goods(제품)'), ('Merchandise(상품)', 'Merchandise(상품)'), ('Raw Material(원자재)', 'Raw Material(원자재)'), ('Semi-Finished Goods(반제품)', 'Semi-Finished Goods(반제품)')], max_length=100, null=True)),
                ('item_name', models.CharField(blank=True, max_length=50, null=True)),
                ('ecus_code', models.CharField(blank=True, max_length=50, null=True)),
                ('item_desciption', models.CharField(blank=True, max_length=150, null=True)),
<<<<<<< HEAD
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('begin_quantity', models.FloatField(blank=True, default=0, null=True)),
                ('begin_price', models.FloatField(blank=True, default=0, null=True)),
                ('pr_purchase_quantity', models.FloatField(blank=True, default=0, null=True)),
                ('pr_purchase_price', models.FloatField(blank=True, default=0, null=True)),
                ('mr_production_quantity', models.FloatField(blank=True, default=0, null=True)),
                ('mr_production_price', models.FloatField(blank=True, default=0, null=True)),
                ('or_unplanned_quantity', models.FloatField(blank=True, default=0, null=True)),
                ('or_unplanned_price', models.FloatField(blank=True, default=0, null=True)),
                ('stock_transfer_quantity', models.FloatField(blank=True, default=0, null=True)),
                ('stock_transfer_price', models.FloatField(blank=True, default=0, null=True)),
                ('pi_issue_production_quantity', models.FloatField(blank=True, default=0, null=True)),
                ('pi_issue_production_price', models.FloatField(blank=True, default=0, null=True)),
                ('di_sale_issue_quantity', models.FloatField(blank=True, default=0, null=True)),
                ('di_sale_issue_price', models.FloatField(blank=True, default=0, null=True)),
                ('oi_unplanned_issue_quantity', models.FloatField(blank=True, default=0, null=True)),
                ('oi_unplanned_issue_price', models.FloatField(blank=True, default=0, null=True)),
                ('stock_transfer_issue_quantity', models.FloatField(blank=True, default=0, null=True)),
                ('stock_transfer_issue_price', models.FloatField(blank=True, default=0, null=True)),
=======
                ('date', models.DateTimeField(blank=True, null=True)),
                ('begin_quantity', models.FloatField(blank=True, null=True)),
                ('begin_price', models.FloatField(blank=True, null=True)),
                ('pr_purchase_quantity', models.FloatField(blank=True, null=True)),
                ('pr_purchase_price', models.FloatField(blank=True, null=True)),
                ('mr_production_quantity', models.FloatField(blank=True, null=True)),
                ('mr_production_price', models.FloatField(blank=True, null=True)),
                ('or_unplanned_quantity', models.FloatField(blank=True, null=True)),
                ('or_unplanned_price', models.FloatField(blank=True, null=True)),
                ('stock_transfer_quantity', models.FloatField(blank=True, null=True)),
                ('stock_transfer_price', models.FloatField(blank=True, null=True)),
                ('pi_issue_production_quantity', models.FloatField(blank=True, null=True)),
                ('pi_issue_production_price', models.FloatField(blank=True, null=True)),
                ('di_sale_issue_quantity', models.FloatField(blank=True, null=True)),
                ('di_sale_issue_price', models.FloatField(blank=True, null=True)),
                ('oi_unplanned_issue_quantity', models.FloatField(blank=True, null=True)),
                ('oi_unplanned_issue_price', models.FloatField(blank=True, null=True)),
                ('stock_transfer_issue_quantity', models.FloatField(blank=True, null=True)),
                ('stock_transfer_issue_price', models.FloatField(blank=True, null=True)),
>>>>>>> 2a2cb229b4c727c4212802a7b390e8e05b1ecf3b
                ('export_to_CSV', models.BooleanField(default=False)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ecus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('account_number', models.CharField(blank=True, max_length=50, null=True)),
                ('registered_date', models.DateField(blank=True, default=datetime.datetime(2021, 10, 6, 20, 1, 26, 198861), null=True)),
                ('type_code', models.CharField(blank=True, max_length=3, null=True)),
                ('goods_no', models.FloatField(blank=True, default=0, null=True)),
                ('npl_sp_code', models.CharField(blank=True, max_length=50, null=True)),
                ('erp_code', models.CharField(blank=True, max_length=50, null=True)),
                ('hs', models.CharField(blank=True, max_length=10, null=True)),
                ('item_name', models.CharField(blank=True, max_length=250, null=True)),
                ('from_country', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_price', models.FloatField(blank=True, default=0, null=True)),
                ('unit_price_taxed', models.FloatField(blank=True, default=0, null=True)),
                ('total', models.FloatField(blank=True, default=0, null=True)),
                ('unit', models.CharField(blank=True, max_length=15, null=True)),
                ('total_2', models.FloatField(blank=True, default=0, null=True)),
                ('unit_2', models.CharField(blank=True, max_length=15, null=True)),
                ('nt_value', models.FloatField(blank=True, default=0, null=True)),
                ('total_value', models.FloatField(blank=True, default=0, null=True)),
                ('tax_rate', models.FloatField(blank=True, default=0, null=True)),
                ('tax_cost', models.FloatField(blank=True, default=0, null=True)),
                ('partner', models.CharField(blank=True, max_length=100, null=True)),
                ('bill', models.CharField(blank=True, max_length=50, null=True)),
                ('bill_date', models.DateField(blank=True, null=True)),
                ('contract', models.CharField(blank=True, max_length=50, null=True)),
=======
                ('account_number', models.CharField(blank=True, max_length=20, null=True)),
                ('registered_date', models.DateField(blank=True, null=True)),
                ('type_code', models.CharField(blank=True, max_length=3, null=True)),
                ('goods_no', models.FloatField(blank=True, null=True)),
                ('npl_sp_code', models.CharField(blank=True, max_length=20, null=True)),
                ('erp_code', models.CharField(blank=True, max_length=20, null=True)),
                ('hs', models.CharField(blank=True, max_length=10, null=True)),
                ('item_name', models.CharField(blank=True, max_length=100, null=True)),
                ('from_country', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_price', models.FloatField(blank=True, null=True)),
                ('unit_price_taxed', models.FloatField(blank=True, null=True)),
                ('total', models.FloatField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, max_length=15, null=True)),
                ('total_2', models.FloatField(blank=True, null=True)),
                ('unit_2', models.CharField(blank=True, max_length=15, null=True)),
                ('nt_value', models.FloatField(blank=True, null=True)),
                ('total_value', models.FloatField(blank=True, null=True)),
                ('tax_rate', models.FloatField(blank=True, null=True)),
                ('tax_cost', models.FloatField(blank=True, null=True)),
                ('partner', models.CharField(blank=True, max_length=50, null=True)),
                ('bill', models.CharField(blank=True, max_length=20, null=True)),
                ('bill_date', models.DateField(blank=True, null=True)),
                ('contract', models.CharField(blank=True, max_length=20, null=True)),
>>>>>>> 2a2cb229b4c727c4212802a7b390e8e05b1ecf3b
                ('contract_date', models.DateField(blank=True, null=True)),
                ('export_to_CSV', models.BooleanField(default=False)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BOM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
<<<<<<< HEAD
                ('tp_code', models.CharField(blank=True, max_length=50, null=True)),
                ('ecus_code', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('rm_code', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('unit', models.CharField(blank=True, max_length=20, null=True)),
                ('ecus', models.CharField(blank=True, max_length=50, null=True)),
                ('name_2', models.CharField(blank=True, max_length=50, null=True)),
                ('description_2', models.CharField(blank=True, max_length=100, null=True)),
                ('unit_2', models.CharField(blank=True, max_length=20, null=True)),
                ('bom', models.FloatField(blank=True, default=0, null=True)),
                ('loss', models.FloatField(blank=True, default=0, null=True)),
                ('finish_product', models.FloatField(blank=True, default=0, null=True)),
                ('finish_product_convert', models.FloatField(blank=True, default=0, null=True)),
                ('finish_product_inventory', models.FloatField(blank=True, default=0, null=True)),
                ('finish_product_exchange', models.FloatField(blank=True, default=0, null=True)),
=======
                ('tp_code', models.CharField(blank=True, max_length=20, null=True)),
                ('ecus_code', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('rm_code', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('unit', models.CharField(blank=True, max_length=4, null=True)),
                ('ecus', models.CharField(blank=True, max_length=20, null=True)),
                ('name_2', models.CharField(blank=True, max_length=20, null=True)),
                ('description_2', models.CharField(blank=True, max_length=100, null=True)),
                ('unit_2', models.CharField(blank=True, max_length=4, null=True)),
                ('bom', models.FloatField(blank=True, null=True)),
                ('loss', models.FloatField(blank=True, null=True)),
                ('finish_product', models.FloatField(blank=True, null=True)),
                ('finish_product_convert', models.FloatField(blank=True, null=True)),
                ('finish_product_inventory', models.FloatField(blank=True, null=True)),
                ('finish_product_exchange', models.FloatField(blank=True, null=True)),
>>>>>>> 2a2cb229b4c727c4212802a7b390e8e05b1ecf3b
                ('export_to_CSV', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Balance',
            fields=[
<<<<<<< HEAD
                ('erp_code', models.CharField(blank=True, max_length=50, null=True)),
                ('ecus_code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('ecus_unit', models.CharField(blank=True, max_length=4, null=True)),
                ('unit', models.CharField(blank=True, max_length=4, null=True)),
                ('e21', models.FloatField(blank=True, default=0, null=True)),
                ('b13', models.FloatField(blank=True, default=0, null=True)),
                ('a42', models.FloatField(blank=True, default=0, null=True)),
                ('e52', models.FloatField(blank=True, default=0, null=True)),
                ('ecus', models.FloatField(blank=True, default=0, null=True)),
                ('rm_stock', models.FloatField(blank=True, default=0, null=True)),
                ('fg_stock', models.FloatField(blank=True, default=0, null=True)),
                ('wip_stock', models.FloatField(blank=True, default=0, null=True)),
=======
                ('erp_code', models.CharField(blank=True, max_length=20, null=True)),
                ('ecus_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('ecus_unit', models.CharField(blank=True, max_length=4, null=True)),
                ('unit', models.CharField(blank=True, max_length=4, null=True)),
                ('e21', models.FloatField(blank=True, null=True)),
                ('b13', models.FloatField(blank=True, null=True)),
                ('a42', models.FloatField(blank=True, null=True)),
                ('e52', models.FloatField(blank=True, null=True)),
                ('ecus', models.FloatField(blank=True, null=True)),
                ('rm_stock', models.FloatField(blank=True, null=True)),
                ('fg_stock', models.FloatField(blank=True, null=True)),
                ('wip_stock', models.FloatField(blank=True, null=True)),
>>>>>>> 2a2cb229b4c727c4212802a7b390e8e05b1ecf3b
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
