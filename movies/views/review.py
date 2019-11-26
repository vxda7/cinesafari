from django.shortcuts import render, get_object_or_404
from ..serializers import GenreSerializer, DirectorSerializer, MovieSerializer, ActorSerializer, UserSerializer, CreateUserSerializer, ReviewSerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import Movie, Genre, Director, Actor, Review
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from accounts.models import User



@api_view(['POST'])
@permission_classes((AllowAny,))
def review_create(request):
    serializer = ReviewSerializer(data=request.data)
    # reviews = Review.objects.filter(movie=request.movieid)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse({"msg":"저장이 완료되었습니다"})


@api_view(['POST'])
@permission_classes((AllowAny,))
def reviews(request):
    movieid = request.data["movie"]
    reviewdatas = list(Review.objects.filter(movie_id=movieid).values())
    return JsonResponse(reviewdatas, safe=False)


@api_view(['PUT'])
@permission_classes((AllowAny,))
def review_update(request):
    reviewid = request.data['id']
    content = request.data['content']
    score = request.data['score']
    review = Review.objects.get(id=reviewid)
    review.content = content
    review.score = score
    review.save()
    return JsonResponse({"msg":"수정이 완료되었습니다."})


@api_view(['DELETE'])
@permission_classes((AllowAny,))
def review_delete(request):
    reviewid = request.data['id']
    review = Review.objects.get(id=reviewid)
    review.delete()
    return JsonResponse({"msg":"삭제가 완료되었습니다."})


@api_view(['POST'])
@permission_classes((AllowAny,))
def user_reviews(request):
    userid = request.data['userid']
    reviewdatas = list(Review.objects.filter(user_id=userid).values())
    return JsonResponse(reviewdatas, safe=False)