from rest_framework.fields import SerializerMethodField

from .models import *
from rest_framework import serializers


from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model= Country
        fields = ['id', 'country_name']

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Director
        fields = ['director_name']


class DirectorListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'director_name']


class ActorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'actor_name']


class ActorListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'actor_name']



class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre_name']


class MovieListSerializers(serializers.ModelSerializer):
    year = serializers.DateField(format='%Y')
    country = CountrySerializer(many=True)
    genre = GenreSerializers(many=True)


    class Meta:
        model = Movie
        fields = ['id', 'movie_image', 'movie_name', 'year', 'country', 'genre', 'status_movie']


class DirectorDetailSerializers(serializers.ModelSerializer):
    director_movie = MovieListSerializers(many=True, read_only=True)

    class Meta:
        model = Director
        fields = ['director_name', 'director_image', 'age', 'bio', 'director_movie']


class ActorDetailSerializers(serializers.ModelSerializer):
    actor_movie = MovieListSerializers(many=True, read_only=True)

    class Meta:
        model = Actor
        fields = ['actor_name', 'actor_image', 'age', 'bio', 'actor_movie']


class MovieLanguagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['id', 'language', 'video']


class MomentsSerializers (serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie_moments']



class MovieDetailSerializers(serializers.ModelSerializer):
    year = serializers.DateField(format=('%d-%m-%Y'))
    country = CountrySerializer(many=True)
    director = DirectorSerializer(many=True)
    actor = ActorSerializers(many=True)
    genre = GenreSerializers(many=True)
    videos = MovieLanguagesSerializers(many=True, read_only=True)
    images = MomentsSerializers(many=True, read_only=True)
    avg_rating = serializers.SerializerMethodField()
    get_count_people = serializers.SerializerMethodField()


    class Meta:
        model = Movie
        fields = ['movie_name', 'year', 'country', 'director', 'actor', 'genre', 'types', 'movie_time', 'movie_trailer',
                  'movie_image', 'description', 'status_movie', 'videos', 'images', 'avg_rating', 'get_count_people']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id','user', 'parent','movie', 'stars', 'text', 'created_date']


class FavoriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteMovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = '__all__'


class HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'