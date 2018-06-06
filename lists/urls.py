from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import ListsViewSet, ItemViewSet

router = DefaultRouter()
router.register(r'', ListsViewSet, base_name='list')


items_router = routers.NestedSimpleRouter(router, r'', lookup='list')
items_router.register(r'items', ItemViewSet, base_name='item')

urlpatterns = router.urls + items_router.urls
