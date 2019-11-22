from rest_framework import serializers
from .models import Movie, Genre, Director, Actor
from django.contrib.auth import get_user_model

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name')


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('name')


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('name')


class MovieSerializer(serializers.ModelSerializer):
    director_set = GenreSerializer(many=True)
    actor_set = ActorSerializer(many=True)
    class Meta:
        model = Movie
        fields = ('id', 'title', 'link', 'image', 'subtitle', 'pubDate', 'userRating', )

class UserSerializer(serializers.ModelSerializer):
    movie_set = MovieSerializer(many=True)
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'movie_set',)