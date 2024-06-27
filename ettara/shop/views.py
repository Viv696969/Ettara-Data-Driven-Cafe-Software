from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import *
from .serializers import *
from pandas import *
# Create your views here.
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def load_data(request):
    df=read_csv("")
    for index,data in df.iterrows():
        product=Product.objects.create(
            name=data['items'],price=data['prices']
        )
        product.save()
    return JsonResponse(
        {'status':True},status=200
    )

