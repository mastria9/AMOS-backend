from django.db import models
from companies.models import Company
import string
import random
import os
from django.conf import settings
# Create your models here.

class WareHouse(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    code=models.CharField(max_length=20,blank=True)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    province=models.CharField(max_length=2)
    country=models.CharField(max_length=2)

    class Meta:
        unique_together=('company','code')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code=self.company.vid+generate_code()
        super(WareHouse, self).save(*args, **kwargs)


class ItemInfoFiles(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    item_code=models.CharField(max_length=50)
    name=models.CharField(max_length=200)
    path=models.CharField(max_length=300,null=True)

    class Meta:
        unique_together=('company','item_code','name','path')

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.PRIVATE_DIR,self.path))
        super(ItemInfoFiles, self).delete(*args, **kwargs)
    


class ItemQty(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    warehouse=models.ForeignKey(WareHouse,on_delete=models.CASCADE)
    item_code=models.CharField(max_length=50)
    qty=models.IntegerField(default=0)
    class Meta:
        unique_together=('company','warehouse','item_code')

class Item(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    item_code=models.CharField(max_length=50)
    name=models.CharField(max_length=200)
    inStockQty=models.IntegerField(default=0)
    weight=models.IntegerField(default=0,blank=True,null=True)
    length=models.IntegerField(default=0,blank=True,null=True)
    height=models.IntegerField(default=0,blank=True,null=True)
    width=models.IntegerField(default=0,blank=True,null=True)
    text=models.TextField(default=None,null=True,blank=True)
    files=models.ManyToManyField(ItemInfoFiles,blank=True)
    item_qty=models.ManyToManyField(ItemQty)

    class Meta:
        unique_together=('company','item_code')



    def delete(self, *args, **kwargs):
        for file in self.files.all():
            file.delete()
        for itemqty in self.item_qty.all():
            itemqty.delete()
        super(Item, self).delete(*args, **kwargs)



    


def generate_code():
    code_list=WareHouse.objects.all().values_list('code',flat=True)
    def random_string():
        letters = random.choice(string.ascii_letters).upper()
        digits = random.choice(string.digits)
        sample_list = list(letters + digits)
        random.shuffle(sample_list)
        generated = ''.join(sample_list)
        return generated
    generated=random_string()
    while(generated in code_list):
        generated=random_string
    return generated
    




