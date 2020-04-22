from shop.models import products, cart, order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def home_view(request):
	context = products.objects.all()
	return render(request, 'home.html', {'products':context})

def add_cart_view(request, slug):
	item = get_object_or_404(products, slug=slug)
	order_item, created = cart.objects.get_or_create(user=request.user, item=item)    #order_item --> instance of the retrieved or created object
	#checking for if the product exists:
	order_qs = order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():                    #if user exists in False ordered model
		uzer = order_qs[0]
		if uzer.oredereditems.filter(item__slug=item.slug).exists():
			quant = order_item.quantity
			quant+=1
			order_item.quantity = quant
			order_item.save(update_fields=['quantity'])           #if item exists, increase the qunatity
			messages.info(request, "This item quantity is updated")
		else:
			uzer.oredereditems.add(order_item)   #if item doesn't exists, add it
	else:
		order_create = order.objects.create(user=request.user)   #if user doesn't exists, create the model order
		order_create.oredereditems.add(oredereditems=order_item)   #add the instance of the cart model
	return redirect('home')