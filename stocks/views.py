# from .models import StockSimpleProduct,StockBulkProduct,StockMultipleProduct
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from backend.mixins import AuthorizationMixin
# from rest_framework import serializers

# class StockSimpleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StockSimpleProduct
#         fields = '__all__'
#         read_only_fields = ('company','product')

# class StockMultipleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StockMultipleProduct
#         fields = '__all__'
#         read_only_fields = ('company','product')

# class StockBulkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StockBulkProduct
#         fields = '__all__'
#         read_only_fields = ('company','product')
        
# class StockViewMixin(object):
#     def get_queryset(self):
#         queryset=super().get_queryset("offers")
#         return queryset.order_by("id")

# class StockSimpleViewSet(StockViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = StockSimpleProduct
#     permission_class = IsAuthenticated
#     serializer_class = StockSimpleSerializer
# stocks_simple_list = StockSimpleViewSet.as_view({'get':'list'})
# stock_simple_detail = StockSimpleViewSet.as_view({'get':'retrieve','put':'update'})

# class StockBulkViewSet(StockViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = StockBulkProduct
#     permission_class = IsAuthenticated
#     serializer_class = StockBulkSerializer
# stocks_bulk_list = StockSimpleViewSet.as_view({'get':'list'})
# stock_bulk_detail = StockSimpleViewSet.as_view({'get':'retrieve'})

# class StockMultipleViewSet(StockViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = StockMultipleProduct
#     permission_class = IsAuthenticated
#     serializer_class = StockMultipleSerializer
# stocks_multiple_list = StockMultipleViewSet.as_view({'get':'list'})
# stock_multiple_detail = StockMultipleViewSet.as_view({'get':'retrieve'})