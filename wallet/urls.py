from django.urls import path
from .views import WalletApiView

app_name = "wallet"

urlpatterns = [
    path("balance/", WalletApiView.as_view(), name="wallet-balance"),
]