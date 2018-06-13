from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, base_name='category')
router.register(r'', ProductViewSet, base_name='product')
urlpatterns = router.urls
