from hscode.views import export
from django.db.models import query
from django.utils.datastructures import MultiValueDictKeyError
from client.models import Client
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Balance, Stock, Ecus, BOM
from .forms import BOMCreateForm, BOMSearchForm, BOMUpdateForm, BalanceSearchForm, EcusSearchForm, EcusUpdateForm, StockCreateForm, StockSearchForm, StockUpdateForm, EcusCreateForm
from django.contrib.auth.decorators import login_required
import pandas as pd
import csv
from django.views.generic import ListView


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
        print(export_to_csv)
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
    format = ['Item Acount Description', 'Item', 'Mã Ecus', 'Item Description',
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
            for _, row in imported_data.iterrows():
                item = Stock(client=request.user)

                if row['Item Acount Description']:
                    item.description = row['Item Acount Description'],
                if row['Item']:
                    item.item_name = row['Item']
                if row['Mã Ecus']:
                    item.ecus_code = row['Mã Ecus']
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
            messages.warning(request, '''Wrong format, please make sure the excel table contains at least these columns ['Item Acount Description', 'Item', 'Mã Ecus', 'Item Description',
                                        'Quantity', 'Amount', 'Price', 'Quantity.1', 'Amount.1', 'Price.1',
                                        'Quantity.2', 'Amount.2', 'Price.2', 'Quantity.3', 'Amount.3',
                                        'Price.3', 'Quantity.4', 'Amount.4', 'Price.4', 'Quantity.5',
                                        'Amount.5', 'Price.5', 'Quantity.6', 'Amount.6', 'Price.6',
                                        'Quantity.7', 'Amount.7', 'Price.7', 'Quantity.8', 'Amount.8',
                                        'Price.8', 'Quantity.9', 'Amount.9', 'Price.9']''')
            return redirect('import_excel')
    return render(request, 'stocksmanagement/import_excel.html', {'title': 'Import as excel'})


['Item Acount Description', 'Item', 'Mã Ecus', 'Item Description',
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
    format = ['Số TK', 'Ngày ĐK', 'Mã loại hình', 'STT hàng', 'Mã NPL/SP', 'Mã ERP', 'Mã HS', 'Tên hàng', 'Xuất xứ', 'Đơn giá', 'Đơn giá tính thuế', 'Tổng số lượng', 'Đơn vị tính',
              'Tổng số lượng 2', 'Đơn vị tính 2', 'Trị giá NT', 'Tổng trị giá', 'Thuế suất XNK', 'Tiền thuế XNK', 'Tên đối tác', 'Số hóa đơn', 'Ngày hóa đơn', 'Số hợp đồng', 'Ngày hợp đồng']
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
                if row['Số TK']:
                    item.account_number = row['Số TK']
                if row['Ngày ĐK']:
                    item.registered_date = row['Ngày ĐK'].date()
                if row['Mã loại hình']:
                    item.type_code = row['Mã loại hình']
                if row['STT hàng']:
                    item.goods_no = row['STT hàng']
                if row['Mã NPL/SP']:
                    item.npl_sp_code = row['Mã NPL/SP']
                if row['Mã ERP']:
                    item.erp_code = row['Mã ERP']
                if row['Mã HS']:
                    item.hs = row['Mã HS']
                if row['Tên hàng']:
                    item.item_name = row['Tên hàng']
                if row['Xuất xứ']:
                    item.from_country = row['Xuất xứ']
                if row['Đơn giá']:
                    item.unit_price = row['Đơn giá']
                if row['Đơn giá tính thuế']:
                    item.unit_price_taxed = row['Đơn giá tính thuế']
                if row['Tổng số lượng']:
                    item.total = row['Tổng số lượng']
                if row['Đơn vị tính']:
                    item.unit = row['Đơn vị tính']
                if row['Tổng số lượng 2']:
                    item.total_2 = row['Tổng số lượng 2']
                if row['Đơn vị tính 2']:
                    item.unit_2 = row['Đơn vị tính 2']
                if row['Trị giá NT']:
                    item.nt_value = row['Trị giá NT']
                if row['Tổng trị giá']:
                    item.total_value = row['Tổng trị giá']
                if row['Thuế suất XNK']:
                    item.tax_rate = row['Thuế suất XNK']
                if row['Tiền thuế XNK']:
                    item.tax_cost = row['Tiền thuế XNK']
                if row['Tên đối tác']:
                    item.partner = row['Tên đối tác']
                if row['Số hóa đơn']:
                    item.bill = row['Số hóa đơn']
                if row['Ngày hóa đơn']:
                    item.bill_date = row['Ngày hóa đơn'].date()
                if row['Số hợp đồng']:
                    item.contract = row['Số hợp đồng']
                if not pd.isnull(row['Ngày hợp đồng']):
                    item.contract_date = row['Ngày hợp đồng'].date()
                item.save()
            messages.success(request, 'Data Imported')
            return redirect('list_ecus')
        else:
            messages.warning(request, '''Wrong format, make sure your file has at least these column ['Số TK', 'Ngày ĐK', 'Mã loại hình', 'STT hàng', 'Mã NPL/SP', 'Mã ERP', 'Mã HS', 'Tên hàng', 'Xuất xứ', 'Đơn giá', 'Đơn giá tính thuế', 'Tổng số lượng', 'Đơn vị tính',
              'Tổng số lượng 2', 'Đơn vị tính 2', 'Trị giá NT', 'Tổng trị giá', 'Thuế suất XNK', 'Tiền thuế XNK', 'Tên đối tác', 'Số hóa đơn', 'Ngày hóa đơn', 'Số hợp đồng', 'Ngày hợp đồng']''')
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
            'Thành phẩm xuất',
            'Quy đổi TP xuất',
            'Thành phẩm tồn',
            'Quy đổi thành phẩm tồn'
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
                if row['Code TP']:
                    item.tp_code = row['Code TP']
                if row['Mã Ecus']:
                    item.ecus_code = row['Mã Ecus']
                if row['Tên']:
                    item.name = row['Tên']
                if row['Decription']:
                    item.rm_code = row['Decription']
                if row['Unit']:
                    item.description = row['Unit']
                if row['RM.code']:
                    item.unit = row['RM.code']
                if row['Ecus code']:
                    item.ecus = row['Ecus code']
                if row['Name']:
                    item.name_2 = row['Name']
                if row['Decription.1']:
                    item.description_2 = row['Decription.1']
                if row['Unit.1']:
                    item.unit_2 = row['Unit.1']
                if row['BOM']:
                    item.bom = row['BOM']
                if row['Loss']:
                    item.loss = row['Loss']
                if row['Thành phẩm xuất']:
                    item.finish_product = row['Thành phẩm xuất']
                if row['Quy đổi TP xuất']:
                    item.finish_product_convert = row['Quy đổi TP xuất']
                if row['Thành phẩm tồn']:
                    item.finish_product_inventory = row['Thành phẩm tồn']
                if row['Quy đổi thành phẩm tồn']:
                    item.finish_product_exchange = row['Quy đổi thành phẩm tồn']
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
            return redirect('import_excel_bom')
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
    content_disposition += '.csv"'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    writer.writerow(
        [
            'ERP code',
            'Ecus Code',
            'Decription',
            'E21',
            'B13',
            'A42',
            'E52',
            'RM Stock',
            'FG Stock',
            'WIP',
            'BALANCE',
        ]
    )
    for stock in query_set:
        writer.writerow(
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
    return response
