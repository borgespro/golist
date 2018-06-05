from rest_framework import viewsets

from base.filters import IsOwnerFilterBackend
from .serializers import CategorySerializer
from .models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (IsOwnerFilterBackend, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
