from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from wallet.views import WalletIndex

schema_view = get_schema_view(
   openapi.Info(
      title="BRITISH MARKETPLACE E-FRANCHISE/E-HUB API",
      default_version='v1',
      description="Documentation of british marketplace e-franchise/e-hub api",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/wallet/', WalletIndex.as_view(), name="home"),
    path("api/users/", include("user.urls", namespace="users")),
    path("api/referral/", include("referral.urls", namespace="referral")),
    path("api/wallet/", include("wallet.urls", namespace="wallet")),
    path("api/withdraw/", include("withdraw.urls", namespace="withdraw")),
    path("api/meta/", include("meta.urls", namespace="meta")),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
