from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.store, name="store"), 
    path("cart/", views.cart, name="cart"), 
    path("checkout", views.checkout, name="checkout"), 
    path("add_to_cart", views.AddToCart, name="add_to_cart"), 
    # path("update_cart", views.update_cart, name="update_cart"), 
    path("confirm_payment/<str:pk>", views.ConfirmPayment, name="confirm_payment"), 






    # USER CREDENTIALS
    path("register/", Register.as_view(), name="register"), 






]
