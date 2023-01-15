from rest_framework.routers import DefaultRouter

from .views import ShopsViewSet

router = DefaultRouter()
router.register(r'', ShopsViewSet)

urlpatterns = router.urls
