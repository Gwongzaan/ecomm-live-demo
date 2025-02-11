from django.db import models

class ACCOUNT_TYPE(models.IntegerChoices):
    PERSONAL = 0, 'Personal'
    MEMBER = 1, 'Member'
    GUEST = 2, 'Guest'
    DEVELOPER = 3, 'Developer'

class Account(models.Model):
    account_type = models.PositiveSmallIntegerField(choices=ACCOUNT_TYPE.choices, default=ACCOUNT_TYPE.MEMBER)
    
class ADDRESS_TYPE(models.IntegerChoices):
    BILLING = 0, 'Billing'
    SHIPPING = 1, 'Shipping'
    BOTH = 2, 'Both'

class Address(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='addresses')



class CustomerProfile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='customer_profile')

class DeveloperProfile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='developer_profile' )


class Category(models.Model):
    parent = models.ForeignKey('self', related_name='sub_category', on_delete=models.SET_NULL, blank=True, null=True, help_text="Parent category for hierachical organization") 

class CategoryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='images', help_text="The category this image belongs to.")

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='bundle')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')

class Coupon(models.Model):
    products = models.ManyToManyField(Product, blank=True, related_name='coupons')

class Wishlist(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='whishlisted_by')

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='reviews')
    likes = models.ManyToManyField(Account, related_name='liked_reviews', blank=True)
    dislikes = models.ManyToManyField(Account, related_name="disliked_reviews", blank=True)

class ShoppingCart(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='shopping_cart')

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_item')


class Order(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+') # disable reverse query to this model

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')

class Return(models.Model):
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='returns') 

class Refund(models.Model):
    return_item = models.OneToOneField(Return, on_delete=models.CASCADE, related_name='refund')

class PaymentInfo(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment_info')

class PaymentTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_transaction')
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE, related_name='payment_info')

class Vendor(models.Model):
    pass

class VendorProduct(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendors')


class Warehouse(models.Model):
    pass

class BinLocation(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='bin_location')

class Lot(models.Model):
    pass

class Stock(models.Model):
    product = models.ForeignKey(Product, related_name='warehouse_stock', on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, related_name='stock', on_delete=models.CASCADE)
    bin_location = models.ForeignKey(BinLocation, on_delete=models.CASCADE, related_name='stock')
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name='stock')

class Shipment(models.Model):
    warehouse = models.ForeignKey(Warehouse, related_name='shipments', on_delete=models.CASCADE)