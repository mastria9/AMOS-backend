from django.contrib import admin
from django.contrib.admin import ModelAdmin

# Register your models here.

from .models import ProductSimple,ProductMultiple,ProductBulk,ProductConfigurable
from .models import ProductBooleanEav,ProductCharEav,ProductIntEav,ProductTextEav,ProductDecimalEav,ProductUrlEav
from .models import Attribute,CustomAttribute,Category
# from .models import Variation,CustomVariation
from .models import DefaultAttribute
from .models import BulkProductQty

# from .models import ProductBulkOfMultiple,ProductBulkOfBulk
# from .models import ProductMultipleOfBulk,ProductMultipleOfMultiple
# from .models import ProductConfigurableOfMultiple,ProductConfigurableOfBulk
# admin.site.register(ProductMultipleOfBulk)
# admin.site.register(ProductMultipleOfMultiple)
# admin.site.register(ProductBulkOfBulk)
# admin.site.register(ProductBulkOfMultiple)
# admin.site.register(ProductConfigurableOfBulk)
# admin.site.register(ProductConfigurableOfMultiple)


class CategoryAdmin(ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]
admin.site.register(Category,CategoryAdmin)

# class VariationAdmin(ModelAdmin):
#     list_display = [field.name for field in Variation._meta.fields]
# admin.site.register(Variation,VariationAdmin)

# class CustomVariationAdmin(ModelAdmin):
#     list_display = [field.name for field in CustomVariation._meta.fields]
# admin.site.register(CustomVariation,CustomVariationAdmin)

class CustomAttributeAdmin(ModelAdmin):
    list_display = [field.name for field in CustomAttribute._meta.fields]
admin.site.register(CustomAttribute,CustomAttributeAdmin)

class DefaultAttributeAdmin(ModelAdmin):
    list_display = [field.name for field in DefaultAttribute._meta.fields]
admin.site.register(DefaultAttribute,DefaultAttributeAdmin)

class AttributeAdmin(ModelAdmin):
    list_display = [field.name for field in Attribute._meta.fields]
admin.site.register(Attribute,AttributeAdmin)

class ProductSimpleAdmin(ModelAdmin):
    list_display = [field.name for field in ProductSimple._meta.fields]
admin.site.register(ProductSimple,ProductSimpleAdmin)

class ProductConfigurableAdmin(ModelAdmin):
    list_display = [field.name for field in ProductConfigurable._meta.fields]
admin.site.register(ProductConfigurable,ProductConfigurableAdmin)

class ProductBulkAdmin(ModelAdmin):
    list_display = [field.name for field in ProductBulk._meta.fields]
admin.site.register(ProductBulk,ProductBulkAdmin)
class BulkProductQtyAdmin(ModelAdmin):
    list_display = [field.name for field in BulkProductQty._meta.fields]
admin.site.register(BulkProductQty,BulkProductQtyAdmin)

class ProductMultipleAdmin(ModelAdmin):
    list_display = [field.name for field in ProductMultiple._meta.fields]
admin.site.register(ProductMultiple,ProductMultipleAdmin)


class ProductCharEavAdmin(ModelAdmin):
    list_display = [field.name for field in ProductCharEav._meta.fields]
admin.site.register(ProductCharEav,ProductCharEavAdmin)

class ProductDecimalEavAdmin(ModelAdmin):
    list_display = [field.name for field in ProductDecimalEav._meta.fields]
admin.site.register(ProductDecimalEav,ProductDecimalEavAdmin)

class ProductTextEavAdmin(ModelAdmin):
    list_display = [field.name for field in ProductTextEav._meta.fields]
admin.site.register(ProductTextEav,ProductTextEavAdmin)

class ProductIntEavAdmin(ModelAdmin):
    list_display = [field.name for field in ProductIntEav._meta.fields]
admin.site.register(ProductIntEav,ProductIntEavAdmin)

class ProductBooleanEavAdmin(ModelAdmin):
    list_display = [field.name for field in ProductBooleanEav._meta.fields]
admin.site.register(ProductBooleanEav,ProductBooleanEavAdmin)

class ProductUrlEavAdmin(ModelAdmin):
    list_display = [field.name for field in ProductUrlEav._meta.fields]
admin.site.register(ProductUrlEav,ProductUrlEavAdmin)

