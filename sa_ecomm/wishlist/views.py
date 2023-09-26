from django.shortcuts import render, redirect
from .models import Wishlist
from core.models import Product
from django.contrib import messages
from cart.views import cart_add
import datetime


# Create your views here.
def wishlist_view(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})



def wishlist_add_view(request,id):
    product = Product.objects.get(id=id)
    if Wishlist.objects.filter(product=product).exists():
        messages.success(request,f'Selected product already in wishlist.')
    else:    
        wishlist_item = Wishlist.objects.create(
                                user=request.user,
                                product=product,
                                date_created = datetime.datetime.now()
                               )

        wishlist_item.save()
    return redirect("wishlist:wishlist")

def wishlist_add_to_cart_view(request,id):
    product = Product.objects.get(id=id)
    wishlist_item = Wishlist.objects.get(product=product)
    wishlist_item.delete()
   # cart_add(request,id)
    return redirect("cart:cart_add",product_id=id)