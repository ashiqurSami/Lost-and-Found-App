from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LostFoundItemViewSet, MatchFoundItemView

router = DefaultRouter()
router.register('items', LostFoundItemViewSet, basename='item')

urlpatterns = router.urls

urlpatterns += [
    path('items/match/<int:lost_item_id>/',MatchFoundItemView.as_view(), name='match-found-items'),
]