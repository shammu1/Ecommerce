from django.shortcuts import render
from wishlist.models import *
from cart.cart import Cart

def about_us_view(request):
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    cart = Cart(request)
    cart_count = cart.get_cart_count()
    context = {'wishlist_count' : wishlist_count,
                'cart_count' : cart_count,
            }
    return render(request,"about/about_us.html")    


def payment_policy_view(request):
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    cart = Cart(request)
    cart_count = cart.get_cart_count()
    context = {'wishlist_count' : wishlist_count,
                'cart_count' : cart_count,
            }
    return render(request,"about/payment_policy.html") 


def return_policy_view(request):
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    cart = Cart(request)
    cart_count = cart.get_cart_count()
    context = {'wishlist_count' : wishlist_count,
                'cart_count' : cart_count,
            }
    return render(request,"about/return_policy.html")     


def shipping_policy_view(request):
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    cart = Cart(request)
    cart_count = cart.get_cart_count()
    context = {'wishlist_count' : wishlist_count,
                'cart_count' : cart_count,
            }    
    return render(request,"about/shipping_policy.html") 

def terms_and_conditions_view(request):
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    cart = Cart(request)
    cart_count = cart.get_cart_count()
    context = {'wishlist_count' : wishlist_count,
                'cart_count' : cart_count,
            }    
    return render(request,"about/terms_and_conditions.html")     