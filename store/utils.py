from .models import *

def CartData(request):
   if request.user.is_authenticated:
      customer = request.user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False)
      items = order.orderitem_set.all()
   else:
   
      item=[]
      order={'get_cart_total':0,'get_cart_items':0}

        
   return {'items': items, 'order': order}
