from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
#Checkout
    path('checkout/',views.checkout,name='checkout'),
]

