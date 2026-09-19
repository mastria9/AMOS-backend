from django.contrib import admin
from .models import Inventory,InventoryDimension,InventoryOffer,IVA
# Register your models here.
admin.site.register(Inventory)
admin.site.register(InventoryDimension)
admin.site.register(InventoryOffer)
admin.site.register(IVA)