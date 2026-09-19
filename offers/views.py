from django.shortcuts import render
from rest_framework import serializers
import django.core.serializers

from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied,APIException
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.mixins import AuthorizationMixin
from .models import ProductSimpleOffer,ProductBulkOffer,ProductMultipleOffer,Iva
from marketplaces.models import Marketplace
from companies.models import Company,Authorization
from warehouses.models import Item
from django.http import JsonResponse
import json

from products.models import ProductSimple,ProductBulk,ProductMultiple
# Create your views here.

class ProductSimpleOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSimpleOffer
        fields = '__all__'

    def validate(self, data):
        if data["marketplace"].company!=data["company"]:
            raise serializers.ValidationError("Company/marketplace errati")
        return data

class ProductMultipleOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMultipleOffer
        fields = '__all__'

    def validate(self, data):
        if data["marketplace"].company!=data["company"]:
            raise serializers.ValidationError("Company/marketplace errati")
        return data

class ProductBulkOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBulkOffer
        fields = '__all__'

    def validate(self, data):
        if data["marketplace"].company!=data["company"]:
            raise serializers.ValidationError("Company/marketplace errati")
        return data
        
class ProductSimpleOfferViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("offers")
        return queryset.order_by("id")

class ProductMultipleOfferViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("offers")
        return queryset.order_by("id")

class ProductBulkOfferViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("offers")
        return queryset.order_by("id")

    
class IvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iva
        fields = '__all__'
    

class IvaViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("iva")
        if self.request.GET.get("marketplace"):
            company=Company.objects.get(id=self.request.GET.get("company"))
            marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
            queryset=queryset.filter(marketplace=marketplace,company=company)
        return queryset.order_by("id")

class IvaViewSet(IvaViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Iva
    permission_class = IsAuthenticated
    serializer_class = IvaSerializer

iva_list = IvaViewSet.as_view({'get':'list','post':'create'})
iva_detail = IvaViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


class ProductSimpleOfferViewSet(ProductSimpleOfferViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductSimpleOffer
    permission_class = IsAuthenticated
    serializer_class = ProductSimpleOfferSerializer

product_simple_offers_list = ProductSimpleOfferViewSet.as_view({'get':'list','post':'create'})
product_simple_offer_detail = ProductSimpleOfferViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


class ProductMultipleOfferViewSet(ProductMultipleOfferViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductMultipleOffer
    permission_class = IsAuthenticated
    serializer_class = ProductMultipleOfferSerializer

product_multiple_offers_list = ProductMultipleOfferViewSet.as_view({'get':'list','post':'create'})
product_multiple_offer_detail = ProductMultipleOfferViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class ProductBulkOfferViewSet(ProductBulkOfferViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductBulkOffer
    permission_class = IsAuthenticated
    serializer_class = ProductBulkOfferSerializer

product_bulk_offers_list = ProductBulkOfferViewSet.as_view({'get':'list','post':'create'})
product_bulk_offer_detail = ProductBulkOfferViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


class OffersView(APIView):
    permission_class= IsAuthenticated
    
    def get(self,request):
        if not Company.objects.filter(pk=self.request.GET.get("company")).exists():
            raise PermissionDenied("Permesso negato")
        company=Company.objects.get(id=self.request.GET.get("company"))
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            permission=Authorization.Permissions.READ
            try:
                if Authorization.objects.get(user=self.request.user,application="offers",company=company).permission<permission:
                    raise PermissionDenied("Permesso negato")
            except:
                raise PermissionDenied("Permesso negato")
        productsObjs=None
        if self.request.GET.get("type")=="simple":
            productsObjs=ProductSimple.objects.filter(company=company).order_by("sku")
        elif self.request.GET.get("type")=="bulk":
            productsObjs=ProductBulk.objects.filter(company=company).order_by("sku")
        elif self.request.GET.get("type")=="multiple":
            productsObjs=ProductMultiple.objects.filter(company=company).order_by("sku")
        else:
            raise PermissionDenied(detail="Tipo di prodotto non valido")
        if self.request.GET.get("search"):
            productsObjs=productsObjs.filter(sku__icontains=self.request.GET.get("search"))

        response={}
        
        results={}
        
        for obj in productsObjs:
            if obj.sku not in results:
                results[obj.sku]={}
                results[obj.sku]["marketplaces"]={}
            results[obj.sku]["marketplaces"][obj.marketplace.id]={}
            if self.request.GET.get("type")=="simple":
                if obj.item is not None:
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["item"]={}
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["item"]["id"]=obj.item.id
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["item"]["item_code"]=obj.item.item_code
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["item"]["name"]=obj.item.name
                else:
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["item"]=None
            elif self.request.GET.get("type")=="multiple":
                results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]={}
                results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["id"]=obj.product.id
                results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["sku"]=obj.product.sku
                results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["qty"]=obj.qty
                if obj.product.item is not None:
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["item"]={}
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["item"]["id"]=obj.product.item.id
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["item"]["item_code"]=obj.product.item.item_code
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["item"]["name"]=obj.product.item.name
                else:
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["item"]=None
                try:
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["title"]=obj.product.char_eav.get(attribute="title").value
                except:
                    pass
            elif self.request.GET.get("type")=="bulk":
                results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]=[]
                for childObj in obj.bulk_products_qty.filter(company=company):
                    child={}
                    child["id"]=childObj.product.id
                    child["sku"]=childObj.product.sku
                    child["qty"]=childObj.qty
                    try:
                        child["title"]=childObj.product.char_eav.get(attribute="title").value
                    except:
                        pass
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["child"].append(child)
                    
                try:
                    results[obj.sku]["marketplaces"][obj.marketplace.id]["child"]["title"]=obj.product.char_eav.get(attribute="title").value
                except:
                    pass
            results[obj.sku]["marketplaces"][obj.marketplace.id]["product"]=obj.id
            try:
                results[obj.sku]["marketplaces"][obj.marketplace.id]["title"]=obj.char_eav.get(attribute="title").value
            except:
                pass
            try:
                offer=None
                if self.request.GET.get("type")=="simple":
                    offer=ProductSimpleOffer.objects.get(company=company,product=obj,marketplace=obj.marketplace)
                elif self.request.GET.get("type")=="multiple":
                    offer=ProductMultipleOffer.objects.get(company=company,product=obj,marketplace=obj.marketplace)
                elif self.request.GET.get("type")=="bulk":
                    offer=ProductBulkOffer.objects.get(company=company,product=obj,marketplace=obj.marketplace)
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]={}
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["id"]=offer.id
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["price"]=offer.price
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["is_min_max"]=offer.is_min_max
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["min_price"]=offer.min_price
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["max_price"]=offer.max_price
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["offer_is_active"]=offer.offer_is_active
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["offer_price"]=offer.offer_price
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["start_offer"]=offer.start_offer
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["end_offer"]=offer.end_offer
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["iva"]=offer.iva.id
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]["is_active"]=offer.is_active
            except:
                results[obj.sku]["marketplaces"][obj.marketplace.id]["offer"]={}

        response["count"]=len(results)
        response["results"]={}
        offset=int(self.request.GET.get("offset"))
        limit=int(self.request.GET.get("limit"))
        
        if offset>0:
            response["previous"]=True
        if limit+offset<len(results):
            response["next"]=True
        i=0
        for key,value in results.items():
            i+=1
            if offset>i:
                continue
            print(i)
            response["results"][key]=value
            if limit+offset<=i:
                print(i)
                break


        return JsonResponse(response)
        

    def post(self,request):
        if not Company.objects.filter(pk=self.request.GET.get("company")).exists():
            raise PermissionDenied("Permesso negato")
        company=Company.objects.get(id=self.request.GET.get("company"))
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            permission=Authorization.Permissions.MODIFY
            try:
                if Authorization.objects.get(user=self.request.user,application="offers",company=company).permission<permission:
                    raise PermissionDenied("Permesso negato")
            except:
                raise PermissionDenied("Permesso negato")

