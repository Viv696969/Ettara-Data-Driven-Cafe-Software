from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class Product(models.Model):
    id = models.UUIDField( primary_key = True, default = uuid.uuid4, editable = False)
    name=models.CharField(max_length=200,null=False,blank=False)
    price=models.FloatField(null=False,blank=False)

    def __str__(self) -> str:
        return self.name

class CustomerInfo(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    phone_number=models.CharField(max_length=20,blank=False,null=False,unique=True)
    full_name=models.CharField(max_length=300,blank=False,null=False)

    def __str__(self) -> str:
        return self.full_name

class Cart(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    customer=models.ForeignKey(CustomerInfo,on_delete=models.DO_NOTHING)
    quantity=models.IntegerField(null=False,blank=False)
    total_price=models.FloatField(null=False,blank=False)
    date=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.customer.full_name

class Order(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    total_price=models.FloatField(null=False,blank=False)
    payment_mode=models.CharField(max_length=100,default='cash')
    customer=models.ForeignKey(CustomerInfo,on_delete=models.DO_NOTHING)
    date=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.customer.full_name
    
class OrderItem(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    order=models.ForeignKey(Order,on_delete=models.DO_NOTHING)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    quantity=models.IntegerField(null=False,blank=False)
    total_price=models.FloatField(null=False,blank=False)

    def __str__(self) -> str:
        return self.product.name
    
class MarketBasket(models.Model):
    order=models.ForeignKey(Order,on_delete=models.DO_NOTHING)
    date=models.DateField(auto_now_add=True)
    basket_string=models.TextField(blank=True,null=True)

    def __str__(self) -> str:
        return self.basket_string
