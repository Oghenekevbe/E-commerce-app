from django.shortcuts import render
from .models import *
from .utils import CartData
from django.http import JsonResponse
import json

# Create your views here.

def store(request):
    products = Product.objects.all()
    cart_data = CartData(request)
    items = cart_data['items']
    order = cart_data['order']
    

    context = {'products':products,'items': items, 'order': order }
    return render(request, 'store.html', context)

def cart(request):
        
    cart_data = CartData(request)
    items = cart_data['items']
    order = cart_data['order']
    
    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context)

def checkout(request):
    
    cart_data = CartData(request)
    items = cart_data['items']
    order = cart_data['order']

    
    context = {'items': items, 'order': order}
    return render(request, 'checkout.html', context)


def AddToCart(request):
    data = json.loads(request.body)
    product_id= data['id']
    product = Product.objects.get(id=product_id)
    
    # we create check if there is a cart for the user. if none, we create
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
        print(order)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity +=1
        order_item.save()
        
        total_items = order.get_cart_items
        
        
    
    return JsonResponse(total_items,safe=False)


