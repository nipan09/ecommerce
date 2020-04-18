from django.utils.text import slugify
import random
import string

def random_string_generator(size):
	return ''.join(random.choice(string.ascii_uppercase +
		                         string.ascii_lowercase +
		                         string.digits+
		                         string.punctuation)
	                             for n in range(size))


def unique_slug_generator(model_instance):
	slug = slugify(model_instance.name)
	model_class = model_instance.__class__

	while model_class.objects.filter(slug=slug).exists():
		slug = "{slug}-{randstr}".format(slug=slug, 
		                                randstr=random_string_generator(4)
		                                )
		                                   
	return slug
