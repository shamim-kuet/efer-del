from django.urls import path
from .views import AddReferralApiView, AddReferralOrderApiView, MonthlyReferralApiView, UserReferral, UserReferralPerson,\
        ReminderEmailApiView, DownloadReferralBannerApiView, YearlyReferralApiView, ReferralPersonInfoUpdateApiView

app_name = "referral"

urlpatterns = [
    path("referral/", UserReferral.as_view(), name="user-referral"),
    path("referral-person/", UserReferralPerson.as_view(), name="user-referral-person"),
    path("referral-person/reminder/", ReminderEmailApiView.as_view(), name="user-referral-person-reminder"),
    path("add/", AddReferralApiView.as_view(), name="add-referral"),
    path("profile/edit/", ReferralPersonInfoUpdateApiView.as_view(), name="profile-edit"),
    path("purchase/", AddReferralOrderApiView.as_view(), name="referral-purchase"),
    path("monthly/", MonthlyReferralApiView.as_view(), name="referral-purchase-monthly"),
    path("yearly/", YearlyReferralApiView.as_view(), name="referral-purchase-yearly"),
    path("banner/", DownloadReferralBannerApiView.as_view(), name="referral-banner"),
]