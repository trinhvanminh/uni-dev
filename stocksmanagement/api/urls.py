from django.urls import include, path
from rest_framework import routers
from .views import StockViewSet, EcusViewSet, BOMViewSet, BalanceViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'iob', StockViewSet, basename='stock-detail')
router.register(r'ecus', EcusViewSet, basename='ecus-detail')
router.register(r'bom', BOMViewSet, basename='bom-detail')
router.register(r'balance', BalanceViewSet, basename='balance-detail')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('stocks/', include(router.urls)),
]
