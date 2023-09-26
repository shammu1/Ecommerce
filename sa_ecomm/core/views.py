from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,SubCategory,Product,ProductImages,ProductReview
from django.contrib import messages
from django.db.models import Avg
from users.models import User
from .forms import ReviewForm
from taggit.models import Tag
import datetime


def index(request):
    products = Product.objects.filter(featured=True)
    categories = Category.objects.all()

    context = {
        'products' : products,
        'categories' : categories,
    }
    return render(request,"core/index.html",context)


from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
PRODUCTS_PER_PAGE = 4

def products_list_view(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()    
    
    # Sort Products
    sort_by = request.GET.get('sort_by')
    print(sort_by)
    if sort_by:
        products = Product.objects.filter(status=True).order_by(sort_by)
    else:
        products = Product.objects.filter(status=True)


    #Search Products
    search = request.GET.get('search',"")
    
    if search:
        products = Product.objects.filter(title__icontains=search).order_by("-date_created")
      

    # Filter Products

    colors = request.GET.getlist('color')
    filtered_products = Product.objects.none()
    for color in colors:
           filtered_products |= products.filter(tags__name__icontains = color) 

    if colors:
        products = filtered_products

    price_list = request.GET.getlist('price-filter')
    filtered_products = Product.objects.none()
    print(price_list)
    for price in price_list:
        if price == "100":
           filtered_products |= products.filter(price__range = [0,101]) 
        if price == "250":
           filtered_products |= products.filter(price__range = [101,251]) 
        if price == "500":
           filtered_products |= products.filter(price__range = [251,501])
 
    if price_list:
        products = filtered_products

    count = products.count()

    # Display No. of items as per color and price

    color = {}
    price = {}
    color['red'] = products.filter(tags__name__icontains = 'red').count()
    color['black'] = products.filter(tags__name__icontains = 'black').count()
    color['blue'] = products.filter(tags__name__icontains = 'blue').count()

    price['100'] = products.filter(price__range = [0,101]).count()
    price['250'] = products.filter(price__range = [101,251]).count()
    price['500'] = products.filter(price__range = [251,501]).count()

    #Pagination
    page = request.GET.get('page',1)
    products_paginator = Paginator(products,PRODUCTS_PER_PAGE)
    try:
        products = products_paginator.page(page)    
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)
    except: 
        products = products_paginator.page(PRODUCTS_PER_PAGE)        

    context = {
        'products' : products,
        'categories' : categories,
        'subcategories' : subcategories,
        'page_obj': products,
        'is_paginated': True,
        'paginator': products_paginator,
        'count' : count,
        'search' : search,
        'price_list' : price_list,
        'sort_by' : sort_by,
        'color': color,
        'price' : price,
    }

    return render(request,"core/products.html",context)



def products_list_view_category(request,cat_id):   
    category = Category.objects.get(id=cat_id)
    subcategories = SubCategory.objects.filter(category=category)

    # Sort Products
    sort_by = request.GET.get('sort_by')
    if sort_by:
        products = Product.objects.filter(category=category,status=True).order_by(sort_by)
    else:
        products = Product.objects.filter(category=category,status=True)


    #Search Products
    search = request.GET.get('search',"")
    
    if search:
        products = Product.objects.filter(title__icontains=search).order_by("-date_created")
      

    # Filter Products

    colors = request.GET.getlist('color')
    filtered_products = Product.objects.none()
    for color in colors:
           filtered_products |= products.filter(tags__name__icontains = color) 

    if colors:
        products = filtered_products

    price_list = request.GET.getlist('price-filter')
    filtered_products = Product.objects.none()
    print(price_list)
    for price in price_list:
        if price == "100":
           filtered_products |= products.filter(price__range = [0,101]) 
        if price == "250":
           filtered_products |= products.filter(price__range = [101,251]) 
        if price == "500":
           filtered_products |= products.filter(price__range = [251,501])
 
    if price_list:
        products = filtered_products

    count = products.count()

    # Display No. of items as per color and price

    color = {}
    price = {}
    color['red'] = products.filter(tags__name__icontains = 'red').count()
    color['black'] = products.filter(tags__name__icontains = 'black').count()
    color['blue'] = products.filter(tags__name__icontains = 'blue').count()

    price['100'] = products.filter(price__range = [0,101]).count()
    price['250'] = products.filter(price__range = [101,251]).count()
    price['500'] = products.filter(price__range = [251,501]).count()


    #Pagination
    page = request.GET.get('page',1)
    products_paginator = Paginator(products,PRODUCTS_PER_PAGE)
    try:
        products = products_paginator.page(page)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)
    except: 
        products = products_paginator.page(PRODUCTS_PER_PAGE)        

    context = {
        'products' : products,
        'category' : category,
        'subcategories' : subcategories,
        'page_obj': products,
        'is_paginated': True,
        'paginator': products_paginator,
        'count' : count,
        'color' : color,
        'price' : price,
    }
    return render(request,"core/products_category.html",context)


def products_list_view_subcategory(request,scat_id):  
    subcategory = SubCategory.objects.get(id=scat_id)

# Sort Products
    sort_by = request.GET.get('sort_by')
    if sort_by:
        products = Product.objects.filter(sub_category=subcategory,status=True).order_by(sort_by)
    else:
        products = Product.objects.filter(sub_category=subcategory,status=True)


    #Search Products
    search = request.GET.get('search',"")
    
    if search:
        products = Product.objects.filter(title__icontains=search).order_by("-date_created")
      

    # Filter Products

    colors = request.GET.getlist('color')
    filtered_products = Product.objects.none()
    for color in colors:
           filtered_products |= products.filter(tags__name__icontains = color) 

    if colors:
        products = filtered_products

    price_list = request.GET.getlist('price-filter')
    filtered_products = Product.objects.none()
    print(price_list)
    for price in price_list:
        if price == "100":
           filtered_products |= products.filter(price__range = [0,101]) 
        if price == "250":
           filtered_products |= products.filter(price__range = [101,251]) 
        if price == "500":
           filtered_products |= products.filter(price__range = [251,501])
 
    if price_list:
        products = filtered_products

    count = products.count()

    # Display No. of items as per color and price

    color = {}
    price = {}
    color['red'] = products.filter(tags__name__icontains = 'red').count()
    color['black'] = products.filter(tags__name__icontains = 'black').count()
    color['blue'] = products.filter(tags__name__icontains = 'blue').count()

    price['100'] = products.filter(price__range = [0,101]).count()
    price['250'] = products.filter(price__range = [101,251]).count()
    price['500'] = products.filter(price__range = [251,501]).count()

    #Pagination
    page = request.GET.get('page',1)
    products_paginator = Paginator(products,PRODUCTS_PER_PAGE)
    try:
        products = products_paginator.page(page)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)
    except: 
        products = products_paginator.page(PRODUCTS_PER_PAGE)        

    context = {
        'products' : products,
        'subcategory' : subcategory,
        'page_obj': products,
        'is_paginated': True,
        'paginator': products_paginator,
        'count' : count,
        'color' : color,
        'price' : price,
    }
    return render(request,"core/products_subcategory.html",context)




def product_detail_view(request,id):
    product = Product.objects.get(id=id)
    images = product.images.all()
    rel_products = Product.objects.filter(category=product.category)

    reviews = ProductReview.objects.filter(product=product)
    print(reviews)
    reviews_count = reviews.count()
    avg_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))['rating']

    context = {
        'product' : product,
        'images' : images,
        'reviews' : reviews,
        'avg_rating' : avg_rating,
        'reviews_count' : reviews_count,
        'rel_products': rel_products,
    }
    return render(request,"core/product_detail.html",context)



def tag_list(request,tag_slug=None):
    products = Product.objects.filter(status=True).order_by('-id')

    tag=None

    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        products = products.filter(tags__in=[tag])
        count = products.count()

    context = {
        "products" : products,
        "count" : count,
        "tag" : tag,
    }

    return render(request,'core/tags.html',context)

def submit_review(request,id):
        url = request.META.get('HTTP_REFERER')
        if request.method == "POST":
            try:
                reviews = ProductReview.objects.get(product__id=id,user__id=request.user.id)
                form = ReviewForm(request.POST,instance=reviews)
                form.save()
                messages.success(request,'Thankyou! Your review has been updated')
                return redirect(url)
            except ProductReview.DoesNotExist:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    product = Product.objects.get(id=id)
                    user = User.objects.get(id=request.user.id)
                    data = ProductReview()
                    data.rating = form.cleaned_data['rating']
                    data.review = form.cleaned_data['review']
                    data.product = product
                    data.user = user
                    data.save()
                    messages.success(request,'Thankyou! Your review has been updated')
                    return redirect(url)


def sort_products(request):
    color = request.GET.get('color')
    price
    products = Product.objects.filter(title__icontains=query).order_by("-date")

    context = {
        "products": products,
        "query": query, 
    }

    return render(request,"core/search.html",context)


