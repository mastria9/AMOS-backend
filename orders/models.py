from django.db import models
from companies.models import Company
from marketplaces.models import Marketplace
from django.utils import timezone
from backend import globals
from customers.models import Customer
from products.models import ProductBulk,ProductSimple,ProductMultiple
from phonenumber_field.modelfields import PhoneNumberField
from warehouses.views import update_InStockQty
# Create your models here.


class OrderDetail(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH,verbose_name="SKU prodotto")
    product_type=models.CharField(max_length=2,choices=[("S","Simple"),("B","Bulk"),("M","Multiple")])
    product_id=models.PositiveIntegerField(default=0)
    qty=models.PositiveIntegerField(verbose_name="Quantità acquistata")
    title=models.CharField(max_length=200,null=True,verbose_name='Titolo prodotto')
    company=models.ForeignKey(Company,on_delete=models.CASCADE,null=True)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE,null=True)
    price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Prezzo articolo")
    iva=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="IVA articolo")
    shipping_price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Prezzo spedizione",default=0)
    shipping_iva=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="IVA Spedizione",default=0)
    date=models.DateTimeField(default=timezone.now,verbose_name="Data d'ordine")
    max_shipping_date=models.DateTimeField(blank=True,null=True,verbose_name="Data di spedizione")
    max_consignment_date=models.DateTimeField(blank=True,null=True,verbose_name="Data di consegna")
    payments_date=models.DateTimeField(blank=True,null=True,verbose_name="Data di pagamento")
    business=models.BooleanField(default=False,verbose_name="B2B")
    order_id=models.CharField(max_length=50,verbose_name="ID Ordine del Marketplace",null=True)
    order_item_id=models.CharField(max_length=50,verbose_name="ID Ordine del Prodotto",null=True)
    status=models.CharField(max_length=2,choices=globals.ORDER_STATUS_CHOICES,default="PP",verbose_name="Stato d'ordine")
    shipping_name=models.CharField(max_length=50,verbose_name="Nome Destinatario")
    shipping_address=models.CharField(max_length=200,verbose_name="Indirizzo destinatario",blank=True,null=True)
    shipping_phone=PhoneNumberField(blank=True,verbose_name="Telefono destinatario")
    shipping_city=models.CharField(max_length=50,verbose_name="Città di destinazione")
    shipping_cap=models.CharField(max_length=5,blank=True,null=True,verbose_name="CAP di destinazione")
    shipping_country=models.CharField(max_length=20,verbose_name="Nazione di destinazione")
    shipping_state=models.CharField(max_length=20,verbose_name="Provincia di destinazione",null=True)
    shipping_instructions=models.CharField(max_length=200,blank=True,null=True)
    
    def save(self,*args,**kwargs):
        if len(self.title)>80:
            self.title=str(self.title)[:200]

        if self.id is None:
            qty=self.qty
        else:
            qty=self.qty-OrderDetail.objects.get(sku=self.sku,company=self.company,marketplace=self.marketplace,order_id=self.order_id,order_item_id=self.order_item_id).qty
        if ProductSimple.objects.filter(company=self.company,sku=self.sku,marketplace=self.marketplace).exists():
            product=ProductSimple.objects.get(company=self.company,sku=self.sku,marketplace=self.marketplace)
            self.product_id=product.id
            self.product_type="S"
            update_InStockQty(product.item,product.item.inStockQty-qty)
            
        elif ProductBulk.objects.filter(company=self.company,sku=self.sku,marketplace=self.marketplace).exists():
            product=ProductBulk.objects.get(company=self.company,sku=self.sku,marketplace=self.marketplace)
            self.product_id=product.id
            self.product_type="B"
            for product_qty in product.bulk_products_qty.all():
                newQty=product_qty.product.item.inStockQty-(qty*product_qty.qty)
                update_InStockQty(product.item,newQty)
                   
        elif ProductMultiple.objects.filter(company=self.company,sku=self.sku,marketplace=self.marketplace).exists():
            product=ProductMultiple.objects.get(company=self.company,sku=self.sku,marketplace=self.marketplace)
            self.product_id=product.id
            self.product_type="M"
            newQty=product.product.item.inStockQty-(qty*product.qty)
            update_InStockQty(product.item,newQty)
            
        super(OrderDetail,self).save(*args,*kwargs)



class Order(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    order_detail=models.ManyToManyField(OrderDetail)
    order_id=models.CharField(max_length=50,verbose_name="ID Ordine")
    order_price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale Ordine (IVA incl.)",null=True)
    order_iva=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale IVA",null=True)
    shipping_price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale Spedizione (IVA incl.)",null=True)
    shipping_iva=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale IVA Spedizione",null=True)
    order_total=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="Totale Ordine (IVA Incl)",null=True)
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Cliente")
    
    

    

