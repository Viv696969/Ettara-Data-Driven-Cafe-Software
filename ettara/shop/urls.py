from django.urls import path
from .views import *

urlpatterns=[
    path('load_data',load_data,name='load_data'),

]