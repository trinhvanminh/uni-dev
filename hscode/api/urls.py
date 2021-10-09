from django.urls.conf import path, include

from .views import ProductList
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'hs', ProductList)

urlpatterns = [
    path('', include(router.urls)),
]
