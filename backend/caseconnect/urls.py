from django.urls import path
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
    
    path('admin/', admin.site.urls),
    path('api/', include('caseconnect.urls')),  
]
