from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (CheckAccountView, CheckBalanceView, ConfirmTransferView,
                    AddPaymentInputView, AddPaymentAmountView, ConfirmPaymentView, CheckPaymentStatusView,
                    ConfirmPaymentView, CheckTransactionStatusView, CheckStatusView, AddAccountView, 
                    AddAmountView, ConfirmTransactionView)

urlpatterns = [
    path("transfer/check_status/", CheckStatusView.as_view(), name="check_transfer_status"),
    path("transfer/", AddAccountView.as_view(), name="add_account"),
    path("transfer/add_amount/", AddAmountView.as_view(), name="add_amount"),
    path("transfer/confirm/", ConfirmTransactionView.as_view(), name="confirm"),
    path("payment/", AddPaymentInputView.as_view(), name="add_input"),
    path("payment/add_amount/", AddPaymentAmountView.as_view(), name="add_amount"),
    path("payment/confirm/", ConfirmPaymentView.as_view(), name="confirm"),
    path("payment/check_status/", CheckPaymentStatusView.as_view(), name="check_payment_status"),

]