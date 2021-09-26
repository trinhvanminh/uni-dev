from django.urls.conf import path
from .views import (
    delete_items, delete_items, add_items, update_items, stock_detail, import_excel, IOBListView, export_csv_iob,
    EcusListView, update_ecus, import_excel_ecus, add_items_ecus, delete_items_ecus, ecus_detail, export_csv_ecus,
    update_bom, import_excel_bom, add_items_bom, delete_items_bom, bom_detail, BOMListView, export_csv_bom,
    BalanceListView, export_csv_balance
)

urlpatterns = [
    path('list-items/', IOBListView.as_view(), name='list_items'),
    path('add-items/', add_items, name='add_items'),
    path('update-items/<str:pk>/', update_items, name="update_items"),
    path('delete-items/<str:pk>/', delete_items, name="delete_items"),
    path('stock-detail/<str:pk>/', stock_detail, name="stock_detail"),
    path('import-excel/', import_excel, name="import_excel"),
    path('export-csv-iob/',
         export_csv_iob,  name='export_csv_iob'),

    path('ecus/', EcusListView.as_view(), name="list_ecus"),
    path('add-items-ecus/', add_items_ecus, name='add_items_ecus'),
    path('update-ecus-item/<str:pk>/', update_ecus, name="update_ecus"),
    path('ecus-detail/<str:pk>/', ecus_detail, name="ecus_detail"),
    path('import-excel-ecus/', import_excel_ecus, name="import_excel_ecus"),
    path('delete-items-ecus/<str:pk>/',
         delete_items_ecus, name="delete_items_ecus"),
    path('export-csv-ecus/',
         export_csv_ecus,  name='export_csv_ecus'),

    path('bom/', BOMListView.as_view(), name="list_bom"),
    path('add-items-bom/', add_items_bom, name='add_items_bom'),
    path('update-bom-item/<str:pk>/', update_bom, name="update_bom"),
    path('bom-detail/<str:pk>/', bom_detail, name="bom_detail"),
    path('import-excel-bom/', import_excel_bom, name="import_excel_bom"),
    path('delete-items-bom/<str:pk>/', delete_items_bom, name="delete_items_bom"),
    path('export-csv-bom/',
         export_csv_bom,  name='export_csv_bom'),

    path('balance/', BalanceListView.as_view(), name="list_balance"),
    path('export-csv-balance/',
         export_csv_balance,  name='export_csv_balance'),
]
