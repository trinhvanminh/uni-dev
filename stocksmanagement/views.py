from client.models import Client
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Balance, Stock, Ecus, BOM
from .forms import BOMCreateForm, BOMSearchForm, BOMUpdateForm, BalanceSearchForm, EcusSearchForm, EcusUpdateForm, StockCreateForm, StockSearchForm, StockUpdateForm, EcusCreateForm
from django.contrib.auth.decorators import login_required
import pandas as pd
import csv
from django.views.generic import ListView
from datetime import datetime
from django.core.paginator import Paginator


@login_required
def list_items(request):
    form = StockSearchForm(request.POST or None)
    client = request.user
    title = 'IOB'
    queryset = Stock.objects.all().filter(client=client)
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }

    if request.method == 'POST':
        queryset = queryset.filter(
            description__icontains=form['description'].value(),
            item_name__icontains=form['item_name'].value()
        )
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['description', 'ITEM NAME', 'QUANTITY'])
            for stock in queryset:
                writer.writerow(
                    [stock.description, stock.item_name, stock.quantity])
            return response
        context = {
            "title": title,
            "form": form,
            "queryset": queryset,
        }

    return render(request, "stocksmanagement/list_items.html", context)


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


def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('list_items')
    return render(request, 'stocksmanagement/confirm_delete.html', {"title": 'Confirm delete'})


def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stocksmanagement/stock_detail.html", context)


def check_format(df):
    if len(df.columns) != 34:
        return False
    if df.columns[0] != 'Item Acount Description':
        return False
    print('NICE FORMAT')
    return True


@login_required
def import_excel(request):
    if request.method == 'POST':
        file_name = request.FILES['myfile']
        imported_data = pd.read_excel(
            file_name.read(), header=10, sheet_name='IOB')
        if check_format(imported_data):
            for _, row in imported_data.iterrows():
                item = Stock(
                    client=request.user,
                    description=row['Item Acount Description'],
                    item_name=row['Item'],
                    ecus_code=row['Mã Ecus'],
                    item_desciption=row['Item Description'],
                    begin_quantity=row['Quantity'],
                    begin_price=row['Price'],
                    pr_purchase_quantity=row['Quantity.1'],
                    pr_purchase_price=row['Amount.1'],
                    mr_production_quantity=row['Quantity.2'],
                    mr_production_price=row['Amount.2'],
                    or_unplanned_quantity=row['Quantity.3'],
                    or_unplanned_price=row['Amount.3'],
                    stock_transfer_quantity=row['Quantity.4'],
                    stock_transfer_price=row['Amount.4'],
                    pi_issue_production_quantity=row['Quantity.5'],
                    pi_issue_production_price=row['Amount.5'],
                    di_sale_issue_quantity=row['Quantity.6'],
                    di_sale_issue_price=row['Amount.6'],
                    oi_unplanned_issue_quantity=row['Quantity.7'],
                    oi_unplanned_issue_price=row['Amount.7'],
                    stock_transfer_issue_quantity=row['Quantity.8'],
                    stock_transfer_issue_price=row['Amount.8'],
                )
                item.save()
            messages.success(request, 'Data Imported')
    return render(request, 'stocksmanagement/import_excel.html', {'title': 'Import as excel'})


['Item Acount Description', 'Item', 'Mã Ecus', 'Item Description',
 'Quantity', 'Amount', 'Price', 'Quantity.1', 'Amount.1', 'Price.1',
 'Quantity.2', 'Amount.2', 'Price.2', 'Quantity.3', 'Amount.3',
 'Price.3', 'Quantity.4', 'Amount.4', 'Price.4', 'Quantity.5',
 'Amount.5', 'Price.5', 'Quantity.6', 'Amount.6', 'Price.6',
 'Quantity.7', 'Amount.7', 'Price.7', 'Quantity.8', 'Amount.8',
 'Price.8', 'Quantity.9', 'Amount.9', 'Price.9']


'''----------ECUS---------'''


@login_required
def list_ecus(request):
    form = EcusSearchForm(request.POST or None)
    client = request.user
    title = 'List of Items'
    queryset = Ecus.objects.all().filter(client=client)
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }

    if request.method == 'POST':
        queryset = queryset.filter(
            type_code__icontains=form['type_code'].value(),
            from_country__icontains=form['from_country'].value()
        )
        context = {
            "title": title,
            "form": form,
            "queryset": queryset,
        }
        return render(request, "stocksmanagement/list_ecus.html", context)

    return render(request, "stocksmanagement/list_ecus.html", context)


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
    if len(df.columns) != 26:
        return False
    if df.columns[1] != 'Số TK':
        return False
    print('NICE FORMAT')
    return True


@login_required
def import_excel_ecus(request):
    if request.method == 'POST':
        file_name = request.FILES['myfile']
        try:
            imported_data = pd.read_excel(
                file_name.read(), sheet_name='Ecus')
        except ValueError:
            messages.warning(
                request, 'Wrong format, make sure the sheet contain informations name Ecus')
            return render(request, 'stocksmanagement/import_excel.html')
        if check_ecus_format(imported_data):
            for _, row in imported_data.iterrows():
                item = Ecus(
                    client=request.user,
                    account_number=row['Số TK'],
                    registered_date=row['Ngày ĐK'].date(),
                    type_code=row['Mã loại hình'],
                    goods_no=row['STT hàng'],
                    npl_sp_code=row['Mã NPL/SP'],
                    erp_code=row['Mã ERP'],
                    hs=row['Mã HS'],
                    item_name=row['Tên hàng'],
                    from_country=row['Xuất xứ'],
                    unit_price=row['Đơn giá'],
                    unit_price_taxed=row['Đơn giá tính thuế'],
                    total=row['Tổng số lượng'],
                    unit=row['Đơn vị tính'],
                    total_2=row['Tổng số lượng 2'],
                    unit_2=row['Đơn vị tính 2'],
                    nt_value=row['Trị giá NT'],
                    total_value=row['Tổng trị giá'],
                    tax_rate=row['Thuế suất XNK'],
                    tax_cost=row['Tiền thuế XNK'],
                    partner=row['Tên đối tác'],
                    bill=row['Số hóa đơn'],
                    bill_date=row['Ngày hóa đơn'].date(),
                    contract=row['Số hợp đồng'],
                )
                if not pd.isnull(row['Ngày hợp đồng']):
                    item.contract_date = row['Ngày hợp đồng'].date()
                item.save()
            messages.success(request, 'Data Imported')
            return redirect('list_ecus')
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
        return redirect('list_items_ecus')
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


class BOMListView(ListView):
    model = BOM
    template_name = 'stocksmanagement/list_bom.html'
    context_object_name = 'queryset'
    # ordering = ['-date_posted']
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BOMSearchForm(self.request.GET)
        context['title'] = 'BOM'
        return context

    def get_queryset(self):
        query_set = BOM.objects.all().filter(client=self.request.user)
        ecus_code = self.request.GET.get('ecus_code', '')
        tp_code = self.request.GET.get('tp_code', '')
        ecus = self.request.GET.get('ecus', '')
        if ecus_code:
            query_set = query_set.filter(
                ecus_code__icontains=ecus_code
            )
        if tp_code:
            query_set = query_set.filter(
                tp_code__icontains=tp_code
            )
        if ecus:
            query_set = query_set.filter(
                ecus__icontains=ecus
            )
        return query_set


@login_required
def list_bom(request):
    form = BOMSearchForm(request.POST or None)
    client = request.user
    title = 'List of BOM'
    queryset = BOM.objects.all().filter(client=client)
    paginator = Paginator(queryset, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
        "page_obj": page_obj
    }

    if request.method == 'POST':
        queryset = queryset.filter(
            tp_code__icontains=form['tp_code'].value(),
            ecus_code__icontains=form['ecus_code'].value(),
        ).filter(
            ecus__icontains=form['ecus'].value(),
        )
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['description', 'ITEM NAME', 'QUANTITY'])
            for ecus in queryset:
                writer.writerow(
                    [ecus.tp_code, ecus.tp_code, ecus.tp_code])
            return response
        context['queryset'] = queryset
    return render(request, "stocksmanagement/list_bom.html", context)


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
    format = ['Code TP', 'Mã Ecus', 'Tên', 'Decription', 'Unit', 'RM.code',
              'Ecus code', 'Name', 'Decription.1', 'Unit.1', 'BOM', 'Loss', 'Thành phẩm xuất', 'Quy đổi TP xuất', 'Thành phẩm tồn',
              'Quy đổi thành phẩm tồn']
    set1 = set(format)
    set2 = set(df.columns.tolist())
    is_subset = set1.issubset(set2)
    if not is_subset:
        return False
    return True


@login_required
def import_excel_bom(request):
    if request.method == 'POST':
        file_name = request.FILES['myfile']
        try:
            imported_data = pd.read_excel(
                file_name.read(), sheet_name='BOM')
        except ValueError:
            messages.warning(
                request, 'Wrong format, make sure the sheet contain informations name BOM')
            return render(request, 'stocksmanagement/import_excel.html')
        if check_bom_format(imported_data):
            imported_data = imported_data.iloc[1:, :]
            for _, row in imported_data.iterrows():
                item = BOM(
                    client=request.user,
                    tp_code=row['Code TP'],
                    ecus_code=row['Mã Ecus'],
                    name=row['Tên'],
                    rm_code=row['Decription'],
                    description=row['Unit'],
                    unit=row['RM.code'],
                    ecus=row['Ecus code'],
                    name_2=row['Name'],
                    description_2=row['Decription.1'],
                    unit_2=row['Unit.1'],
                    bom=row['BOM'],
                    loss=row['Loss'],
                    finish_product=row['Thành phẩm xuất'],
                    finish_product_convert=row['Quy đổi TP xuất'],
                    finish_product_inventory=row['Thành phẩm tồn'],
                    finish_product_exchange=row['Quy đổi thành phẩm tồn'],
                )
                item.save()
            messages.success(request, 'Data Imported')
            return redirect('list_bom')
        else:
            messages.warning(request, '''
            Wrong format, make sure table has at least these columns:
            'Code TP', 'Mã Ecus', 'Tên', 'Decription', 'Unit', 'RM.code',
            'Ecus code', 'Name', 'Decription.1', 'Unit.1', 'BOM', 'Loss', 
            'Thành phẩm xuất', 'Quy đổi TP xuất', 'Thành phẩm tồn',
            'Quy đổi thành phẩm tồn' 
            ''')
    return render(request, 'stocksmanagement/import_excel.html', {'title': 'Import as excel'})


['Code TP', 'Mã Ecus', 'Tên', 'Decription', 'Unit', 'RM.code',
 'Ecus code', 'Name', 'Decription.1', 'Unit.1', 'BOM', 'Loss',
 'BOM + Loss', 'Thành phẩm xuất', 'Quy đổi TP xuất', 'Thành phẩm tồn',
 'Quy đổi thành phẩm tồn']


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


@login_required
def list_balance(request):
    form = BalanceSearchForm(request.POST or None)
    client = request.user
    title = 'Balance'
    queryset = Balance.objects.all().filter(client=client)
    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }

    if request.method == 'POST':
        queryset = queryset.filter(
            ecus_code__icontains=form['ecus_code'].value(),
            description__icontains=form['description'].value()
        )
        context = {
            "title": title,
            "form": form,
            "queryset": queryset,
        }
        return render(request, "stocksmanagement/list_balance.html", context)

    return render(request, "stocksmanagement/list_balance.html", context)


class BalanceListView(ListView):
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
