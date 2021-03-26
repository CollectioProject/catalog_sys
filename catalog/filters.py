import django_filters

from .models import *
from django_filters import DateFilter, CharFilter


class RecordFilter(django_filters.FilterSet):
    date_created_start = DateFilter(field_name="date_start", lookup_expr='gte')
    date_created_end = DateFilter(field_name="date_start", lookup_expr='lte')
    record_description = CharFilter(field_name='description', lookup_expr='icontains')
    cond_description = CharFilter(field_name='condition_description', lookup_expr='icontains')

    class Meta:
        model = Record
        fields = '__all__'
        exclude = ['creation_date', 'last_modified', 'description', 'date_start', 'date_end', 'condition_description']
