from django.db import models

class CrimeNews(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Crimes(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_committed = models.DateField()

    def __str__(self):
        return self.name

class Criminals(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.TextField()

    def __str__(self):
        return self.name

class CriminalCrime(models.Model):
    criminal = models.ForeignKey(Criminals, on_delete=models.CASCADE)
    crime = models.ForeignKey(Crimes, on_delete=models.CASCADE)
    date_of_arrest = models.DateField()

    def __str__(self):
        return f"{self.criminal.name} - {self.crime.name}"
