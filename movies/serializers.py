from rest_framework import serializers
from .models import Movie, Genre, Director, Actor, Review
from django.contrib.auth import get_user_model
from accounts.models import User
from django.contrib.auth import authenticate

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name',)


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('id', 'name',)


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'name',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    directors = DirectorSerializer(many=True)
    actors = ActorSerializer(many=True)
    class Meta:
        model = Movie
        fields = ('id', 'title', 'image', 'subtitle', 'pubDate', 'userRating','watchGrade', 'showTm', 'boxoffice', 'genres', 'actors', 'directors', 'descript_point', 'description', 'video')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "content", "score", "user", "movie")