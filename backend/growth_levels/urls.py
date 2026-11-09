from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MiNetGrowthLevelViewSet

router = DefaultRouter()
router.register(r'mi-net-growth-levels', MiNetGrowthLevelViewSet, basename='mi-net-growth-levels')

urlpatterns = [
    path('', include(router.urls)),
]
