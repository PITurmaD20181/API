from rest_framework import routers
from .views import DisciplineViewSet, ClassViewSet, StudentViewSet

ROUTER = routers.DefaultRouter()
ROUTER.register(r'^discipline', DisciplineViewSet)
ROUTER.register(r'^class', ClassViewSet)
ROUTER.register(r'^student', StudentViewSet)

urlpatterns = ROUTER.urls
