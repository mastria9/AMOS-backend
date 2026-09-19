from django.db import models
from companies.models import Company
from marketplaces.models import Marketplace
# Create your models here.
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from backend import globals


class IVA(models.Model):
    code=models.CharField(max_length=10,unique=True)
    percentage=models.IntegerField(default=22)
    
    def __str__(self):
        return str(self.code)


class InventoryDimension(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    weight=models.DecimalField(max_digits=8,decimal_places=3)
    volume=models.DecimalField(max_digits=8,decimal_places=3)
    length=models.DecimalField(max_digits=8,decimal_places=3)
    height=models.DecimalField(max_digits=8,decimal_places=3)
    width=models.DecimalField(max_digits=8,decimal_places=3)

    class Meta:
        unique_together = ('sku','company')

    def __str__(self):
        return str(self.company)+"_"+str(self.sku)


class InventoryOffer(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    buy_price=models.DecimalField(max_digits=8,decimal_places=2)
    buy_iva=models.ForeignKey(IVA,on_delete=models.SET_NULL,null=True,related_name="buy_iva")
    price=models.DecimalField(max_digits=8,decimal_places=2)
    is_min_max=models.BooleanField(default=False)
    min_price=models.DecimalField(max_digits=8,decimal_places=2,blank=True)
    max_price=models.DecimalField(max_digits=8,decimal_places=2,blank=True)
    offer_price=models.DecimalField(max_digits=8,decimal_places=2,blank=True)
    start_offer=models.DateField(blank=True)
    end_offer=models.DateField(blank=True)
    iva=models.ForeignKey(IVA,on_delete=models.SET_NULL,null=True,related_name="offer_iva")
    is_active=models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('sku','company','marketplace')

class Inventory(models.Model):
    sku=models.CharField(max_length=globals.SKU_LENGTH)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    offer=models.ManyToManyField(InventoryOffer,blank=True)
    dimension=models.ForeignKey(InventoryDimension,null=True,on_delete=models.SET_NULL)

    class Meta:
        unique_together = ('sku','company')
    
    def __str__(self):
        return str(self.company)+"_"+str(self.sku)



