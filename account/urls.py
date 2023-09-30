from rest_framework.routers import DefaultRouter

from account.routers import PersonalOnlyRouter
from account.views import UserPersonalViewSet, UserViewSet

router = DefaultRouter()
router.register(r"", UserViewSet)

personal_router = PersonalOnlyRouter()
personal_router.register(r"", UserPersonalViewSet, basename="personal")


urlpatterns = [
    *personal_router.urls,
    *router.urls,
]
