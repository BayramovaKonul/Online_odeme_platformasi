from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (RegisterUserView, UpdateUserProfile, CustomTokenObtainPairView, PasswordResetView)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterUserView.as_view(), name='register'),
    path('update-profile', UpdateUserProfile.as_view(), name='update_profile'),
    path('reset-password', PasswordResetView.as_view(), name='reset_password'),
]