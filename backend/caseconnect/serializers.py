from rest_framework import serializers
from .models import Criminal, Crime, CrimeNews

class CriminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criminal
        fields = '__all__'

class CrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crime
        fields = '__all__'

class CrimeNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeNews
        fields = '__all__'
