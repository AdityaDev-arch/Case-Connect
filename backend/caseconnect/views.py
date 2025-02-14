from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

from .models import Criminal, Crime, CrimeNews

def api_overview(request):
    return JsonResponse({"message": "Welcome to Case Connect API!"})

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Criminal, Crime, CrimeNews
from .serializers import CriminalSerializer, CrimeSerializer, CrimeNewsSerializer

# CRUD for Criminals
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def criminal_list(request):
    if request.method == 'GET':
        criminals = Criminal.objects.all()
        serializer = CriminalSerializer(criminals, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CriminalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def criminal_detail(request, pk):
    try:
        criminal = Criminal.objects.get(pk=pk)
    except Criminal.DoesNotExist:
        return Response({'error': 'Criminal not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CriminalSerializer(criminal)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CriminalSerializer(criminal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        criminal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CRUD for Crimes
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def crime_list(request):
    if request.method == 'GET':
        crimes = Crime.objects.all()
        serializer = CrimeSerializer(crimes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CrimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def crime_detail(request, pk):
    try:
        crime = Crime.objects.get(pk=pk)
    except Crime.DoesNotExist:
        return Response({'error': 'Crime not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CrimeSerializer(crime)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CrimeSerializer(crime, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        crime.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CRUD for Crime News
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def crime_news_list(request):
    if request.method == 'GET':
        news = CrimeNews.objects.all()
        serializer = CrimeNewsSerializer(news, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CrimeNewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def crime_news_detail(request, pk):
    try:
        news = CrimeNews.objects.get(pk=pk)
    except CrimeNews.DoesNotExist:
        return Response({'error': 'Crime news not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CrimeNewsSerializer(news)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CrimeNewsSerializer(news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to Case Connect</h1>")

from rest_framework import generics
from .models import Criminal
from .serializers import CriminalSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.throttling import UserRateThrottle

class CriminalListCreateView(generics.ListCreateAPIView):
    queryset = Criminal.objects.all()
    serializer_class = CriminalSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]  # Limit requests per user


