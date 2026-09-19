from django.contrib import admin
from .models import Order,OrderDetail
from django.contrib.admin import ModelAdmin

# Register your models here.


class OrderAdmin(ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

admin.site.register(Order,OrderAdmin)

class OrderDetailAdmin(ModelAdmin):
    list_display = [field.name for field in OrderDetail._meta.fields]
    
admin.site.register(OrderDetail,OrderDetailAdmin)


