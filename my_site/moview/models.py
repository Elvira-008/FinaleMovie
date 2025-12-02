from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

STATUS_CHOICES = (
    ('pro', 'pro'),
    ('simple', 'simple')
    )


class Profile(AbstractUser):
    age = models.PositiveIntegerField(validators=[MinValueValidator(12), MaxValueValidator(70)], null=True, blank=True)
    phone_number = PhoneNumberField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')

    def __str__(self):
        return f'{self.first_name}-{self.last_name}'

class Country(models.Model):
   country_name = models.CharField(max_length=64, unique=True)

   def __str__(self):
       return self.country_name

class Director(models.Model):
    director_name = models.CharField(max_length=64)
    bio = models.TextField()
    age = models.PositiveIntegerField(validators=[MinValueValidator(16), MaxValueValidator(100)],
                                      null=True, blank=True)
    director_image = models.ImageField(upload_to='director_image/', null=True, blank=True)

    def __str__(self):
        return f'{self.director_name}'

class Actor(models.Model):
    actor_name = models.CharField(max_length=64)
    bio = models.TextField()
    age = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                      null=True, blank=True)
    actor_image = models.ImageField(upload_to='actor_image/', null=True, blank=True)

    def __str__(self):
        return f'{self.actor_name}'

class Genre(models.Model):
    genre_name = models.CharField(max_length=32, unique=True, null=True, blank=True)

    def __str__(self):
        return self.genre_name

class Movie(models.Model):
    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    country = models.ManyToManyField(Country)
    director = models.ManyToManyField(Director, related_name='director_movie')
    actor = models.ManyToManyField(Actor, related_name='actor_movie')
    genre = models.ManyToManyField(Genre)
    TYPES_CHOICES = (
    ('144p', '144p'),
    ('360p', '360p'),
    ('480p', '480p'),
    ('720p', '720p'),
    ('1080p', '1080p'),
    )
    types = models.CharField(max_length=6, choices=TYPES_CHOICES, default='360p')
    movie_time = models.PositiveIntegerField()
    description = models.TextField()
    movie_trailer = models.FileField(upload_to='movie_trailer/')
    movie_image = models.ImageField(upload_to='movie_image/')
    status_movie  = models.CharField(max_length=20, choices=STATUS_CHOICES)


    def get_avg_rating(self):
        score = self.rating_set.all()
        if score.exists():
            return round(sum([i.stars for i in score]) / score.count(), 2)
        return 0

    def get_count_people(self):
        return self.rating_set.count()


    def __str__(self):
        return f'{self.movie_name}'



class MovieLanguages(models.Model):
    language = models.CharField(max_length=32)
    video = models.FileField(upload_to='movie_languages/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.language

class Moments(models.Model):
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
  movie_moments = models.FileField(upload_to='movie_moments/')

class Rating(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)], null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} → {self.movie.movie_name}'


class Favorite(models.Model):
    user =  models.OneToOneField(Profile, on_delete=models.CASCADE)


class FavoriteMovie(models.Model):
    cart = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class History(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

