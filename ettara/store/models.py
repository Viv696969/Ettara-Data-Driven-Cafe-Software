from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=250,blank=False,null=False,unique=True)
    description=models.TextField(null=False,blank=False)

    class Meta:
        db_table = 'Categories'

    def __str__(self) -> str:
        return self.name
    
    
class Product(models.Model):
    name=models.CharField(max_length=1000,blank=False,null=False)
    qty=models.IntegerField(blank=False,null=False)
    price=models.IntegerField(blank=False,null=False)
    description=models.TextField(blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product_image=models.ImageField(upload_to='product_images/',blank=False,null=False)
    related_products = models.ManyToManyField('self', symmetrical=False,blank=True)


    class Meta:
        db_table = 'Products'

    def __str__(self) -> str:
        return self.name
    
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rating=models.IntegerField(blank=False,null=False)
    review=models.CharField(max_length=1000,blank=False,null=False)

    class Meta:
        db_table = 'Reviews'

    def __str__(self) -> str:
        return self.review[:100]
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qauntity=models.IntegerField(blank=True,null=True)
    total_price=models.IntegerField(blank=True,null=True)

    class Meta:
        db_table = 'Cart'
        indexes = [
        models.Index(fields=['user',]),
        ]

    def __str__(self) -> str:
        return self.user.username+"  |  "+self.product.name
    
    
class Order(models.Model):
    shipping_address=models.TextField(null=True,blank=True)
    city=models.CharField(max_length=300,blank=True,null=True)
    state=models.CharField(max_length=300,blank=True,null=True)
    pincode=models.CharField(max_length=20,blank=True,null=True)
    phone_number=models.CharField(max_length=20,blank=True,null=True)
    email=models.CharField(max_length=200,blank=True,null=True)
    payment_mode=models.CharField(max_length=200,blank=True,null=True)
    total_price=models.FloatField(blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table="Orders"
        indexes=[models.Index(fields=['user',])]

    def __str__(self) -> str:
        return self.user.username+" "+self.id
    
class OrderedItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qauntity=models.IntegerField(blank=True,null=True)
    total_price=models.IntegerField(blank=True,null=True)

    class Meta:
        db_table = 'OrderedItems'
        indexes = [
        models.Index(fields=['order',]),
        ]

    def __str__(self) -> str:
        return self.user.username+"  |  "+self.product.name