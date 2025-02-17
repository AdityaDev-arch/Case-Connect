from django.contrib import admin
from django.urls import path, include
from caseconnect.views import home  # Import the home view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", home, name="home"),  # Home page
    path("admin/", admin.site.urls),  # Django admin panel
    path("api/", include("caseconnect.urls")),  # API URLs for Case Connect
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("__debug__/", include("debug_toolbar.urls")),  # Django Debug Toolbar
]
