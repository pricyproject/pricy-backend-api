from rest_framework.routers import DefaultRouter
from discovers.views import HomeDiscoversViewSet


router = DefaultRouter()

router.register(r'home', HomeDiscoversViewSet)

urlpatterns = router.urls
