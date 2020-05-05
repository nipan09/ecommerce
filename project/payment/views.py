from django.shortcuts import render
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def pay_view(request, slug):
	return render(request,'payment.html', {'slug':slug})