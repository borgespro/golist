from rest_framework import viewsets


class OwnerModelViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
