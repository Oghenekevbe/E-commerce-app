from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingAddress)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Categories)