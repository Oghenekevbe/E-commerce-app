from django.shortcuts import render
from .models import *
from .utils import *

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
