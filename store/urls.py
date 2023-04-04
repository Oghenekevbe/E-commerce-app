from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.store, name="store"), 
    path("cart/", views.cart, name="cart"), 
    path("orders/", Orders.as_view(), name="orders"), 
    path("orders/<str:pk>", OrderDetail.as_view(), name="order_detail"), 
    path("checkout", views.checkout, name="checkout"), 
    path("add_to_cart", views.AddToCart, name="add_to_cart"), 
    path('delete/<int:pk>/', CartItemDeleteView.as_view(), name='cart-item-delete'),
    path("products/<str:pk>/", Products.as_view(), name="products"), 
    path("add_product/", AddProduct.as_view(), name="add_product"), 
    path("edit_product/<str:pk>/", EditProduct.as_view(), name="edit_product"), 
    path("categories/", Category.as_view(), name="categories"), 
    path("add_category/", AddCategory.as_view(), name="add_category"), 
    path("categories/<str:pk>", CategoryDetail.as_view(), name="category_detail"), 
    path("confirm_payment/<str:pk>", views.ConfirmPayment, name="confirm_payment"), 






    # USER CREDENTIALS
    path("register/", Register.as_view(), name="register"), 
    path("<str:pk>/profile/", Profile.as_view(), name="profile"), 
    path("<str:pk>/edit_profile/", EditProfile.as_view(), name="edit_profile"), 
    path("<str:pk>/change_password/", ChangePassword.as_view(template_name='registration/change_password.html'), name="change_password"), 
    path('confirm-email/<str:token>/', confirm_email, name='confirm_email'),  
    
    path("contact_us/", ContactView.as_view(), name="contact_us"), 
    path("contact_us2/", ContactView2.as_view(), name="contact_us2"), 
    path("unauthorized/", views.unauthorized, name="unauthorized"), 
    path('add_address/', AddAddress.as_view(), name='add_address'),
    path('<str:pk>/edit_address/', EditAddress.as_view(), name='edit_address'),
    path('<str:pk>/delete_address/', DeleteAddress.as_view(), name='delete_address'),



]


