from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BankAccountViewSets, WithdrawApiView, WithdrawUserReportApiView, DeleteWithdrawApiView

app_name = "withdraw"

router = DefaultRouter()
router.register('bank-account', BankAccountViewSets, basename='bank-account')

urlpatterns = [
    path("request/", WithdrawApiView.as_view(), name="get-withdraw"),
    path("summary/", WithdrawUserReportApiView.as_view(), name="summary-withdraw"),
    path("delete/<int:pk>/", DeleteWithdrawApiView.as_view(), name="delete-withdraw"),
    path("", include(router.urls)),
]