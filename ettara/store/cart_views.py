from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import *
from .serializers import *



@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user=request.user
    id=int(request.POST['product_id'])
    quantity=int(request.POST['quantity'])
    cart,created=Cart.objects.get_or_create(user=user,product=Product.objects.get(id=id))
    if created:
        cart.quantity=quantity
        cart.total_price=quantity*cart.product.price
        cart.save()
        return JsonResponse({
            'mssg':f'Product {cart.product.name} added to cart..with quantity={quantity}','status':1
        },status=200)
    else:
        return JsonResponse(
            {'mssg':'Product Already In Cart...','status':0},status=200
        )

@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    try:
        product_id=int(request.POST['product_id'])
        product=Product.objects.get(id=product_id)
        mssg=f"{product.name} Removed from Cart"
        cart=Cart.objects.filter(user=request.user,product=product).first()
        cart.delete()
        return JsonResponse({
            'mssg':mssg,
        },status=200)
    except:
        return JsonResponse({'mssg':f'error finding product in cart..'},status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    cart_size=len(cart)
    if cart_size>0:
        data=CartSerializer(cart,many=True).data
        return JsonResponse({
            'quantity':cart_size,
            'data':data,
            'status':True
        },status=200)

    else:
        return JsonResponse({
            'status':False,
            'mssg':'No items in Cart..'
        })

@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def change_quantity(request):
    type_of_change=request.POST['type']
    quantity=int(request.POST['quantity'])
    id=int(request.POST['product_id'])
    cart=Cart.objects.filter(user=request.user,product__id=id).first()
    if type_of_change=='reduce':
        cart.quantity=cart.quantity-quantity
    else:
        if cart.product.qty<cart.quantity+quantity:
            return JsonResponse({
                'mssg':f'Only {cart.product.qty} {cart.product.name} left in stock..',
                'status':False
            })
        cart.quantity=cart.quantity+quantity
    cart.total_price=cart.quantity*cart.product.price
    cart.save()
    return JsonResponse(
        {
        'mssg':f'Quantity changed for {cart.product.name}',
        'status':True
        }
        )
