from django.db import models
from companies.models import Company
from backend import globals 
# Create your models here.



    
class Marketplace(models.Model):

    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    account=models.EmailField()
    country=models.CharField(max_length=2,choices=globals.COUNTRY_CHOICES)
    code=models.CharField(max_length=5,choices=globals.MARKETPLACE_CHOICES)
    website=models.URLField(blank=True,null=True,default=None)
    endpoint=models.URLField(blank=True,null=True,verbose_name="API URL",default=None)
    endpoint_user=models.CharField(max_length=50,null=True,blank=True,verbose_name="API USER/TOKEN",default=None)
    endpoint_password=models.CharField(max_length=400,blank=True,null=True,verbose_name="API_SECRET_KEY",default=None)
    status=models.BooleanField(default=False)
    
    
    class Meta:
        unique_together = ('company','account','country','code')
        verbose_name = "Marketplace"
        verbose_name_plural = "Marketplaces"

    def __str__(self):
        return ("%s_%s_%s_%s" % (self.company,self.account,self.code,self.country))

    

