import csv
from io import StringIO

import pandas as pd
import xlsxwriter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView

from .forms import (BalanceSearchForm, BOMCreateForm, BOMSearchForm,
                    BOMUpdateForm, EcusCreateForm, EcusSearchForm,
                    EcusUpdateForm, StockCreateForm, StockSearchForm,
                    StockUpdateForm)
from .models import BOM, Balance, Ecus, Stock


class IOBListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'stocksmanagement/list_items.html'
    context_object_name = 'queryset'
    ordering = ['-date']
    paginate_by = 20
    query_set = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StockSearchForm(self.request.GET)
        context['title'] = 'IOB'
        return context

    def get_queryset(self):
        self.query_set = Stock.objects.all().filter(client=self.request.user)
        description = self.request.GET.get('description', '')
        item_name = self.request.GET.get('item_name', '')
        export_to_csv = self.request.GET.get('export_to_CSV', False)
        if description:
            self.query_set = self.query_set.filter(
                description__icontains=description
            )
        if item_name:
            self.query_set = self.query_set.filter(
                item_name__icontains=item_name
            )
        if export_to_csv:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['description', 'ITEM NAME', 'QUANTITY'])
            for stock in self.query_set:
                writer.writerow(
                    [stock.description, stock.item_name])
        return self.query_set


class SavedSamplesCsvView(IOBListView):
    """
    Subclass of above view, to produce a csv file
    """
    paginate_by = None
    template_name = 'stocksmanagement/stock.csv'
    content_type = 'text/csv'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
        return context


@login_required
def export_csv_iob(request):
    query_set = Stock.objects.all().filter(client=request.user)
    description = request.GET.get('description', '')
    item_name = request.GET.get('item_name', '')
    content_disposition = 'attachment; filename="List of stock'
    if description:
        query_set = query_set.filter(
            description__icontains=description
        )
        content_disposition += f' - {description}'
    if item_name:
        query_set = query_set.filter(
            item_name__icontains=item_name
        )
        content_disposition += f' - {item_name}'
    content_disposition += '.csv"'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    writer.writerow(['', ' ', ' ', ' ', ' Beginning Inventory', ' ', ' ', ' PR Purchase Receipt', ' ', ' ', ' MR Production Receipt', ' ', ' ', ' OR Unplanned Receipt', ' ', ' ', ' Stock Transfer Receipt',
                    ' ', ' ', ' PI Issue for production', ' ', ' ', ' DI Sales Issue', ' ', ' ', ' OI Unplanned Issue', ' ', ' ', ' Stock Transfer Issue', ' ', ' '])
    writer.writerow(['Item Acount Description', ' Item', ' Ecus', ' Item Description', ' Quantity', ' Amount', ' Price', ' Quantity', ' Amount', ' Price', ' Quantity', ' Amount', ' Price', ' Quantity', ' Amount', ' Price',
                    ' Quantity', ' Amount', ' Price', ' Quantity', ' Amount', ' Price', ' Quantity', ' Amount', ' Price', ' Quantity', ' Amount', ' Price', ' Quantity', ' Amount', ' Price'])
    for stock in query_set:
        writer.writerow(
            [
                stock.description,
                stock.item_name,
                stock.ecus_code,
                stock.item_desciption,
                stock.begin_quantity,
                stock.get_beginning_amount(),
                stock.begin_price,
                stock.pr_purchase_quantity,
                stock.get_pr_purchase_amount(),
                stock.pr_purchase_price,
                stock.mr_production_quantity,
                stock.get_mr_production_amount(),
                stock.mr_production_price,
                stock.or_unplanned_quantity,
                stock.get_or_unplanned_amount(),
                stock.or_unplanned_price,
                stock.stock_transfer_quantity,
                stock.get_stock_transfer_amount(),
                stock.stock_transfer_price,
                stock.pi_issue_production_quantity,
                stock.get_pi_issue_production_amount(),
                stock.pi_issue_production_price,
                stock.di_sale_issue_quantity,
                stock.get_di_sale_issue_amount(),
                stock.di_sale_issue_price,
                stock.oi_unplanned_issue_quantity,
                stock.get_oi_unplanned_issue_amount(),
                stock.oi_unplanned_issue_price,
                stock.stock_transfer_issue_quantity,
                stock.get_stock_transfer_amount(),
                stock.stock_transfer_issue_price,
            ]
        )
    return response


@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.client = request.user
        instance.save()
        messages.success(request, 'Successfully Saved')
        return redirect('list_items')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "stocksmanagement/add_items.html", context)


@login_required
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('list_items')

    context = {
        'title': 'update item',
        'form': form
    }
    return render(request, "stocksmanagement/add_items.html", context)


@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('list_items')
    return render(request, 'stocksmanagement/confirm_delete.html', {"title": 'Confirm delete'})


@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stocksmanagement/stock_detail.html", context)


def check_format(df):
    format = ['Item Acount Description', 'Item', 'M?? Ecus', 'Item Description',
              'Quantity', 'Amount', 'Price', 'Quantity.1', 'Amount.1', 'Price.1',
              'Quantity.2', 'Amount.2', 'Price.2', 'Quantity.3', 'Amount.3',
              'Price.3', 'Quantity.4', 'Amount.4', 'Price.4', 'Quantity.5',
              'Amount.5', 'Price.5', 'Quantity.6', 'Amount.6', 'Price.6',
              'Quantity.7', 'Amount.7', 'Price.7', 'Quantity.8', 'Amount.8',
              'Price.8', 'Quantity.9', 'Amount.9', 'Price.9']
    set1 = set(format)
    set2 = set(df.columns.tolist())
    is_subset = set1.issubset(set2)
    if not is_subset:
        return False
    return True


@login_required
def import_excel(request):
    if request.method == 'POST':
        try:
            file_name = request.FILES['myfile']
        except MultiValueDictKeyError:
            messages.warning(request, 'Please choose your file')
            return redirect('import_excel')
        try:
            imported_data = pd.read_excel(
                file_name.read(), header=10, sheet_name='IOB')
        except Exception:
            messages.warning(
                request, "Wrong format, please make sure the file you input is excel and the sheet contain information name 'IOB'")
            return redirect('import_excel')
        if check_format(imported_data):
            imported_data.fillna(method='ffill', inplace=True)
            for _, row in imported_data.iterrows():
                item = Stock(client=request.user)

                if row['Item Acount Description']:
                    item.description = row['Item Acount Description'],
                if row['Item']:
                    item.item_name = row['Item']
                if row['M?? Ecus']:
                    item.ecus_code = row['M?? Ecus']
                if row['Item Description']:
                    item.item_desciption = row['Item Description']
                if row['Quantity']:
                    item.begin_quantity = row['Quantity']
                if row['Price']:
                    item.begin_price = row['Price']
                if row['Quantity.1']:
                    item.pr_purchase_quantity = row['Quantity.1']
                if row['Amount.1']:
                    item.pr_purchase_price = row['Amount.1']
                if row['Quantity.2']:
                    item.mr_production_quantity = row['Quantity.2']
                if row['Amount.2']:
                    item.mr_production_price = row['Amount.2']
                if row['Quantity.3']:
                    item.or_unplanned_quantity = row['Quantity.3']
                if row['Amount.3']:
                    item.or_unplanned_price = row['Amount.3']
                if row['Quantity.4']:
                    item.stock_transfer_quantity = row['Quantity.4']
                if row['Amount.4']:
                    item.stock_transfer_price = row['Amount.4']
                if row['Quantity.5']:
                    item.pi_issue_production_quantity = row['Quantity.5']
                if row['Amount.5']:
                    item.pi_issue_production_price = row['Amount.5']
                if row['Quantity.6']:
                    item.di_sale_issue_quantity = row['Quantity.6']
                if row['Amount.6']:
                    item.di_sale_issue_price = row['Amount.6']
                if row['Quantity.7']:
                    item.oi_unplanned_issue_quantity = row['Quantity.7']
                if row['Amount.7']:
                    item.oi_unplanned_issue_price = row['Amount.7']
                if row['Quantity.8']:
                    item.stock_transfer_issue_quantity = row['Quantity.8']
                if row['Amount.8']:
                    item.stock_transfer_issue_price = row['Amount.8']
                item.save()
            messages.success(request, 'Data Imported')
            return redirect('list_items')
        else:
            messages.warning(request, '''Wrong format, please make sure the excel table contains at least these columns ['Item Acount Description', 'Item', 'M?? Ecus', 'Item Description',
                                        'Quantity', 'Amount', 'Price', 'Quantity.1', 'Amount.1', 'Price.1',
                                        'Quantity.2', 'Amount.2', 'Price.2', 'Quantity.3', 'Amount.3',
                                        'Price.3', 'Quantity.4', 'Amount.4', 'Price.4', 'Quantity.5',
                                        'Amount.5', 'Price.5', 'Quantity.6', 'Amount.6', 'Price.6',
                                        'Quantity.7', 'Amount.7', 'Price.7', 'Quantity.8', 'Amount.8',
                                        'Price.8', 'Quantity.9', 'Amount.9', 'Price.9']''')
            return redirect('import_excel')
    return render(request, 'stocksmanagement/import_excel.html', {'title': 'Import as excel'})


['Item Acount Description', 'Item', 'M?? Ecus', 'Item Description',
 'Quantity', 'Amount', 'Price', 'Quantity.1', 'Amount.1', 'Price.1',
 'Quantity.2', 'Amount.2', 'Price.2', 'Quantity.3', 'Amount.3',
 'Price.3', 'Quantity.4', 'Amount.4', 'Price.4', 'Quantity.5',
 'Amount.5', 'Price.5', 'Quantity.6', 'Amount.6', 'Price.6',
 'Quantity.7', 'Amount.7', 'Price.7', 'Quantity.8', 'Amount.8',
 'Price.8', 'Quantity.9', 'Amount.9', 'Price.9']


'''----------ECUS---------'''


class EcusListView(LoginRequiredMixin, ListView):
    model = Ecus
    template_name = 'stocksmanagement/list_ecus.html'
    context_object_name = 'queryset'
    ordering = ['-registered_date']
    paginate_by = 20
    query_set = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ecus'
        return context

    def get_queryset(self):
        self.query_set = Ecus.objects.all().filter(client=self.request.user)
        type_code = self.request.GET.get('type_code', '')
        from_country = self.request.GET.get('from_country', '')
        if type_code:
            self.query_set = self.query_set.filter(
                type_code__icontains=type_code
            )
        if from_country:
            self.query_set = self.query_set.filter(
                from_country__icontains=from_country
            )
        return self.query_set


@login_required
def export_csv_ecus(request):
    query_set = Ecus.objects.all().filter(client=request.user)
    type_code = request.GET.get('type_code', '')
    from_country = request.GET.get('from_country', '')
    content_disposition = 'attachment; filename="Ecus'
    if type_code:
        query_set = query_set.filter(
            type_code__icontains=type_code
        )
        content_disposition += f' - {type_code}'
    if from_country:
        query_set = query_set.filter(
            from_country__icontains=from_country
        )
        content_disposition += f' - {from_country}'
    content_disposition += '.csv"'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    writer.writerow([
                    'Account Number',
                    'Registered Date',
                    'Type Code',
                    'Goods No',
                    'NPL/SP Code',
                    'ERP Code',
                    'HS',
                    'Item Name',
                    'Country',
                    'Unit Price',
                    'Taxed Price',
                    'Total',
                    'Unit',
                    'Total 2',
                    'Unit 2',
                    'NT value',
                    'Total value',
                    'Tax rate',
                    'Tax cost',
                    'Partner',
                    'Bill',
                    'Bill date',
                    'Contract',
                    'Contract date'
                    ])
    for stock in query_set:
        writer.writerow(
            [
                stock.account_number,
                stock.registered_date,
                stock.type_code,
                stock.goods_no,
                stock.npl_sp_code,
                stock.erp_code,
                stock.hs,
                stock.item_name,
                stock.from_country,
                stock.unit_price,
                stock.unit_price_taxed,
                stock.total,
                stock.unit,
                stock.total_2,
                stock.unit_2,
                stock.nt_value,
                stock.total_value,
                stock.tax_rate,
                stock.tax_cost,
                stock.partner,
                stock.bill,
                stock.bill_date,
                stock.contract,
                stock.contract_date
            ]
        )
    return response


@login_required
def update_ecus(request, pk):
    queryset = Ecus.objects.get(id=pk)
    form = EcusUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = EcusUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('list_ecus')

    context = {
        'title': 'Update Item',
        'form': form
    }
    return render(request, "stocksmanagement/add_items.html", context)


def check_ecus_format(df):
    format = ['S??? TK', 'Ng??y ??K', 'M?? lo???i h??nh', 'STT h??ng', 'M?? NPL/SP', 'M?? ERP', 'M?? HS', 'T??n h??ng', 'Xu???t x???', '????n gi??', '????n gi?? t??nh thu???', 'T???ng s??? l?????ng', '????n v??? t??nh',
              'T???ng s??? l?????ng 2', '????n v??? t??nh 2', 'Tr??? gi?? NT', 'T???ng tr??? gi??', 'Thu??? su???t XNK', 'Ti???n thu??? XNK', 'T??n ?????i t??c', 'S??? h??a ????n', 'Ng??y h??a ????n', 'S??? h???p ?????ng', 'Ng??y h???p ?????ng']
    set1 = set(format)
    set2 = set(df.columns.tolist())
    is_subset = set1.issubset(set2)
    if not is_subset:
        return False
    return True


@login_required
def import_excel_ecus(request):
    if request.method == 'POST':
        try:
            file_name = request.FILES['myfile']
        except MultiValueDictKeyError:
            messages.warning(request, 'Please choose your file')
            return redirect('import_excel_ecus')
        try:
            imported_data = pd.read_excel(
                file_name.read(), sheet_name='Ecus')
        except Exception:
            messages.warning(
                request, 'Wrong format, make sure the files you import is excel file and the sheet contain informations name Ecus')
            return render(request, 'stocksmanagement/import_excel.html')
        if check_ecus_format(imported_data):
            for _, row in imported_data.iterrows():
                item = Ecus(client=request.user)
                if not pd.isna(row['S??? TK']):
                    item.account_number = row['S??? TK']
                if not pd.isna(row['Ng??y ??K']):
                    item.registered_date = row['Ng??y ??K'].date()
                if not pd.isna(row['M?? lo???i h??nh']):
                    item.type_code = row['M?? lo???i h??nh']
                if not pd.isna(row['STT h??ng']):
                    item.goods_no = row['STT h??ng']
                if not pd.isna(row['M?? NPL/SP']):
                    item.npl_sp_code = row['M?? NPL/SP']
                if not pd.isna(row['M?? ERP']):
                    item.erp_code = row['M?? ERP']
                if not pd.isna(row['M?? HS']):
                    item.hs = row['M?? HS']
                if not pd.isna(row['T??n h??ng']):
                    item.item_name = row['T??n h??ng']
                if not pd.isna(row['Xu???t x???']):
                    item.from_country = row['Xu???t x???']
                if not pd.isna(row['????n gi??']):
                    item.unit_price = row['????n gi??']
                if not pd.isna(row['????n gi?? t??nh thu???']):
                    item.unit_price_taxed = row['????n gi?? t??nh thu???']
                if not pd.isna(row['T???ng s??? l?????ng']):
                    item.total = row['T???ng s??? l?????ng']
                if not pd.isna(row['????n v??? t??nh']):
                    item.unit = row['????n v??? t??nh']
                if not pd.isna(row['T???ng s??? l?????ng 2']):
                    item.total_2 = row['T???ng s??? l?????ng 2']
                if not pd.isna(row['????n v??? t??nh 2']):
                    item.unit_2 = row['????n v??? t??nh 2']
                if not pd.isna(row['Tr??? gi?? NT']):
                    item.nt_value = row['Tr??? gi?? NT']
                if not pd.isna(row['T???ng tr??? gi??']):
                    item.total_value = row['T???ng tr??? gi??']
                if not pd.isna(row['Thu??? su???t XNK']):
                    item.tax_rate = row['Thu??? su???t XNK']
                if not pd.isna(row['Ti???n thu??? XNK']):
                    item.tax_cost = row['Ti???n thu??? XNK']
                if not pd.isna(row['T??n ?????i t??c']):
                    item.partner = row['T??n ?????i t??c']
                if not pd.isna(row['S??? h??a ????n']):
                    item.bill = row['S??? h??a ????n']
                if not pd.isna(row['Ng??y h??a ????n']):
                    item.bill_date = row['Ng??y h??a ????n'].date()
                if not pd.isna(row['S??? h???p ?????ng']):
                    item.contract = row['S??? h???p ?????ng']
                if not pd.isnull(row['Ng??y h???p ?????ng']):
                    item.contract_date = row['Ng??y h???p ?????ng'].date()
                item.save()
            messages.success(request, 'Data Imported')
            return redirect('list_ecus')
        else:
            messages.warning(request, '''Wrong format, make sure your file has at least these column ['S??? TK', 'Ng??y ??K', 'M?? lo???i h??nh', 'STT h??ng', 'M?? NPL/SP', 'M?? ERP', 'M?? HS', 'T??n h??ng', 'Xu???t x???', '????n gi??', '????n gi?? t??nh thu???', 'T???ng s??? l?????ng', '????n v??? t??nh',
              'T???ng s??? l?????ng 2', '????n v??? t??nh 2', 'Tr??? gi?? NT', 'T???ng tr??? gi??', 'Thu??? su???t XNK', 'Ti???n thu??? XNK', 'T??n ?????i t??c', 'S??? h??a ????n', 'Ng??y h??a ????n', 'S??? h???p ?????ng', 'Ng??y h???p ?????ng']''')
            return redirect('import_excel_ecus')
    return render(request, 'stocksmanagement/import_excel.html', {'title': 'Import as excel'})


@login_required
def add_items_ecus(request):
    form = EcusCreateForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.client = request.user
        instance.save()
        messages.success(request, 'Successfully Saved')
        return redirect('list_ecus')
    context = {
        "form": form,
        "title": "Add Ecus",
    }
    return render(request, "stocksmanagement/add_items.html", context)


@login_required
def delete_items_ecus(request, pk):
    queryset = Ecus.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('list_ecus')
    return render(request, 'stocksmanagement/confirm_delete_ecus.html', {'title': 'Confirm delete'})


@login_required
def ecus_detail(request, pk):
    queryset = Ecus.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stocksmanagement/ecus_detail.html", context)


'''------------BOM------------'''


class BOMListView(LoginRequiredMixin, ListView):
    model = BOM
    template_name = 'stocksmanagement/list_bom.html'
    context_object_name = 'queryset'
    # ordering = ['-date_posted']
    paginate_by = 20
    query_set = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BOMSearchForm(self.request.GET)
        context['title'] = 'BOM'
        return context

    def get_queryset(self):
        self.query_set = BOM.objects.all().filter(client=self.request.user)
        ecus_code = self.request.GET.get('ecus_code', '')
        tp_code = self.request.GET.get('tp_code', '')
        ecus = self.request.GET.get('ecus', '')
        if ecus_code:
            self.query_set = self.query_set.filter(
                ecus_code__icontains=ecus_code
            )
        if tp_code:
            self.query_set = self.query_set.filter(
                tp_code__icontains=tp_code
            )
        if ecus:
            self.query_set = self.query_set.filter(
                ecus__icontains=ecus
            )
        return self.query_set


@login_required
def export_csv_bom(request):
    query_set = BOM.objects.all().filter(client=request.user)
    ecus_code = request.GET.get('ecus_code', '')
    tp_code = request.GET.get('tp_code', '')
    content_disposition = 'attachment; filename="BOM'
    if ecus_code:
        query_set = query_set.filter(
            ecus_code__icontains=ecus_code
        )
        content_disposition += f' - {ecus_code}'
    if tp_code:
        query_set = query_set.filter(
            tp_code__icontains=tp_code
        )
        content_disposition += f' - {tp_code}'
    content_disposition += '.csv"'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    writer.writerow(
        [
            'Code TP',
            'Ecus Code',
            'Name',
            'Decription',
            'Unit',
            'Ecus',
            'Name 2',
            'Decription',
            'Unit',
            'BOM',
            'Loss',
            'Th??nh ph???m xu???t',
            'Quy ?????i TP xu???t',
            'Th??nh ph???m t???n',
            'Quy ?????i th??nh ph???m t???n'
        ]
    )
    for stock in query_set:
        writer.writerow(
            [
                stock.tp_code,
                stock.ecus_code,
                stock.name,
                stock.description,
                stock.unit,
                stock.ecus,
                stock.name_2,
                stock.description_2,
                stock.unit_2,
                stock.bom,
                stock.loss,
                stock.finish_product,
                stock.finish_product_convert,
                stock.finish_product_inventory,
                stock.finish_product_exchange
            ]
        )
    return response


@login_required
def update_bom(request, pk):
    queryset = BOM.objects.get(id=pk)
    form = BOMUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = BOMUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('list_bom')

    context = {
        'title': 'Add item',
        'form': form
    }
    return render(request, "stocksmanagement/add_items.html", context)


def check_bom_format(df):
    format = ['Code TP', 'M?? Ecus', 'T??n', 'Decription', 'Unit', 'RM.code',
              'Ecus code', 'Name', 'Decription.1', 'Unit.1', 'BOM', 'Loss', 'Th??nh ph???m xu???t', 'Quy ?????i TP xu???t', 'Th??nh ph???m t???n',
              'Quy ?????i th??nh ph???m t???n']
    set1 = set(format)
    set2 = set(df.columns.tolist())
    is_subset = set1.issubset(set2)
    if not is_subset:
        return False
    return True


@login_required
def import_excel_bom(request):
    if request.method == 'POST':
        try:
            file_name = request.FILES['myfile']
        except MultiValueDictKeyError:
            messages.warning(request, 'Please choose your file')
            return redirect('import_excel_bom')
        try:
            imported_data = pd.read_excel(
                file_name.read(), sheet_name='BOM')
        except Exception:
            messages.warning(
                request, 'Wrong format, make sure the file you import is excel and the sheet contain informations name BOM')
            return render(request, 'stocksmanagement/import_excel.html')
        if check_bom_format(imported_data):
            imported_data = imported_data.iloc[1:, :]
            for _, row in imported_data.iterrows():
                item = BOM(client=request.user)
                if not pd.isna(row['Code TP']):
                    item.tp_code = row['Code TP']
                if not pd.isna(row['M?? Ecus']):
                    item.ecus_code = row['M?? Ecus']
                if not pd.isna(row['T??n']):
                    item.name = row['T??n']
                if not pd.isna(row['Decription']):
                    item.rm_code = row['Decription']
                if not pd.isna(row['Unit']):
                    item.description = row['Unit']
                if not pd.isna(row['RM.code']):
                    item.unit = row['RM.code']
                if not pd.isna(row['Ecus code']):
                    item.ecus = row['Ecus code']
                if not pd.isna(row['Name']):
                    item.name_2 = row['Name']
                if not pd.isna(row['Decription.1']):
                    item.description_2 = row['Decription.1']
                if not pd.isna(row['Unit.1']):
                    item.unit_2 = row['Unit.1']
                if not pd.isna(row['BOM']):
                    item.bom = row['BOM']
                if not pd.isna(row['Loss']):
                    item.loss = row['Loss']
                if not pd.isna(row['Th??nh ph???m xu???t']):
                    item.finish_product = row['Th??nh ph???m xu???t']
                if not pd.isna(row['Quy ?????i TP xu???t']):
                    item.finish_product_convert = row['Quy ?????i TP xu???t']
                if not pd.isna(row['Th??nh ph???m t???n']):
                    item.finish_product_inventory = row['Th??nh ph???m t???n']
                if not pd.isna(row['Quy ?????i th??nh ph???m t???n']):
                    item.finish_product_exchange = row['Quy ?????i th??nh ph???m t???n']
                item.save()
            messages.success(request, 'Data Imported')
            return redirect('list_bom')
        else:
            messages.warning(request, '''
            Wrong format, make sure table has at least these columns:
            'Code TP', 'M?? Ecus', 'T??n', 'Decription', 'Unit', 'RM.code',
            'Ecus code', 'Name', 'Decription.1', 'Unit.1', 'BOM', 'Loss', 
            'Th??nh ph???m xu???t', 'Quy ?????i TP xu???t', 'Th??nh ph???m t???n',
            'Quy ?????i th??nh ph???m t???n' 
            ''')
            return redirect('import_excel_bom')
    return render(request, 'stocksmanagement/import_excel.html', {'title': 'Import as excel'})


['Code TP', 'M?? Ecus', 'T??n', 'Decription', 'Unit', 'RM.code',
 'Ecus code', 'Name', 'Decription.1', 'Unit.1', 'BOM', 'Loss',
 'BOM + Loss', 'Th??nh ph???m xu???t', 'Quy ?????i TP xu???t', 'Th??nh ph???m t???n',
 'Quy ?????i th??nh ph???m t???n']


@login_required
def add_items_bom(request):
    form = BOMCreateForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.client = request.user
        instance.save()
        messages.success(request, 'Successfully Saved')
        return redirect('list_bom')
    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "stocksmanagement/add_items.html", context)


@login_required
def delete_items_bom(request, pk):
    queryset = BOM.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('list_items_bom')
    return render(request, 'stocksmanagement/confirm_delete_bom.html', {'title': 'Confirm delete'})


@login_required
def bom_detail(request, pk):
    queryset = BOM.objects.get(id=pk)
    context = {
        "title": queryset.name,
        "queryset": queryset,
    }
    return render(request, "stocksmanagement/bom_detail.html", context)


class BalanceListView(LoginRequiredMixin, ListView):
    model = Balance
    template_name = 'stocksmanagement/list_balance.html'
    context_object_name = 'queryset'
    # ordering = ['-date_posted']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BalanceSearchForm(self.request.GET)
        context['title'] = 'Balance'
        return context

    def get_queryset(self):
        query_set = Balance.objects.all().filter(client=self.request.user)
        ecus_code = self.request.GET.get('ecus_code', '')
        description = self.request.GET.get('description', '')
        if ecus_code:
            query_set = query_set.filter(
                ecus_code__icontains=ecus_code
            )
        if description:
            query_set = query_set.filter(
                description__icontains=description
            )
        return query_set


@login_required
def export_csv_balance(request):
    query_set = Balance.objects.all().filter(client=request.user)
    ecus_code = request.GET.get('ecus_code', '')
    description = request.GET.get('description', '')
    content_disposition = 'attachment; filename="Balance'
    if ecus_code:
        query_set = query_set.filter(
            ecus_code__icontains=ecus_code
        )
        content_disposition += f' - {ecus_code}'
    if description:
        query_set = query_set.filter(
            description__icontains=description
        )
        content_disposition += f' - {description}'
    content_disposition += '.xlsx"'
    output = StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write('ERP code',
                    'Ecus Code',
                    'Decription',
                    'E21',
                    'B13',
                    'A42',
                    'E52',
                    'RM Stock',
                    'FG Stock',
                    'WIP',
                    'BALANCE')

    for stock in query_set:
        worksheet.write(
            [
                stock.erp_code,
                stock.ecus_code,
                stock.description,
                stock.e21,
                stock.b13,
                stock.a42,
                stock.e52,
                stock.rm_stock,
                stock.fg_stock,
                stock.wip_stock,
                stock.get_balance()
            ]
        )

    workbook.close()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = content_disposition
    response.write(output.getvalue())
    return response

    # query_set = Balance.objects.all().filter(client=request.user)
    # ecus_code = request.GET.get('ecus_code', '')
    # description = request.GET.get('description', '')
    # content_disposition = 'attachment; filename="Balance'
    # if ecus_code:
    #     query_set = query_set.filter(
    #         ecus_code__icontains=ecus_code
    #     )
    #     content_disposition += f' - {ecus_code}'
    # if description:
    #     query_set = query_set.filter(
    #         description__icontains=description
    #     )
    #     content_disposition += f' - {description}'
    # content_disposition += '.csv"'
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = content_disposition
    # writer = csv.writer(response)
    # writer.writerow(
    #     [
    #         'ERP code',
    #         'Ecus Code',
    #         'Decription',
    #         'E21',
    #         'B13',
    #         'A42',
    #         'E52',
    #         'RM Stock',
    #         'FG Stock',
    #         'WIP',
    #         'BALANCE',
    #     ]
    # )
    # for stock in query_set:
    #     writer.writerow(
    #         [
    #             stock.erp_code,
    #             stock.ecus_code,
    #             stock.description,
    #             stock.e21,
    #             stock.b13,
    #             stock.a42,
    #             stock.e52,
    #             stock.rm_stock,
    #             stock.fg_stock,
    #             stock.wip_stock,
    #             stock.get_balance()
    #         ]
    #     )
    # return response
