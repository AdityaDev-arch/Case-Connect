from django.db import models

class Criminal(models.Model):  # Not Criminals
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    photo_url = models.URLField()
    address = models.TextField()
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Crime(models.Model):  # Not Crimes
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_occurred = models.DateField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class CrimeNews(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

class CriminalCrime(models.Model):
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
