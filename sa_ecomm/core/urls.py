from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.index,name="index"),
    path('products/',views.products_list_view,name="products-list"),
    path('products/category/<int:cat_id>',views.products_list_view_category,name="products-list-category"),
    path('products/subcategory/<int:scat_id>',views.products_list_view_subcategory,name="products-list-subcategory"),
    #path('products/category/<int:id>',views.products_list_view,name="products-list"),
    path('product/<int:id>/',views.product_detail_view,name="product-detail"),

    # Tags
    path('products/tag/<slug:tag_slug>/',views.tag_list,name="tags"),
    path('submit-review/<int:id>/',views.submit_review,name="submit-review"),
   # path('search/',views.search_view,name="search"),
]
