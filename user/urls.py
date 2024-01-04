from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationApiView, AccountConfirmApiView, Login, UserApiView, EHubReportApiView, ResendActivationCode,\
    EditProfileApiView, UserResetPasswordApiView, UserResetPasswordConfirmApiView, AddEHubPurchasePersonApiView, EHubViewSets,\
    EHubPersonApiView, TotalEHubPurchaseApiView

app_name = "users"
router = DefaultRouter()
router.register('list/ehub', EHubViewSets, basename='bank-account')

urlpatterns = [
    path("registration/", RegistrationApiView.as_view(), name="registration"),
    path("login/", Login.as_view(), name="login"),
    path("", UserApiView.as_view(), name="user-details"),
    path("profile/edit/", EditProfileApiView.as_view(), name="user-profile-edit"),
    path('account/resend/code/', ResendActivationCode.as_view(), name="account-resend-code"),
    path('account/confirm/', AccountConfirmApiView.as_view(), name="account-confirm"),
    path('e-hub/product/add/', EHubReportApiView.as_view(), name="ehub-product-add"),
    path('e-hub/person/add/', AddEHubPurchasePersonApiView.as_view(), name="ehub-person-add"),
    path('e-hub/person/list/', EHubPersonApiView.as_view(), name="ehub-person-list"),
    path('e-hub/person/total/', TotalEHubPurchaseApiView.as_view(), name="ehub-person-total"),
    path('password/reset', UserResetPasswordApiView.as_view(), name="password-reset"),
    path('password/reset/confirm', UserResetPasswordConfirmApiView.as_view(), name="password-reset-confirm"),
    path("", include(router.urls)),

]