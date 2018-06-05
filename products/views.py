from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from base.filters import IsOwnerFilterBackend
from base.viewsets import OwnerModelViewSet
from products.filters import ProductFilter
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product


class CategoryViewSet(OwnerModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (IsOwnerFilterBackend, )


class ProductViewSet(OwnerModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, IsOwnerFilterBackend)
    filter_class = ProductFilter
    search_fields = ('name', 'category__title')
