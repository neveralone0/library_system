from .filters import ProductFilter
from .models import Product


def filter(request):
    products = Product.objects.filter(available=True)
    return {'filter': ProductFilter(request.GET, queryset=products)}
