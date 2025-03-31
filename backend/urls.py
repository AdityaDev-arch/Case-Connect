from django.contrib import admin
from django.urls import path, include
from caseconnect.views import home, RegisterView, LoginView  # Import the home, register, and login views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('caseconnect.urls')),  # Ensure caseconnect has `urls.py`
    path("", home, name="home"),  # Home page
    path("admin/", admin.site.urls),  # Django admin panel
    path("api/", include("caseconnect.urls")),  # Include application URLs
    path("__debug__/", include("debug_toolbar.urls")),  # Django Debug Toolbar

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
