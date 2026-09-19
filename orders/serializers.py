from rest_framework import serializers
from marketplaces.models import Marketplace
from customers.models import Customer
from shippings.models import Shipping
from companies.models import Company
from .models import Order, OrderDetail


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id',)
        read_only_fields = ('id',)
        depth=0

class MarketplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = ('id')
        read_only_fields = ('id',)
        depth=0

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        

class OrderDetailSerializer(serializers.ModelSerializer):
    _date=serializers.DateTimeField(source="date",format="%d-%m-%Y %H:%M:%S")
    _max_shipping_date=serializers.DateTimeField(source="max_shipping_date",format="%d-%m-%Y %H:%M:%S")
    _max_consignment_date=serializers.DateTimeField(source="max_consignment_date",format="%d-%m-%Y %H:%M:%S")
    _status=serializers.CharField(source="get_status_display")
    class Meta:
        model = OrderDetail
        fields = '__all__'
        depth=0

class OrderSerializer(serializers.ModelSerializer):
    order_detail=OrderDetailSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields =('order_id',)
        depth=1