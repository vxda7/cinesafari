from rest_framework import serializers
from .models import Movie, Genre, Director, Actor
from django.contrib.auth import get_user_model
from accounts.models import User
from django.contrib.auth import authenticate

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
        model = User
        fields = ('username', 'password',)


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    directors = DirectorSerializer(many=True)
    actors = ActorSerializer(many=True)
    class Meta:
        model = Movie
        fields = ('title', 'image', 'subtitle', 'pubDate', 'userRating','watchGrade', 'showTm', 'boxoffice', 'genres', 'actors', 'directors', 'descript_point', 'description')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user