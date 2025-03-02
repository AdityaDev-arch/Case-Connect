

# Register your models here.
from django.contrib import admin
from .models import CrimeNews, Crime, CriminalCrime, Criminal
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CrimeNews)
admin.site.register(Crime)
admin.site.register(CriminalCrime)
admin.site.register(Criminal)
admin.site.register(CustomUser, UserAdmin)  # ✅ Register CustomUser in Admin Panel
