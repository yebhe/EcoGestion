from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UpdateUserInfoView,
    UpdatePasswordView,
    AccountActivateView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('user/me/', UserProfileView.as_view(), name='user-profile'),
    path('update-user-info/', UpdateUserInfoView.as_view(), name='update-user-info'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password'),
    path('activate/<str:uidb64>/<str:token>/', AccountActivateView.as_view(), name='activate'),
]