from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from project.utils import unique_slug_generator

class products(models.Model):
	image = models.ImageField(upload_to='products/')
	name =  models.CharField(max_length=50)
	slug = models.SlugField(blank=True, unique=True)
	title = models.CharField(max_length=50)
	price = models.FloatField()

	def __str__(self):
		return self.name

def slug_generator(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=products)