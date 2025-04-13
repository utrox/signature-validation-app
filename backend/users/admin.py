from django.contrib import admin
from .models import User, UserProfile
from unfold.admin import ModelAdmin

# Register your models here.
admin.site.register(User, ModelAdmin)
admin.site.register(UserProfile, ModelAdmin)
