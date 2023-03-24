from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.store, name="store"), 
    path("cart/", views.cart, name="cart"), 
    path("checkout", views.checkout, name="checkout"), 
    path("add_to_cart", views.AddToCart, name="add_to_cart"), 
    path("products/<str:pk>/", Products.as_view(), name="products"), 
    # path("update_cart", views.update_cart, name="update_cart"), 
    path("confirm_payment/<str:pk>", views.ConfirmPayment, name="confirm_payment"), 






    # USER CREDENTIALS
    path("register/", Register.as_view(), name="register"), 
    path("<str:pk>/profile/", Profile.as_view(), name="profile"), 
    path("<str:pk>/edit_profile/", EditProfile.as_view(), name="edit_profile"), 
    path("<str:pk>/change_password/", ChangePassword.as_view(template_name='registration/change_password.html'), name="change_password"), 

    # USER INTERACTIONS
    path("contact_us/", ContactView.as_view(), name="contact_us"), 
    path("contact_us2/", ContactView2.as_view(), name="contact_us2"), 
    path("unauthorized/", views.unauthorized, name="unauthorized"), 




]


