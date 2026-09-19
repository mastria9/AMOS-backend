from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import WareHouse,Item,ItemInfoFiles,ItemQty
# # Register your models here.

class WareHouseAdmin(ModelAdmin):
    list_display = [field.name for field in WareHouse._meta.fields]
admin.site.register(WareHouse,WareHouseAdmin)


class ItemAdmin(ModelAdmin):
    list_display = [field.name for field in Item._meta.fields]
admin.site.register(Item,ItemAdmin)

class ItemInfoFilesAdmin(ModelAdmin):
    list_display = [field.name for field in ItemInfoFiles._meta.fields]
admin.site.register(ItemInfoFiles,ItemInfoFilesAdmin)

class ItemQtyAdmin(ModelAdmin):
    list_display = [field.name for field in ItemQty._meta.fields]
admin.site.register(ItemQty,ItemQtyAdmin)