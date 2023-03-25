from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
import json
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import LoginView
from django.views import generic
from .forms import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test



# Create your views here.
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('unauthorized')
    
def unauthorized(request):
    return render(request, 'unauthorized.html')


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
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()


    context = {'products': products, 'order': order, 'items':items,'query':query}
    return render(request, 'store.html', context)

class Orders(StaffRequiredMixin, ListView):
    model = Order
    template_name = "customer/orders.html"
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-date_ordered')
    
class OrderDetail(StaffRequiredMixin,DetailView):
    model = Order
    template_name = 'customer/order_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        order_items = order.orderitem_set.all()
        context['order_items'] = order_items
        return context

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
      customer_email = order.customer.user.email
      customer_address = order.billing_address
      cart_total = order.get_cart_total

    
    context = {'product':product, 'items': order_item, 'order': order,'customer_id': customer_id,'customer_name': customer_name,
    'customer_email': customer_email, 'customer_address':customer_address}
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
        print(str(order_item) + ' - ' + str(order_item.quantity) + 'pcs in your cart')
        order_item.save()

        total_items = order.get_cart_items
        
        
    
        return JsonResponse(total_items, safe=False)
    
    
class Products(DetailView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=self.request.user.customer, complete=False)
            order_item = order.orderitem_set.all()
            context["order"] = order
            context["order_item"] = order_item
        return context
        
    


def ConfirmPayment(request,pk):
    Order = order.object.get(id=pk)
    order.completed = True
    order.save()
    messages.success(request, "Payment made successfully")
    return redirect('store')



# USER CREDENTIALS

class Register(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class EmailLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = 'login.html'



class Profile(DetailView):
      
    model = Customer
    template_name = "registration/profile.html"
    context_object_name = 'customer'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=self.request.user.customer, complete=False)
            order_item = order.orderitem_set.all()
            context["order"] = order
            context["order_item"] = order_item
        return context
        

class EditProfile(UpdateView):
    model = User
    template_name = "registration/edit_profile.html"
    form_class = ProfileForm
    success_url = '/'
    
class ChangePassword(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('store')




class ContactView(StaffRequiredMixin,CreateView):
    model = Contact
    template_name = 'customer/contact_us.html'
    fields = ['name', 'to_email', 'subject', 'message']    
    success_url = reverse_lazy('store')

    def form_valid(self, form):
        # Save the contact message to the database
        response = super().form_valid(form)

        # Send an email to the specified address
        contact = form.save(commit=False)
        subject = 'New contact message from {}'.format(contact.name)
        message = 'From: {} <{}>\n\n{}'.format(contact.name, settings.EMAIL_HOST_USER, contact.message)
        send_mail(subject, 
                  message, 
                  settings.EMAIL_HOST_USER, 
                  [contact.to_email],
                  fail_silently=False,
                  )
                  
        return response
    
    
    
class ContactView2(CreateView):
    form_class = ContactForm
    template_name = 'customer/contact_us2.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            order, created = Order.objects.get_or_create(customer=self.request.user.customer, complete=False)
            order_item = order.orderitem_set.all()
            context["order"] = order
            context["order_item"] = order_item
        return context
        

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.send_email()
            return redirect('store')
        return render(request, self.template_name, {'form': form})


