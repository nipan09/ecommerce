from django.db import models

class products(models.Model):
	image = models.ImageField(upload_to='products/')
	name =  models.CharField(max_length=50)
	title = models.CharField(max_length=50)
	price = models.FloatField()

	def __str__(self):
		return self.name
