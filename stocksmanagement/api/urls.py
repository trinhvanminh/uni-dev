from django.urls import include, path
from rest_framework import routers
from .views import StockViewSet, EcusViewSet, BOMViewSet, BalanceViewSet, IOBExcelImport, EcusExcelImport, BOMExcelImport

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
]
