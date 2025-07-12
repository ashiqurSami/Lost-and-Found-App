from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from item.models import LostFoundItem
from item.serializers import LostFoundItemSerializer


# Create your views here.
class LostFoundItemViewSet(viewsets.ModelViewSet):
    queryset = LostFoundItem.objects.all().order_by('-created_at')
    serializer_class = LostFoundItemSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update','destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this item.")
        return super().perform_destroy(instance)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this item.")
        serializer.save()