from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProfileViewSet, CountryViewSet, DirectorListAPIView, DirectorDetailAPIView,
                    ActorListSerializers, ActorDetailSerializers, GenreViewSet, MovieListView, MovieDetailView,
                    RatingViewSet, FavoriteViewSet, FavoriteMovieViewSet, HistoryViewSet,
                    RegisterView, CustomLoginView, LogoutView, ActorListAPIView, ActorDetailAPIView)


router = DefaultRouter()
router.register('profile',  ProfileViewSet, basename='profile')
router.register('country', CountryViewSet, basename='country')
router.register('genre', GenreViewSet, basename='genre')
router.register('rating', RatingViewSet, basename='rating')
router.register('favorite', FavoriteViewSet, basename='favorite')
router.register('favoriteMovie', FavoriteMovieViewSet, basename='favorite-movie')
router.register('history', HistoryViewSet, basename='history')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logaut'),
    path('movie/', MovieListView.as_view(), name='movie_list'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('director/', DirectorListAPIView.as_view(), name='director_list'),
    path('director/<int:pk>/', DirectorDetailAPIView.as_view(), name='director_detail'),
    path('actor/', ActorListAPIView.as_view(), name='actor_list'),
    path('actor/<int:pk>/', ActorDetailAPIView.as_view(), name='actor_detail'),
]


