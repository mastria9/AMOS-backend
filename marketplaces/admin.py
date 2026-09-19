from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Marketplace
# Register your models here.


class MarketplaceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Marketplace._meta.fields]
admin.site.register(Marketplace,MarketplaceAdmin)