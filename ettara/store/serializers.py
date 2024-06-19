from rest_framework import serializers
from .models import *
from rest_framework.serializers import SerializerMethodField

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = "__all__"


class AllProductSerializer(serializers.ModelSerializer):

    category=SerializerMethodField()

    class Meta:
        model=Product
        fields=[
            'name',
            'qty',
            'price',
            'description',
            'product_image',
            'category'
            ]
    
    def get_category(self,product):
        return {'name':product.category.name,'id':product.category.id}
    
class RecommendedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=[
            'name',
            'id',
            'price',
            'product_image',
            ]
    
class CartSerializer(serializers.ModelSerializer):
    # user=serializers.SerializerMethodField()
    product_info=SerializerMethodField()
    class Meta:
        model=Cart
        fields=[
            'quantity',
            'total_price',
            'product_info',
        ]
        depth=1
    
    def get_product_info(self,cart):
        return {
            'name':cart.product.name,
            'id':cart.product.id,
            'price':cart.product.price,
            'product_image':cart.product.product_image.url   
        }
    
class CheckoutSerializer(serializers.ModelSerializer):
    product_info=SerializerMethodField()
    class Meta:
        model=Cart
        fields=[
            'quantity',
            'total_price',
            'product_info',
        ]
    
    def get_product_info(self,cart):
        return {
            'name':cart.product.name,
            'id':cart.product.id,
            'product_image':cart.product.product_image.url   
        }
    