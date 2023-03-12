from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name="store"), 
    path("cart/", views.cart, name="cart"), 
    path("checkout", views.checkout, name="checkout"), 
    path("add_to_cart", views.AddToCart, name="add_to_cart"), 
    path("confirm_payment/<str:pk>", views.ConfirmPayment, name="confirm_payment"), 
]
