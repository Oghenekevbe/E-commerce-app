from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib import messages
from django.db.models import Q

# Create your views here.


def store(request):
    products = Product.objects.all()
    query =  request.GET.get('q')
    print(query)
    if query:
        products = products.filter(Q(name__icontains=query) |Q(description__icontains=query))
        print(products)
    
    order = None
    items = []
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()


    context = {'products': products, 'order': order, 'items':items,'query':query}
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
        
        
    
        return JsonResponse(total_items, safe=False)

# def update_cart(request):
#     data = json.loads(request.body)
#     product_id= data['id']
#     operation = data['operation']
#     quantity = data['quantity']
#     product = Product.objects.get(id=product_id)
    
#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
#         order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
#         if operation == 'add':
#             order_item.quantity = quantity
#         elif operation == 'remove':
#             order_item.quantity -= 1
#         if order_item.quantity <= 0:
#             order_item.delete()
#         else:
#             order_item.save()

#         total_items = order.get_cart_items()

#         return JsonResponse({'quantity': order_item.quantity, 'total_items': total_items}, safe=False)

def ConfirmPayment(request,pk):
    Order = order.object.get(id=pk)
    order.completed = True
    order.save()
    messages.success(request, "Payment made successfully")
    return redirect('store')