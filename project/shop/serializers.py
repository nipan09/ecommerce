from rest_framework import serializers
from .models import products

'''

Converting querysets and model instances to native python datatypes

'''

class ProductsSerializer(serializers.ModelSerializer):
	class Meta:
		model = products
		fields = ('image','name','slug','title','price')