from django.db import models
from marketplaces.models import Marketplace
from companies.models import Company
from django.utils import timezone
# Create your models here.

class InboxMessage(models.Model):
    date=models.DateTimeField(default=timezone.now)
    text=models.TextField()
    address=models.EmailField()

    def __str__(self):
        return str(self.date)+"_"+str(self.address)

class OutboxMessage(models.Model):
    date=models.DateTimeField(default=timezone.now)
    text=models.TextField()
    address=models.EmailField()

    def __str__(self):
        return str(self.date)+"_"+str(self.address)


class Message(models.Model):
    message_id=models.CharField(max_length=50)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    marketplace=models.ForeignKey(Marketplace,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    typo=models.CharField(max_length=6,choices=[("O","Orders"),("I","Info"),("W","Attenzione")])
    inbox=models.ManyToManyField(InboxMessage)
    outbox=models.ManyToManyField(OutboxMessage)

    def __str__(self):
        return str(self.message_id)