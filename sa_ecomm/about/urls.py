from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('',views.about_us_view,name="about-us"),
    path('payment-policy/',views.payment_policy_view,name="payment-policy"),
    path('return-policy/',views.return_policy_view,name="return-policy"),
    path('shipping-policy/',views.shipping_policy_view,name="shipping-policy"),
    path('terms-and-conditions/',views.terms_and_conditions_view,name="terms-and-conditions"),

]
