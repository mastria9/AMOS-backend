from django.db import models
from buckets.models import Bucket
from companies.models import Company
from marketplaces.models import Marketplace
from django.utils import timezone
from backend import globals 
# Create your models here.
class Import(models.Model):

    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    create=models.DateTimeField(default=timezone.now)
    template=models.CharField(max_length=3,choices=[("AMZ","Amazon")],default="AMZ")
    ftype=models.CharField(max_length=10,choices=[("products","Prodotti"),("orders","Ordini"),("prices","Prezzi"),("qty","Quantità")])
    status=models.CharField(max_length=2,choices=[("N","Nuovo"),("R","In elaborazione"),("E","Errore"),("D","Elaborato"),("DE","Elaborato con errori")],default="N")
    path=models.CharField(max_length=200,null=True)
    messages=models.TextField(blank=True,null=True)
    country=models.CharField(max_length=3,choices=globals.COUNTRY_CHOICES+[('ALL','Tutte')],default="ALL")
    