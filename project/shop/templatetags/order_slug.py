from django import template
from shop.models import order

register = template.Library()

@register.filter(name='order_slug')
def order_slug(slug):
	if order.objects.filter(slug=slug).exists():
		return True