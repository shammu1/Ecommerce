from django.db import models
from core.models import * 
from users.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
#from localflavor.us.models import USStateField

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

STATUS_CHOICES = (
    ("inprocess","Processing"),
    ("shipped","Shipped"),
    ("delivered","Delivered"),
)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    state = models.CharField(max_length=50)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'



class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    order = models.ForeignKey(
        to="Order",
        related_name='items',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.quantity} x {self.product.title}"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Order(models.Model):
    order_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    billing_address = models.ForeignKey(
        to=Address,
        on_delete=models.SET_NULL,
        related_name='billing_address',
        blank=True, null=True,
    )
    shipping_address = models.ForeignKey(
        to=Address,
        on_delete=models.SET_NULL,
        related_name='shipping_address',
        blank=True, null=True,
    )
    price = models.DecimalField(max_digits=9999999999,decimal_places=2,default="1.99")
    status = models.CharField(default="inprocess", max_length=30, choices=STATUS_CHOICES)
    paid_status = models.BooleanField(default=False,null=True)
    
    def __str__(self) -> str:
        return self.reference_number

    @property
    def order_number(self) -> str:
        return f"ORDER-{self.pk}"



