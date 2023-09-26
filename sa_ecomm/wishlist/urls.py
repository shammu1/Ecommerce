from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('/wishlist-add/<int:id>/',views.wishlist_add_view,name='wishlist-add'),
    path('/cart-add/<int:id>/',views.wishlist_add_to_cart_view,name='add-to-cart'),
    ]