from django.db import models


# Create your models here.
class Bucket(models.Model):

    aws_access_key_id=models.CharField(max_length=100)
    aws_secret_access_key=models.CharField(max_length=100)
    bucket_name=models.CharField(max_length=20)






    