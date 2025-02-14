from django.urls import path
from .views import api_overview

urlpatterns = [
    path('', api_overview, name="api-overview"),
]

from django.urls import path
from .views import criminal_list, criminal_detail, crime_list, crime_detail, crime_news_list, crime_news_detail

urlpatterns = [
    path('criminals/', criminal_list, name='criminal-list'),
    path('criminals/<int:pk>/', criminal_detail, name='criminal-detail'),
    path('crimes/', crime_list, name='crime-list'),
    path('crimes/<int:pk>/', crime_detail, name='crime-detail'),
    path('crime-news/', crime_news_list, name='crime-news-list'),
    path('crime-news/<int:pk>/', crime_news_detail, name='crime-news-detail'),
]

from django.urls import path
from .views import CriminalListCreateView  # Import your API views

urlpatterns = [
    path("criminals/", CriminalListCreateView.as_view(), name="criminal-list"),
]
