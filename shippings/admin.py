from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Shipping,Courier,ShippedProducts
# Register your models here.


class CourierAdmin(ModelAdmin):
    list_display = [field.name for field in Courier._meta.fields]

class ShippingAdmin(ModelAdmin):
    list_display = [field.name for field in Shipping._meta.fields]

class ShippedProductsAdmin(ModelAdmin):
    list_display = [field.name for field in ShippedProducts._meta.fields]

admin.site.register(Courier,CourierAdmin)
admin.site.register(Shipping,ShippingAdmin)
admin.site.register(ShippedProducts,ShippedProductsAdmin)