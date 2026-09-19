from django.db import models
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from backend import globals
from django.utils import timezone
import json

#Create your models here.
class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone=models.CharField(max_length=20,blank=True,null=True)
    
    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"

    def __str__(self):
        return self.user.username





# # Create your models here.
# class Request(models.Model):
#     sys_id = models.AutoField(primary_key=True, null=False, blank=True)
#     session_key = models.CharField(max_length=1024, null=True, blank=True)
#     path = models.CharField(max_length=1024, null=True, blank=True)
#     method = models.CharField(max_length=8, null=True, blank=True)
#     body = models.TextField(null=True, blank=True)
#     ip_address = models.GenericIPAddressField(null=True, blank=True)
#     referrer = models.CharField(max_length=512, null=True, blank=True)
#     timestamp = models.DateTimeField(null=True, blank=True)
#     host = models.CharField(max_length=512, null=True, blank=True)
#     ctype = models.CharField(max_length=512, null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
#     user_agent = models.CharField(max_length=100,null=True, blank=True)
    
