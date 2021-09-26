from django.urls.conf import path

from .views import IndexView, profile, ExportHS, SearchView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('profile/', profile, name='profile'),
    path('import-hs/', ExportHS.as_view(), name='import_hs'),
    path('search-hs/', SearchView.as_view(), name='search_hs'),
]
