from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.forms import DateTimeInput
from .models import Post


class PostFilter(FilterSet):
    created_time = DateTimeFilter(
        field_name='created_time',
        lookup_expr='gt',
        widget=DateTimeInput(attrs={
            'id': 'start',
            'type': 'date',
        }),
        label='сортировать позже'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains',],
            'author__user__username': ['icontains'],
        }
