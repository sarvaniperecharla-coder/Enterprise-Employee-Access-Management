from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveTypeViewSet, LeaveViewSet

router = DefaultRouter()
router.register(r"leave-types", LeaveTypeViewSet)
router.register(
    r"leaves",
    LeaveViewSet,
    basename="leaves"
)

urlpatterns = [
    path("", include(router.urls)),
]