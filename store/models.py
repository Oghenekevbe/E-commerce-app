from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime
from django.utils import timezone

# Create your models here.

class BillingAddress(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True,related_name='billing_addresses')
    address = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    zipcode = models.CharField(max_length=225, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.address   


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    billing_address = models.ForeignKey(BillingAddress, related_name='customers', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user)



 
 



        
class Product(models.Model):
    name = models.CharField(max_length=225, null=True)
    image = models.ImageField(blank=False, null=False)
    description = models.CharField(null=True, blank=True,max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.name)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, related_name='orders', null=True, blank=True, on_delete =models.CASCADE )
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, blank=True, null=True, related_name='billing_address_order_set')    
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    def __str__(self):
        return str(self.transaction_id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total() for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    

    
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.product.name
    
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

  