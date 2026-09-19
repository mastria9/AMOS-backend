from django.db import models
from companies.models import Company
# from products.models import ProductSimple,ProductBulk,ProductMultiple
# from warehouses import Item

# #Trasformare in Magazzino

# # Create your models here.
# class StockSimpleProduct(models.Model):
#     company=models.ForeignKey(Company,on_delete=models.CASCADE)
#     qty=models.IntegerField(default=0)
    
#     def save(self,*args,**kwargs):
#         super(StockSimpleProduct,self).save(*args,**kwargs)
#         productMultiple=ProductMultiple.objects.filter(company=self.company,product=self.product)
#         stockMultiple=StockMultipleProduct.objects.filter(company=self.company,product__in=productMultiple)
#         for obj in stockMultiple:
#             obj.qty=int(self.qty/obj.product.qty)
#             obj.save()
#         for productBulk in ProductBulk.objects.filter(company=self.company,bulk_products_qty__product=self.product):
#             qtys=[]
#             for product_qty_obj in productBulk.bulk_products_qty.all():
#                 qty_now=StockSimpleProduct.objects.get(company=self.company,product=product_qty_obj.product).qty
#                 qtys.append(int(qty_now/product_qty_obj.qty))
#             stockBulk=StockBulkProduct.objects.get(company=self.company,product=productBulk)
#             stockBulk.qty=min(qtys)
#             stockBulk.save()
        
        
#     class Meta:
#         unique_together=('company','product')

# class StockBulkProduct(models.Model):
#     company=models.ForeignKey(Company,on_delete=models.CASCADE)
#     product=models.ManyToManyField(ProductBulk)
#     qty=models.IntegerField(default=0)

#     class Meta:
#         unique_together=('company','product')

# class StockMultipleProduct(models.Model):
#     company=models.ForeignKey(Company,on_delete=models.CASCADE)
#     product=models.ManyToManyField(ProductMultiple,on_delete=models.CASCADE)
#     qty=models.IntegerField(default=0)

#     class Meta:
#         unique_together=('company','product')

