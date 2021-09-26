from django.contrib import admin
from .models import Section, Chapter, Heading, SubHeading, Note, Product
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProductResource(resources.ModelResource):
    class meta:
        model = Product


class ProductAdmin(ImportExportModelAdmin):
    list_display = ('name', 'heading', 'subheading')


admin.site.register(Heading)
admin.site.register(SubHeading)
admin.site.register(Product, ProductAdmin)
