from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Import

class ImportAdmin(ModelAdmin):
    list_display = [field.name for field in Import._meta.fields]
admin.site.register(Import,ImportAdmin)
