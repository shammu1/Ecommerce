from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm, PasswordChangeForm
from users.models import User
from order.models import * 
from django_countries import widgets, countries
from django_countries.widgets import CountrySelectWidget



class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=150)  
    email = forms.EmailField(label='Email')  
    mobile = forms.CharField(label='Phone Number')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)  
    
    class Meta:
        model = User
        fields = ['username','email','mobile','password1','password2']


class AccountUpdateForm(UserChangeForm):
    username = forms.CharField(min_length=5, max_length=150,widget=forms.TextInput(attrs={'class':'form-control','label':'Username'}))  
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','label':'Email'}))  
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','label':'Phone Number'}))
    
    class Meta:
        model = User
        fields = ['username','email','mobile']


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','placeholder':'Current Password'}))  
    new_password1 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','placeholder':'New Password'}))  
    new_password2 = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','placeholder':'Confirm Password'}))  
    
    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']



class EditAddressForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=50,required=False)
    address = forms.CharField(required=False)
    city = forms.CharField(max_length=50)  
    state = forms.CharField(max_length=50) 
    country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={ 
            'class': 'form-control'
        }))
    zip = forms.CharField(required=False)
    set_default = forms.BooleanField(initial=False,required=False)
    