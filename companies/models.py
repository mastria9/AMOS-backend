from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random

class Company(models.Model):
    

    vid=models.CharField(max_length=10,blank=True)
    name=models.CharField(max_length=50)
    vat=models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=2)
    country = models.CharField(max_length=2,default="IT",choices=[("IT","Italia"),("ES","Spagna"),("DE","Germania"),("UK","United Kingdom"),("FR","Francia")])
    cap = models.CharField(max_length=5)
    address = models.CharField(max_length=50)
    pec=models.EmailField(blank=True,null=True)
    sdi=models.CharField(max_length=11,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=False)
    vendor=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.vid

    def save(self, *args, **kwargs):
        if not self.pk:
            self.vid=generate_vid()
        super(Company, self).save(*args, **kwargs)

    

class Authorization(models.Model):
    class Permissions(models.IntegerChoices):
        DENY=0
        READ=1
        MODIFY=2
        DELETE=3
        
    class Applications(models.Choices):
        PRODUCT="products"
        ORDER="orders"
        MARKETPLACE="marketplaces"
        COMPANY="companies"
        SHIPPING="shippings"
        COURIERS="couriers"
        MESSAGES="messages"
        AUTHORIZATIONS="authorizations"
        IMPORTS="imports"
        OFFERS="offers"
        ITEM="warehouse_item"
        WAREHOUSES="warehouses"

        
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    application=models.CharField(max_length=15,choices=Applications.choices)
    permission=models.IntegerField(choices=Permissions.choices,default=Permissions.DENY)

    class Meta:
        unique_together=('company','user','application')

    def __str__(self):
        return str(self.company)+" "+str(self.user)+str(self.application)+str(self.permission)


def generate_vid():
    vid_list=Company.objects.all().values_list('vid',flat=True)
    def random_string():
        letters = ''.join((random.choice(string.ascii_letters) for i in range(8))).upper()
        digits = ''.join((random.choice(string.digits) for i in range(2)))
        sample_list = list(letters + digits)
        random.shuffle(sample_list)
        generated = ''.join(sample_list)
        return generated
    generated=random_string()
    while(generated in vid_list):
        generated=random_string
    return generated
