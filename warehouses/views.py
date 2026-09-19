from django.shortcuts import render
from products.models import ProductSimple,ProductBulk,ProductMultiple
from .models import Item,ItemQty,WareHouse,ItemInfoFiles
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.mixins import AuthorizationMixin
from rest_framework import serializers
from companies.models import Company
from rest_framework.parsers import MultiPartParser
import os
from django.conf import settings
from datetime import datetime
import shutil
from rest_framework.exceptions import APIException,PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
def update_InStockQty(item,qty):
    company=item.company
    item.inStockQty=qty
    item.save()
    for product in ProductSimple.objects.filter(company=item.company,item=item):
        product.inStockQty=item.inStockQty
        print(product.sku)
        product.save()
        productsMultiple=ProductMultiple.objects.filter(company=company,product=product)
        for productMultiple in productsMultiple:
            
            print(int(product.inStockQty/productMultiple.qty))
            productMultiple.inStockQty=int(product.inStockQty/productMultiple.qty)
            productMultiple.save()

        for productBulk in ProductBulk.objects.filter(company=company,bulk_products_qty__product=product):
            qtys=[]
            for product_qty_obj in productBulk.bulk_products_qty.all():
                qty_now=product.inStockQty
                qtys.append(int(qty_now/product_qty_obj.qty))
            
            productBulk.inStockQty=min(qtys)
            productBulk.save()
        

def updateWarehouseQtyItem(item,warehouse,qty):
    obj=ItemQty.objects.get(item=item,warehouse=warehouse)
    difference=obj.qty-qty
    obj.qty=qty
    if item.inStockQty-difference<0:
        print("errore")
    else:
        obj.save()
        update_InStockQty(item,item.inStockQty-difference)
    

class WareHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WareHouse
        fields = '__all__'
        read_only_fields = ('company','code')

class WarehouseViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("warehouses")
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            queryset=queryset.filter(code__icontains=search)|queryset.filter(code__contains=search)\
                |queryset.filter(name__contains=search)|queryset.filter(name__icontains=search)\
                    |queryset.filter(address__contains=search)|queryset.filter(address__icontains=search)
            return queryset.order_by("id").distinct()
        return queryset.order_by("id")

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        serializer.validated_data["company"]=company
        if serializer.is_valid():
            serializer.save()
            
class WarehouseViewSet(WarehouseViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = WareHouse
    permission_class = IsAuthenticated
    serializer_class = WareHouseSerializer

warehouse_list = WarehouseViewSet.as_view({'get':'list','post':'create'})
warehouse_detail = WarehouseViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


class ItemInfoFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInfoFiles
        fields = '__all__'
        read_only_fields = ('company','path')

class ItemInfoFilesMixin(object):
    def get_queryset(self):
        return super().get_queryset('warehouse').order_by('-create')

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        serializer.validated_data["company"]=company
        
        
        if serializer.is_valid():
            path=os.path.join(settings.PRIVATE_DIR,company.vid,"items",serializer.validated_data["item_code"])
            relative_path=os.path.join(company.vid,"items",serializer.validated_data["item_code"])
            now=datetime.now()
            filename=serializer.validated_data["item_code"]+"_"+self.request.FILES["file"].name
            if not os.path.exists(path):
                os.makedirs(path,exist_ok=True)
            shutil.move(self.request.FILES["file"].temporary_file_path(), os.path.join(path,filename))
            serializer.validated_data["path"]=os.path.join(relative_path,filename)
            serializer.save()


class ItemInfoFilesViewSet(ItemInfoFilesMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ItemInfoFiles
    permission_class = IsAuthenticated
    serializer_class = ItemInfoFilesSerializer
    parser_classes= (MultiPartParser,)

item_info_files_list = ItemInfoFilesViewSet.as_view({'get':'list','post':'create'})

# import_file = ItemInfoFilesRetrieveViewSet.as_view({'get':'retrieve'})


class ItemQtySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemQty
        fields = '__all__'
        read_only_fields = ('company','item','warehouse')

class ItemQtyViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("warehouses")
        return queryset.order_by("id")

class ItemQtyViewSet(ItemQtyViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = ItemQty
    permission_class = IsAuthenticated
    serializer_class = ItemQtySerializer

items_qty_list = ItemQtyViewSet.as_view({'get':'list','post':'create'})
items_qty_detail = ItemQtyViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ('company','inStockQty','item_qty')
        depth=1

class ItemViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("warehouses")
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            queryset=queryset.filter(item_code__icontains=search)|queryset.filter(item_code__contains=search)\
                |queryset.filter(name__contains=search)|queryset.filter(name__icontains=search)
            return queryset.order_by("id").distinct()
        return queryset.order_by("id")

    def perform_create(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        warehouse=WareHouse.objects.get(id=self.request.GET.get("warehouse"),company=company)
        serializer.validated_data["company"]=company
        if serializer.is_valid():
            serializer.save()
            id=serializer.data["id"]
            item=Item.objects.get(company=company,id=id)
            for id_files in serializer.initial_data["files"]:
                item_infoObj=ItemInfoFiles.objects.get(id=id_files,company=company)
                item.files.add(item_infoObj)
            for warehouse in WareHouse.objects.filter(company=company,id=warehouse.id):
                itemqtyObj=ItemQty(company=company,warehouse=warehouse,qty=0,item_code=serializer.validated_data["item_code"])
                itemqtyObj.save()
                item.item_qty.add(itemqtyObj)
            item.inStockQty=0

            item.save()
            
    def perform_update(self,serializer):
        company=Company.objects.get(id=self.request.GET.get("company"))
        warehouse=None
        if "warehouse" in serializer.initial_data:
            warehouse=WareHouse.objects.get(id=serializer.initial_data["warehouse"])
            if serializer.instance.item_qty.filter(company=company,warehouse=warehouse).exists():
                qty=serializer.initial_data["qty"]
            else:
                qty=0
        
        if serializer.is_valid():
            serializer.save()


            item=Item.objects.get(id=serializer.data["id"],company=company)
            for id_files in serializer.initial_data["files"]:
                item_infoObj=ItemInfoFiles.objects.get(id=id_files,company=company)
                item.files.add(item_infoObj)
            item.save()
            toDeleteFiles=item.files.exclude(id__in=serializer.initial_data["files"])
            for obj in toDeleteFiles:
                obj.delete()
            #Aggiorno Qta nel magazzino scelto
            if warehouse:
                try:
                    item_qty=item.item_qty.get(warehouse=warehouse,company=company)
                    old_item_qty=item_qty.qty     # 3 nel magazzino
                    old_inStockQty=item.inStockQty   #3 disponibili
                    item_qty.qty=qty          # 3 -> 7
                    item_qty.save()
                    update_InStockQty(item,old_inStockQty+(qty-old_item_qty))
                except ObjectDoesNotExist:
                    item_qty=ItemQty(warehouse=warehouse,company=company)
                    item_qty.qty=0
                    item_qty.item_code=item.item_code
                    item_qty.save()
                    item.item_qty.add(item_qty)

    def perform_destroy(self,instance):
        # 2) se non ci sono ordini associati
        # si mettono le quantità di tutti i magazzini a zero-> di conseguenza cambieranno le inStockQty
        # 3) se non ci sono ordini associati e se le quantità dei magazzini sono a zero
        # posso eliminare il prodotto e chiedo se si vogliono eliminare anche le schede del prodotto associate
        company=Company.objects.get(id=self.request.GET.get("company"))
        qty_all=0
        for obj in instance.item_qty.all():
            qty_all+=obj.qty
        if qty_all-instance.inStockQty>0:
            raise PermissionDenied(detail="Non puoi eliminare l'articolo. \nCi sono ordini con questo articolo che devono essere ancora spediti!")
        elif qty_all>0:
            update_InStockQty(instance,0)
            for obj in instance.item_qty.all():
                obj.qty=0
                obj.save()
        elif qty_all==0 and instance.inStockQty==0:
            if self.request.GET.get("purge")==1:
                for product in ProductSimple.objects.filter(company=company,item=instance):
                    product.delete()
            instance.delete()
            
            # non si può eliminare e si invia il messaggio .. ci sono prodotti da spedire
            


    
        




class ItemViewSet(ItemViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Item
    permission_class = IsAuthenticated
    serializer_class = ItemSerializer
    

items_list = ItemViewSet.as_view({'get':'list','post':'create'})
items_detail = ItemViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})





