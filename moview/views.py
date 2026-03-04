from rest_framework import viewsets, generics, status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *

from .serializers import (ProfileSerializer, CountrySerializer, DirectorListSerializers, DirectorDetailSerializers, ActorListSerializers,
                          ActorDetailSerializers, GenreSerializers,
                          MovieListSerializers, MovieDetailSerializers, UserSerializer,
                          RatingSerializers, FavoriteSerializers, FavoriteMovieSerializers, HistorySerializers,
                          LoginSerializer)

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer



class DirectorListAPIView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorListSerializers

class DirectorDetailAPIView(generics.RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorDetailSerializers


class ActorListAPIView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializers


class ActorDetailAPIView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializers


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializers
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['country', 'year', 'genre', 'status_movie', 'actor', 'director']
    search_fields = ['movie_name']
    ordering_fields = ['year']
    permission_classes = [IsAuthenticatedOrReadOnly]

class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializers


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers


class FavoriteMovieViewSet(viewsets.ModelViewSet):
    queryset = FavoriteMovie.objects.all()
    serializer_class = FavoriteMovieSerializers


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializers



