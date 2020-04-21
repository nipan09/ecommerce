from shop.models import products, cart
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def home_view(request):
	context = products.objects.all()
	return render(request, 'home.html', {'products':context})

def add_cart_view(request, slug):
	item = get_object_or_404(products, slug=slug)
	cart.objects.create(user=request.user, item=item)
	messages.info(request, "This item has been added to your cart")
	return redirect('home')