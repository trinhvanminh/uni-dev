from django.db import models
from client.models import Client

description_choice = (
    ('Finished Goods(제품)', 'Finished Goods(제품)'),
    ('Merchandise(상품)', 'Merchandise(상품)'),
    ('Raw Material(원자재)', 'Raw Material(원자재)'),
    ('Semi-Finished Goods(반제품)', 'Semi-Finished Goods(반제품)'),
)


class Stock(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=True, null=True)

    description = models.CharField(
        choices=description_choice, max_length=100, null=True, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    ecus_code = models.CharField(max_length=50, blank=True, null=True)
    item_desciption = models.CharField(max_length=150, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    begin_quantity = models.FloatField(blank=True, null=True)
    begin_price = models.FloatField(blank=True, null=True)

    pr_purchase_quantity = models.FloatField(blank=True, null=True)
    pr_purchase_price = models.FloatField(blank=True, null=True)

    mr_production_quantity = models.FloatField(blank=True, null=True)
    mr_production_price = models.FloatField(blank=True, null=True)

    or_unplanned_quantity = models.FloatField(blank=True, null=True)
    or_unplanned_price = models.FloatField(blank=True, null=True)

    stock_transfer_quantity = models.FloatField(blank=True, null=True)
    stock_transfer_price = models.FloatField(blank=True, null=True)

    pi_issue_production_quantity = models.FloatField(blank=True, null=True)
    pi_issue_production_price = models.FloatField(blank=True, null=True)

    di_sale_issue_quantity = models.FloatField(blank=True, null=True)
    di_sale_issue_price = models.FloatField(blank=True, null=True)

    oi_unplanned_issue_quantity = models.FloatField(blank=True, null=True)
    oi_unplanned_issue_price = models.FloatField(blank=True, null=True)

    stock_transfer_issue_quantity = models.FloatField(blank=True, null=True)
    stock_transfer_issue_price = models.FloatField(blank=True, null=True)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name


class Ecus(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    registered_date = models.DateField(blank=True, null=True)
    type_code = models.CharField(max_length=3, blank=True, null=True)
    goods_no = models.FloatField(blank=True, null=True)
    npl_sp_code = models.CharField(max_length=50, blank=True, null=True)
    erp_code = models.CharField(max_length=50, blank=True, null=True)
    hs = models.CharField(max_length=10, blank=True, null=True)
    item_name = models.CharField(max_length=250, blank=True, null=True)
    from_country = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.FloatField(blank=True, null=True)
    unit_price_taxed = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=15, blank=True, null=True)
    total_2 = models.FloatField(blank=True, null=True)
    unit_2 = models.CharField(max_length=15, blank=True, null=True)
    nt_value = models.FloatField(blank=True, null=True)
    total_value = models.FloatField(blank=True, null=True)
    tax_rate = models.FloatField(blank=True, null=True)
    tax_cost = models.FloatField(blank=True, null=True)
    partner = models.CharField(max_length=100, blank=True, null=True)
    bill = models.CharField(max_length=50, blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True)
    contract = models.CharField(max_length=50, blank=True, null=True)
    contract_date = models.DateField(blank=True, null=True)

    export_to_CSV = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.npl_sp_code


class BOM(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    tp_code = models.CharField(max_length=50, blank=True, null=True)
    ecus_code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    rm_code = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    ecus = models.CharField(max_length=50, blank=True, null=True)
    name_2 = models.CharField(max_length=50, blank=True, null=True)
    description_2 = models.CharField(max_length=100, blank=True, null=True)
    unit_2 = models.CharField(max_length=20, blank=True, null=True)
    bom = models.FloatField(blank=True, null=True)
    loss = models.FloatField(blank=True, null=True)
    finish_product = models.FloatField(blank=True, null=True)
    finish_product_convert = models.FloatField(blank=True, null=True)
    finish_product_inventory = models.FloatField(blank=True, null=True)
    finish_product_exchange = models.FloatField(blank=True, null=True)

    export_to_CSV = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.ecus_code


class Balance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    erp_code = models.CharField(max_length=50, blank=True, null=True)
    ecus_code = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)
    ecus_unit = models.CharField(max_length=4, blank=True, null=True)
    unit = models.CharField(max_length=4, blank=True, null=True)
    e21 = models.FloatField(blank=True, null=True)
    b13 = models.FloatField(blank=True, null=True)
    a42 = models.FloatField(blank=True, null=True)
    e52 = models.FloatField(blank=True, null=True)
    ecus = models.FloatField(blank=True, null=True)
    rm_stock = models.FloatField(blank=True, null=True)
    fg_stock = models.FloatField(blank=True, null=True)
    wip_stock = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return self.ecus_code
