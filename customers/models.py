from django.db import models
from backend import globals
from companies.models import Company
from marketplaces.models import Marketplace
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Customer(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE,null=True)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE,null=True)
    customer_name=models.CharField(max_length=80,verbose_name="Nome cliente")
    customer_address=models.CharField(max_length=100,verbose_name="Indirizzo cliente",null=True)
    customer_city=models.CharField(max_length=50,verbose_name="Città cliente",null=True)
    customer_state=models.CharField(max_length=50,verbose_name="Provincia cliente",null=True)
    customer_cap=models.CharField(max_length=5,blank=True,verbose_name="CAP cliente",null=True)
    customer_phone=PhoneNumberField(blank=True,verbose_name="Telefono cliente",null=True)
    customer_country=models.CharField(max_length=2,choices=globals.COUNTRY_CHOICES,verbose_name="Nazione cliente",null=True)
    customer_email=models.EmailField(blank=True,null=True,verbose_name="Email cliente")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

    def __str__(self):
        return str(self.customer_name)