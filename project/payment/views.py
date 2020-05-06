from django.shortcuts import render
from django.conf import settings
from shop.models import cart
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def pay_view(request, slug):
	cart_qs = cart.objects.filter(user=request.user, slug=slug)
	cart_obj = cart_qs[0]
	amount = cart_obj.get_total()
	return render(request,'payment.html', {'slug':slug, 'amount':amount})