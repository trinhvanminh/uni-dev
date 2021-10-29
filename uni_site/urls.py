from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from dj_rest_auth.views import PasswordResetConfirmView
from client.views import CustomRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('hscode.urls')),
    path('stocks/', include('stocksmanagement.urls')),
]

api_url = [
    path('iob-api/', include('iob_demo.api.urls')),
    path('hs-api/', include('hscode.api.urls')),
    path('auth-api/', include('dj_rest_auth.urls')),
    path('auth-api/registration/', CustomRegisterView.as_view()),
    path('auth-api/registration/', include('dj_rest_auth.registration.urls')),
    path('password/reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth-api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth-api/token/refresh/',
         jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('iob-api/', include('stocksmanagement.api.urls')),
    path('clients-api/', include('client.urls')),
]

urlpatterns += api_url

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
