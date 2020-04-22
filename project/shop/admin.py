from django.contrib import admin
from shop.models import products, cart, order

admin.site.register(products)
admin.site.register(cart)
admin.site.register(order)
