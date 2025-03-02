from rest_framework import serializers
from .models import Criminal, Crime, CrimeNews

# ✅ Criminal Serializer
class CriminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criminal
        fields = '__all__'
        read_only_fields = ['id', 'created_at']  # Prevent modifications on ID & timestamp

    def validate_age(self, value):
        """Ensure the age is a positive number."""
        if value <= 0:
            raise serializers.ValidationError("Age must be a positive number.")
        return value

    def validate_name(self, value):
        """Ensure name is at least 2 characters long."""
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value


# ✅ Crime Serializer
class CrimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crime
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def validate_title(self, value):
        """Ensure crime title is at least 3 characters long."""
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    def validate_location(self, value):
        """Ensure location is provided."""
        if not value.strip():
            raise serializers.ValidationError("Location cannot be empty.")
        return value


# ✅ Crime News Serializer
class CrimeNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeNews
        fields = '__all__'
        read_only_fields = ['id', 'published_at']

    def validate_title(self, value):
        """Ensure news title is meaningful."""
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
