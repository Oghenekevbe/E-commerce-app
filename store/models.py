from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid
import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your models here.

class BillingAddress(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, blank=True, null=True, related_name='billing_addresses')
    address = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    zipcode = models.CharField(max_length=225, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    is_no_billing_address = models.BooleanField(default=False)

    
    def __str__(self):
        if self.is_no_billing_address:
            return "No Billing Address"
        elif self.customer is not None and self.customer.user is not None:
            return str(self.customer.user) + ' - ' + self.address
        else:
            return str(self.address)

    class Meta:
        ordering = ('is_no_billing_address', 'id')

User = get_user_model()
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    phone_number = models.IntegerField(("Phone Number"), null=True, blank=True)
    billing_address = models.ForeignKey(BillingAddress, related_name='customers', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.user)



 
 
class Categories(models.Model):
    name = models.CharField(max_length=225, null=True)
    
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('store')
    
    


        
class Product(models.Model):
    name = models.CharField(max_length=225, null=True)
    image = models.ImageField(blank=False, null=False)
    description = models.CharField(null=True, blank=True,max_length=50)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name = 'product_category', null = True)
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
    transaction_id = models.UUIDField(default=uuid.uuid4().hex, primary_key=True)
    def __str__(self):
        return str(self.customer.user) + ' - ' + str(self.transaction_id)
    
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
        if self.product:
            return self.product.name
        else:
            return 'Order Item ' + str(self.id)

    
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    to_email = models.EmailField(max_length=100, null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name + ' - ' + self.to_email
    

  