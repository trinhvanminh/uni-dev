from django.contrib import admin
from .models import ItemsTakeIn, ItemsTakeOut, IOB
# Register your models here.

admin.site.register(ItemsTakeIn)
admin.site.register(ItemsTakeOut)
admin.site.register(IOB)
