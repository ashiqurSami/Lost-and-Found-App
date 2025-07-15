import django_filters
from .models import LostFoundItem

class LostFoundItemFilter(django_filters.FilterSet):
    date_after= django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_before= django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = LostFoundItem
        fields=['status', 'category', 'location']