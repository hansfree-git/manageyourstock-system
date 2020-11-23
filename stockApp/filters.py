import django_filters
from django_filters import DateFilter
from .models import*

class CatalogFilter(django_filters.FilterSet):
	start_date=DateFilter(field_name='date_created', lookup_expr='gte')
	end_date=DateFilter(field_name='date_created', lookup_expr='lte')

	class Meta:
		model=Stock
		fields=['category','item_name',]
		