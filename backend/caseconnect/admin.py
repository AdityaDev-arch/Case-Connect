

# Register your models here.
from django.contrib import admin
from .models import CrimeNews, Crime, CriminalCrime, Criminal

admin.site.register(CrimeNews)
admin.site.register(Crime)
admin.site.register(CriminalCrime)
admin.site.register(Criminal)
