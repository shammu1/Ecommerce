from django.shortcuts import render,redirect
from .forms import UserRegisterForm, PasswordChangingForm, AccountUpdateForm,EditAddressForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from order.models import Order,OrderItem,Address
from django.http import JsonResponse

User = settings.AUTH_USER_MODEL

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f'Hey {username}, Your account was created successfully.')
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            login(request,new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()
        print("User cannot be registered")

    
    context = {
        'form' : form,
    }
    return render(request,'users/register.html',context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            print(password)
            print('test')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request,user)
                messages.success(request,f'You are logged in.')
                return redirect("core:index")

            else:
                messages.warning(request,f'User does not exist. Please create an account')

        else:
            messages.warning(request,f'User does not exist. Please create an account')

    form = AuthenticationForm()    

    context = {
       'form' : form
    }

    return render(request,'users/login.html',context)    



def logout_view(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect("users:login")


def myaccount_view(request):   
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    billing_addresses = Address.objects.filter(user=request.user,address_type='B').order_by('-default')
    shipping_addresses = Address.objects.filter(user=request.user,address_type='S').order_by('-default')
    
    if request.method == "GET":    
        account_form = AccountUpdateForm(instance=request.user)
        password_form = PasswordChangingForm(user=request.user)
    elif request.method =='POST':
        account_form = AccountUpdateForm(instance=request.user,data=request.POST)
        password_form = PasswordChangingForm(user=request.user,data=request.POST)
        if account_form.is_valid():
            account_form.save()
            messages.success(request,"Account Updated Successfully.")
            return redirect("users:myaccount")
        elif not password_form.is_valid():
            messages.error(request,"Unable to update your account. Please enter valid email or phone number.")

        if password_form.is_valid():
            password_form.save()
            messages.success(request,"Password Changed Successfully.Please Login again.")
            return redirect("users:login")
        elif not account_form.is_valid():
            messages.error(request,"Please correct the error below.")
   
    
    context = {"orders": orders,
               "billing_addresses": billing_addresses,
               "shipping_addresses": shipping_addresses,
               "account_form": account_form, 
               "password_form": password_form,
            }
    return render(request,'users/my_account.html',context)


def make_default_view(request,addr_id):
    print("entering view")
    #addr_id = request.GET['addr_id']
    print("step1")
   # address_type = request.GET['address_type']
    print("step2")
    address = Address.objects.get(user=request.user,id=addr_id)
    print("step3")
    previous_default_address = Address.objects.get(user=request.user,address_type=address.address_type,default=True)
    print("step4")
    previous_default_address.default= False
    print("step5")
    address.default = True
    print("step6") 
    previous_default_address.save()
    print("step7")
    address.save()
    print("step8")
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    billing_addresses = Address.objects.filter(user=request.user,address_type='B').order_by('-default')
    shipping_addresses = Address.objects.filter(user=request.user,address_type='S').order_by('-default')
    
    messages.success(request,'Your Selected Address has been made default.')
    return redirect('users:myaccount')
   # return JsonResponse({'success':success_message})

def order_details_view(request,id):
    order = Order.objects.get(id=id)
    order_details = OrderItem.objects.filter(order=order)

    context = {
        'order' : order,
        'order_details' : order_details,
    }
    return render(request,'users/order_details.html',context)


def edit_address_view(request,id):
    
    if request.method == "POST":
        addr = Address.objects.get(id=id)
        address_type = 'Billing' if addr.address_type == 'B' else 'Shipping'
        form = EditAddressForm(request.POST) 

        if form.is_valid():                    
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            set_default = form.cleaned_data.get('set_default')
            print("form is valid")    
            print(addr)
            addr.first_name = first_name
            addr.last_name = last_name
            addr.email = email
            addr.mobile = mobile
            addr.address = address
            addr.city = city
            addr.state = state
            addr.country = country
            addr.zip_code = zip
            addr.save() 
            messages.success(request,'Address Saved') 
            print(set_default)      
            if set_default == True and addr.default == False:
                print("entered default")
                return make_default_view(request,addr.id)
    else:
        addr = Address.objects.get(id=id)
        address_type = 'Billing' if addr.address_type == 'B' else 'Shipping'
        form = EditAddressForm()

    context = {
        'address' : addr,
        'address_type' : address_type,
        'form' : form,
    }
    return render(request,'users/edit_address.html',context)    