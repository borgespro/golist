from rest_framework import serializers

from .models import List


class ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = ('id', 'name', 'valid_at', 'is_active', 'created_at', 'updated_at')
