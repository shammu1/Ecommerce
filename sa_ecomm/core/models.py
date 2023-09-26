from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Avg
from decimal import Decimal


RATING = (
    (1,'★☆☆☆☆'),
    (2,'★★☆☆☆'),
    (3,'★★★☆☆'),
    (4,'★★★★☆'),
    (5,'★★★★★'),
)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefghijklmnop12345")
    name = models.CharField(max_length=100)
    description = RichTextUploadingField(max_length=500,null=True)
    image = models.ImageField(upload_to="category")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))

    def __str__(self):
        return self.name    


class SubCategory(models.Model):
    sc_id = ShortUUIDField(unique=True, length=10, max_length=20, prefix="scat", alphabet="abcdefgh12345")
    category = models.ForeignKey("Category", on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,null=True)
    description = RichTextUploadingField(max_length=500,null=True)
    image = models.ImageField(upload_to="sub-category")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sub-Categories"

    def sub_category_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))

    def __str__(self):
        return self.name

class Tags(models.Model):
    pass

class Product(models.Model):
    pid = ShortUUIDField(unique=True,length=10, max_length=20, alphabet="abcdefgh12345")

    category =  models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100,default="Unknown Product")
    image = models.ImageField(upload_to="products")
    description = RichTextUploadingField(null=True, blank=True, default="Product Description")

    price = models.DecimalField(max_digits=9999999999,decimal_places=2,default="1.99")
    old_price = models.DecimalField(max_digits=9999999999,decimal_places=2,default="1.99")

    specifications = models.TextField(null=True, blank=True)
    tags = TaggableManager(blank=True)

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    digital = models.BooleanField(default=True)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix="sku", alphabet='1234567890') 

    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)



    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = (self.price/self.old_price) * 100
        return new_price

    @property
    def avg_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating')).get('rating__avg')
        if avg_rating is not None:
            return Decimal(avg_rating).quantize(Decimal('0.00'))
        else:
            return None

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images")
    product = models.ForeignKey(Product, related_name= "images",on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"



class ProductReview(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,related_name="reviews", null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title 



