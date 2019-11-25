from rest_framework import serializers
from .models import Movie, Genre, Director, Actor
from django.contrib.auth import get_user_model

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('name',)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password',)


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    directors = DirectorSerializer(many=True)
    actors = ActorSerializer(many=True)
    # like_users = UserSerializer(many=True)
    class Meta:
        model = Movie
        fields = ('title', 'image', 'subtitle', 'pubDate', 'userRating','watchGrade', 'showTm', 'boxoffice', 'genres', 'actors', 'directors', )

