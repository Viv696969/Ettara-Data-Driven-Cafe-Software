from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import *
from .serializers import *
import json
from .apps import StoreConfig
import numpy as np
from django.db.models import Sum
collection=StoreConfig.collection
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
@csrf_exempt
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
            activity_list=json.loads(
                json.dumps(request.data)
                )['activity']
            
            data=collection.get(
                ids=activity_list,
                include=['embeddings']
            )['embeddings']

            target_embedding=np.array(data).mean(0).tolist()

            ids=list(map(int,collection.query(
                query_embeddings=[target_embedding],
                include=['distances'],
                n_results=5
            )['ids'][0]))[::-1]
            print(ids)
            prods=Product.objects.filter(id__in=ids)
            recommended_products=sorted(
                prods,
                key=lambda x : ids.index(x.id)
            )
            data=RecommendedProductSerializer(recommended_products,many=True).data

            return JsonResponse({'data':data},status=200)
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

@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def checkout(request):
    carts=Cart.objects.filter(user=request.user)
    aggregated_data=carts.aggregate(
        total_price=Sum('total_price'),
        total_quantity=Sum('quantity')

    )
    data=CheckoutSerializer(carts,many=True).data
    return JsonResponse({
        'data':data,
        'total_price':aggregated_data['total_price'] or 0,
        'total_quantity':aggregated_data['total_quantity'] or 0
    },status=200)


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def place_order(request):
    shipping_address=request.POST['shipping_address']
    city=request.POST['city']
    state=request.POST['state']
    pincode=request.POST['pincode']
    phone_number=request.POST['phone_number']
    email=request.POST['email']
    payment_mode=request.POST['payment_mode']
    total_price=0
    carts=Cart.objects.filter(user=request.user)
    order=Order.objects.create(
        shipping_address=shipping_address,city=city,state=state,pincode=pincode,phone_number=phone_number,email=email,payment_mode=payment_mode,user=request.user
    )
    
    for cart in carts:
        total_price+=cart.total_price
        ordered_item=OrderedItem.objects.create(
            order=order,product=cart.product,total_price=cart.total_price,quantity=cart.quantity
            )
        ordered_item.save()
        cart.delete()

    order.total_price=total_price
    order.save()
    return JsonResponse({
        'mssg':'Order Placed successffully!!',
        'order_id':order.id
    },status=201)

