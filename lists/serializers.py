from rest_framework import serializers

from products.serializers import ProductSerializer
from .models import List, Item


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id', 'name', 'total_value', 'valid_at', 'is_active', 'created_at', 'updated_at')


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Item
        fields = ('id', 'total_price', 'quantity', 'product', 'list', 'created_at', 'updated_at')
