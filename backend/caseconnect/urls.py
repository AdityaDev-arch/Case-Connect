from django.urls import path
from .views import (
    signup, logout, refresh_token, CustomTokenObtainPairView,
    api_overview, home, public_criminal_list,
    CriminalListCreateView, CriminalDetailView,
    CrimeListCreateView, CrimeDetailView,
    CrimeNewsListCreateView, CrimeNewsDetailView
)

urlpatterns = [
    # ✅ Home & API Overview
    path('', home, name='home'),  # Default home route
    path('api/', api_overview, name='api_overview'),  # API documentation

    # ✅ Authentication Routes
    path('api/signup/', signup, name='signup'),  # User Registration
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (JWT Token)
    path('api/token/refresh/', refresh_token, name='token_refresh'),  # Refresh Token
    path('api/logout/', logout, name='logout'),  # Logout (Blacklist Token)

    # ✅ Criminal Endpoints (Admin Only)
    path('api/criminals/', CriminalListCreateView.as_view(), name='criminal-list'),  # List & Create
    path('api/criminals/<int:pk>/', CriminalDetailView.as_view(), name='criminal-detail'),  # Retrieve, Update, Delete

    # ✅ Crime Endpoints (Admin Only)
    path('api/crimes/', CrimeListCreateView.as_view(), name='crime-list'),  # List & Create
    path('api/crimes/<int:pk>/', CrimeDetailView.as_view(), name='crime-detail'),  # Retrieve, Update, Delete

    # ✅ Crime News Endpoints (Admin Only)
    path('api/crime-news/', CrimeNewsListCreateView.as_view(), name='crime-news-list'),  # List & Create
    path('api/crime-news/<int:pk>/', CrimeNewsDetailView.as_view(), name='crime-news-detail'),  # Retrieve, Update, Delete

    # ✅ Public API: List Criminals (Accessible to All Users)
    path('api/public/criminals/', public_criminal_list, name='public-criminal-list'),
]
