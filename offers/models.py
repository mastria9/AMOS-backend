from django.db import models
from marketplaces.models import Marketplace
from companies.models import Company
from products.models import ProductSimple,ProductMultiple,ProductBulk
from django.core.exceptions import ValidationError

# Create your models here.
class Iva(models.Model):
    code=models.CharField(max_length=10)
    percentage=models.IntegerField(default=22)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('code','company','marketplace')
    def __str__(self):
        return str(self.code)


class ProductSimpleOffer(models.Model):
    product=models.ForeignKey(ProductSimple,on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    is_min_max=models.BooleanField(default=False)
    min_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    max_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    offer_is_active=models.BooleanField(default=False)
    offer_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    start_offer=models.DateField(blank=True,null=True,default=None)
    end_offer=models.DateField(blank=True,null=True,default=None)
    iva=models.ForeignKey(Iva,on_delete=models.SET_NULL,null=True)
    is_active=models.BooleanField(default=False)
    
    
    class Meta:
        unique_together = ('product','company','marketplace')


class ProductMultipleOffer(models.Model):
    product=models.ForeignKey(ProductMultiple,on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    is_min_max=models.BooleanField(default=False)
    min_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    max_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    offer_is_active=models.BooleanField(default=False)
    offer_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    start_offer=models.DateField(blank=True,null=True,default=None)
    end_offer=models.DateField(blank=True,null=True,default=None)
    iva=models.ForeignKey(Iva,on_delete=models.SET_NULL,null=True)
    is_active=models.BooleanField(default=False)
    
    
    class Meta:
        unique_together = ('product','company','marketplace')


class ProductBulkOffer(models.Model):
    product=models.ForeignKey(ProductBulk,on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    is_min_max=models.BooleanField(default=False)
    min_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    max_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    offer_is_active=models.BooleanField(default=False)
    offer_price=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    start_offer=models.DateField(blank=True,null=True,default=None)
    end_offer=models.DateField(blank=True,null=True,default=None)
    iva=models.ForeignKey(Iva,on_delete=models.SET_NULL,null=True)
    is_active=models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('product','company','marketplace')
