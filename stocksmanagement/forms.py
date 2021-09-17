from django import forms
from .models import Balance, Stock, Ecus, BOM

''' STOCK IOB '''


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = [
            'description',
            'item_name',
            'ecus_code',
            'item_desciption',
            'date',
            'begin_quantity',
            'begin_price',
            'pr_purchase_quantity',
            'pr_purchase_price',
            'mr_production_quantity',
            'mr_production_price',
            'or_unplanned_quantity',
            'or_unplanned_price',
            'stock_transfer_quantity',
            'stock_transfer_price',
            'pi_issue_production_quantity',
            'pi_issue_production_price',
            'di_sale_issue_quantity',
            'di_sale_issue_price',
            'oi_unplanned_issue_quantity',
            'oi_unplanned_issue_price',
            'stock_transfer_issue_quantity',
            'stock_transfer_issue_price',
        ]

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError('This field is required')
        return description

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name


class StockSearchForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['description', 'item_name']

    export_to_CSV = forms.BooleanField(required=False)


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['description', 'item_name', 'begin_quantity']


''' ECUS '''


class EcusSearchForm(forms.ModelForm):
    class Meta:
        model = Ecus
        fields = ['type_code', 'from_country']

    export_to_CSV = forms.BooleanField(required=False)


class EcusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ecus
        fields = [
            'account_number',
            'registered_date',
            'type_code',
            'goods_no',
            'total_value',
            'tax_cost',
            'partner',
        ]


class EcusCreateForm(forms.ModelForm):
    class Meta:
        model = Ecus
        fields = [
            'account_number',
            'registered_date',
            'type_code',
            'goods_no',
            'npl_sp_code',
            'erp_code',
            'hs',
            'item_name',
            'from_country',
            'unit_price',
            'unit_price_taxed',
            'total',
            'unit',
            'total_2',
            'unit_2',
            'nt_value',
            'total_value',
            'tax_rate',
            'tax_cost',
            'partner',
            'bill',
            'bill_date',
            'contract',
            'contract_date',
        ]

    def clean_account_number(self):
        account_number = self.cleaned_data.get('account_number')
        if not account_number:
            raise forms.ValidationError('This field is required')
        return account_number

    def clean_type_code(self):
        type_code = self.cleaned_data.get('type_code')
        if not type_code:
            raise forms.ValidationError('This field is required')
        return type_code


''' BOM '''


class BOMSearchForm(forms.ModelForm):
    class Meta:
        model = BOM
        fields = ['tp_code', 'ecus_code', 'ecus']

    export_to_CSV = forms.BooleanField(required=False)


class BOMUpdateForm(forms.ModelForm):
    class Meta:
        model = BOM
        fields = [
            'tp_code',
            'ecus_code',
            'description',
            'ecus',
            'name_2',
            'description_2',
            'unit_2',
        ]


class BOMCreateForm(forms.ModelForm):
    class Meta:
        model = BOM
        fields = [
            'tp_code',
            'ecus_code',
            'name',
            'description',
            'unit',
            'ecus',
            'name_2',
            'description_2',
            'unit_2',
            'bom',
            'loss',
            'finish_product',
            'finish_product_convert',
            'finish_product_inventory',
            'finish_product_exchange',
        ]

    def clean_tp_code(self):
        tp_code = self.cleaned_data.get('tp_code')
        if not tp_code:
            raise forms.ValidationError('This field is required')
        return tp_code


class BalanceSearchForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['ecus_code', 'description']
