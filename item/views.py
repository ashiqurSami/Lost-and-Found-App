from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from rest_framework.exceptions import PermissionDenied
from item.models import LostFoundItem
from .filter import LostFoundItemFilter
from item.serializers import LostFoundItemSerializer


# Create your views here.
class LostFoundItemViewSet(viewsets.ModelViewSet):
    queryset = LostFoundItem.objects.all().order_by('-created_at')
    serializer_class = LostFoundItemSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class=LostFoundItemFilter
    ordering_fields = ['created_at', 'date']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search')
        if search_query:
            vector = SearchVector('name', 'description', 'category', 'location', config='english')
            query = SearchQuery(search_query, config='english')
            queryset = queryset.annotate(search=vector).filter(search=query)
            queryset = queryset.annotate(rank=SearchRank(vector, query)).order_by('-rank', '-created_at')
        return queryset

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