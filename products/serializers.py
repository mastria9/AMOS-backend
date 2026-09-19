from rest_framework import serializers


from .models import CustomAttribute, ProductSimple,ProductMultiple,ProductBulk,ProductConfigurable
from .models import ProductBooleanEav,ProductCharEav,ProductIntEav,ProductTextEav,ProductDecimalEav,ProductUrlEav
from .models import Category,Attribute,BulkProductQty

# from .models import ProductBulkOfMultiple,ProductBulkOfBulk
# from .models import ProductMultipleOfBulk,ProductMultipleOfMultiple
# from .models import ProductConfigurableOfMultiple,ProductConfigurableOfBulk




class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields='__all__'
        read_only_fields = ('id',)

class DefaultAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        exclude = ('company',)
class CustomAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAttribute
        exclude = ('company',)
        

class ProductIntEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductIntEav
        fields = '__all__'
        read_only_fields = ('id','company','marketplace','sku','attribute')


class ProductCharEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCharEav
        fields = '__all__'
        read_only_fields = ('id','company','marketplace','sku','attribute')

class ProductBooleanEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBooleanEav
        fields = '__all__'
        read_only_fields = ('id','company','marketplace','sku','attribute')

class ProductTextEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTextEav
        fields = '__all__'
        read_only_fields = ('id','company','marketplace','sku','attribute')

class ProductDecimalEavSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDecimalEav
        fields = '__all__'
        read_only_fields = ('id','company','marketplace','sku','attribute')

class ProductUrlEavSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductUrlEav
        fields = '__all__'
        read_only_fields = ('id','company','marketplace','sku','attribute')

class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSimple
        exclude=('company',)
        read_only_fields = ('int_eav','boolean_eav','char_eav','decimal_eav','text_eav','url_eav')
        depth=1


class AbstractProductsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSimple
        fields= ('id','sku','item')
        depth=0

class AbstractProductsForCategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSimple
        fields= ('id','sku','item')
        depth=0

class AbstractProductsForCategoryMultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMultiple
        fields= ('id','sku',)
        depth=0

class AbstractProductsForCategoryConfigurableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductConfigurable
        fields= ('id','sku',)
        depth=0

class AbstractProductsForCategoryBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBulk
        fields= ('id','sku',)
        depth=0

class AbstractProductsBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBulk
        fields= ('id','sku')
        depth=0

class AbstractProductsConfigurableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductConfigurable
        fields= ('id','sku',)
        depth=0

class AbstractProductsMultipleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMultiple
        fields= ('id','sku',)
        depth=0

class CategorySerializer(serializers.ModelSerializer):
    simple=AbstractProductsSimpleSerializer(many=True,read_only=True)
    bulk=AbstractProductsBulkSerializer(many=True,read_only=True)
    multiple=AbstractProductsConfigurableSerializer(many=True,read_only=True)
    configurable=AbstractProductsMultipleSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        exclude = 'company',
        read_only_fields = ('custom_attributes','variations','marketplace','simple','bulk','configurable','multiple')
        depth=2
class ProductMultipleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductMultiple
        exclude = ('company',)
        read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')
        depth=1

class BulkProductsQtySerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkProductQty
        exclude = ('company',)
        depth=1



class ProductBulkSerializer(serializers.ModelSerializer):
    bulk_products_qty=BulkProductsQtySerializer(many=True,read_only=True)
    class Meta:
        model = ProductBulk
        exclude = ('company',)
        read_only_fields = ('int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav','bulk_products_qty')
        depth=1

class ProductConfigurableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductConfigurable
        exclude = ('company',)
        read_only_fields = ('int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav','variations','products')
        depth=1


# class ProductBulkOfMultipleSerializer(serializers.ModelSerializer):
#     int_eav=ProductIntEavSerializer(many=True)
#     boolean_eav=ProductBooleanEavSerializer(many=True)
#     char_eav=ProductCharEavSerializer(many=True)
#     decimal_eav=ProductDecimalEavSerializer(many=True)
#     text_eav=ProductTextEavSerializer(many=True)
#     url_eav=ProductUrlEavSerializer(many=True)
#     class Meta:
#         model = ProductBulkOfMultiple
#         exclude = ('company',)
#         read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

# class ProductBulkOfBulkSerializer(serializers.ModelSerializer):
#     int_eav=ProductIntEavSerializer(many=True)
#     boolean_eav=ProductBooleanEavSerializer(many=True)
#     char_eav=ProductCharEavSerializer(many=True)
#     decimal_eav=ProductDecimalEavSerializer(many=True)
#     text_eav=ProductTextEavSerializer(many=True)
#     url_eav=ProductUrlEavSerializer(many=True)
#     class Meta:
#         model = ProductBulkOfBulk
#         exclude = ('company',)
#         read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

# class ProductMultipleOfBulkSerializer(serializers.ModelSerializer):
#     int_eav=ProductIntEavSerializer(many=True)
#     boolean_eav=ProductBooleanEavSerializer(many=True)
#     char_eav=ProductCharEavSerializer(many=True)
#     decimal_eav=ProductDecimalEavSerializer(many=True)
#     text_eav=ProductTextEavSerializer(many=True)
#     url_eav=ProductUrlEavSerializer(many=True)
#     class Meta:
#         model = ProductMultipleOfBulk
#         fields = '__all__'
#         read_only_fields = ('id','company','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

# class ProductMultipleOfMultipleSerializer(serializers.ModelSerializer):
#     int_eav=ProductIntEavSerializer(many=True)
#     boolean_eav=ProductBooleanEavSerializer(many=True)
#     char_eav=ProductCharEavSerializer(many=True)
#     decimal_eav=ProductDecimalEavSerializer(many=True)
#     text_eav=ProductTextEavSerializer(many=True)
#     url_eav=ProductUrlEavSerializer(many=True)
#     class Meta:
#         model = ProductMultipleOfMultiple
#         exclude = ('company',)
#         read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

# class ProductConfigurableOfMultipleSerializer(serializers.ModelSerializer):
#     int_eav=ProductIntEavSerializer(many=True)
#     boolean_eav=ProductBooleanEavSerializer(many=True)
#     char_eav=ProductCharEavSerializer(many=True)
#     decimal_eav=ProductDecimalEavSerializer(many=True)
#     text_eav=ProductTextEavSerializer(many=True)
#     url_eav=ProductUrlEavSerializer(many=True)
#     class Meta:
#         model = ProductConfigurableOfMultiple
#         exclude = ('company',)
#         read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')

# class ProductConfigurableOfBulkSerializer(serializers.ModelSerializer):
#     int_eav=ProductIntEavSerializer(many=True)
#     boolean_eav=ProductBooleanEavSerializer(many=True)
#     char_eav=ProductCharEavSerializer(many=True)
#     decimal_eav=ProductDecimalEavSerializer(many=True)
#     text_eav=ProductTextEavSerializer(many=True)
#     url_eav=ProductUrlEavSerializer(many=True)
#     class Meta:
#         model = ProductConfigurableOfBulk
#         exclude = ('company',)
#         read_only_fields = ('id','int_eav','char_eav','text_eav','decimal_eav','boolean_eav','url_eav')


