from django.urls import include, path
from rest_framework import routers
from .views import IOBViewSet, TestTing, TakeInViewSet, TakeOutViewSet

router = routers.DefaultRouter(trailing_slash=True)
router.register(r'iob', IOBViewSet, basename='iob')
router.register(r'take-in', TakeInViewSet, basename='take-in')
router.register(r'take-out', TakeOutViewSet, basename='take-out')

urlpatterns = [
    path('', include(router.urls)),
    path('testing/', TestTing.as_view())
]
