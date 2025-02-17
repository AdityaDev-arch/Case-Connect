from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.throttling import UserRateThrottle
from .models import Criminal, Crime, CrimeNews
from .serializers import CriminalSerializer, CrimeSerializer, CrimeNewsSerializer


# API Overview
@api_view(['GET'])
def api_overview(request):
    return JsonResponse({"message": "Welcome to Case Connect API!"})


# Home View
def home(request):
    return HttpResponse("<h1>Welcome to Case Connect</h1>")


# CRUD for Criminals
class CriminalListCreateView(generics.ListCreateAPIView):
    queryset = Criminal.objects.all()
    serializer_class = CriminalSerializer
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]  # Limit requests per user


class CriminalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Criminal.objects.all()
    serializer_class = CriminalSerializer
    permission_classes = [IsAdminUser]


# CRUD for Crimes
class CrimeListCreateView(generics.ListCreateAPIView):
    queryset = Crime.objects.all()
    serializer_class = CrimeSerializer
    permission_classes = [IsAdminUser]


class CrimeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crime.objects.all()
    serializer_class = CrimeSerializer
    permission_classes = [IsAdminUser]


# CRUD for Crime News
class CrimeNewsListCreateView(generics.ListCreateAPIView):
    queryset = CrimeNews.objects.all()
    serializer_class = CrimeNewsSerializer
    permission_classes = [IsAdminUser]


class CrimeNewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CrimeNews.objects.all()
    serializer_class = CrimeNewsSerializer
    permission_classes = [IsAdminUser]


# Public API: Get Criminals List (For Frontend)
@api_view(['GET'])
def public_criminal_list(request):
    criminals = Criminal.objects.all()
    serializer = CriminalSerializer(criminals, many=True)
    return Response(serializer.data)
