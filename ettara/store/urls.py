
from django.urls import path
from .views import *
urlpatterns = [
    path('show_categories',show_categories,name='show_categories'),
    path('show_products',show_products,name='show_products'),
    # path('test',test,name='test'),
    
]
