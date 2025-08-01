# Remplacez le contenu de votre backend/backend/urls.py par ceci :

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView  
from ecodeli_auth.views import AccountActivateView, CustomPasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('ecodeli_auth.urls')),
    path('api/', include('livreur.urls')),
    path('activate/<uidb64>/<token>/', AccountActivateView.as_view(), name='activate'),
    path('password/reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password-reset'),    
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('djoser.urls')),  
    path('auth/', include('django.contrib.auth.urls')),
]

# WhiteNoise s'occupe des fichiers statiques automatiquement
# Mais on garde ces lignes pour la compatibilité
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)