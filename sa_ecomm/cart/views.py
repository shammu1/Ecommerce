from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.models import Product
from order.models import *
from wishlist.models import *
from .cart import Cart
from .forms import CheckoutForm
from django.http import JsonResponse,HttpResponse
import json
from django.template.loader import render_to_string
#from coupons.forms import CouponApplyForm

#@require_POST
def cart_add(request, product_id):
    print('add cart')
    qty = int(request.GET.get('quantity',1)) 
    #if not qty:
    #    qty = 1
    cart = Cart(request)
    print(cart)
    print('no cart')
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product,qty=qty)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success':1})
    return redirect('cart:cart_detail')


#@require_POST
def update_cart(request):
    print('Reduce cart qty')
    product_id = str(request.GET['id'])
    action = request.GET['action']
    qty = int(request.GET['quantity'])
   #cart_price = request.GET['cart_price']
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    print(qty)
    cart.update_qty(product=product,action=action,qty=qty)
    total_cart_price = float(cart.get_total_cart_price())
    return JsonResponse({'total_cart_price':total_cart_price})
 

def delete_cart(request,product_id):
    print("entering delete_cart view")
    product_id = str(product_id)
    #product_id = str(request.GET['id'])
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    total_cart_price = cart.get_total_cart_price()
    #context = {'cart': cart, 'total_cart_price': total_cart_price}
    #return JsonResponse({"data":context})
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    cart_count = cart.get_cart_count()
    total_cart_price = cart.get_total_cart_price()
    context = {'cart': cart, 
                'total_cart_price': total_cart_price, 
                'wishlist_count' : wishlist_count,
                'cart_count' : cart_count,
    }
    return render(request, 'cart/cart.html', context)


