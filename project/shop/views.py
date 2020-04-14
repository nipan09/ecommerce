from django.shortcuts import render
from shop.models import products 

def home_view(request):
	objects = products.objects.all()
	return render(request, 'home.html', {'products': objects})
