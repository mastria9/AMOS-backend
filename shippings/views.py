from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from backend.mixins import AuthorizationMixin
from .models import Shipping,Courier,ShippedProducts
from rest_framework import serializers
from companies.models import Company
from warehouses.models import WareHouse
from marketplaces.models import Marketplace
from orders.models import Order
from .utils import ShippingInterface

class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'
        read_only_fields =('company','sede','cliente','codice')
        depth=1

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'
        read_only_fields =('id','company','marketplace','create','sent','status','tracking','shipped_products')
        depth=1



class ShippingViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("shippings")
        company=Company.objects.get(id=self.request.GET.get("company"))
        if self.request.GET.get("order"):
            marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
            order=Order.objects.get(id=self.request.GET.get("order"),company=company,marketplace=marketplace)
            queryset=queryset.filter(order=order)

        return queryset.order_by("id")
    
    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(company=company,id=serializer.initial_data["marketplace"])
        order=Order.objects.get(company=company,marketplace=marketplace,id=serializer.initial_data["order_id"])
        serializer.validated_data["company"]=company
        serializer.validated_data["marketplace"]=marketplace
        serializer.validated_data["order"]=order
        
        if serializer.is_valid():
            serializer.validated_data["shipped_products"]=[]
            for shipProd in serializer.initial_data["shippedProducts"]:
                shipProdObj=ShippedProducts(company=company,marketplace=marketplace,qty=shipProd["qty"],sku=shipProd["sku"])
                try:
                    shipProdObj.save()
                    serializer.validated_data["shipped_products"].append(shipProdObj)
                except:
                    for obj in serializer.validated_data["shipped_products"]:
                        obj.delete()
                    raise APIException(detail="Errore nell'associare i prodotti alla spedizione")
            try:    
                serializer.save()
                # shippingProcess=ShippingInterface(serializer.instance)
            except:
                raise APIException(detail="Errore nel creare la spedizione i prodotti alla spedizione")


    def perform_update(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(company=company,id=serializer.initial_data["marketplace"])
        order=Order.objects.get(company=company,marketplace=marketplace,id=serializer.initial_data["order_id"])
        serializer.validated_data["company"]=company
        serializer.validated_data["marketplace"]=marketplace
        serializer.validated_data["order"]=order
        
        if serializer.is_valid():
            
            serializer.validated_data["shipped_products"]=[]
            for shipProd in serializer.initial_data["shippedProducts"]:
                shipProdObj=ShippedProducts(company=company,marketplace=marketplace,qty=shipProd["qty"],sku=shipProd["sku"])
                shipProdObj.save()
                serializer.validated_data["shipped_products"].append(shipProdObj)
                print(serializer.validated_data)
            serializer.save()

    def perform_destroy(self,instance):
        for obj in instance.shipped_products.all():
            obj.delete()
        instance.delete()

class ShippingViewSet(ShippingViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Shipping
    permission_class = IsAuthenticated
    serializer_class = ShippingSerializer


shipping_list = ShippingViewSet.as_view({'get':'list','post':'create'})
shipping_detail = ShippingViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


class CourierViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("couriers")
        if self.request.GET.get("active")=="1":
            queryset=queryset.filter(active=True)
        elif self.request.GET.get("active")=="0":
            queryset=queryset.filter(active=False)
        return queryset.order_by("id")

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        serializer.validated_data["company"]=company
        serializer.validated_data["warehouse"]=WareHouse.objects.get(company=company,id=serializer.initial_data["warehouse"])
        if serializer.is_valid():
            serializer.save()

class CourierViewSet(CourierViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Courier
    permission_class = IsAuthenticated
    serializer_class = CourierSerializer


courier_list = CourierViewSet.as_view({'get':'list','post':'create'})
courier_detail = CourierViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


# marketplace_router = DefaultRouter()
# marketplace_router.register(r'marketplaces',MarketplaceViewSet)