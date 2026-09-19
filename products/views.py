from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import AbstractProductsForCategorySimpleSerializer
from .serializers import AbstractProductsForCategoryBulkSerializer
from .serializers import AbstractProductsForCategoryMultipleSerializer
from .serializers import AbstractProductsForCategoryConfigurableSerializer

from .serializers import ProductSimpleSerializer,ProductMultipleSerializer,ProductConfigurableSerializer,ProductBulkSerializer
from .serializers import CustomAttributeSerializer,AttributeSerializer,DefaultAttributeSerializer,CategorySerializer
from .serializers import AbstractProductsSimpleSerializer,AbstractProductsMultipleSerializer,AbstractProductsConfigurableSerializer,AbstractProductsBulkSerializer
from .mixins import ProductAttributeViewMixin, ProductSimpleViewMixin,CategoryViewMixin,CustomAttributeViewMixin,CategorySimplifyViewMixin
from .mixins import ProductConfigurableViewMixin,ProductBulkViewMixin,ProductMultipleViewMixin
from .mixins import FilterCategoryMixin
from backend.mixins import AuthorizationMixin
from .models import ProductSimple,ProductMultiple,ProductBulk,ProductConfigurable
# from .models import ProductBulkOfMultiple,ProductBulkOfBulk
# from .models import ProductMultipleOfBulk,ProductMultipleOfMultiple
# from .models import ProductConfigurableOfMultiple,ProductConfigurableOfBulk
# from .serializers import ProductBulkOfBulkSerializer,ProductBulkOfMultipleSerializer,ProductMultipleOfBulkSerializer,ProductMultipleOfMultipleSerializer
# from .serializers import ProductConfigurableOfBulkSerializer,ProductConfigurableOfMultipleSerializer
from .models import ProductBooleanEav,ProductCharEav,ProductIntEav,ProductTextEav,ProductDecimalEav,ProductUrlEav
from .models import Attribute,DefaultAttribute,CustomAttribute,Category
from companies.models import Company
from marketplaces.models import Marketplace
from rest_framework.exceptions import PermissionDenied
from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
import shutil
import re
import base64
from io import BytesIO
import os
from companies.models import Authorization
import json
# Create your views here.

class CustomAttributeViewSet(CustomAttributeViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = CustomAttribute
    permission_class = IsAuthenticated
    serializer_class = CustomAttributeSerializer

custom_attributes_list = CustomAttributeViewSet.as_view({'get':'list','post':'create'})
custom_attribute_detail = CustomAttributeViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class AttributeViewSet(ProductAttributeViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Attribute
    permission_class = IsAuthenticated
    serializer_class = AttributeSerializer

attributes_list = AttributeViewSet.as_view({'get':'list','post':'create'})
attribute_detail = AttributeViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class CategoryViewSet(CategoryViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Category
    permission_class = IsAuthenticated
    serializer_class = CategorySerializer

categories_list = CategoryViewSet.as_view({'get':'list','post':'create'})
category_detail = CategoryViewSet.as_view({'get':'retrieve','put':'partial_update','delete':'destroy'})

class CategorySimplifyViewSet(CategorySimplifyViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Category
    permission_class = IsAuthenticated
    serializer_class = CategorySerializer

categories_simplify_list = CategorySimplifyViewSet.as_view({'get':'list'})










class ProductSimpleViewSet(ProductSimpleViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductSimple
    permission_class = IsAuthenticated
    serializer_class = ProductSimpleSerializer

product_simple_list = ProductSimpleViewSet.as_view({'get':'list','post':'create'})
product_simple_detail = ProductSimpleViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class ProductConfigurableViewSet(ProductConfigurableViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductConfigurable
    permission_class = IsAuthenticated
    serializer_class = ProductConfigurableSerializer

product_configurable_list = ProductConfigurableViewSet.as_view({'get':'list','post':'create'})
product_configurable_detail = ProductConfigurableViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


class AbstractProductsSimpleViewSet(ProductSimpleViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductSimple
    permission_class = IsAuthenticated
    serializer_class = AbstractProductsSimpleSerializer

abstract_product_simple_list = AbstractProductsSimpleViewSet.as_view({'get':'list'})

class AbstractProductsForCategorySimpleViewSet(FilterCategoryMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductSimple
    permission_class = IsAuthenticated
    serializer_class = AbstractProductsForCategorySimpleSerializer

abstract_product_for_category_simple_list = AbstractProductsForCategorySimpleViewSet.as_view({'get':'list'})

class AbstractProductsForCategoryConfigurableViewSet(FilterCategoryMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductConfigurable
    permission_class = IsAuthenticated
    serializer_class = AbstractProductsForCategoryConfigurableSerializer

abstract_product_for_category_configurable_list = AbstractProductsForCategoryConfigurableViewSet.as_view({'get':'list'})

class AbstractProductsForCategoryMultipleViewSet(FilterCategoryMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductMultiple
    permission_class = IsAuthenticated
    serializer_class = AbstractProductsForCategoryMultipleSerializer

abstract_product_for_category_multiple_list = AbstractProductsForCategoryMultipleViewSet.as_view({'get':'list'})


class AbstractProductsForCategoryBulkViewSet(FilterCategoryMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductBulk
    permission_class = IsAuthenticated
    serializer_class = AbstractProductsForCategoryBulkSerializer

abstract_product_for_category_bulk_list = AbstractProductsForCategoryBulkViewSet.as_view({'get':'list'})

class AbstractProductsConfigurableViewSet(ProductConfigurableViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductConfigurable
    permission_class = IsAuthenticated
    serializer_class = AbstractProductsConfigurableSerializer

abstract_product_configurable_list = AbstractProductsConfigurableViewSet.as_view({'get':'list'})

class AbstractProductsMultipleViewSet(ProductMultipleViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductMultiple
    permission_class = IsAuthenticated
    serializer_class = AbstractProductsMultipleSerializer

abstract_product_multiple_list = AbstractProductsMultipleViewSet.as_view({'get':'list'})

class AbstractProductsBulkViewSet(ProductBulkViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductBulk
    permission_class = IsAuthenticated
    serializer_class = AbstractProductsBulkSerializer

abstract_product_bulk_list = AbstractProductsBulkViewSet.as_view({'get':'list'})






class CategoryProductAddDelete(APIView):
    permission_class= IsAuthenticated

    def put(self,request,pk):
        if not Company.objects.filter(pk=self.request.GET.get("company")).exists():
            raise PermissionDenied("Permesso negato")
        company=Company.objects.get(id=self.request.GET.get("company"))
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            permission=Authorization.Permissions.MODIFY
            try:
                if Authorization.objects.get(user=self.request.user,application="products",company=company).permission<permission:
                    raise PermissionDenied("Permesso negato")
            except:
                raise PermissionDenied("Permesso negato")
        try:
            marketplace=Marketplace.objects.get(company=company,id=self.request.GET.get("marketplace"))
        except:
            raise PermissionDenied("Market non valido")
        try:
            category=Category.objects.get(company=company,marketplace=marketplace,id=pk)
        except:
            raise PermissionDenied("Market non valido")
        source=json.loads(self.request.body)
        products_id=source["products"]
        products_type=source["products_type"]
        products=None
        if products_type=="simple":
            products=ProductSimple.objects.filter(id__in=products_id,company=company,marketplace=marketplace)
            for product in products:
                category.simple.add(product)
            category.save()
        elif products_type=="configurable":
            products=ProductConfigurable.objects.filter(id__in=products_id,company=company,marketplace=marketplace)
            for product in products:
                category.configurable.add(product)
            category.save()
        elif products_type=="multiple":
            products=ProductMultiple.objects.filter(id__in=products_id,company=company,marketplace=marketplace)
            for product in products:
                category.multiple.add(product)
            category.save()
        elif products_type=="bulk":
            products=ProductBulk.objects.filter(id__in=products_id,company=company,marketplace=marketplace)
            for product in products:
                category.bulk.add(product)
            category.save()
        else:
            raise PermissionDenied("Prodotti non validi")
        return JsonResponse({"response":"Prodotti aggiunti"})
    
    def delete(self,request,pk):
        if not Company.objects.filter(pk=self.request.GET.get("company")).exists():
            raise PermissionDenied("Permesso negato")
        company=Company.objects.get(id=self.request.GET.get("company"))
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            permission=Authorization.Permissions.MODIFY
            try:
                if Authorization.objects.get(user=self.request.user,application="products",company=company).permission<permission:
                    raise PermissionDenied("Permesso negato")
            except:
                raise PermissionDenied("Permesso negato")
        try:
            marketplace=Marketplace.objects.get(company=company,id=self.request.GET.get("marketplace"))
        except:
            raise PermissionDenied("Market non valido")
        try:
            category=Category.objects.get(company=company,marketplace=marketplace,id=pk)
        except:
            raise PermissionDenied("Market non valido")
        source=json.loads(self.request.body)
        products_id=source["products"]
        products_type=source["products_type"]
        products=None
        if products_type=="simple":
            products=ProductSimple.objects.filter(id__in=products_id,company=company,marketplace=marketplace)
            for product in products:
                category.simple.remove(product)
            category.save()
        elif products_type=="configurable":
            products=ProductConfigurable.objects.filter(id__in=products_id,company=company,marketplace=marketplace)
            for product in products:
                category.configurable.remove(product)
            category.save()
        elif products_type=="multiple":
            products=ProductMultiple.objects.filter(id__in=products_id,company=company,marketplace=marketplace)
            for product in products:
                category.multiple.remove(product)
            category.save()
        elif products_type=="bulk":
            products=ProductBulk.objects.filter(id__in=products_id,company=company,marketplace=marketplace)
            for product in products:
                category.bulk.remove(product)
            category.save()
        else:
            raise PermissionDenied("Prodotti non validi")
        return JsonResponse({"response":"Prodotti eliminati"})

class CopyFromSimple(APIView):
    permission_class= IsAuthenticated

    def put(self,request):
        
        if not Company.objects.filter(pk=self.request.GET.get("company")).exists():
            raise PermissionDenied("Permesso negato")
        company=Company.objects.get(id=self.request.GET.get("company"))
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            permission=Authorization.Permissions.MODIFY
            try:
                if Authorization.objects.get(user=self.request.user,application="products",company=company).permission<permission:
                    raise PermissionDenied("Permesso negato")
            except:
                raise PermissionDenied("Permesso negato")
        try:
            destinationMarketplace=Marketplace.objects.get(company=company,id=self.request.GET.get("marketplace"))
        except:
            raise PermissionDenied("Market di destinazione non valido")

        source=json.loads(self.request.body)
        sourceProduct=None
        sourceMarketplace=None
        overwriteifnull=source["overwrite"]
        try:
            if source["product"]["simple"] is not None:
                sourceProduct=ProductSimple.objects.get(company=company,id=source["product"]["simple"])
            elif source["product"]["configurable"] is not None:
                sourceProduct=ProductConfigurable.objects.get(company=company,id=source["product"]["configurable"])
            elif source["product"]["multiple"] is not None:
                sourceProduct=ProductMultiple.objects.get(company=company,id=source["product"]["multiple"])
            elif source["product"]["bulk"] is not None:
                sourceProduct=ProductBulk.objects.get(company=company,id=source["product"]["bulk"])
            else:
                raise PermissionDenied("Errore prodotto di origine")    
        except:
            raise PermissionDenied("Errore prodotto di origine")
        
        try:
            if source["marketplace"] is not None:
                sourceMarketplace=Marketplace.objects.get(company=company,id=source["marketplace"])
            else:
                raise PermissionDenied("Errore Marketplace di origine")    
        except:
            raise PermissionDenied("Errore Marketplace di origine")

        for field in source["fields"]:
            if field not in ["title","description","short_description","keywords","bullet_point","brand","images"]:
                raise PermissionDenied("Campo non valido! ["+str(field)+"]")

        data={}
        for field in source["fields"]:
            sourceAttribute=None
            destinationAttribute=None
            if DefaultAttribute.objects.filter(name=field).exists():
                attribute_type=DefaultAttribute.objects.get(name=field).type
                eav=None
                if attribute_type == "CHAR":
                    eav=sourceProduct.char_eav
                elif attribute_type == "INT":
                    eav=sourceProduct.int_eav
                elif attribute_type == "TEXT":
                    eav=sourceProduct.text_eav
                elif attribute_type == "BOOLEAN":
                    eav=sourceProduct.boolean_eav
                elif attribute_type == "DECIMAL":
                    eav=sourceProduct.decimal_eav
                elif attribute_type == "URL":
                    eav=sourceProduct.url_eav
                
                try:
                    sourceAttribute=eav.get(sku=sourceProduct.sku,attribute=field,marketplace=sourceMarketplace,company=company)
                    data[field]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data[field]=None
                
                
            elif field=="bullet_point":
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="bullet_point1",marketplace=sourceMarketplace,company=company)
                    data["bullet_point1"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["bullet_point1"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="bullet_point2",marketplace=sourceMarketplace,company=company)
                    data["bullet_point2"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["bullet_point2"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="bullet_point3",marketplace=sourceMarketplace,company=company)
                    data["bullet_point3"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["bullet_point3"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="bullet_point4",marketplace=sourceMarketplace,company=company)
                    data["bullet_point4"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["bullet_point4"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="bullet_point5",marketplace=sourceMarketplace,company=company)
                    data["bullet_point5"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["bullet_point5"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="bullet_point6",marketplace=sourceMarketplace,company=company)
                    data["bullet_point6"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["bullet_point6"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="bullet_point7",marketplace=sourceMarketplace,company=company)
                    data["bullet_point7"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["bullet_point7"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="bullet_point8",marketplace=sourceMarketplace,company=company)
                    data["bullet_point8"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["bullet_point8"]=None
                
            elif field=="images":
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="image0",marketplace=sourceMarketplace,company=company)
                    data["image0"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["image0"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="image1",marketplace=sourceMarketplace,company=company)
                    data["image1"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["image1"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="image2",marketplace=sourceMarketplace,company=company)
                    data["image2"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["image2"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="image3",marketplace=sourceMarketplace,company=company)
                    data["image3"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["image3"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="image4",marketplace=sourceMarketplace,company=company)
                    data["image4"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["image4"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="image5",marketplace=sourceMarketplace,company=company)
                    data["image5"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["image5"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="image6",marketplace=sourceMarketplace,company=company)
                    data["image6"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["image6"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="image7",marketplace=sourceMarketplace,company=company)
                    data["image7"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["image7"]=None
                try:
                    sourceAttribute=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute="image8",marketplace=sourceMarketplace,company=company)
                    data["image8"]=sourceAttribute.value
                except ObjectDoesNotExist:
                    if overwriteifnull:
                        data["image8"]=None
            else:
                pass
        destinationProduct=ProductSimple.objects.get(id=self.request.GET.get("product"),company=company)
        for name,value in data.items():
            destinationAttribute=None
            attribute_type=DefaultAttribute.objects.get(name=name).type
            eav=None
            if attribute_type == "CHAR":
                try:
                    destinationAttribute=destinationProduct.char_eav.get(sku=destinationProduct.sku,attribute=name,company=company,marketplace=destinationMarketplace)
                    if value not in [None,""]:
                        destinationAttribute.value=value
                        destinationAttribute.save()
                    else:
                        destinationAttribute.delete()
                except ObjectDoesNotExist:
                    if value not in [None,""]:
                        destinationAttribute=ProductCharEav(attribute=name,marketplace=destinationMarketplace,company=company,sku=destinationProduct.sku,value=value)
                        destinationAttribute.save()
                        destinationProduct.char_eav.add(destinationAttribute)
                        destinationProduct.save()
            elif attribute_type == "INT":
                try:
                    destinationAttribute=destinationProduct.int_eav.get(sku=destinationProduct.sku,attribute=name,company=company,marketplace=destinationMarketplace)
                    if value not in [None,""]:
                        destinationAttribute.value=value
                        destinationAttribute.save()
                    else:
                        destinationAttribute.delete()
                except ObjectDoesNotExist:
                    if value not in [None,""]:
                        destinationAttribute=ProductIntEav(attribute=name,marketplace=destinationMarketplace,company=company,sku=destinationProduct.sku,value=value)
                        destinationAttribute.save()
                        destinationProduct.int_eav.add(destinationAttribute)
                        destinationProduct.save()
            elif attribute_type == "TEXT":
                try:
                    destinationAttribute=destinationProduct.text_eav.get(sku=destinationProduct.sku,attribute=name,company=company,marketplace=destinationMarketplace)
                    if value not in [None,""]:
                        destinationAttribute.value=value
                        destinationAttribute.save()
                    else:
                        destinationAttribute.delete()
                except ObjectDoesNotExist:
                    if value not in [None,""]:
                        destinationAttribute=ProductTextEav(attribute=name,marketplace=destinationMarketplace,company=company,sku=destinationProduct.sku,value=value)
                        destinationAttribute.save()
                        destinationProduct.text_eav.add(destinationAttribute)
                        destinationProduct.save()
            elif attribute_type == "BOOLEAN":
                try:
                    destinationAttribute=destinationProduct.boolean_eav.get(sku=destinationProduct.sku,attribute=name,company=company,marketplace=destinationMarketplace)
                    if value not in [None,""]:
                        destinationAttribute.value=value
                        destinationAttribute.save()
                    else:
                        destinationAttribute.delete()
                except ObjectDoesNotExist:
                    if value not in [None,""]:
                        destinationAttribute=ProductBooleanEav(attribute=name,marketplace=destinationMarketplace,company=company,sku=destinationProduct.sku,value=value)
                        destinationAttribute.save()
                        destinationProduct.boolean_eav.add(destinationAttribute)
                        destinationProduct.save()
            elif attribute_type == "DECIMAL":
                try:
                    destinationAttribute=destinationProduct.decimal_eav.get(sku=destinationProduct.sku,attribute=name,company=company,marketplace=destinationMarketplace)
                    if value not in [None,""]:
                        destinationAttribute.value=value
                        destinationAttribute.save()
                    else:
                        destinationAttribute.delete()
                except ObjectDoesNotExist:
                    if value not in [None,""]:
                        destinationAttribute=ProductDecimalEav(attribute=name,marketplace=destinationMarketplace,company=company,sku=destinationProduct.sku,value=value)
                        destinationAttribute.save()
                        destinationProduct.decimal_eav.add(destinationAttribute)
                        destinationProduct.save()
            elif attribute_type == "URL":
                try:
                    destinationAttribute=destinationProduct.url_eav.get(sku=destinationProduct.sku,attribute=name,company=company,marketplace=destinationMarketplace)
                    if value not in [None,""]:
                        destinationAttribute.value=value
                        destinationAttribute.save()
                    else:
                        destinationAttribute.delete()
                except ObjectDoesNotExist:
                    if value not in [None,""]:
                        destinationAttribute=ProductUrlEav(attribute=name,marketplace=destinationMarketplace,company=company,sku=destinationProduct.sku,value=value)
                        destinationAttribute.save()
                        destinationProduct.url_eav.add(destinationAttribute)
                        destinationProduct.save()
        return JsonResponse({"content":"OK"})


class CopyToSimple(APIView):
    permission_class= IsAuthenticated

    def put(self,request):
        if not Company.objects.filter(pk=self.request.GET.get("company")).exists():
            raise PermissionDenied("Permesso negato")
        company=Company.objects.get(id=self.request.GET.get("company"))
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            permission=Authorization.Permissions.MODIFY
            try:
                if Authorization.objects.get(user=self.request.user,application="products",company=company).permission<permission:
                    raise PermissionDenied("Permesso negato")
            except:
                raise PermissionDenied("Permesso negato")
        
        sourceProduct=ProductSimple.objects.get(id=self.request.GET.get("product"),company=company)
        sourceMarketplace=Marketplace.objects.get(company=company,id=self.request.GET.get("marketplace"))

        destination=json.loads(self.request.body)
        
        overwriteifnull=destination["overwrite"]
        for field in destination["fields"]:
            if field not in ["title","description","short_description","keywords","bullet_point","brand","images"]:
                raise PermissionDenied("Campo non valido! ["+str(field)+"]")

        
        
        try:
            Marketplace.objects.get(company=company,id=destination["marketplace"])
        except:
            raise PermissionDenied("Market di destinazione non valido")
        

        for product in destination["products"]["simple"]:
            try:
                ProductSimple.objects.get(id=product,company=company)
            except:
                raise PermissionDenied("Prodotto di destinazione non esistente")
        for product in destination["products"]["multiple"]:
            try:
                ProductMultiple.objects.get(id=product,company=company)
            except:
                raise PermissionDenied("Prodotto di destinazione non esistente")
        for product in destination["products"]["bulk"]:
            try:
                ProductBulk.objects.get(id=product,company=company)
            except:
                raise PermissionDenied("Prodotto di destinazione non esistente")
        for product in destination["products"]["configurable"]:
            try:
                ProductConfigurable.objects.get(id=product,company=company)
            except:
                raise PermissionDenied("Prodotto di destinazione non esistente")


        data={}
        for field in destination["fields"]:
            sourceAttribute=None
            if DefaultAttribute.objects.filter(name=field).exists():
                attribute_type=DefaultAttribute.objects.get(name=field).type
                if attribute_type == "CHAR":
                    try:
                        data[field]=sourceProduct.char_eav.get(sku=sourceProduct.sku,attribute=field,marketplace=sourceMarketplace).value
                    except ObjectDoesNotExist:
                        if overwriteifnull:
                            data[field]=None
                elif attribute_type == "INT":
                    try:
                        data[field]=sourceProduct.int_eav.get(sku=sourceProduct.sku,attribute=field,marketplace=sourceMarketplace).value
                    except ObjectDoesNotExist:
                        if overwriteifnull:
                            data[field]=None
                elif attribute_type == "TEXT":
                    try:
                        data[field]=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute=field,marketplace=sourceMarketplace).value
                    except ObjectDoesNotExist:
                        if overwriteifnull:
                            data[field]=None
                elif attribute_type == "BOOLEAN":
                    try:
                        data[field]=sourceProduct.boolean_eav.get(sku=sourceProduct.sku,attribute=field,marketplace=sourceMarketplace).value
                    except ObjectDoesNotExist:
                        if overwriteifnull:
                            data[field]=None
                elif attribute_type == "DECIMAL":
                    try:
                        data[field]=sourceProduct.decimal_eav.get(sku=sourceProduct.sku,attribute=field,marketplace=sourceMarketplace).value
                    except ObjectDoesNotExist:
                        if overwriteifnull:
                            data[field]=None
                elif attribute_type == "URL":
                    try:
                        data[field]=sourceProduct.url_eav.get(sku=sourceProduct.sku,attribute=field,marketplace=sourceMarketplace).value
                    except ObjectDoesNotExist:
                        if overwriteifnull:
                            data[field]=None
                
            elif field=="bullet_point":
                for bullet in ["bullet_point1","bullet_point2","bullet_point3","bullet_point4","bullet_point5","bullet_point6","bullet_point7","bullet_point8"]:
                    try:
                        data[bullet]=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute=bullet,marketplace=sourceMarketplace).value
                    except ObjectDoesNotExist:
                        if overwriteifnull:
                            data[bullet]=None
            elif field=="images":
               for image in ["image0","image1","image2","image3","image4","image5","image6","image7","image8"]:
                    try:
                        data[image]=sourceProduct.text_eav.get(sku=sourceProduct.sku,attribute=image,marketplace=sourceMarketplace).value
                    except ObjectDoesNotExist:
                        if overwriteifnull:
                            data[image]=None
            else:
                pass
        
        destinationProducts=[]
        for product_id in destination["products"]["simple"]:
            destinationProducts.append(ProductSimple.objects.get(id=product_id,company=company))
        for product_id in destination["products"]["bulk"]:
            destinationProducts.append(ProductBulk.objects.get(id=product_id,company=company))
        for product_id in destination["products"]["multiple"]:
            destinationProducts.append(ProductMultiple.objects.get(id=product_id,company=company))
        for product_id in destination["products"]["configurable"]:
            destinationProducts.append(ProductConfigurable.objects.get(id=product_id,company=company))
        destinationMarketplace=Marketplace.objects.get(id=destination["marketplace"],company=company)
        for product in destinationProducts:
            for name,value in data.items():
                
                attribute_type=DefaultAttribute.objects.get(name=name).type
                if attribute_type == "CHAR":
                    try:
                        attribute=product.char_eav.get(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name)
                        if value is None:
                            attribute.delete()
                        else:
                            attribute.value=data[name]
                    except ObjectDoesNotExist:
                        if value is not None:
                            attribute=ProductCharEav(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name,value=value)
                            attribute.save()
                            product.char_eav.add(attribute)
                            product.save()
                elif attribute_type == "TEXT":
                    try:
                        attribute=product.text_eav.get(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name)
                        if value is None:
                            attribute.delete()
                        else:
                            attribute.value=data[name]
                    except ObjectDoesNotExist:
                        if value is not None:
                            attribute=ProductTextEav(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name,value=value)
                            attribute.save()
                            product.text_eav.add(attribute)
                            product.save()
                elif attribute_type == "URL":
                    try:
                        attribute=product.url_eav.get(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name)
                        if value is None:
                            attribute.delete()
                        else:
                            attribute.value=data[name]
                    except ObjectDoesNotExist:
                        if value is not None:
                            attribute=ProductUrlEav(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name,value=value)
                            attribute.save()
                            product.url_eav.add(attribute)
                            product.save()
                elif attribute_type == "BOOLEAN":
                    try:
                        attribute=product.boolean_eav.get(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name)
                        if value is None:
                            attribute.delete()
                        else:
                            attribute.value=data[name]
                    except ObjectDoesNotExist:
                        if value is not None:
                            attribute=ProductBooleanEav(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name,value=value)
                            attribute.save()
                            product.boolean_eav.add(attribute)
                            product.save()
                elif attribute_type == "INT":
                    try:
                        attribute=product.int_eav.get(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name)
                        if value is None:
                            attribute.delete()
                        else:
                            attribute.value=data[name]
                    except ObjectDoesNotExist:
                        if value is not None:
                            attribute=ProductIntEav(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name,value=value)
                            attribute.save()
                            product.int_eav.add(attribute)
                            product.save()
                elif attribute_type == "DECIMAL":
                    try:
                        attribute=product.decimal_eav.get(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name)
                        if value is None:
                            attribute.delete()
                        else:
                            attribute.value=data[name]
                    except ObjectDoesNotExist:
                        if value is not None:
                            attribute=ProductDecimalEav(sku=product.sku,company=company,marketplace=destinationMarketplace,attribute=name,value=value)
                            attribute.save()
                            product.decimal_eav.add(attribute)
                            product.save()

        return JsonResponse({"content":"OK"})

class SimplifyConfigurableCombinations(APIView):
    permission_class= IsAuthenticated

    def put(self,request):
        from pprint import PrettyPrinter
        pp=PrettyPrinter()

        if not Company.objects.filter(pk=self.request.GET.get("company")).exists():
            raise PermissionDenied("Permesso negato")
        company=Company.objects.get(id=self.request.GET.get("company"))
        if not Marketplace.objects.filter(company=company,id=self.request.GET.get("marketplace")).exists():
            raise PermissionDenied("Permesso negato")
        marketplace=Marketplace.objects.get(id=self.request.GET.get("marketplace"),company=company)
        if not self.request.user.is_superuser and not self.request.user.is_staff:
            permission=Authorization.Permissions.MODIFY
            try:
                if Authorization.objects.get(user=self.request.user,application="products",company=company).permission<permission:
                    raise PermissionDenied("Permesso negato")
            except:
                raise PermissionDenied("Permesso negato")
        
        
        data=json.loads(self.request.body)
        results={}
        results["category"]=data["category"]
        category=Category.objects.get(id=data["category"],marketplace=marketplace,company=company)
        pp.pprint(data)
        
        if len(data["childs_selected"])==0 and len(data["variations_selected"])==0:
            results["childs_availables"]=json.loads(json.dumps(AbstractProductsSimpleSerializer(category.simple.all(),many=True).data))
            results["variations_availables"]=json.loads(json.dumps(AttributeSerializer(category.variations.all(),many=True).data))
            results["childs_selected"]=None
            results["variations_selected"]=None

        elif len(data["childs_selected"])==0 and len(data["variations_selected"])>0:
            results["childs_selected"]=data["childs_selected"]
            results["variations_selected"]=data["variations_selected"]
            variations_availables=category.variations.all()
            for var in data["variations_selected"]:
                variations_availables=variations_availables.exclude(id=var['id'])
            results["variations_availables"]=json.loads(json.dumps(AttributeSerializer(variations_availables,many=True).data))
            childs=category.simple.all()
            for selvar in data["variations_selected"]:
                if selvar["type"]=="INT":
                    childs=childs.filter(int_eav__attribute=selvar["name"])
                if selvar["type"]=="CHAR":
                    childs=childs.filter(char_eav__attribute=selvar["name"])
                if selvar["type"]=="DECIMAL":
                    childs=childs.filter(decimal_eav__attribute=selvar["name"])
                if selvar["type"]=="BOOLEAN":
                    childs=childs.filter(boolean_eav__attribute=selvar["name"])
            results["childs_availables"]=json.loads(json.dumps(AbstractProductsSimpleSerializer(childs,many=True).data))

        elif len(data["childs_selected"])>0 and len(data["variations_selected"])==0:
            variations_availables=category.variations.all()
            results["childs_selected"]=data["childs_selected"]
            childs_selected_id=[]
            for child in results["childs_selected"]:
                childs_selected_id.append(child["id"])
            childs_selected=category.simple.filter(id__in=childs_selected_id)
            
            for child in childs_selected:
                for variation in variations_availables:
                    if child.char_eav.filter(attribute=variation.name).exists():
                        pass
                    elif child.text_eav.filter(attribute=variation.name).exists():
                        pass
                    elif child.int_eav.filter(attribute=variation.name).exists():
                        pass
                    elif child.decimal_eav.filter(attribute=variation.name).exists():
                        pass
                    elif child.boolean_eav.filter(attribute=variation.name).exists():
                        pass
                    else:
                        variations_availables=variations_availables.exclude(name=variation.name)

            childs_availables=category.simple.all().difference(childs_selected)
            results["childs_availables"]=json.loads(json.dumps(AbstractProductsSimpleSerializer(childs_availables,many=True).data))
            results["variations_selected"]=None
            results["variations_availables"]=json.loads(json.dumps(AttributeSerializer(variations_availables,many=True).data))


        elif len(data["childs_selected"])>0 and len(data["variations_selected"])>0:
            variations_availables=category.variations.all()
            results["childs_selected"]=data["childs_selected"]
            childs_selected_id=[]
            for child in results["childs_selected"]:
                childs_selected_id.append(child["id"])
            childs_selected=category.simple.filter(id__in=childs_selected_id)

            for child in childs_selected:
                for variation in variations_availables:
                    if child.char_eav.filter(attribute=variation.name).exists():
                        pass
                    elif child.text_eav.filter(attribute=variation.name).exists():
                        pass
                    elif child.int_eav.filter(attribute=variation.name).exists():
                        pass
                    elif child.decimal_eav.filter(attribute=variation.name).exists():
                        pass
                    elif child.boolean_eav.filter(attribute=variation.name).exists():
                        pass
                    else:
                        variations_availables=variations_availables.exclude(name=variation.name)
            childs_availables=category.simple.all().exclude(id__in=childs_selected_id)
            for selvar in data["variations_selected"]:
                if selvar["type"]=="INT":
                    childs_availables=childs_availables.filter(int_eav__attribute=selvar["name"])
                if selvar["type"]=="CHAR":
                    childs_availables=childs_availables.filter(char_eav__attribute=selvar["name"])
                if selvar["type"]=="DECIMAL":
                    childs_availables=childs_availables.filter(decimal_eav__attribute=selvar["name"])
                if selvar["type"]=="BOOLEAN":
                    childs_availables=childs_availables.filter(boolean_eav__attribute=selvar["name"])
            childs_availables=childs_availables.difference(childs_selected)
            for var in data["variations_selected"]:
                variations_availables=variations_availables.exclude(id=var['id'])
            results["childs_availables"]=json.loads(json.dumps(AbstractProductsSimpleSerializer(childs_availables,many=True).data))
            results["variations_availables"]=json.loads(json.dumps(AttributeSerializer(variations_availables,many=True).data))
            results["variations_selected"]=data["variations_selected"]
            
        
        
        
        
        return JsonResponse({"result":results})
            

# childs_available=set()

#         if len(childs_selected) is 0 and len(variations_selected) is 0:
#             for obj in objs:
#                 try:
#                     variations_available=variations_available.union(set(dict(json.loads(obj.value)).keys()))
#                 except json.decoder.JSONDecodeError:
#                     pass
#             childs_available=set(objs.order_by("sku").values_list("sku",flat=True))
#         elif len(childs_selected) > 0 and len(variations_selected) is 0:
#             for sku in childs_selected:
#                 if len(variations_available) is 0:
#                     variations_available=set(dict(json.loads(objs.get(sku=sku,attribute="others").value)).keys())
#                 else:
#                     variations_available=variations_available.intersection(set(dict(json.loads(objs.get(sku=sku,attribute="others").value)).keys()))
#             for obj in objs:
#                 if len(variations_available-set(dict(json.loads(obj.value)).keys())) is 0:
#                     childs_available.add(obj.sku)

#         elif len(childs_selected) is 0 and len(variations_selected) > 0:
#             for obj in objs:
#                 if len(set(variations_selected)-set(dict(json.loads(obj.value)).keys())) is 0:
#                     childs_available.add(obj.sku)
#                     if len(variations_available) is 0:
#                         variations_available = set(dict(json.loads(obj.value)).keys())
#                     else:
#                         variations_available = variations_available.intersection(set(dict(json.loads(obj.value)).keys()))
#         else:
#             for sku in childs_selected:
#                 if len(variations_available) is 0:
#                     variations_available=set(dict(json.loads(objs.get(sku=sku,attribute="others").value)).keys())
#                 else:
#                     variations_available=variations_available.intersection(set(dict(json.loads(objs.get(sku=sku,attribute="others").value)).keys()))
#             for obj in objs:
#                 if len(variations_available-set(dict(json.loads(obj.value)).keys())) is 0:
#                     childs_available.add(obj.sku)

#             for obj in objs:
#                 if len(set(variations_selected)-set(dict(json.loads(obj.value)).keys())) is 0:
#                     childs_available.add(obj.sku)
#                     if len(variations_available) is 0:
#                         variations_available = set(dict(json.loads(obj.value)).keys())
#                     else:
#                         variations_available = variations_available.intersection(set(dict(json.loads(obj.value)).keys()))

#         childs_available=list(set(childs_available)-set(childs_selected))
#         variations_available=list(variations_available-set(variations_selected))
#         childs={"availables":childs_available,"selected":childs_selected}
#         variations={"availables":variations_available,"selected":variations_selected}
#         response={"childs":childs,"variations":variations}
#         return JsonResponse(response)


class ProductMultipleViewSet(ProductMultipleViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductMultiple
    permission_class = IsAuthenticated
    serializer_class = ProductMultipleSerializer

product_multiple_list = ProductMultipleViewSet.as_view({'get':'list','post':'create'})
product_multiple_detail = ProductMultipleViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class ProductBulkViewSet(ProductBulkViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ProductBulk
    permission_class = IsAuthenticated
    serializer_class = ProductBulkSerializer

product_bulk_list = ProductBulkViewSet.as_view({'get':'list','post':'create'})
product_bulk_detail = ProductBulkViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})




# class ProductBulkOfBulkViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductBulkOfBulk
#     permission_classes = IsAuthenticated
#     serializer_class = ProductBulkOfBulkSerializer

# product_bulk_of_bulk_list = ProductBulkOfBulkViewSet.as_view({'get':'list'})
# product_bulk_of_bulk_detail = ProductBulkOfBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductBulkOfMultipleViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductBulkOfMultiple
#     permission_classes = IsAuthenticated
#     serializer_class = ProductBulkOfMultipleSerializer

# product_bulk_of_multiple_list = ProductBulkOfMultipleViewSet.as_view({'get':'list'})
# product_bulk_of_multiple_detail = ProductBulkOfMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductMultipleOfBulkViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductMultipleOfBulk
#     permission_classes = IsAuthenticated
#     serializer_class = ProductMultipleOfBulkSerializer

# product_multiple_of_bulk_list = ProductMultipleOfBulkViewSet.as_view({'get':'list'})
# product_multiple_of_bulk_detail = ProductMultipleOfBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductMultipleOfMultipleViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductMultipleOfMultiple
#     permission_classes = IsAuthenticated
#     serializer_class = ProductMultipleOfMultipleSerializer

# product_multiple_of_multiple_list = ProductMultipleOfMultipleViewSet.as_view({'get':'list'})
# product_multiple_of_multiple_detail = ProductMultipleOfMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductConfigurableOfBulkViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductConfigurableOfBulk
#     permission_classes = IsAuthenticated
#     serializer_class = ProductConfigurableOfBulkSerializer

# product_configurable_of_bulk_list = ProductConfigurableOfBulkViewSet.as_view({'get':'list'})
# product_configurable_of_bulk_detail = ProductConfigurableOfBulkViewSet.as_view({'get':'retrieve','delete':'destroy'})

# class ProductConfigurableOfMultipleViewSet(ProductMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = ProductConfigurableOfMultiple
#     permission_classes = IsAuthenticated
#     serializer_class = ProductConfigurableOfMultipleSerializer

# product_configurable_of_multiple_list = ProductConfigurableOfMultipleViewSet.as_view({'get':'list'})
# product_configurable_of_multiple_detail = ProductConfigurableOfMultipleViewSet.as_view({'get':'retrieve','delete':'destroy'})



