from django.contrib import admin

from .models import Stock, Ecus, BOM, Balance, File
from .forms import BOMCreateForm, StockCreateForm, EcusCreateForm


class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['description', 'client', 'item_name']
    form = StockCreateForm
    list_filter = ['description', 'client']
    search_fields = ['description', 'item_name']


class EcusCreateAdmin(admin.ModelAdmin):
    list_display = ['type_code', 'from_country']
    form = EcusCreateForm
    list_filter = ['from_country', 'client']
    search_fields = ['type_code', 'from_country']


class BOMCreateAdmin(admin.ModelAdmin):
    list_display = ['tp_code', 'ecus_code']
    form = BOMCreateForm
    list_filter = ['client']
    search_fields = ['client']


admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Ecus, EcusCreateAdmin)
admin.site.register(BOM, BOMCreateAdmin)
admin.site.register(Balance)
admin.site.register(File)
