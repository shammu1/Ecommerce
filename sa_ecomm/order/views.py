from django.shortcuts import render
from cart.cart import Cart
from .forms import CheckoutForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.models import Product
from order.models import *
from django.http import JsonResponse,HttpResponse
import json
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.urls import reverse
from django.conf import settings
#from paypal.standard.forms import PayPalPaymentsForm

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request, 'order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})


def checkout(request):
    if request.method == "GET":
        print("get checkout")
        try:
            cart = Cart(request)
            total_cart_price = cart.get_total_cart_price()
            form = CheckoutForm()   
            context = {
                'form': form,
                'cart': cart,
                'total_cart_price': total_cart_price,
               # 'paypal_payment_button': paypal_payment_button,
            }
            print('check billing')
            try:
                billing_address_qs = Address.objects.filter(
                    user=request.user,
                    address_type='B',
                    default=True
                )
            except: 
                print('No Default Billing Address')
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})
            print("billing address")
            print(billing_address_qs[0])
            shipping_address_qs = Address.objects.filter(
                user=request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})
            print(shipping_address_qs[0])
        except:
            pass    
        return render(request, "order/checkout.html", context)
#        except ObjectDoesNotExist:
#            messages.warning(request,f'No items in the Cart.')
#            return redirect("cart:checkout")

    if request.method == "POST":
        cart = Cart(request)
        total_cart_price = cart.get_total_cart_price()
        form = CheckoutForm(request.POST)
        print("post")

     #   use_default_billing = request.POST.get('use_default_billing')
        if form.is_valid():                    
            billing_first_name = form.cleaned_data.get('billing_first_name')
            billing_last_name = form.cleaned_data.get('billing_last_name')
            billing_email = form.cleaned_data.get('billing_email')
            billing_mobile = form.cleaned_data.get('billing_mobile')
            billing_addr = form.cleaned_data.get('billing_address')
            billing_city = form.cleaned_data.get('billing_city')
            billing_state = form.cleaned_data.get('billing_state')
            billing_country = form.cleaned_data.get('billing_country')
            billing_zip = form.cleaned_data.get('billing_zip')
            set_default_billing = form.cleaned_data.get('set_default_billing')
            print("form is valid")    
            billing_address = Address.objects.create(
                                user=request.user,
                                first_name=billing_first_name,
                                last_name=billing_last_name,
                                email=billing_email,
                                mobile=billing_mobile,
                                address=billing_addr,
                                city=billing_city,
                                state=billing_state,
                                country=billing_country,
                                zip_code=billing_zip,
                                address_type='B',
                                default=set_default_billing,
                            )
                
            print("saving") 
            billing_address.save()
            print("saved")
            print("printing billing address")
            print(billing_address)
      
            
        
            shipping_first_name = form.cleaned_data.get('shipping_first_name')
            shipping_last_name = form.cleaned_data.get('shipping_last_name')
            shipping_email = form.cleaned_data.get('shipping_email')
            shipping_mobile = form.cleaned_data.get('shipping_mobile')
            shipping_addr = form.cleaned_data.get('shipping_address')
            shipping_city = form.cleaned_data.get('shipping_city')
            shipping_state = form.cleaned_data.get('shipping_state')
            shipping_country = form.cleaned_data.get('shipping_country')
            shipping_zip = form.cleaned_data.get('shipping_zip')
            set_default_shipping = form.cleaned_data.get('set_default_shipping')
            print("form is valid")
            shipping_address = Address.objects.create(
                            user=request.user,
                            first_name=shipping_first_name,
                            last_name=shipping_last_name,
                            email=shipping_email,
                            mobile=shipping_mobile,
                            address=shipping_addr,
                            city=shipping_city,
                            state=shipping_state,
                            country=shipping_country,
                            zip_code=shipping_zip,
                            address_type='S',
                            default=set_default_shipping,
                        )
            print("saving") 
            shipping_address.save()
            print("shipping saved")
        else:
            print("form not valid")    
        

        # Order Creation 
        order = Order.objects.create(
                                order_date=datetime.datetime.now(),
                                user=request.user,
                                billing_address=billing_address,
                                shipping_address=shipping_address,
                                price=total_cart_price,
                                status="inprocess",
                                paid_status=False
                            )

        # Order Items Creation
        for item in cart: 
            OrderItem.objects.create(
                                    quantity=item['quantity'],
                                    product=item['product'],
                                    order=order,
                                    )    
        print('Order created successfully')
        cart.clear()
        context = {
                    'form': form,
                    'cart': cart,
                   # 'paypal_payment_button': paypal_payment_button,
                }
        return render(request,"order/checkout.html",context)    

@csrf_exempt
def payment_completed_view(request):
    context = request.POST
    return render(request,'order/payment-completed.html',context)


@csrf_exempt
def payment_failed_view(request):
    return render(request,'order/payment-failed.html')