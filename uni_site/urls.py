from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients-api/', include('client.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('hscode.urls')),
    path('stocks/', include('stocksmanagement.urls')),
    path('auth-api/', include('dj_rest_auth.urls')),
    path('hs-api/', include('hscode.api.urls')),
    path('iob-api/', include('stocksmanagement.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
