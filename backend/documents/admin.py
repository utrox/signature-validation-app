from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Document

# Register your models here.
admin.site.register(Document, ModelAdmin)
