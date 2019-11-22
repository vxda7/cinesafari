from django.shortcuts import render, get_object_or_404
import json
import requests
from decouple import config
from datetime import datetime, timedelta
from .serializers import GenreSerializer, DirectorSerializer, MovieSerializer, ActorSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Movie, Genre, Director, Actor
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from bs4 import BeautifulSoup
import urllib.request

# Create your views here.

# 영화들 데이터 저장하기
@api_view(['GET'])
@permission_classes((AllowAny,))
def datasave(request):
    # 영진위
    thisyear = datetime.now().year
    MOVIE_KEY = config('MOVIE_KEY')
    BASIC_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
    DETAIL_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
    MOVIE_URL = f'{BASIC_URL}?key={MOVIE_KEY}&openStartDt=2019&openEndDt={thisyear}&itemPerPage=100'
    # 영화 데이터 갯수 --------------------------------------------------------------------------↑
    movie_datas = requests.get(MOVIE_URL).json()

    # 네이버 데이터
    NAVER_ID = config('NAVER_ID')
    NAVER_SECRET = config('NAVER_KEY')
    NAVER_URL = 'https://openapi.naver.com/v1/search/movie.json'
    
    headers = {
        'X-Naver-Client-Id': NAVER_ID,
        'X-Naver-Client-Secret': NAVER_SECRET,
    }
    
    # 데이터 통합
    movie_detail_datas = []
    imageurls = []
    naver_scores = []
    directors = set()
    actors = set()
    genres = set()
    idx = 0
    for movie_data in movie_datas['movieListResult']['movieList']:
        movie_name = movie_data['movieNm']
        naver_data = requests.get(f'{NAVER_URL}?query={movie_name}', headers=headers).json()
        movie_code = movie_data['movieCd']
        movie_detail_data = requests.get(f'{DETAIL_URL}?key={MOVIE_KEY}&movieCd={movie_code}').json()
        movie_detail_datas.append(movie_detail_data)

        if naver_data['items']:
            naver_score = naver_data['items'][0]['userRating']
            # 이미지 가져오기
            stackcode = []
            image_code = naver_data['items'][0]['link']
            for j in range(len(image_code)-1, -1, -1):
                if image_code[j] == '=':
                    break
                else:
                    stackcode.insert(0, image_code[j])
            image_code = ''.join(stackcode)
            image_detail = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='
            img_url = image_detail + image_code
            html = urllib.request.urlopen(img_url)
            source = html.read()
            soup = BeautifulSoup(source, "html.parser")
            img = soup.find("img")
            if img:
                img_src = img.get("src")
                imageurls.append(img_src)
            else:
                imageurls.append("")
        else:
            naver_score = 0
            imageurls.append("nosrc")
        naver_scores.append(naver_score)
        # movie_datas['movieListResult']['movieList'][idx]['userRating'] = naver_score
        if len(naver_data['items']) > 0:
            image_data = naver_data['items'][0]['image']
            movie_datas['movieListResult']['movieList'][idx]['image'] = image_data
        # 영화감독, 배우 추가            
        if movie_data['directors']:
            for one in movie_data['directors']:
                directors.add(one['peopleNm'])
        if movie_detail_data['movieInfoResult']['movieInfo']['actors']:
            for one in movie_detail_data['movieInfoResult']['movieInfo']['actors']:
                actors.add(one['peopleNm'])
        if movie_detail_data['movieInfoResult']['movieInfo']['genres']:
            for one in movie_detail_data['movieInfoResult']['movieInfo']['genres']:
                genres.add(one['genreNm'])
        idx += 1

    for one in actors:
        Actor.objects.get_or_create(name=one)
    for one in directors:
        Director.objects.get_or_create(name=one)
    for one in genres:
        Genre.objects.get_or_create(name=one)
    idx = 0
    for one in movie_detail_datas:
        title = one['movieInfoResult']['movieInfo']['movieNm']
        image = imageurls[idx]
        subtitle = one['movieInfoResult']['movieInfo']['movieNmEn']
        pubDate = one['movieInfoResult']['movieInfo']['openDt']
        userRating = naver_scores[idx]
        genres_list = []
        directors = []
        actors = []
        movie = Movie.objects.get_or_create(title=title, image=image, subtitle=subtitle, pubDate=pubDate, userRating=userRating)[0]
        for genre in one['movieInfoResult']['movieInfo']['genres']:
            genreinstance = Genre.objects.get(name=genre['genreNm'])
            movie.genres.add(genreinstance)
        for director in one['movieInfoResult']['movieInfo']['directors']:
            directorinstance = Director.objects.get(name=director['peopleNm'])
            movie.directors.add(directorinstance)
        for actor in one['movieInfoResult']['movieInfo']['actors']:
            actorinstance = Actor.objects.get(name=actor['peopleNm'])
            movie.actors.add(actorinstance)
        idx += 1
    

    moviedatas = list(Movie.objects.values())
    return JsonResponse(moviedatas, safe=False)

    # context = {
    #     'MOVIE_URL': MOVIE_URL,
    #     'movie_datas' : movie_datas,
    #     'directors': directors,
    #     'actors': actors,
    #     'movie_detail_datas': movie_detail_datas,
    # }
    # return render(request, 'index.html', context)


# 박스오피스 데이터 api에서 모아서 저장하기
@api_view(['GET'])
@permission_classes((AllowAny,))
def boxoffice_create(request):
    now = datetime.now() + timedelta(days=-7)
    today = now.strftime('%Y%m%d')
    MOVIE_KEY = config('MOVIE_KEY')
    BASIC_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json'
    DETAIL_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
    MOVIE_URL = f'{BASIC_URL}?key={MOVIE_KEY}&targetDt={today}'
    movie_datas = requests.get(MOVIE_URL).json()

    # 네이버
    NAVER_ID = config('NAVER_ID')
    NAVER_SECRET = config('NAVER_KEY')
    NAVER_URL = 'https://openapi.naver.com/v1/search/movie.json'

    headers = {
        'X-Naver-Client-Id': NAVER_ID,
        'X-Naver-Client-Secret': NAVER_SECRET,
    }
    print(movie_datas)
    raise
    ########################################################## 수정
    movie_detail_datas = []
    imageurls = []
    naver_scores = []
    directors = set()
    actors = set()
    genres = set()
    idx = 0
    for movie_data in movie_datas['movieListResult']['weeklyBoxOfficeList']:
        movie_name = movie_data['movieNm']
        naver_data = requests.get(f'{NAVER_URL}?query={movie_name}', headers=headers).json()
        movie_code = movie_data['movieCd']
        movie_detail_data = requests.get(f'{DETAIL_URL}?key={MOVIE_KEY}&movieCd={movie_code}').json()
        movie_detail_datas.append(movie_detail_data)

        if naver_data['items']:
            naver_score = naver_data['items'][0]['userRating']
            # 이미지 가져오기
            stackcode = []
            image_code = naver_data['items'][0]['link']
            for j in range(len(image_code)-1, -1, -1):
                if image_code[j] == '=':
                    break
                else:
                    stackcode.insert(0, image_code[j])
            image_code = ''.join(stackcode)
            image_detail = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='
            img_url = image_detail + image_code
            html = urllib.request.urlopen(img_url)
            source = html.read()
            soup = BeautifulSoup(source, "html.parser")
            img = soup.find("img")
            if img:
                img_src = img.get("src")
                imageurls.append(img_src)
            else:
                imageurls.append("")
        else:
            naver_score = 0
            imageurls.append("nosrc")
        naver_scores.append(naver_score)
        # movie_datas['movieListResult']['movieList'][idx]['userRating'] = naver_score
        if len(naver_data['items']) > 0:
            image_data = naver_data['items'][0]['image']
            movie_datas['movieListResult']['weeklyBoxOfficeList'][idx]['image'] = image_data
        # 영화감독, 배우 추가            
        if movie_data['directors']:
            for one in movie_data['directors']:
                directors.add(one['peopleNm'])
        if movie_detail_data['movieInfoResult']['movieInfo']['actors']:
            for one in movie_detail_data['movieInfoResult']['movieInfo']['actors']:
                actors.add(one['peopleNm'])
        if movie_detail_data['movieInfoResult']['movieInfo']['genres']:
            for one in movie_detail_data['movieInfoResult']['movieInfo']['genres']:
                genres.add(one['genreNm'])
        idx += 1

    for one in actors:
        Actor.objects.get_or_create(name=one)
    for one in directors:
        Director.objects.get_or_create(name=one)
    for one in genres:
        Genre.objects.get_or_create(name=one)
    idx = 0
    for one in movie_detail_datas:
        title = one['movieInfoResult']['movieInfo']['movieNm']
        image = imageurls[idx]
        subtitle = one['movieInfoResult']['movieInfo']['movieNmEn']
        pubDate = one['movieInfoResult']['movieInfo']['openDt']
        userRating = naver_scores[idx]
        boxoffice = one['rank']
        genres_list = []
        directors = []
        actors = []
        
        movie = Movie.objects.get_or_create(title=title, image=image, subtitle=subtitle, pubDate=pubDate, userRating=userRating)[0]
        for genre in one['movieInfoResult']['movieInfo']['genres']:
            genreinstance = Genre.objects.get(name=genre['genreNm'])
            movie.genres.add(genreinstance)
        for director in one['movieInfoResult']['movieInfo']['directors']:
            directorinstance = Director.objects.get(name=director['peopleNm'])
            movie.directors.add(directorinstance)
        for actor in one['movieInfoResult']['movieInfo']['actors']:
            actorinstance = Actor.objects.get(name=actor['peopleNm'])
            movie.actors.add(actorinstance)
        idx += 1
    

    moviedatas = list(Movie.objects.values())
    return JsonResponse(moviedatas, safe=False)



    # # 이미지 붙여넣기
    # for i in range(len(movie_datas['boxOfficeResult']['weeklyBoxOfficeList'])):
    #     movie_name = movie_datas['boxOfficeResult']['weeklyBoxOfficeList'][i]["movieNm"]
    #     naver_data = requests.get(f'{NAVER_URL}?query={movie_name}', headers=headers).json()
    #     # return JsonResponse(naver_data)
    #     if naver_data['items']:
    #         stackcode = []
    #         image_code = naver_data['items'][0]['link']
    #         for j in range(len(image_code)-1, -1, -1):
    #             if image_code[j] == '=':
    #                 break
    #             else:
    #                 stackcode.insert(0, image_code[j])
    #         image_code = ''.join(stackcode)
    #         image_detail = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='
    #         img_url = image_detail + image_code
    #         html = urllib.request.urlopen(img_url)
    #         source = html.read()
    #         soup = BeautifulSoup(source, "html.parser")
    #         img = soup.find("img")
    #         img_src = img.get("src")
    #         # movie_datas['boxOfficeResult']['weeklyBoxOfficeList'][i]['image'] = image_detail + image_code
    #         movie_datas['boxOfficeResult']['weeklyBoxOfficeList'][i]['image'] = img_src

    #     else:
    #         movie_datas['boxOfficeResult']['weeklyBoxOfficeList'][i]['image'] = ""
        
    #     # model에 저장하기
    #     movieNm = movie_name
    #     audiAcc = movie_datas['boxOfficeResult']['weeklyBoxOfficeList'][i]["audiAcc"]
    #     openDt = movie_datas['boxOfficeResult']['weeklyBoxOfficeList'][i]["audiAcc"]
    #     image = img_src
    #     Boxoffice.objects.get_or_create(movieNm=movieNm, audiAcc=audiAcc, openDt=openDt, image=image)
    # return JsonResponse(movie_datas)



# 저장된 박스오피스 불러내주기
@api_view(['GET'])
@permission_classes((AllowAny,))
def boxoffice(request):
    boxoffices = list(Boxoffice.objects.values())
    return JsonResponse(boxoffices, safe=False)


# 저장된 영화 정보 불러내주기
@api_view(['GET'])
@permission_classes((AllowAny,))
def moviedata(request):
    moviedatas = list(Movie.objects.values())
    return JsonResponse(moviedatas, safe=False)


# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(request.POST)
#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse(serializer.data)
#     return HttpResponse(status=400)

def reviews(request):
    
    reviews = Review.query.filter_by().all()