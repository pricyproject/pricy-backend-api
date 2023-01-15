from rest_framework.routers import DefaultRouter
from .views import ProductCategoriesViewSet

router = DefaultRouter()
router.register(r'', ProductCategoriesViewSet)

urlpatterns = router.urls
