from django.shortcuts import render


def about_us_view(request):
    return render(request,"about/about_us.html")    


def payment_policy_view(request):
    return render(request,"about/payment_policy.html") 


def return_policy_view(request):
    return render(request,"about/return_policy.html")     


def shipping_policy_view(request):
    return render(request,"about/shipping_policy.html") 

def terms_and_conditions_view(request):
    return render(request,"about/terms_and_conditions.html")     