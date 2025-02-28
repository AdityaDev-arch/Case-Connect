from django.contrib import admin
from django.urls import path, include
from django.urls import path
from .views import signup, logout, refresh_token, CustomTokenObtainPairView
from .views import (
    api_overview, home, public_criminal_list,
    CriminalListCreateView, CriminalDetailView,
    CrimeListCreateView, CrimeDetailView,
    CrimeNewsListCreateView, CrimeNewsDetailView
)

urlpatterns = [
    path('', home, name='home'),
    path('api/', api_overview, name='api_overview'),

    # Criminals
    path('api/criminals/', CriminalListCreateView.as_view(), name='criminal-list'),
    path('api/criminals/<int:pk>/', CriminalDetailView.as_view(), name='criminal-detail'),

    # Crimes
    path('api/crimes/', CrimeListCreateView.as_view(), name='crime-list'),
    path('api/crimes/<int:pk>/', CrimeDetailView.as_view(), name='crime-detail'),

    # Crime News
    path('api/crime-news/', CrimeNewsListCreateView.as_view(), name='crime-news-list'),
    path('api/crime-news/<int:pk>/', CrimeNewsDetailView.as_view(), name='crime-news-detail'),

    # Public Endpoint (For Frontend)
    path('api/public/criminals/', public_criminal_list, name='public-criminal-list'),

    # Admin Panel
    path('admin/', admin.site.urls),

    # 🔹 Only include other app URLs if this is the main `urls.py` (not inside `caseconnect`)
    # path('api/', include('another_app.urls')),  # Uncomment if you have a different app
]

urlpatterns = [
    path('api/signup/', signup, name='signup'),  # Signup API
        path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', refresh_token, name='token_refresh'),
    path('api/logout/', logout, name='logout'),
]


urlpatterns = [
    path('api/signup/', signup, name='signup'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', refresh_token, name='token_refresh'),
    path('api/logout/', logout, name='logout'),
]
