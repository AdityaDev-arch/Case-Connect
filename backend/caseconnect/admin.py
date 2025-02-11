

# Register your models here.
from django.contrib import admin
from .models import CrimeNews, Crimes, CriminalCrime, Criminals

admin.site.register(CrimeNews)
admin.site.register(Crimes)
admin.site.register(CriminalCrime)
admin.site.register(Criminals)
