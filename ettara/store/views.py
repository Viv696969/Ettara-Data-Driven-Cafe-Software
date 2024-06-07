from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .models import *
from django.shortcuts import get_object_or_404
from .serializers import *
import json
# Create your views here.

@api_view(['POST'])
@csrf_exempt
def show_categories(request):
    cats=Category.objects.all()
    for cat in cats:
        print(cat.name)

    serializer=CategorySerializer(cats,many=True)
    return JsonResponse({
        'categories':serializer.data
    },status=200)


@api_view(['POST'])
def show_products(request):
    user=request.user
    if user.is_authenticated:
        '''
        do something like recommendation...
        '''
        if 'activity' in request.data:
            '''
            give recommendation based on activity...
            '''
            activity_list=json.loads(json.dumps(request.data))['activity']
            return JsonResponse({'data':'test'},status=200)
        else:
            products=Product.objects.all()
            data=AllProductSerializer(products,many=True).data

            return JsonResponse({
                'data':data
            },
            status=200
            ) 
    else:
        '''
        Just show the Products..
        '''
        products=Product.objects.all()
        data=AllProductSerializer(products,many=True).data

    return JsonResponse({
        'data':data
    },
    status=200
    )

