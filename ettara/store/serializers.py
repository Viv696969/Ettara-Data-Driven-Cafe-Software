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
    
