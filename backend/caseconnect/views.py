from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.throttling import UserRateThrottle
from .models import Criminal, Crime, CrimeNews
from .serializers import CriminalSerializer, CrimeSerializer, CrimeNewsSerializer
from django.contrib.auth.models import User
from rest_framework import status


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

from django.contrib.auth.models import User
from django.http import JsonResponse
import json

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

# ✅ Custom Signup View
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully'}, status=201)

# ✅ Custom Login View with HTTP-Only Cookies
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Set HTTP-Only Cookies
        response.set_cookie(
            key='access_token',
            value=response.data['access'],
            httponly=True,
            secure=True,  # Set to True in production
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=response.data['refresh'],
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        return response

# ✅ Refresh Token View
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({'error': 'Refresh token is missing'}, status=400)

    try:
        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)

        response = Response({'access': access_token})
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response
    except Exception as e:
        return Response({'error': 'Invalid refresh token'}, status=400)

# ✅ Logout View (Blacklists Refresh Token)
@api_view(['POST'])
def logout(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=400)

    response = Response({'message': 'Logged out successfully'})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')

    return response
