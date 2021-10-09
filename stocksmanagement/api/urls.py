from django.urls import include, path
from rest_framework import routers
from .views import StockViewSet

router = routers.DefaultRouter()
router.register(r'', StockViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('stocks', include(router.urls)),
]
