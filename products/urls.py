from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import ProductsViewSet

router = DefaultRouter()
router.register(r'', ProductsViewSet)

urlpatterns = router.urls
