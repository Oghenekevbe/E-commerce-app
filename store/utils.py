from .models import *


def CartData(request):
   #this will enable the page not to return an error till we fix authentication for anonymous users
   order = None
   items = []
   
   if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
      cart_total = order.get_cart_total
   # else:
   
   #    item=[]
   #    order={'get_cart_total':0,'get_cart_items':0}

   return {'items': items, 'order': order}


