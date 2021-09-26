import pandas as pd
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView, View
from marketing.models import Signup

from .admin import ProductResource
from .models import Heading, Product, SubHeading


class AdminStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'uni/index.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        try:
            Signup.objects.get(email=email)
            messages.info(request, "You're already subcribed, thanks though.")
            return redirect('home')
        except Signup.DoesNotExist:
            new_signup = Signup()
            new_signup.email = email
            new_signup.save()
            messages.success(
                request, "Thank you for your subscription, now you'll be charge 15$ a month...")
            return redirect('home')


def profile(request):
    context = {
        'title': request.user
    }
    return render(request, "uni/profile.html", context)


def export(request):
    product_resource = ProductResource()
    dataset = product_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="list_hs.csv"'
    return response


def check_hs_format(df):
    format = ['HS', 'PRODUCT NAME VIETNAMESE']
    set1 = set(format)
    set2 = set(df.columns.tolist())
    is_subset = set1.issubset(set2)
    if not is_subset:
        return False
    return True


class SearchView(ListView):

    model = Product
    template_name = 'hs/search_hs.html'
    context_object_name = 'queryset'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HS LOOKUP'
        return context

    def get_queryset(self):
        self.queryset = Product.objects.all()
        query = self.request.GET.get('q')
        if query:
            self.queryset = self.queryset.filter(
                Q(name__icontains=query) |
                Q(heading__no__icontains=query) |
                Q(subheading__no__icontains=query)
            ).distinct()
        return self.queryset


class ExportHS(AdminStaffRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hs/import_hs.html')

    def post(self, request, *args, **kwargs):
        try:
            file_name = request.FILES['myfile']
        except MultiValueDictKeyError:
            messages.warning(request, 'Please choose your file')
            return redirect('import_hs')
        try:
            imported_data = pd.read_excel(
                file_name.read(), sheet_name='VIETNAM', dtype={'HS': object})
        except Exception:
            messages.warning(
                request, 'Wrong format, make sure the file you import is excel and the sheet contain informations name VIETNAME')
            return redirect('import_hs')
        if check_hs_format(imported_data):
            imported_data = imported_data[['HS', 'PRODUCT NAME VIETNAMESE']]
            imported_data.fillna(method='ffill', inplace=True)
            for _, row in imported_data.iterrows():
                product = Product(name=row['PRODUCT NAME VIETNAMESE'])
                if len(row['HS']) == 4:
                    heading, _ = Heading.objects.get_or_create(
                        no=row['HS']
                    )
                    product.heading = heading
                    product.save()
                    heading.save()

                else:
                    heading, _ = Heading.objects.get_or_create(
                        no=row['HS'][0:4]
                    )
                    subheading, _ = SubHeading.objects.get_or_create(
                        no=row['HS'],
                        heading=heading
                    )
                    product.subheading = subheading
                    product.heading = heading
                    heading.save()
                    product.save()
                    subheading.save()
            messages.success(request, 'Data Imported')
            return redirect('home')
        else:
            messages.warning(request, '''
            Wrong format, make sure table has at least these columns:
            'Code TP', 'Mã Ecus', 'Tên', 'Decription', 'Unit', 'RM.code',
            'Ecus code', 'Name', 'Decription.1', 'Unit.1', 'BOM', 'Loss', 
            'Thành phẩm xuất', 'Quy đổi TP xuất', 'Thành phẩm tồn',
            'Quy đổi thành phẩm tồn' 
            ''')
            return redirect('import_hs')
