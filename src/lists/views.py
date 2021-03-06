from django.http import Http404
from rest_framework import filters, viewsets

from base.filters import IsOwnerFilterBackend
from base.viewsets import OwnerModelViewSet
from .serializers import ListSerializer, ItemSerializer
from .models import List, Item


class ListsViewSet(OwnerModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, IsOwnerFilterBackend)
    search_fields = ('name', )


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('product__name', )

    def get_queryset(self):
        return Item.objects.filter(list=self.kwargs['list_pk'], list__owner=self.request.user)

    def perform_create(self, serializer):
        try:
            items_list = List.objects.get(pk=self.kwargs['list_pk'])
            serializer.save(list=items_list)
        except List.DoesNotExist:
            raise Http404
