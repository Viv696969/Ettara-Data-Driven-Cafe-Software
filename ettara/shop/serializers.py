from rest_framework import serializers
from .models import *
from rest_framework.serializers import SerializerMethodField

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

