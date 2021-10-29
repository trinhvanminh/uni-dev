from django.urls import include, path
from rest_framework import routers
from .views import StockViewSet, EcusViewSet, BOMViewSet, BalanceViewSet, IOBExcelImport, EcusExcelImport, BOMExcelImport, IOBExcelExport, BalanceExcelExport, EcusExcelExport, BOMExcelExport

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'iob', StockViewSet, basename='stock-detail')
router.register(r'ecus', EcusViewSet, basename='ecus-detail')
router.register(r'bom', BOMViewSet, basename='bom-detail')
router.register(r'balance', BalanceViewSet, basename='balance-detail')

urlpatterns = [
    path('stocks/', include(router.urls)),
    path('upload-iob/', IOBExcelImport.as_view(), name='upload-iob'),
    path('upload-ecus/', EcusExcelImport.as_view(), name='upload-ecus'),
    path('upload-bom/', BOMExcelImport.as_view(), name='upload-bom'),
    path('export-iob/', IOBExcelExport.as_view(), name='export-iob'),
    path('export-balance/', BalanceExcelExport.as_view(), name='export-balance'),
    path('export-ecus/', EcusExcelExport.as_view(), name='export-ecus'),
    path('export-bom/', BOMExcelExport.as_view(), name='export-bom'),
]
