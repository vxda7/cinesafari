from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class Director(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name



class Genre(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name


class Movie(models.Model):    
    title = models.CharField(max_length = 200)
    image = models.CharField(max_length = 300, default="")
    subtitle = models.CharField(max_length = 300, default="")
    pubDate = models.IntegerField(default=0)
    userRating = models.FloatField(default=0)
    showTm = models.IntegerField(default=0)
    watchGrade = models.CharField(max_length=100, default="")
    descript_point = models.TextField(default="")
    description = models.TextField(default="")
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    directors = models.ManyToManyField(Director, related_name="movies")
    like_users = models.ManyToManyField(get_user_model(), related_name="like_movies")
    boxoffice = models.IntegerField(default=0)
    def __str__(self):
        return self.title


class Review(models.Model):
    content = models.TextField(default="")
    score = models.IntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    def __str__(self):
        return self.movie.title