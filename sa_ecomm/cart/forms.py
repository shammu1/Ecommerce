from django import forms
from django_countries import widgets, countries
from django_countries.widgets import CountrySelectWidget
from localflavor.us.models import USStateField
from phonenumber_field.modelfields import PhoneNumberField
from order.models import * 
from localflavor.us.forms import USStateSelect

class CheckoutForm(forms.Form):
    billing_first_name = forms.CharField(max_length=50)
    billing_last_name = forms.CharField(max_length=50)
    billing_email = forms.EmailField()
    billing_mobile = forms.CharField(max_length=50,required=False)
    billing_address = forms.CharField()
    billing_city = forms.CharField(max_length=50)  
    billing_state = forms.CharField(max_length=50) 
   # billing_country = CountryField(blank_label='(select country)').formfield(
   #     required=False,
   #     widget=CountrySelectWidget(attrs={
   #         'class': 'form-control',
   #     }))
    billing_country = forms.ChoiceField(widget=CountrySelectWidget, choices=countries)      
    billing_zip = forms.CharField()
    #set_default_billing = forms.BooleanField(required=False)

   # class Meta:
   #     model = Address
   #     fields = '__all__'
                 
    
    
    #same_shipping_address = forms.BooleanField(required=False)
    #set_default_shipping = forms.BooleanField(required=False)
    #use_default_shipping = forms.BooleanField(required=False)
    #set_default_billing = forms.BooleanField(required=False)
    #use_default_billing = forms.BooleanField(required=False)

    #payment_option = forms.ChoiceField(  
    #    widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


   # shipping_first_name = forms.CharField(max_length=50)
   # shipping_last_name = forms.CharField(max_length=50)
   # shipping_email = forms.EmailField()
   # shipping_mobile = forms.CharField(max_length=50,required=False)
   # shipping_address = forms.CharField()
   # shipping_city = forms.CharField(max_length=50)  
   # shipping_state = forms.CharField(max_length=50) 
   # billing_country = CountryField(blank_label='(select country)').formfield(
   #     required=False,
   #     widget=CountrySelectWidget(attrs={
   #         'class': 'form-control',
   #     }))
   # shipping_country = forms.ChoiceField(widget=CountrySelectWidget, choices=countries)      
   # shipping_zip = forms.CharField()
   # set_default_shipping = forms.BooleanField(required=False)
