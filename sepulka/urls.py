from rest_framework.routers import DefaultRouter

from sepulka.views import SepulkaViewSet


router = DefaultRouter()
router.register("", SepulkaViewSet)


urlpatterns = router.urls
