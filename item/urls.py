from rest_framework.routers import DefaultRouter
from .views import LostFoundItemViewSet

router = DefaultRouter()
router.register('items', LostFoundItemViewSet, basename='item')

urlpatterns = router.urls