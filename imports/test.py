from rest_framework.views import APIView
from django.http.response import JsonResponse
from .cron import process_imports


class TestImport(APIView):
    def get(self,request):
        process_imports()
        return JsonResponse({"content":"OK"})
# def imports_job(request):
    
#     objs=Import.objects.filter(status="N").order_by('create')

#     print(datetime.now())
#     if objs.exists():
#         obj=objs[0]
#         print(obj.ftype)
#         print("OK")
#         workbook=WorkBook()
        
#         try:
#             isCSV=False
#             extension=obj.filename.split(".")[-1]
#             if extension in ["csv","txt"]:
#                 isCSV=True
#                 obj.datasheet["sheetindex"]=0

#             workbook.load_workbook_from_path(os.path.join(settings.PRIVATE_DIR,obj.path,obj.filename),isCSV)
            
#             # se c'è uno sheetindex ed è in stato U
#             # restituisco il foglio
            
#             if obj.datasheet["sheetindex"]!="":
#                 if obj.datasheet["index"]!=obj.datasheet["sheetindex"]:
#                     datasheet=workbook.datasheet(int(obj.datasheet["sheetindex"]),cut=True)
#                     obj.datasheet["datasheet"]=datasheet
#                     obj.datasheet["index"]=obj.datasheet["sheetindex"]
#                     attributes={}
#                     if obj.ftype=="products":
#                         print("PRODUCTS")
#                         for attrObj in Attribute.objects.filter(company=obj.company).order_by("name"):
#                             attributes[attrObj.name]=attrObj.description
#                     elif obj.ftype=="orders":
#                         print("ORDER")
#                         attributes["orders"]={}
#                         for attrObj in OrderDetail._meta.get_fields(include_parents=False, include_hidden=False):
#                             if attrObj.name.lower() not in ["id","status",'company','marketplace','customer','shipping']:
#                                 try:
#                                     attributes["orders"][attrObj.name]=OrderDetail._meta.get_field(attrObj.name).verbose_name
#                                 except:
#                                     pass
#                         attributes["customer"]={}
#                         for attrObj in Customer._meta.get_fields(include_parents=False, include_hidden=False):
#                             if attrObj.name.lower() not in ["id",'company']:
#                                 try:
#                                     attributes["customer"][attrObj.name]=Customer._meta.get_field(attrObj.name).verbose_name
#                                 except:
#                                     pass
#                         attributes["shipping"]={}
#                         for attrObj in Shipping._meta.get_fields(include_parents=False, include_hidden=False):
#                             if attrObj.name.lower() not in ["id",'company','tracking','marketplace','courier','create','sent',"status",'qty','cod','cod_method']:
#                                 try:
#                                     attributes["shipping"][attrObj.name]=Shipping._meta.get_field(attrObj.name).verbose_name
#                                 except:
#                                     pass
                        
                        
#                     obj.datasheet["attributes"]=attributes
#                     obj.status="C"
#                     obj.save()
                    

#             elif obj.datasheet["sheetnames"]==[]:
#                 obj.datasheet["sheetnames"]=workbook.sheetnames()
#                 obj.status="C"
#                 obj.save()

        

            
            
#         except Exception as exc:
#             print(exc)
#             obj.status="E"
#             obj.save()
        
#         workbook.close()
#     return HttpResponse("CIAO")

    
    
# def process_imports_job(request):
    
#     objs=Import.objects.filter(status="W").order_by('create')
#     print(datetime.now())
#     if objs.exists():
#         print("Eseguo")

#         obj=objs[0]
#         obj.status="P"
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
#             updateType=obj.datasheet["updateType"]
            
#             fields={}
#             for key,value in columns.items():
#                 if value not in ["",None]:
#                     fields[str(key)]={}
#                     fields[str(key)]["name"]=value
#                     if obj.ftype=="products":
#                         fields[str(key)]["type"]=Attribute.objects.get(company=obj.company,name=value).type
                    

#             sheetindex=obj.datasheet["index"]
#             if obj.ftype=="products":
#                 messages=workbook.importDatasheetToProducts(company=obj.company,sheetindex=sheetindex,jump=jump,columns=fields,rows=rows,marketplaces=obj.marketplace)
#             elif obj.ftype=="orders":
#                 messages=workbook.importDatasheetToOrders(company=obj.company,sheetindex=sheetindex,jump=jump,columns=fields,rows=rows)
#             obj.messages=messages
#             obj.status="D"
#             obj.save()
#         except Exception as exc:
#             obj.status="E"
#             obj.messages=[{0:"Errore non gestito. "+str(exc)}]
#             obj.save()

        
#         workbook.close()
#     return HttpResponse("CIAO")



# def delorders(request):
#     from orders.models import OrderDetail,Order
#     for od in Order.objects.all():
#         od.delete()
#     for od in OrderDetail.objects.all():
#         od.delete()
#     for sh in Shipping.objects.all():
#         sh.delete()
#     for csu in Customer.objects.all():
#         csu.delete()
#     return HttpResponse("Ordini cancellati")
