from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from project.utils import unique_slug_generator
from django.contrib.auth.models import User

class products(models.Model):
	image = models.ImageField(upload_to='products/')
	name =  models.CharField(max_length=50)
	slug = models.SlugField(blank=True, unique=True)
	title = models.CharField(max_length=50)
	price = models.FloatField()

	def __str__(self):
		return self.name

class cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)         #user, FornK: different cart req (quantity of each prdt )
	item = models.ForeignKey(products, on_delete=models.CASCADE)     #item, FornK: One2One will not allow that prdt whatever may be the user is. 
	quantity = models.IntegerField(default=1)                        #quantity: responsible for FornK @user
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.quantity} of {self.item.name}'

	def get_total(self):
		total = self.item.price * self.quantity
		floattotal = float("{0:.2f}".format(total))
		return floattotal

#order model is needed for incrementing quantity in cart model.
class order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)   #user, ForeignKey: one user --> two order (ordered=True, ordered=False)
	oredereditems = models.ManyToManyField(cart)               #ordrditm, Man2Man: one model(True/False) should allow to add more than one items.
	ordered = models.BooleanField(default=False)               #ordered, Bool: responsible for ForeignKey to user in this model
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username

def slug_generator(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=products)