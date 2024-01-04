from django.urls import path
from .views import GetAllCountryApiView, GetAddressByCountryApiView, GetFranchiseAddressByCountryApiView, \
    FranchiseMetaAPIView, TermsAPIView, PrivacyAPIView, SiteMetaAPIView, SiteSocialLinkMetaAPIView, \
    ContactUsApiview, HowThisWorkAPIView, MapApiView, EHubPurchasePersonApiView, OwnHubApiView,\
    AvailableHubApiView, SingleHubDetails

app_name = "meta"

urlpatterns = [
    path("country/", GetAllCountryApiView.as_view(), name="country"),
    path("address/", GetAddressByCountryApiView.as_view(), name="address"),
    path("franchise/address/", GetFranchiseAddressByCountryApiView.as_view(), name="franchise-address"),
    path("franchise/meta/", FranchiseMetaAPIView.as_view(), name="hub-meta"),
    path("how-this-work/", HowThisWorkAPIView.as_view(), name="how-this-work"),
    path("terms/", TermsAPIView.as_view(), name="terms"),
    path("privacy/", PrivacyAPIView.as_view(), name="privacy"),
    path("site/", SiteMetaAPIView.as_view(), name="site-meta"),
    path("social/", SiteSocialLinkMetaAPIView.as_view(), name="social-meta"),
    path("contact-us/", ContactUsApiview.as_view(), name="contact-us"),
    path("map/", MapApiView.as_view(), name="map"),
    path("e-hub/purchase/", EHubPurchasePersonApiView.as_view(), name="ehub-purchase"),
    path("e-hub/own/", OwnHubApiView.as_view(), name="ehub-own"),
    path("e-hub/available/", AvailableHubApiView.as_view(), name="ehub-available"),
    path("e-hub/details/<int:pk>/", SingleHubDetails.as_view(), name="ehub-details"),
]
