from shop.models import products
from django.shortcuts import render, redirect

def home_view(request):
	context = products.objects.all()
	return render(request, 'home.html', {'products':context})