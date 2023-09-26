from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path('register/',views.register_view,name="register"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),   
    path('myaccount/',views.myaccount_view,name='myaccount'), 
    path('make-default-address/<int:addr_id>',views.make_default_view,name='makedefault'),   
    path('order-details/<int:id>',views.order_details_view,name='order-details'), 
    path('edit-address/<int:id>',views.edit_address_view,name='edit-address'),
]