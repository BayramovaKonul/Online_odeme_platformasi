from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (CheckAccountView, CheckBalanceView, ConfirmTransferView, StartTransferView)

urlpatterns = [
    path('transfer', StartTransferView.as_view(), name='start_transfer'),
    path('check-account', CheckAccountView.as_view(), name='check_account'),
    path('check-balance', CheckBalanceView.as_view(), name='check_balance'),
    path('confirm-transfer', ConfirmTransferView.as_view(), name='confirm_transfer'),
]