from datetime import timedelta
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, status
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from rest_framework.exceptions import PermissionDenied, ParseError
from rest_framework.views import APIView
from item.models import LostFoundItem
from .filter import LostFoundItemFilter
from item.serializers import LostFoundItemSerializer
from django.db.models import F


# Create your views here.
class LostFoundItemViewSet(viewsets.ModelViewSet):
    queryset = LostFoundItem.objects.all().order_by('-created_at')
    serializer_class = LostFoundItemSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class=LostFoundItemFilter
    ordering_fields = ['created_at', 'date']

    def get_queryset(self):
        queryset = super().get_queryset()

        #Geo radius filter
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius = self.request.query_params.get('radius')  # in km

        if lat and lon and radius:
            try:
                user_location = Point(float(lon), float(lat), srid=4326)
                queryset = queryset.annotate(distance=Distance('point', user_location))\
                    .filter(distance__lte=D(km=float(radius)))
            except ValueError:
                raise ParseError("Invalid geolocation or radius.")

        # full-text search
        search_query = self.request.query_params.get('search')
        if search_query:
            vector = SearchVector('name', 'description', 'category', 'location', config='english')
            query = SearchQuery(search_query, config='english')
            queryset = queryset.annotate(search=vector).filter(search=query)
            queryset = queryset.annotate(rank=SearchRank(vector, query))

        # final ordering
        if search_query and lat and lon and radius:
            queryset = queryset.order_by('-rank', 'distance', '-created_at')
        elif search_query:
            queryset = queryset.order_by('-rank', '-created_at')
        elif lat and lon and radius:
            queryset = queryset.order_by('distance')
        else:
            queryset = queryset.order_by('-created_at')

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


class MatchFoundItemView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self,request,lost_item_id):
        try:
            lost_item=LostFoundItem.objects.get(id=lost_item_id,status='lost')
        except LostFoundItem.DoesNotExist:
            return Response({"error": "Lost item not found."}, status=status.HTTP_404_NOT_FOUND)

        # calculate date range ±3 days
        start_date = lost_item.date - timedelta(days=3)
        end_date = lost_item.date + timedelta(days=3)

        # Base queryset: all found items with same category and date range
        queryset =  LostFoundItem.objects.filter(
            status='found',
            category=lost_item.category,
            date__range=(start_date, end_date)
        )

        # location based filtering
        if lost_item.point:
            queryset = queryset.annotate(
                distance=Distance('point',lost_item.point)
            ).filter(distance__lte=D(km=3))  # 3 km radius

        # trigram similarity on name and description
        queryset = queryset.annotate(
            name_sim = TrigramSimilarity('name', lost_item.name),
            desc_sim = TrigramSimilarity('description', lost_item.description),
        ).annotate(
            total_sim=F('name_sim')+F('desc_sim')
        ).order_by('-total_sim','-date')[:5]

        serializer = LostFoundItemSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)