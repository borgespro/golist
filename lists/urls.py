from rest_framework.routers import DefaultRouter

from .views import ListsViewSet

router = DefaultRouter()
router.register(r'', ListsViewSet, base_name='list')
urlpatterns = router.urls
