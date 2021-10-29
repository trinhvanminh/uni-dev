from django.db import models
from client.models import Client
from django.utils import timezone
import datetime

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
    date = models.DateTimeField(default=timezone.now)

    begin_quantity = models.FloatField(default=0, blank=True, null=True)
    begin_price = models.FloatField(default=0, blank=True, null=True)

    pr_purchase_quantity = models.FloatField(default=0, blank=True, null=True)
    pr_purchase_price = models.FloatField(default=0, blank=True, null=True)

    mr_production_quantity = models.FloatField(
        default=0, blank=True, null=True)
    mr_production_price = models.FloatField(default=0, blank=True, null=True)

    or_unplanned_quantity = models.FloatField(default=0, blank=True, null=True)
    or_unplanned_price = models.FloatField(default=0, blank=True, null=True)

    stock_transfer_quantity = models.FloatField(
        default=0, blank=True, null=True)
    stock_transfer_price = models.FloatField(default=0, blank=True, null=True)

    pi_issue_production_quantity = models.FloatField(
        default=0, blank=True, null=True)
    pi_issue_production_price = models.FloatField(
        default=0, blank=True, null=True)

    di_sale_issue_quantity = models.FloatField(
        default=0, blank=True, null=True)
    di_sale_issue_price = models.FloatField(default=0, blank=True, null=True)

    oi_unplanned_issue_quantity = models.FloatField(
        default=0, blank=True, null=True)
    oi_unplanned_issue_price = models.FloatField(
        default=0, blank=True, null=True)

    stock_transfer_issue_quantity = models.FloatField(
        default=0, blank=True, null=True)
    stock_transfer_issue_price = models.FloatField(
        default=0, blank=True, null=True)

    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return str(self.item_name)

    def get_beginning_amount(self):
        return (self.begin_price * self.begin_quantity)

    def get_pr_purchase_amount(self):
        return (self.pr_purchase_quantity * self.pr_purchase_price)

    def get_mr_production_amount(self):
        return (self.mr_production_quantity * self.mr_production_price)

    def get_or_unplanned_amount(self):
        return (self.or_unplanned_quantity * self.or_unplanned_price)

    def get_stock_transfer_amount(self):
        return (self.stock_transfer_quantity * self.stock_transfer_price)

    def get_pi_issue_production_amount(self):
        return (self.pi_issue_production_quantity * self.pi_issue_production_price)

    def get_di_sale_issue_amount(self):
        return (self.di_sale_issue_quantity * self.di_sale_issue_price)

    def get_oi_unplanned_issue_amount(self):
        return (self.oi_unplanned_issue_quantity * self.oi_unplanned_issue_price)

    def get_stock_transfer_amount(self):
        return (self.stock_transfer_issue_quantity * self.stock_transfer_issue_price)

    def get_ending_quantity(self):
        return (
            self.begin_quantity + self.pr_purchase_quantity + self.mr_production_quantity + self.or_unplanned_quantity + self.stock_transfer_quantity - self.pi_issue_production_quantity - self.di_sale_issue_quantity -
            self.oi_unplanned_issue_quantity - self.stock_transfer_issue_quantity
        )


class Ecus(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)
    registered_date = models.DateField(
        default=datetime.date.today, blank=True, null=True)
    type_code = models.CharField(max_length=3, blank=True, null=True)
    goods_no = models.FloatField(default=0, blank=True, null=True)
    npl_sp_code = models.CharField(max_length=50, blank=True, null=True)
    erp_code = models.CharField(max_length=50, blank=True, null=True)
    hs = models.CharField(max_length=10, blank=True, null=True)
    item_name = models.CharField(max_length=250, blank=True, null=True)
    from_country = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.FloatField(default=0, blank=True, null=True)
    unit_price_taxed = models.FloatField(default=0, blank=True, null=True)
    total = models.FloatField(default=0, blank=True, null=True)
    unit = models.CharField(max_length=15, blank=True, null=True)
    total_2 = models.FloatField(default=0, blank=True, null=True)
    unit_2 = models.CharField(max_length=15, blank=True, null=True)
    nt_value = models.FloatField(default=0, blank=True, null=True)
    total_value = models.FloatField(default=0, blank=True, null=True)
    tax_rate = models.FloatField(default=0, blank=True, null=True)
    tax_cost = models.FloatField(default=0, blank=True, null=True)
    partner = models.CharField(max_length=100, blank=True, null=True)
    bill = models.CharField(max_length=50, blank=True, null=True)
    bill_date = models.DateField(blank=True, null=True)
    contract = models.CharField(max_length=50, blank=True, null=True)
    contract_date = models.DateField(blank=True, null=True)

    export_to_CSV = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.npl_sp_code if self.npl_sp_code else 'Missing'


class BOM(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
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
    bom = models.FloatField(default=0, blank=True, null=True)
    loss = models.FloatField(default=0, blank=True, null=True)
    finish_product = models.FloatField(default=0, blank=True, null=True)
    finish_product_convert = models.FloatField(
        default=0, blank=True, null=True)
    finish_product_inventory = models.FloatField(
        default=0, blank=True, null=True)
    finish_product_exchange = models.FloatField(
        default=0, blank=True, null=True)

    export_to_CSV = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.ecus_code)


class Balance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    erp_code = models.CharField(max_length=50, blank=True, null=True)
    ecus_code = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    ecus_unit = models.CharField(max_length=4, blank=True, null=True)
    unit = models.CharField(max_length=4, blank=True, null=True)
    e21 = models.FloatField(default=0, blank=True, null=True)
    b13 = models.FloatField(default=0, blank=True, null=True)
    a42 = models.FloatField(default=0, blank=True, null=True)
    e52 = models.FloatField(default=0, blank=True, null=True)
    ecus = models.FloatField(default=0, blank=True, null=True)
    rm_stock = models.FloatField(default=0, blank=True, null=True)
    fg_stock = models.FloatField(default=0, blank=True, null=True)
    wip_stock = models.FloatField(default=0, blank=True, null=True)

    class Meta:
        unique_together = (("client", "ecus_code"),)

    def __str__(self) -> str:
        return self.ecus_code

    def get_ecus(self):
        return self.e21 - (self.b13 + self.a42 + self.e52)

    def get_balance(self):
        return self.rm_stock + self.fg_stock + self.wip_stock - self.get_ecus()


class File(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    excel_file = models.FileField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.excel_file.name
