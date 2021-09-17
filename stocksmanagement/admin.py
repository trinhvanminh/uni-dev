from django.contrib import admin
from .models import Stock, Ecus, BOM, Balance
from .forms import StockCreateForm, EcusCreateForm


class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['description', 'client', 'item_name']
    form = StockCreateForm
    list_filter = ['description']
    search_fields = ['description', 'item_name']


class EcusCreateAdmin(admin.ModelAdmin):
    list_display = ['type_code', 'from_country']
    form = EcusCreateForm
    list_filter = ['from_country']
    search_fields = ['type_code', 'from_country']


admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Ecus, EcusCreateAdmin)
admin.site.register(BOM)
admin.site.register(Balance)
