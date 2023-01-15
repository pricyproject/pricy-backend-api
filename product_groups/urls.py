from rest_framework.routers import DefaultRouter

from product_groups.views import ProductGroupsViewSet

router = DefaultRouter()
router.register(r'', ProductGroupsViewSet)

urlpatterns = router.urls
