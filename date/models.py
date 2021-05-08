from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Contact(models.Model):
    email = models.CharField(max_length=75)
    message = models.CharField(max_length=500)

class History(models.Model):
    id = models.ForeignKey(User,primary_key=True,on_delete=models.CASCADE)
    mobno = models.IntegerField(blank=True,null=True)
    instaid = models.CharField(max_length=75)
    one = models.CharField(max_length=100)
    two = models.CharField(max_length=100)
    three = models.CharField(max_length=100)
    four = models.CharField(max_length=100)
    five = models.CharField(max_length=100)