from rest_framework import viewsets, filters

from base.filters import IsOwnerFilterBackend
from .serializers import ListSerializer
from .models import List


class ListsViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, IsOwnerFilterBackend)
    search_fields = ('name', )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
