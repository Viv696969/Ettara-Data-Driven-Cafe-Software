from django.urls import path
from .views import *

urlpatterns=[
    path('load_data',load_data,name='load_data'),
    path('get_products',get_products,name='get_products'),
    path('add_user',add_user,name='add_user'),
    path('give_user',give_user,name='give_user'),
    path('add_to_cart',add_to_cart,name='add_to_cart'),
    path('market_basket_analysis',market_basket_analysis,name='market_basket_analysis'),
    path('place_order',place_order,name='place_order'),

]