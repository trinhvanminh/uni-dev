from django.urls.conf import path

from .views import IndexView, profile

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('profile/', profile, name='profile'),
]
