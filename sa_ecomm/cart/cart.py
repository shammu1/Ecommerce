from decimal import Decimal
from django.conf import settings
#from coupons.models import Coupon
from core.models import Product

class Cart():

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # store current applied coupon
        #self.coupon_id = self.session.get('coupon_id')

    def add(self, product,qty=1):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += qty
        self.cart[product_id]['total_price'] = self.cart[product_id]['price'] * self.cart[product_id]['quantity']
        #self.cart[cart_price] += self.cart[product_id]['total_price']
        print('saving')
        print(product)
        self.save()


    def update_qty(self, product,action,qty):
        """
        Reduce a product's quantity in the cart.
        """
        product_id = str(product.id)
        print(product_id)
        print(qty)
        if (qty <= 0):
            self.remove(product)
            print("Product removed")
        else:  
            print('updating cart')
            print(self.cart[product_id])
            self.cart[product_id]['quantity'] = qty
        #self.cart[cart_price] -= self.cart[product_id]['price']
        self.save()

    def save(self):
        """
        mark the session as "modified" to make sure it gets saved
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            #self.cart[cart_price] = self.get_total_cart_price() 
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_cart_count(self):
        """
        Count all items in the cart.
        """
        return len(self.cart)

    def get_total_cart_price(self):
        """
        calculate the total cost of the items in the cart
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        remove cart from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

#    @property
#    def coupon(self):
#        if self.coupon_id:
#            return Coupon.objects.get(id=self.coupon_id)
#        return None

#    def get_discount(self):
#        if self.coupon:
#            return (self.coupon.discount / Decimal('100')) \
#                * self.get_total_price()
#        return Decimal('0')

#    def get_total_price_after_discount(self):
#        return self.get_total_price() - self.get_discount()