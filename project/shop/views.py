from shop.models import products, cart, order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def home_view(request):
	context = products.objects.all()
	quant = 0
	cart_qs = [int(obj.quantity) for obj in cart.objects.filter(user=request.user)]
	for i in range(len(cart_qs)):
		quant = quant+cart_qs[i]
	return render(request, 'home.html', {'products':context, 'quant':quant})

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
			messages.info(request, "The item quantity is updated")
		else:
			uzer.oredereditems.add(order_item)   #if item doesn't exists, add it
			messages.info(request,"This item is added to your cart")
	else:
		order_create = order.objects.create(user=request.user)   #if user doesn't exists, create the model order
		order_create.oredereditems.add(oredereditems=order_item)   #add the instance of the cart model
		messages.success(request, "This item is added to your cart")
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

