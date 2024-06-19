
from django.urls import path
from .views import *
urlpatterns = [
    path('show_categories',show_categories,name='show_categories'),
    path('show_products',show_products,name='show_products'),
    path('add_to_cart',add_to_cart,name='add_to_cart'),
    path('remove_from_cart',remove_from_cart,name='remove_from_cart'),
    path('show_cart',show_cart,name='show_cart'),
    path('change_quantity',change_quantity,name='change_quantity'),
    
]
