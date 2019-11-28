from accounts.models import User
from ..models import Movie, Genre, Director, Review, Actor
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.db.models import Q
import operator
from django.forms.models import model_to_dict
import json
from django.core import serializers
from ..serializers import MovieSerializer, GenreSerializer
@api_view(['GET'])
@permission_classes((AllowAny,))
def recommand(request, id):
    if id == 0:
        user = User.object.get(id=1)
    else:
        user = User.objects.get(id=id)
    # 처음온 사람이 아니면
    # 리뷰를 쓴 갯수 확인
    reviews = user.review_set
    if reviews.count():
        # 유저가 쓴 리뷰들 모아오기
        reviews = Review.objects.filter(user_id=id)
        like_reviews = []
        for review in reviews:
            if review.score > 6:
                like_reviews.append(review)
        movie_ids = list(map(lambda x:x.movie_id, like_reviews))
        # 유저가 본 좋아하던 영화들 모아오기
        movies = Movie.objects.filter(id__in=movie_ids)
        # 본 영화 모으기
        every_ids = list(map(lambda x:x.movie_id, reviews))
        every_movies = Movie.objects.filter(id__in=every_ids)
        # 유저가 좋아하는 장르 뽑기
        genres = {} # id: 장르점수
        for movie in movies:
            for genre in movie.genres.all(): 
                if genre in genres:
                    genres[genre] += 1
                else:
                    genres[genre] = 1

        # 순서대로 나열해서 가중치대로 나열하기 내림차순
        sortedgenres = sorted(genres.items(), key=operator.itemgetter(1), reverse=True)
        #  가장 좋아하는 장르 3가지가 있는 영화 추천
        removies = []
        for i in range(3):
            if sortedgenres:
                one = sortedgenres.pop(0)
                movies = Movie.objects.filter(genres=one[0]).filter(~Q(id__in=every_movies))[:10]
                removies.extend(movies)
        serializers = MovieSerializer(removies, many=True)
        return JsonResponse(serializers.data, safe=False)
        
    # 좋은 리뷰가 많은 순으로 추천
    else:
        reviews = Review.objects.all()
        like_reviews = []
        for review in reviews:
            if review.score > 6:
                like_reviews.append(review)
        movie_ids = list(map(lambda x:x.movie_id, like_reviews))

        # 유저들이 본 좋아하던 영화들 모아오기
        movies = Movie.objects.filter(id__in=movie_ids)[:10]
        return JsonResponse(movies.json(), safe=False)



@api_view(['GET'])
@permission_classes((AllowAny,))
def similar(request, id):
    movie = Movie.objects.get(id=id)
    # 영화의 장르들 모으기
    genres = []
    for genre in movie.genres.all():
        genres.append(genre)
    # 같은 장르의 영화들 모으기
    movies = Movie.objects.filter(genres__in=genres).filter(~Q(id=id))
    serializers = MovieSerializer(movies, many=True)
    return JsonResponse(serializers.data, safe=False)



@api_view(['GET'])
@permission_classes((AllowAny,))
def search(request, query, choose):
    # 검색어로 검색
    if choose == 0:
        movies = Movie.objects.filter(title__contain=query)
        serializers = MovieSerializer(movies, many=True)
        return JsonResponse(serializers.data, safe=False)
    # 장르별로 검색
    else:
        movies = Movie.objects.filter(genres__in=choose)
        serializers = MovieSerializer(movies, many=True)
        return JsonResponse(serializers.data, safe=False)
