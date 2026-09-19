from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import ProductSimpleOffer,Iva
# Register your models here.

class IvaAdmin(ModelAdmin):
    list_display = [field.name for field in Iva._meta.fields]
admin.site.register(Iva,IvaAdmin)

class ProductSimpleOfferAdmin(ModelAdmin):
    list_display = [field.name for field in ProductSimpleOffer._meta.fields]
admin.site.register(ProductSimpleOffer,ProductSimpleOfferAdmin)
