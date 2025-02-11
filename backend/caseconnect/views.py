from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def api_overview(request):
    return JsonResponse({"message": "Welcome to Case Connect API!"})
