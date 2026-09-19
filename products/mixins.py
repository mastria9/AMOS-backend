from pprint import PrettyPrinter
from django.core.exceptions import ValidationError
from .serializers import CategorySerializer
from xmlrpc.client import boolean
from urllib3 import HTTPResponse
from rest_framework.exceptions import APIException,PermissionDenied
from django.db.utils import IntegrityError
import urllib
from PIL import Image
from io import BytesIO
import base64
import os
from django.conf import settings
from rest_framework.response import Response
import json
from django.core.paginator import Paginator
from companies.models import Company
from marketplaces.models import Marketplace
from backend.mixins import AuthorizationMixin
from django.db.models import Q
from rest_framework import serializers
from .serializers import ProductIntEavSerializer,ProductCharEavSerializer,ProductDecimalEavSerializer,ProductBooleanEavSerializer,ProductTextEavSerializer,ProductUrlEavSerializer
from .models import Category,CustomAttribute,Attribute,DefaultAttribute,BulkProductQty
from .models import ProductSimple,ProductConfigurable,ProductMultiple,ProductBulk
from .models import ProductCharEav,ProductBooleanEav,ProductIntEav,ProductDecimalEav,ProductTextEav,ProductUrlEav
from django.core import serializers
from django.http import JsonResponse
from warehouses.models import Item
from warehouses.views import update_InStockQty
# from stocks.models import StockBulkProduct,StockMultipleProduct,StockSimpleProduct
from django.core.exceptions import ObjectDoesNotExist

class CustomAttributeViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("products")
        return queryset.order_by("id")

    def perform_create(self,serializer):
        try:
            company=Company.objects.get(id=self.request.GET.get("company"))
            marketplace=Marketplace.objects.get(company=company,id=self.request.GET.get("marketplace"))
            
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                if serializer.validated_data["marketplace"]==marketplace.id:
                    serializer.save()
                else:
                    raise PermissionDenied("Errore nel creare l'attributo. Marketplace non valido")    
        except:
            raise PermissionDenied("Errore nel creare l'attributo")

    def perform_update(self,serializer):
        try:
            company=Company.objects.get(id=self.request.GET.get("company"))
            marketplace=Marketplace.objects.get(company=company,id=self.request.GET.get("marketplace"))
            
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                if serializer.validated_data["marketplace"]==marketplace.id:
                    serializer.save()
                else:
                    raise PermissionDenied("Errore aggiornamento attributo. Marketplace non valido")    
        except:
            raise PermissionDenied("Errore aggiornamento attributo")

class CategoryViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        queryset=queryset.filter(marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace")))
        if self.request.GET.get("simple"):
            queryset=queryset.filter(simple__id=self.request.GET.get("simple"))
        if self.request.GET.get("configurable"):
            queryset=queryset.filter(configurable__id=self.request.GET.get("configurable"))
        if self.request.GET.get("bulk"):
            queryset=queryset.filter(bulk__id=self.request.GET.get("bulk"))
        if self.request.GET.get("multiple"):
            queryset=queryset.filter(multiple__id=self.request.GET.get("multiple"))
        return queryset.order_by("id")

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        
        parent=None
        if serializer.initial_data["parent"] is not None:
            if Category.objects.filter(company=company,marketplace=marketplace,id=serializer.initial_data["parent"]).exists():
                parent=Category.objects.get(company=company,marketplace=marketplace,id=serializer.initial_data["parent"])
            
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.validated_data["marketplace"]=marketplace
                serializer.validated_data["parent"]=parent
                serializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s errore nella creazione" % (self.model._meta.verbose_name))

    def perform_update(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        
        
        if "parent" in serializer.initial_data:
            if serializer.initial_data["parent"] is not None:
                try:
                    parent=Category.objects.get(company=company,marketplace=marketplace,id=serializer.initial_data["parent"])
                    serializer.validated_data["parent"]=parent
                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["parent"]=None
        if "attributes" in serializer.initial_data:
            serializer.validated_data["attributes"]=serializer.initial_data["attributes"]
        if "custom_attributes" in serializer.initial_data:
            serializer.validated_data["custom_attributes"]=serializer.initial_data["custom_attributes"]

        if "variations" in serializer.initial_data:
            serializer.validated_data["variations"]=serializer.initial_data["variations"]

        if "custom_variations" in serializer.initial_data:
            serializer.validated_data["custom_variations"]=serializer.initial_data["custom_variations"]

        if "_simple" in serializer.initial_data:
            if len(serializer.initial_data["_simple"]) is not None:
                try:
                    simple=ProductSimple.objects.filter(company=company,id__in=serializer.initial_data["_simple"])
                    serializer.validated_data["simple"]=simple
                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["simple"]=None

        if "_configurable" in serializer.initial_data:
            if len(serializer.initial_data["_configurable"]) is not None:
                try:
                    configurable=ProductConfigurable.objects.filter(company=company,id__in=serializer.initial_data["_configurable"])
                    

                    serializer.validated_data["configurable"]=configurable
                    # se sto salvando il configurabile, questo deve stare nella stessa categoria di tutti i suoi figli

                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["configurable"]=None

        if "_bulk" in serializer.initial_data:
            if len(serializer.initial_data["_bulk"]) is not None:
                try:
                    bulk=ProductBulk.objects.filter(company=company,id__in=serializer.initial_data["_bulk"])
                    serializer.validated_data["bulk"]=bulk
                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["bulk"]=None
        if "_multiple" in serializer.initial_data:
            if len(serializer.initial_data["_multiple"]) is not None:
                try:
                    multiple=ProductMultiple.objects.filter(company=company,id__in=serializer.initial_data["_multiple"])
                    serializer.validated_data["multiple"]=multiple
                except:
                    raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))
            else:
                serializer.validated_data["multiple"]=None
        
        try:
            if serializer.is_valid():
                serializer.save()
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s errore nell'aggiornamento" % (self.model._meta.verbose_name))


class CategorySimplifyViewMixin(object):

    def list(self,request):
        all_categories={}
        marketplace=Marketplace.objects.get(company=self.request.GET.get("company"),id=self.request.GET.get("marketplace"))
        queryset=super().get_queryset("products").filter(marketplace=marketplace).order_by("id")
        catSerializer=CategorySerializer(queryset,many=True)
        categories=json.loads(json.dumps(catSerializer.data))

        def find_parent(atree,id):
            i=0
            while i<len(atree):
                if atree[i]["id"]==id:
                    return atree[i]
                else:
                    if atree[i]["childs"] is not None:
                        obj=find_parent(atree[i]["childs"],id)
                        if obj!=None:
                            return obj
                i+=1
            return None
        
        tree=[]
        
        i=0
        while len(categories)>0:
            if categories[i]["parent"] is None:
                tree.append(
                    {
                        "id":categories[i]["id"],
                        "childs":[],
                        "title":categories[i]["title"],
                        "name":categories[i]["name"],
                        "attributes":categories[i]["attributes"],
                        "custom_attributes":categories[i]["custom_attributes"],
                        "variations":categories[i]["variations"],
                        "custom_variations":categories[i]["custom_variations"],
                        'simple':categories[i]["simple"],
                        'bulk':categories[i]["bulk"],
                        'configurable':categories[i]["configurable"],
                        'multiple':categories[i]["multiple"],
                        'parent':categories[i]["parent"]
                        })
                categories.pop(i)
                i=0
            else:
                parent=find_parent(tree,categories[i]["parent"]["id"])
                if parent is not None:
                    parent["childs"].append(
                    {
                        "id":categories[i]["id"],
                        "childs":[],
                        "title":categories[i]["title"],
                        "name":categories[i]["name"],
                        "attributes":categories[i]["attributes"],
                        "custom_attributes":categories[i]["custom_attributes"],
                        "variations":categories[i]["variations"],
                        "custom_variations":categories[i]["custom_variations"],
                        'simple':categories[i]["simple"],
                        'bulk':categories[i]["bulk"],
                        'configurable':categories[i]["configurable"],
                        'multiple':categories[i]["multiple"],
                        'parent':categories[i]["parent"]
                        })
                    categories.pop(i)
                    i=0
                else:
                    i+=1
        
        return JsonResponse({"results":tree})

    
    
    

class ProductAttributeViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        return queryset.order_by("id")


class FilterCategoryMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        queryset=queryset.filter(marketplace=self.request.GET.get("marketplace"))
        id_products=set()
        for category in Category.objects.filter(company=self.request.GET.get("company"),marketplace=self.request.GET.get("marketplace")).exclude(id=self.request.GET.get("category")):
            id_products.add(category.simple.all().values_list("id",flat=True))
        queryset=queryset.exclude(id__in=list(id_products)).order_by("id").distinct()
        return queryset

        

                
class ProductSimpleViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        marketplace=self.request.GET.get("marketplace")
        queryset=queryset.filter(marketplace=marketplace)
        search=None
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            queryset=queryset.filter(sku__icontains=search)|queryset.filter(gtin__contains=search)\
                |queryset.filter(char_eav__value__icontains=search)\
                |queryset.filter(text_eav__value__icontains=search)
            return queryset.order_by("id").distinct()
        return queryset.order_by("id")


        
        

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.validated_data["marketplace"]=marketplace
                serializer.save()
        except IntegrityError:
            raise PermissionDenied(detail="Lo SKU %s esiste già in questo marketplace" % (serializer.validated_data["sku"]))
                
    def perform_update(self,serializer):
        
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        
        eav_type_objs={}
        for val in ["INT","DECIMAL","BOOLEAN","URL","TEXT","CHAR"]:
            eav_type_objs[val]=[]
        
        
        for attribute,value in serializer.initial_data["marketplace"][str(marketplace.id)].items():
            eav_type=None
            
            if DefaultAttribute.objects.filter(name=attribute).exists():
                eav_type=DefaultAttribute.objects.get(name=attribute).type
            elif Attribute.objects.filter(name=attribute).exists():
                eav_type=Attribute.objects.get(name=attribute).type
            elif marketplace.code=="AMZ" and attribute=="asin":
                eav_type="CHAR"
            
            else:
                raise APIException(detail="L'attributo '"+str(attribute)+"' non esiste!")
            
            if eav_type is not None:
                obj=None
                if eav_type=="DECIMAL":
                    if "value" in value and "unit" in value:
                        try:
                            obj=ProductDecimalEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                            obj.value=value["value"]
                            obj.unit=value["unit"]
                        except ProductDecimalEav.DoesNotExist:
                            obj=ProductDecimalEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value["value"],unit=value["unit"])
                        data=json.loads(serializers.serialize("json",[obj,]))
                        fields=data[0]["fields"]
                        fields["id"]=data[0]["pk"]
                        modelSerializer=ProductDecimalEavSerializer(data=fields)
                elif eav_type=="INT":
                    try:
                        obj=ProductIntEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                        obj.value=value
                    except ProductIntEav.DoesNotExist:
                        obj=ProductIntEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                    data=json.loads(serializers.serialize("json",[obj,]))
                    fields=data[0]["fields"]
                    fields["id"]=data[0]["pk"]
                    modelSerializer=ProductIntEavSerializer(data=fields)
                elif eav_type=="URL":
                    try:
                        obj=ProductUrlEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                        obj.value=value
                    except ProductUrlEav.DoesNotExist:
                        obj=ProductUrlEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                    data=json.loads(serializers.serialize("json",[obj,]))
                    fields=data[0]["fields"]
                    fields["id"]=data[0]["pk"]
                    modelSerializer=ProductUrlEavSerializer(data=fields)
                elif eav_type=="BOOLEAN":
                    try:
                        obj=ProductBooleanEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                        obj.value=value
                    except ProductBooleanEav.DoesNotExist:
                        obj=ProductBooleanEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                    data=json.loads(serializers.serialize("json",[obj,]))
                    fields=data[0]["fields"]
                    fields["id"]=data[0]["pk"]
                    modelSerializer=ProductBooleanEavSerializer(data=fields)
                elif eav_type=="TEXT":
                    try:
                        obj=ProductTextEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                        obj.value=value
                    except ProductTextEav.DoesNotExist:
                        obj=ProductTextEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)
                    data=json.loads(serializers.serialize("json",[obj,]))
                    fields=data[0]["fields"]
                    fields["id"]=data[0]["pk"]
                    modelSerializer=ProductTextEavSerializer(data=fields)
                elif eav_type=="CHAR":
                    try:
                        obj=ProductCharEav.objects.get(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute)
                        obj.value=value
                    except ProductCharEav.DoesNotExist:
                        obj=ProductCharEav(company=company,marketplace=marketplace,sku=serializer.validated_data["sku"],attribute=attribute,value=value)                    
                    data=json.loads(serializers.serialize("json",[obj,]))
                    fields=data[0]["fields"]
                    fields["id"]=data[0]["pk"]
                    modelSerializer=ProductCharEavSerializer(data=fields)

                if eav_type=="DECIMAL" and "value" in value and value["value"] in ["",None] and obj.id:
                    obj.delete()
                elif eav_type=="DECIMAL" and ("value" not in value or "unit" not in value):
                    pass
                elif  eav_type!="DECIMAL" and value in ["",None] and obj.id:
                    obj.delete()
                else:
                    try:
                        if modelSerializer.is_valid():
                            eav_type_objs[eav_type].append(obj)
                    except ValidationError as e:
                        raise APIException(detail="Il valore dell'attributo '"+str(attribute)+"' non è valido! '''"+str(e)+"'''")
            

        try:
            if serializer.is_valid():
                serializer.save()
                productObj=ProductSimple.objects.get(id=serializer.data["id"])
                productObj.save()
                for eav_type,eav_objs in eav_type_objs.items():
                    for eav_obj in eav_objs:
                        eav_obj.save()
                        if eav_type=="INT" and eav_obj not in productObj.int_eav.all():
                            productObj.int_eav.add(eav_obj)
                        elif eav_type=="DECIMAL" and eav_obj not in productObj.decimal_eav.all():
                            productObj.decimal_eav.add(eav_obj)
                        elif eav_type=="URL" and eav_obj not in productObj.url_eav.all():
                            productObj.url_eav.add(eav_obj)
                        elif eav_type=="BOOLEAN" and eav_obj not in productObj.boolean_eav.all():
                            productObj.boolean_eav.add(eav_obj)
                        elif eav_type=="TEXT" and eav_obj not in productObj.text_eav.all():
                            productObj.text_eav.add(eav_obj)
                        elif eav_type=="CHAR" and eav_obj not in productObj.char_eav.all():
                            productObj.char_eav.add(eav_obj)
                if "item" in serializer.initial_data:
                    itemObj=Item.objects.get(id=serializer.initial_data["item"]["id"],company=company)
                    productObj.item=itemObj
                    productObj.save()
                    update_InStockQty(productObj.item,productObj.item.inStockQty)
                
            else:
                raise APIException(detail="Errore!")
        except IntegrityError:
            raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name))

    



class AbstractProductListMixin(object):
    def get_queryset(self):
        
        
        marketplace=self.request.GET.get("marketplace")
        queryset=queryset.filter(char_eav__marketplace=marketplace)|\
            queryset.filter(text_eav__marketplace=marketplace)|\
                queryset.filter(int_eav__marketplace=marketplace)|\
                    queryset.filter(decimal_eav__marketplace=marketplace)|\
                        queryset.filter(boolean_eav__marketplace=marketplace)|\
                            queryset.filter(url_eav__marketplace=marketplace)
        queryset=queryset.order_by('sku').distinct("sku")


class ProductConfigurableViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        marketplace=self.request.GET.get("marketplace")
        queryset=queryset.filter(marketplace=marketplace)

        search=None
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            queryset=queryset.filter(sku__icontains=search)|queryset.filter(gtin__contains=search)\
                |queryset.filter(char_eav__value__icontains=search,char_eav__marketplace=marketplace)\
                |queryset.filter(text_eav__value__icontains=search,text_eav__marketplace=marketplace)
            return queryset.order_by("id").distinct()
        return queryset.order_by("id")

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.validated_data["marketplace"]=marketplace
                serializer.save()
                productConfigurableObj=ProductConfigurable.objects.get(id=serializer.data["id"])
                productConfigurableObj.save()
                for attribute in Attribute.objects.filter(id__in=serializer.initial_data["variations"]):
                    productConfigurableObj.variations.add(attribute)
                for simple in ProductSimple.objects.filter(id__in=serializer.initial_data["products"],company=company,marketplace=marketplace):
                    productConfigurableObj.products.add(simple)
                productConfigurableObj.save()
        except IntegrityError:
            raise PermissionDenied(detail="Lo SKU %s esiste già in questo marketplace" % (serializer.validated_data["sku"]))


    def perform_update(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.validated_data["marketplace"]=marketplace
                serializer.save()
                productConfigurableObj=ProductConfigurable.objects.get(id=serializer.data["id"])
                for attribute in Attribute.objects.filter(id__in=serializer.initial_data["variations"]):
                    productConfigurableObj.variations.add(attribute)
                for simple in ProductSimple.objects.filter(id__in=serializer.initial_data["products"],company=company,marketplace=marketplace):
                    productConfigurableObj.products.add(simple)
                productConfigurableObj.save()
                for variation in productConfigurableObj.variations.all():
                    if variation.id not in serializer.initial_data["variations"]:
                        productConfigurableObj.variations.remove(variation)
                for simple in productConfigurableObj.products.all():
                    if simple.id not in serializer.initial_data["products"]:
                        productConfigurableObj.products.remove(simple)
                productConfigurableObj.save()
        except IntegrityError:
            raise PermissionDenied(detail="Lo SKU %s esiste già in questo marketplace" % (serializer.validated_data["sku"]))
        

class ProductBulkViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        marketplace=self.request.GET.get("marketplace")
        queryset=queryset.filter(marketplace=marketplace)

        search=None
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            queryset=queryset.filter(sku__icontains=search)|queryset.filter(gtin__contains=search)\
                |queryset.filter(char_eav__value__icontains=search,char_eav__marketplace=marketplace)\
                |queryset.filter(text_eav__value__icontains=search,text_eav__marketplace=marketplace)
            return queryset.order_by("id").distinct()
        return queryset.order_by("id")


    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.validated_data["marketplace"]=marketplace
                bulkAssociations=[]
                for child in serializer.initial_data["childs"]:
                    bulkproductqtyObj=BulkProductQty(company=company,marketplace=marketplace,bulk_sku=serializer.validated_data["sku"])
                    bulkproductqtyObj.product=ProductSimple.objects.get(company=company,marketplace=marketplace,id=child["id"])
                    bulkproductqtyObj.qty=child["qty"]
                    try:
                        bulkproductqtyObj.save()
                        bulkAssociations.append(bulkproductqtyObj)
                    except:
                        for obj in bulkAssociations:
                            obj.delete()
                        raise APIException(detail="Errore nel creare l'associazione bulk/semplice")
                
                serializer.save()
                obj=ProductBulk.objects.get(id=serializer.data["id"],company=company,marketplace=marketplace)
                for objass in bulkAssociations:
                    obj.bulk_products_qty.add(objass)
                obj.save()
            else:
                raise APIException(detail="Invalido!")
        except IntegrityError:
            raise PermissionDenied(detail="Lo SKU %s esiste già in questo marketplace" % (serializer.validated_data["sku"]))

    def perform_update(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        try:
            
            if serializer.is_valid():
                serializer.save()
                bulk=ProductBulk.objects.get(id=serializer.instance.id,company=company,marketplace=marketplace)
                bulkAssociations=[]
                
                for child in serializer.initial_data["childs"]:
                    print(child["id"])
                    product=ProductSimple.objects.get(company=company,marketplace=marketplace,id=child["id"])
                    if bulk.bulk_products_qty.filter(product=product).exists():
                        bulkproductqtyObj=bulk.bulk_products_qty.get(product=product)
                        bulkproductqtyObj.qty=child["qty"]
                        bulkproductqtyObj.save()
                    else:
                        bulkproductqtyObj=BulkProductQty(company=company,marketplace=marketplace,bulk_sku=serializer.validated_data["sku"],product=product)
                        bulkproductqtyObj.qty=child["qty"]
                        try:
                            bulkproductqtyObj.save()
                            bulkAssociations.append(bulkproductqtyObj)
                        except:
                            for obj in bulkAssociations:
                                obj.delete()
                            raise APIException(detail="Errore nel creare l'associazione bulk/semplice")
                
                for objass in bulkAssociations:
                    bulk.bulk_products_qty.add(objass)
                bulk.save()

                products_child_ids=[]
                for child in serializer.initial_data["childs"]:
                    products_child_ids.append(child["id"])
                for bulkproductqtyObj in bulk.bulk_products_qty.all():
                    if bulkproductqtyObj.product.id not in products_child_ids:
                        bulkproductqtyObj.delete()
                
            else:
                raise APIException(detail="Invalido!")
        except IntegrityError:
            raise PermissionDenied(detail="Lo SKU %s esiste già in questo marketplace" % (serializer.validated_data["sku"]))

class ProductMultipleViewMixin(object):

    def get_queryset(self):
        queryset=super().get_queryset("products")
        marketplace=self.request.GET.get("marketplace")
        queryset=queryset.filter(marketplace=marketplace)

        search=None
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            queryset=queryset.filter(sku__icontains=search)|queryset.filter(gtin__contains=search)\
                |queryset.filter(char_eav__value__icontains=search,char_eav__marketplace=marketplace)\
                |queryset.filter(text_eav__value__icontains=search,text_eav__marketplace=marketplace)
            return queryset.order_by("id").distinct()
                

        return queryset.order_by("id")

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.validated_data["marketplace"]=marketplace
                serializer.validated_data["product"]=ProductSimple.objects.get(id=serializer.initial_data["child"],company=company,marketplace=marketplace)
                serializer.validated_data["qty"]=serializer.initial_data["qty"]
                serializer.save()
                    
            else:
                raise APIException(detail="Invalido!")
        except IntegrityError:
            raise PermissionDenied(detail="Lo SKU %s esiste già in questo marketplace" % (serializer.validated_data["sku"]))

    def perform_update(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        try:
            if serializer.is_valid():
                serializer.validated_data["company"]=company
                serializer.validated_data["marketplace"]=marketplace
                try:
                    serializer.validated_data["product"]=ProductSimple.objects.get(id=serializer.initial_data["child"],company=company,marketplace=marketplace)
                except:
                    raise APIException(detail="Prodotto semplice non valido!")    
                serializer.validated_data["qty"]=serializer.initial_data["qty"]
                serializer.save()
                    
            else:
                raise APIException(detail="Invalido!")
        except IntegrityError:
            raise PermissionDenied(detail="Errore nell'associare il nuovo prodotto")