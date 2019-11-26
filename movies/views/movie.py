from django.shortcuts import render, get_object_or_404
import json, os, requests
from ..serializers import GenreSerializer, DirectorSerializer, MovieSerializer, ActorSerializer, UserSerializer, CreateUserSerializer, ReviewSerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models import Movie, Genre, Director, Actor, Review
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from accounts.models import User




# 저장된 박스오피스 불러내주기
@api_view(['GET'])
@permission_classes((AllowAny,))
def boxoffice(request):
    boxoffice = Movie.objects.filter(boxoffice__gte=1)   # rank가 1 이상인 사람
    serializer = MovieSerializer(boxoffice, many=True)
    return JsonResponse(serializer.data, safe=False)


# 저장된 영화 정보 불러내주기
@api_view(['GET'])
@permission_classes((AllowAny,))
def moviedata(request):
    moviedatas = list(Movie.objects.values())
    return JsonResponse(moviedatas, safe=False)



@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return JsonResponse({"user": UserSerializer(user).data})