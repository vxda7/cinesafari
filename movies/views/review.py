from django.shortcuts import render, get_object_or_404
from ..serializers import GenreSerializer, DirectorSerializer, MovieSerializer, ActorSerializer, UserSerializer, CreateUserSerializer, ReviewSerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models import Movie, Genre, Director, Actor, Review
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from accounts.models import User


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def review_create(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse({"msg":"저장이 완료되었습니다"})


@api_view(['GET'])
@permission_classes((AllowAny,))
def reviews(request, id):
    reviewdatas = list(Review.objects.filter(movie_id=id).values())
    for reviewdata in reviewdatas:
        reviewdata['username'] = User.objects.get(id=reviewdata['user_id']).username
        reviewdata['moviename'] = Movie.objects.get(id=reviewdata['movie_id']).title
    return JsonResponse(reviewdatas, safe=False)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def review_update(request, id):
    content = request.data['content']
    score = request.data['score']
    review = Review.objects.get(id=id)
    review.content = content
    review.score = score
    review.save()
    return JsonResponse({"msg":"수정이 완료되었습니다."})


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def review_delete(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return JsonResponse({"msg":"삭제가 완료되었습니다."})


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes((JSONWebTokenAuthentication,))
def user_reviews(request, id):
    reviewdatas = list(Review.objects.filter(user_id=id).values())
    for reviewdata in reviewdatas:
        reviewdata['username'] = User.objects.get(id=reviewdata['user_id']).username
        reviewdata['moviename'] = Movie.objects.get(id=reviewdata['movie_id']).title
    return JsonResponse(reviewdatas, safe=False)