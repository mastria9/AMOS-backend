from imports.models import Import
from orders.models import OrderDetail,Order
from products.models import ProductBooleanEav,ProductBulk,ProductCharEav,ProductConfigurable,ProductDecimalEav,ProductIntEav,ProductMultiple,ProductSimple,ProductTextEav,ProductUrlEav
from datetime import datetime
from django.conf import settings
import os
from os.path import splitext,basename,join
from marketplaces.models import Marketplace
from pprint import PrettyPrinter
from django.core.exceptions import ObjectDoesNotExist
import json
class CheckField():
    def __init__(self):
        pass
    def check(self,fields,template,ftype):
        valid_fields=[]
        if template=="AMZ" and ftype=="orders":
            valid_fields=[
                "order-id",
                "order-item-id",
                "purchase-date",
                "payments-date",
                "buyer-email",
                "buyer-name",
                "buyer-phone-number",
                "sku",
                "product-name",
                "quantity-purchased",
                "currency",
                "item-price",
                "item-tax",
                "shipping-price",
                "shipping-tax",
                "ship-service-level",
                "recipient-name",
                "ship-address-1",
                "ship-address-2",
                "ship-address-3",
                "ship-city",
                "ship-state",
                "ship-postal-code",
                "ship-country",
                "ship-phone-number",
                "delivery-start-date",
                "delivery-end-date",
                "delivery-time-zone",
                "delivery-Instructions",
                "sales-channel",
                "is-business-order",
                "purchase-order-number",
                "price-designation",
                "is-iba"
            ]
        elif template=="AMZ" and ftype=="products":
            valid_fields=[
            "seller-sku",
            "asin1",
            "item-name",
            "item-description",
            "product-id-type",
            "product-id",
            "listing-id",
            "price",
            "quantity",
            "open-date",
            "item-note",
            "item-condition",
            "will-ship-internationally",
            "expedited-shipping",
            "pending-quantity",
            "fulfillment-channel",
            "Business Price",
            "Quantity Price Type",
            "Quantity Lower Bound 1",
            "Quantity Price 1",
            "Quantity Lower Bound 2",
            "Quantity Price 2",
            "Quantity Lower Bound 3",
            "Quantity Price 3",
            "Quantity Lower Bound 4",
            "Quantity Price 4",
            "Quantity Lower Bound 5",
            "Quantity Price 5",
            "optional-payment-type-exclusion",
            "scheduled-delivery-sku-set",
            "merchant-shipping-group",
            "standard-price-point",
            "ProductTaxCode",
            "VatExclusivePrice",
            "VatExclusiveBusinessPrice",
            "VatExclusiveQuantityPrice1",
            "VatExclusiveQuantityPrice2",
            "VatExclusiveQuantityPrice3",
            "VatExclusiveQuantityPrice4",
            "VatExclusiveQuantityPrice5",
            "status",
            "minimum-seller-allowed-price",
            "maximum-seller-allowed-price",
            "Progressive Price Type",
            "Progressive Lower Bound 1",
            "Progressive Price 1",
            "Progressive Lower Bound 2",
            "Progressive Price 2",
            "Progressive Lower Bound 3",
            "Progressive Price 3",
            "Minimum order quantity",
            "Sell remainder"
            ]

        else:
            return False
        for field in fields:
            if field not in valid_fields:
                return False
        return True

class ProcessProducts():
    def __init__(self,obj):
        self.obj=obj
        
    
    def selectProcess(self):
        
        if self.obj.template=="AMZ" and splitext(basename(join(settings.PRIVATE_DIR,self.obj.path)))[1][1:].strip().lower()=="txt":
            self.process_amazon_products_txt()
        else:
            self.obj.message="Associazione template/estensione non riconosciuta"
            self.obj.status="E"
            self.obj.save()
            return
        
    
    def process_amazon_products_txt(self):
        import csv

        filepath=os.path.join(settings.PRIVATE_DIR,self.obj.path)
        with open(filepath,"r",newline='',encoding="utf-8-sig") as fp:
            reader=csv.reader(fp,delimiter="\t")
            check=True
            fields=[]
            products=[]
            for row in reader:
                if(check):
                    checking=CheckField()
                    if checking.check(row,self.obj.template,self.obj.ftype):
                        check=False
                        fields=row
                    else:
                        fp.close()
                        return
                else:
                    product={}
                    for i in range(len(fields)):
                        product[fields[i]]=row[i]
                    products.append(product)
                    
        fp.close()
        
        pp=PrettyPrinter()
        messages={}
        
        count=1
        marketplace=Marketplace.objects.get(company=self.obj.company,country=self.obj.country,code="AMZ")
        for product in products:
            count+=1
            detail=None
            try:
                if ProductBulk.objects.filter(sku=product["seller-sku"],company=self.obj.company).exists():
                    detail=ProductBulk.objects.get(sku=product["seller-sku"],company=self.obj.company)
                elif ProductConfigurable.objects.filter(sku=product["seller-sku"],company=self.obj.company).exists():
                    detail=ProductConfigurable.objects.get(sku=product["seller-sku"],company=self.obj.company)
                elif ProductMultiple.objects.filter(sku=product["seller-sku"],company=self.obj.company).exists():
                    detail=ProductMultiple.objects.get(sku=product["seller-sku"],company=self.obj.company)
                elif ProductSimple.objects.filter(sku=product["seller-sku"],company=self.obj.company).exists():
                    detail=ProductSimple.objects.get(sku=product["seller-sku"],company=self.obj.company)
                else:
                    detail=ProductSimple(sku=product["seller-sku"],company=self.obj.company)

                if product["product-id-type"]==1:
                    detail.gtin_type="NOGTIN"
                detail.save()

                if "asin1" in product and product["asin1"] not in [None,""]:
                    attr=None
                    if detail.char_eav.filter(sku=detail.sku,attribute="asin",company=self.obj.company,marketplace=marketplace).exists():
                        attr=detail.char_eav.get(sku=detail.sku,attribute="asin",company=self.obj.company,marketplace=marketplace)
                    else:
                        attr=ProductCharEav(sku=detail.sku,attribute="asin",company=self.obj.company,marketplace=marketplace)
                    attr.value=product["asin1"]
                    attr.save()
                    detail.char_eav.add(attr)
                    detail.save()

                if "item-name" in product and product["item-name"] not in [None,""]:
                    attr=None
                    if detail.char_eav.filter(sku=detail.sku,attribute="title",company=self.obj.company,marketplace=marketplace).exists():
                        attr=detail.char_eav.get(sku=detail.sku,attribute="title",company=self.obj.company,marketplace=marketplace)
                    else:
                        attr=ProductCharEav(sku=detail.sku,attribute="title",company=self.obj.company,marketplace=marketplace)
                    attr.value=product["item-name"]
                    attr.save()
                    detail.char_eav.add(attr)
                    detail.save()

                if "item-description" in product and product["item-description"] not in [None,""]:
                    attr=None
                    if detail.text_eav.filter(sku=detail.sku,attribute="description",company=self.obj.company,marketplace=marketplace).exists():
                        attr=detail.text_eav.get(sku=detail.sku,attribute="description",company=self.obj.company,marketplace=marketplace)
                    else:
                        attr=ProductTextEav(sku=detail.sku,attribute="description",company=self.obj.company,marketplace=marketplace)
                    attr.value=product["item-description"]
                    attr.save()
                    detail.text_eav.add(attr)
                    detail.save()

            except Exception as e:
                pp.pprint(e)
                messages[count]=str(e)
            
        
        if len(messages)==len(products):
            self.obj.messages=json.dumps(messages)
            self.obj.status="E"
        elif len(messages)>0:
            self.obj.messages=json.dumps(messages)
            self.obj.status="DE"
        else:
            self.obj.messages=None
            self.obj.status="D"
        self.obj.save()
        return



class ProcessOrders():
    def __init__(self,obj):
        self.obj=obj
        
    
    def selectProcess(self):
        
        if self.obj.template=="AMZ" and splitext(basename(join(settings.PRIVATE_DIR,self.obj.path)))[1][1:].strip().lower()=="txt":
            self.process_amazon_orders_txt()
        else:
            self.obj.message="Associazione template/estensione non riconosciuta"
            self.obj.status="E"
            self.obj.save()
            return
        

    def process_amazon_orders_txt(self):
        import csv

        filepath=os.path.join(settings.PRIVATE_DIR,self.obj.path)
        with open(filepath,"r",encoding="UTF-8") as fp:
            reader=csv.reader(fp,delimiter="\t")
            check=True
            fields=[]
            orders=[]
            for row in reader:
                if(check):
                    checking=CheckField()
                    if checking.check(row,self.obj.template,self.obj.ftype):
                        check=False
                        fields=row
                    else:
                        fp.close()
                        return
                else:
                    order={}
                    for i in range(len(fields)):
                        order[fields[i]]=row[i]
                    orders.append(order)
                    
        fp.close()
        
        pp=PrettyPrinter()
        pp.pprint(orders)
        messages={}
        count=1
        orders_obj=[]
        for order in orders:
            count+=1
            try:
                marketplace=None
                detail=OrderDetail()

                sales_channel=order["sales-channel"].split(".")
                if sales_channel[0].upper()=="AMAZON":
                    marketplace=Marketplace.objects.get(company=self.obj.company,country=sales_channel[1].upper(),code="AMZ")
                try:
                    detail=OrderDetail.objects.get(order_id=order["order-id"],order_item_id=order["order-item-id"],company=self.obj.company,marketplace=marketplace)
                except ObjectDoesNotExist:
                    detail=OrderDetail(order_id=order["order-id"],order_item_id=order["order-item-id"],company=self.obj.company,marketplace=marketplace)
                detail.order_id=order["order-id"]
                detail.order_item_id=order["order-item-id"]
                detail.marketplace=marketplace
                detail.shipping_name=order["recipient-name"].upper()
                detail.shipping_address=order["ship-address-1"]+" "+order["ship-address-2"]+" "+order["ship-address-3"]
                detail.shipping_phone=order["ship-phone-number"]
                detail.shipping_city=order["ship-city"]
                detail.shipping_cap=order["ship-postal-code"]
                detail.shipping_country=order["ship-country"].upper()
                detail.shipping_state=order["ship-state"]
                detail.shipping_instructions=order["delivery-Instructions"]
                detail.sku=order["sku"]
                detail.qty=int(order["quantity-purchased"])
                detail.title=order["product-name"]
                detail.company=self.obj.company
                detail.price=order["item-price"]
                detail.iva=order["item-tax"]
                detail.shipping_price=order["shipping-price"]
                detail.shipping_iva=order["shipping-tax"]
                detail.date=order["purchase-date"]
                if order["payments-date"]:
                    detail.payments_date=order["payments-date"]
                    detail.status="N"
                else:
                    detail.status="PP"
                if order["is-business-order"].lower()=="true":
                    detail.business=True
                detail.save()
                


                #Creo un oggetto ordine riepilogativo e ci attacco i dettagli
                order_obj=None
                try:
                    order_obj=Order.objects.get(company=self.obj.company,marketplace=marketplace,order_id=detail.order_id)
                except ObjectDoesNotExist:
                    order_obj=Order(company=self.obj.company,marketplace=marketplace,order_id=detail.order_id)
                    order_obj.save()
                try:
                    order_obj.order_detail.get(company=self.obj.company,marketplace=marketplace,order_id=detail.order.id,order_item_id=detail.order_item_id)
                except:
                    order_obj.order_detail.add(detail)
                    order_obj.save()

                if order_obj not in orders_obj:
                    orders_obj.append(order_obj)

                
        

                
                

                
                


            except Exception as e:
                pp.pprint(e)
                messages[count]=str(e)
            
        

        for order_obj in orders_obj:
            order_obj.order_price=0
            order_obj.order_iva=0
            order_obj.shipping_price=0
            order_obj.shipping_iva=0
            order_obj.order_total=0
            order_obj.shipping_total=0
            order_obj.order_shipping_total=0
            for order_list in order_obj.order_detail.all():
                order_obj.order_price+=order_list.price
                order_obj.order_iva+=order_list.iva
                order_obj.shipping_price+=order_list.shipping_price
                order_obj.shipping_iva+=order_list.shipping_iva
                order_obj.order_total+=order_list.price+order_list.shipping_price
            order_obj.save()
            
                

        # shipping=None
                # if detail.shipping is not None:
                #     shipping=detail.shipping
                # else:
                #     shipping=Shipping()
                # shipping.company=self.obj.company
                # shipping.marketplace=marketplace
                # shipping.shipping_name=order["recipient-name"].upper()
                # shipping.shipping_address=order["ship-address-1"]+" "+order["ship-address-2"]+" "+order["ship-address-3"]
                # shipping.shipping_phone=order["ship-phone-number"]
                # shipping.shipping_city=order["ship-city"]
                # shipping.shipping_cap=order["ship-postal-code"]
                # shipping.shipping_country=order["ship-country"].upper()
                # shipping.shipping_state=order["ship-state"]
                # shipping.save()




        if len(messages)==len(orders):
            self.obj.messages=json.dumps(messages)
            self.obj.status="E"
        elif len(messages)>0:
            self.obj.messages=json.dumps(messages)
            self.obj.status="DE"
        else:
            self.obj.messages=None
            self.obj.status="D"
        self.obj.save()
        return




def process_imports():
    objs=Import.objects.filter(status="N").order_by('create')

    
    if objs.exists() and not Import.objects.filter(status="W").exists():
        obj=objs[0]
        if obj.ftype=="orders":
            engine=ProcessOrders(obj)
            engine.selectProcess()
        elif obj.ftype=="products":
            engine=ProcessProducts(obj)
            engine.selectProcess()
        else:
            obj.status="DE"
            obj.message="Nessun tipo di import effettuabile"
            obj.save()

    return
        # workbook=WorkBook()
        
        # try:
        #     isCSV=False
        #     extension=obj.filename.split(".")[-1]
        #     if extension in ["csv","txt"]:
        #         isCSV=True
        #         obj.datasheet["sheetindex"]=0

        #     workbook.load_workbook_from_path(os.path.join(settings.PRIVATE_DIR,obj.path,obj.filename),isCSV)
            
        #     # se c'è uno sheetindex ed è in stato U
        #     # restituisco il foglio
        #     if obj.datasheet["sheetindex"]!="":
        #         if obj.datasheet["index"]!=obj.datasheet["sheetindex"]:
        #             datasheet=workbook.datasheet(int(obj.datasheet["sheetindex"]),cut=True)
        #             obj.datasheet["datasheet"]=datasheet
        #             obj.datasheet["index"]=obj.datasheet["sheetindex"]
        #             attributes={}
        #             if obj.ftype=="products":
        #                 print("PRODUCTS")
        #                 for attrObj in Attribute.objects.filter(company=obj.company).order_by("name"):
        #                     attributes[attrObj.name]=attrObj.description
        #             elif obj.ftype=="orders":
        #                 print("ORDER")
        #                 for attrObj in OrderDetail._meta.fields:
        #                     attributes[attrObj]=OrderDetail._meta.get_field(attrObj).verbose_name
        #             obj.datasheet["attributes"]=attributes
        #             obj.status="C"
        #             obj.save()
                    

        #     elif obj.datasheet["sheetnames"]==[]:
        #         obj.datasheet["sheetnames"]=workbook.sheetnames()
        #         obj.status="C"
        #         obj.save()

        

            
            
        # except:
        #     print("Errore")
        #     obj.status="E"
        #     obj.save()
        
        # workbook.close()









# def process_imports_job():
    
#     objs=Import.objects.filter(status="W").order_by('create')
#     print(datetime.now())
#     if objs.exists():
#         print("Eseguo")

#         obj=objs[0]
#         obj.status="R"
#         obj.save()
#         workbook=WorkBook()
#         isCSV=False
#         extension=obj.filename.split(".")[-1]
#         if extension in ["csv","txt"]:
#             isCSV=True
#         try:
#             workbook.load_workbook_from_path(os.path.join(settings.PRIVATE_DIR,obj.path,obj.filename),isCSV)
#             jump=obj.datasheet["jump"] # 2
#             columns=obj.datasheet["columns"]
#             rows=obj.datasheet["rows"]
            
#             fields={}
#             for key,value in columns.items():
#                 if value not in ["",None]:
#                     fields[str(key)]={}
#                     fields[str(key)]["name"]=value
#                     if obj.ftype=="products":
#                         fields[str(key)]["type"]=Attribute.objects.get(company=obj.company,name=value).type
#                     elif obj.ftype=="orders":
#                         fields[str(key)]["type"]=OrderDetail.objects.get(name=value).type

#             sheetindex=obj.datasheet["index"]
#             if obj.ftype=="products":
#                 messages=workbook.importDatasheetToProducts(company=obj.company,sheetindex=sheetindex,jump=jump,columns=fields,rows=rows,marketplaces=obj.marketplace)
#             elif obj.ftype=="orders":
#                 messages=workbook.importDatasheetToOrders(company=obj.company,sheetindex=sheetindex,jump=jump,columns=fields,rows=rows,marketplace=obj.marketplace)
#             obj.messages=messages
#             obj.status="D"
#             obj.save()
#         except Exception as exc:
#             obj.status="E"
#             obj.messages={0:"Errore non gestito. "+str(exc)}
#             obj.save()

#         workbook.close()