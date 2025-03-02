from django.db import models
from django.contrib.auth.models import AbstractUser

# ✅ Criminal Model
class Criminal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    photo_url = models.URLField()
    address = models.TextField()
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  # Show Criminal name in Django Admin

    class Meta:
        ordering = ['-created_at']  # Order by latest criminals


# ✅ Crime Model
class Crime(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_occurred = models.DateField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  # Show Crime title in Django Admin

    class Meta:
        ordering = ['-date_occurred']  # Order by latest crimes


# ✅ Crime News Model
class CrimeNews(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title  # Show Crime News title in Django Admin

    class Meta:
        ordering = ['-published_at']  # Order by latest news


# ✅ Relationship Model (Criminal & Crime)
class CriminalCrime(models.Model):
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.criminal.name} - {self.crime.title}"

    class Meta:
        unique_together = ['criminal', 'crime']  # Prevent duplicate relations

#Signup 
# ✅ Custom User Model
class CustomUser(AbstractUser):  
    email = models.EmailField(unique=True)  # Ensure unique emails
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username  # Show username in Django Admin