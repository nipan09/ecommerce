from shop.models import products, cart, order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import ProductsSerializer
import stripe


def home_view(request):
	context = products.objects.all()
	quant = 0
	cart_qs = [int(obj.quantity) for obj in cart.objects.filter(user=request.user)]
	for i in range(len(cart_qs)):
		quant = quant+cart_qs[i]
	return render(request, 'home.html', {'products':context, 'quant':quant})

def add_cart_view(request, slug):
	item = get_object_or_404(products, slug=slug)
	cart_qs = cart.objects.filter(user=request.user, item=item)    #cart_qs --> instance of the retrieved or created object
	if cart_qs.exists():
		cart_item = cart_qs[0]
		quant = cart_item.quantity
		quant+=1
		cart_item.quantity = quant
		cart_item.save(update_fields=['quantity'])
		messages.info(request, "The item quantity is updated")
	else:
		cart.objects.create(user=request.user, item=item, slug=slug)
		messages.info(request,"This item is added to your cart")
	return redirect('home')

def remove_cart_view(request, slug):
	item = get_object_or_404(products, slug=slug)
	cart_qs = cart.objects.filter(user=request.user, item=item)
	if cart_qs.exists():
		cart_obj = cart_qs[0]
		if cart_obj.quantity>1:
			quant = cart_obj.quantity
			quant-=1
			cart_obj.quantity = quant
			cart_obj.save(update_fields=['quantity'])
		else:
			cart_qs.delete()
		messages.success(request, "Your Cart is updated")
	else:
		messages.info(request, "This item is not in your cart")
	return redirect('home')

def cart_view(request):
	order_qs = order.objects.filter(user=request.user)
	cart_qs = cart.objects.filter(user=request.user)
	return render(request,'cart.html',{'carts':cart_qs,'orders':order_qs})

def order_view(request, slug):
	cart_qs = cart.objects.filter(user=request.user, slug=slug)
	cart_item = cart_qs[0]
	amount = cart_item.get_total()
	if request.method == 'POST':
		customer = stripe.Customer.create(
			email = request.POST['email'],
			name = request.POST['username'],
			source = request.POST['stripeToken']
			)
		charge = stripe.Charge.create(
			customer = customer,
			amount = int(amount)*100,
			currency = "inr",
			description = cart_item.item.name,
			)

	order.objects.create(user=request.user, item=cart_item, slug=slug, quantity=cart_item.quantity)
	return redirect('cart')


class JSONResponse(HttpResponse):
	'''
	
	An HttpResponse that renders its content into JSON.
	
	'''

	def __init__self(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

def product_list_api(request):
	'''

	List all the products

	'''
	if request.method == 'GET':
		product_qs = products.objects.all()
		serializer = ProductsSerializer(product_qs, many=True)   # many makee sure to serialize querysets instead of model instances
		return JSONResponse(serializer.data)