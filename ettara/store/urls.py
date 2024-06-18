
from django.urls import path
from .views import *
urlpatterns = [
    path('show_categories',show_categories,name='show_categories'),
    path('show_products',show_products,name='show_products'),
    path('add_to_cart',add_to_cart,name='add_to_cart'),
    
]
