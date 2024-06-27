from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Product(models.Model):
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
    name=models.CharField(max_length=200,null=False,blank=False)
    price=models.FloatField(null=False,blank=False)

    def __str__(self) -> str:
        return self.name
    
# class Cart(models.Model):
#     product=


# class MarketBasket(models.Model):
#     order=models.ForeignKey(Order,on_delete=models.CASCADE)
#     date=models.DateField(auto_now_add=True)
#     basket_string=models.TextField(blank=True,null=True)
