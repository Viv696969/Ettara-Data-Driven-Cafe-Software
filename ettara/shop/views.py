from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import *
from .serializers import *
from pandas import *
from django.db.models import Sum

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

@api_view(['POST'])
@csrf_exempt
# @permission_classes([IsAuthenticated])
def give_user(request):
    phone_number=request.POST['phone_number']
    print(phone_number)
    customer=CustomerInfo.objects.filter(phone_number=phone_number).first()
    if customer==None:
        return JsonResponse({
            'status':False,"mssg":"No Such user"
        },status=404)
    return JsonResponse({
            'status':True,
            'user_info':{
                    'name':customer.full_name,
                    'phone_number':customer.phone_number
                    }
    },
    status=200
    )

@api_view(['POST'])
@csrf_exempt
def add_user(request):
    phone_number=request.POST['phone_number']
    full_name=request.POST['full_name']
    customer,created=CustomerInfo.objects.get_or_create(phone_number=phone_number,full_name=full_name)
    if created:
        customer.save()
        return JsonResponse(
            {'status':True,'mssg':'User Created'},status=201
            )
    else:
        return JsonResponse({
            'status':False,'mssg':'user exists'
        },status=200)

@api_view(['POST'])
@csrf_exempt
def add_to_cart(request):
    phone_number=request.POST['phone_number']
    product_id=request.POST['product_id']
    quantity=int(request.POST['quantity'])
    product=Product.objects.get(id=product_id)
    cart=Cart.objects.create(product=product,customer=CustomerInfo.objects.get(phone_number=phone_number),
                        quantity=quantity,total_price=product.price*quantity)
    cart.save()
    return JsonResponse({
        'status':True,'mssg':f'{product.name} added to cart with quantity {quantity}'
    })

@api_view(['GET'])
def get_products(request):
    prods=Product.objects.all()
    data=ProductSerializer(prods,many=True).data
    return JsonResponse({
        'status':True,'products':data

    },status=200)

@api_view(['POST'])
@csrf_exempt
def place_order(request):
    phone=request.POST['phone_number']
    customer=CustomerInfo.objects.get(phone_number=phone)
    cart=Cart.objects.filter(customer=customer)
    aggregated_data=cart.aggregate(total_order_price=Sum('total_price'))

    order=Order.objects.create(
        payment_mode=request.POST['payment_mode'],
        customer=customer,
        total_price=aggregated_data['total_order_price'],
    )
    order.save()
    basket_string=''
    for product_item in cart:
        order_item=OrderItem.objects.create(
            order=order,product=product_item.product,quantity=product_item.quantity,total_price=product_item.total_price
            
        )
        basket_string+=f'{product_item.product.name},'
        order_item.save()
    print(basket_string)
    basket=MarketBasket.objects.create(
        order=order,
        basket_string=basket_string[0:len(basket_string)-1]
    )
    basket.save()
    cart.delete()
    return JsonResponse({
        'status':True,'mssg':f'Order created successfully !! order id is {order.id}'
    })

# # Step 1: Prepare your data
# texts = ["5,6,7,8", "1,2,3,4", "9,10,11,12"]  # Example list of texts; replace with your actual list

# # Step 2: Create a pandas DataFrame from the list
# df = pd.DataFrame(texts, columns=['text'])

# # Step 3: Split the 'text' column into separate columns
# df = df['text'].str.split(',', expand=True)