import random
from celery import shared_task
from bucket import bucket
from .models import Product, SpecialProduct


# TODO: can be async?
def all_bucket_objects_task():
	result = bucket.get_objects()
	return result


@shared_task
def delete_object_task(key):
	bucket.delete_object(key)


@shared_task
def download_object_task(key):
	bucket.download_object(key)


@shared_task
def special_book():
	special_product = SpecialProduct.objects.all()
	ins = special_product[0]
	products = Product.objects.all()
	rnd = Product.objects.get(id=random.randrange(0, len(products)))
	ins.spc = rnd.id
	ins.save()
