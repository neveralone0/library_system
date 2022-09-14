import django_filters
from django_filters import DateFilter, TimeFilter, CharFilter, NumberFilter
from .models import Product


class ProductFilter(django_filters.FilterSet):
    book_name = CharFilter(field_name='name')
    pages = NumberFilter(field_name='pages')
    price = NumberFilter(field_name='price')

    class Meta:
        model = Product
        fields = ('name', 'pages', 'price')
