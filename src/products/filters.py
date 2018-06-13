import django_filters

from products.models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(name='category__title')

    class Meta:
        model = Product
        fields = ['category', ]
