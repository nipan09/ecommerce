from django.urls import path
from . import views

urlpatterns=[
     path('shop/', views.home_view, name='home'),
     path('shop/addcart/<slug>', views.add_cart_view, name='addCart'),
     path('shop/removeCart/<slug>', views.remove_cart_view, name='removeCart'),
     path('shop/cart', views.cart_view, name='cart'),
     path('shop/cart/order/<slug>', views.order_view, name='order'),
]