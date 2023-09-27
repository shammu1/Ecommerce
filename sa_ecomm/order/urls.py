from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
#Checkout
    path('checkout/',views.checkout,name='checkout'),
    path('payment-completed/',views.payment_completed_view,name='payment-completed'),
    path('payment-failed/',views.payment_failed_view,name='payment-failed'),
]

