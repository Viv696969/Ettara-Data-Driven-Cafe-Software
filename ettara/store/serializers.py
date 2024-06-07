from rest_framework import serializers
from .models import *
from rest_framework.serializers import SerializerMethodField

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = "__all__"
