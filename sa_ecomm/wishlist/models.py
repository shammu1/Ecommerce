from django.db import models
from core.models import Product
from users.models import User

class Wishlist(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, related_name="wishlist",on_delete=models.CASCADE,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name_plural = "Wishlist"

    def __str__(self):
        return self.product.title