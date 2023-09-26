from django.contrib import admin
from .models import Category,SubCategory,Product,ProductImages, ProductReview


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title','product_image','price','featured','status']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','image']


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','image']


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(ProductReview)