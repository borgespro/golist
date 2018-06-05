from rest_framework import filters

from base.filters import IsOwnerFilterBackend
from base.viewsets import OwnerModelViewSet
from .serializers import ListSerializer
from .models import List


class ListsViewSet(OwnerModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, IsOwnerFilterBackend)
    search_fields = ('name', )
