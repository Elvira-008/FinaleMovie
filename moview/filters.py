from .models import Movie
from django_filters import filterset

class MovieFilters(filterset.FilterSet):
    class Meta:
        model = Movie
        fields = {
            'country': ['exact'],
            'year': ['gt', 'lt'],
            'genre': ['exact'],
            'status_movie': ['exact'],
            'actor': ['exact'],
            'director': ['exact'],
        }