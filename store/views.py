from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib import messages

# Create your views here.

# def store(request):
#     order = None
#     order_items = []
#     products = Product.objects.all()
#     if request.user.is_authenticated:
#         order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    

#     context = {'products':products, 'order': order }
#     return render(request, 'store.html', context)

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context['items'] = items
    context['order'] = order
    return render(request, 'store.html', context)

def cart(request):
    order = None
    order_item = []
   
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
        order_item = order.orderitem_set.all()


    context = {'items': order_item, 'order': order}
    return render(request, 'cart.html', context)


def checkout(request):
    order = None
    order_item = []
    product = Product.objects.all()
    if request.user.is_authenticated:
      order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
      order_item = order.orderitem_set.all()
      customer_id = order.customer.user.id
      customer_name = order.customer.user
      customer_email = order.customer.email
      cart_total = order.get_cart_total

    
    context = {'product':product, 'items': order_item, 'order': order,'customer_id': customer_id,'customer_name': customer_name,
    'customer_email': customer_email}
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


def ConfirmPayment(request,pk):
    Order = order.object.get(id=pk)
    order.completed = True
    order.save()
    messages.success(request, "Payment made successfully")
    return redirect('store')