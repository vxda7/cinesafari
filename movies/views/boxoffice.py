from django.shortcuts import render, get_object_or_404
import json, os, requests
from decouple import config
from datetime import datetime, timedelta
from ..serializers import GenreSerializer, DirectorSerializer, MovieSerializer, ActorSerializer, UserSerializer, CreateUserSerializer, ReviewSerializer
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models import Movie, Genre, Director, Actor, Review
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from bs4 import BeautifulSoup
import urllib.request
from accounts.models import User

# 박스오피스 데이터 api에서 모아서 저장하기
@api_view(['GET'])
@permission_classes((AllowAny,))
def boxoffice_create(request):
    for i in range(3, 100):
        now = datetime.now() + timedelta(weeks=-i)
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

        # 유튜브 데이터
        GOOGLE_KEY = config('GOOGLE_KEY')
        GOOGLE_URL = f"https://www.googleapis.com/youtube/v3/search?key={GOOGLE_KEY}&part=snippet&type=video&q="
        ########################################################## 수정
        movie_detail_datas = []
        imageurls = []
        naver_scores = []
        rank = []
        watchgrades = []
        showtimes = []
        descriptions = []
        videos = []
        descript_points = []
        thumbnails = []
        directors = set()
        actors = set()
        genres = set()
        idx = 0
        for movie_data in movie_datas['boxOfficeResult']['weeklyBoxOfficeList']:
            movie_name = movie_data['movieNm']
            what = False
            try:
                Movie.objects.get(title=movie_name)
                what = True
                pass
            except:

                naver_data = requests.get(f'{NAVER_URL}?query={movie_name}', headers=headers).json()
                movie_code = movie_data['movieCd']
                movie_detail_data = requests.get(f'{DETAIL_URL}?key={MOVIE_KEY}&movieCd={movie_code}').json()
                movie_detail_datas.append(movie_detail_data)
                if i == 1:
                    rank.append(movie_data['rank'])
                else:
                    rank.append(0)
                if 'audits' in movie_detail_data['movieInfoResult']['movieInfo']:
                    if movie_detail_data['movieInfoResult']['movieInfo']['audits']:
                        watchgrades.append(movie_detail_data['movieInfoResult']['movieInfo']['audits'][0]['watchGradeNm'])
                    else:
                        watchgrades.append("")    
                else:
                    watchgrades.append("")
                if 'showTm' in movie_detail_data['movieInfoResult']['movieInfo']:
                    if movie_detail_data['movieInfoResult']['movieInfo']['showTm'] == "":
                        showtimes.append(0)
                    else:
                        showtimes.append(movie_detail_data['movieInfoResult']['movieInfo']['showTm'])
                else:
                    showtimes.append(0)
                if 'items' in naver_data:
                    if naver_data['items']:
                        if 'userRating' in naver_data['items'][0]:
                            naver_score = naver_data['items'][0]['userRating']
                        else:
                            naver_score = 0
                    else:
                        naver_score = 0
                    # 이미지 가져오기
                    stackcode = []
                    if naver_data['items']:
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

                    # 스토리 가져오기
                    descript_url = "https://movie.naver.com/movie/bi/mi/basic.nhn?code=" + image_code
                    html = urllib.request.urlopen(descript_url)
                    source = html.read()
                    soup = BeautifulSoup(source, "html.parser")
                    descript = soup.find("p", {"class": "con_tx"})
                    if descript:
                        temp = descript.text
                        temp = temp.replace('\r', '')
                        temp = temp.replace('\xa0', '')
                        descriptions.append(temp)
                    else:
                        descriptions.append("no descript")
                    # 한줄스토리 가져오기
                    descript_point = soup.find("h5", {"class":"h_tx_story"})
                    if descript_point:
                        temp = descript_point.text
                        temp = temp.replace('\r', '')
                        temp = temp.replace('\xa0', '')
                        descript_points.append(temp)
                    else:
                        descript_points.append("no descript_point")    
                else:
                    naver_score = 0
                    imageurls.append("nosrc")
                    descriptions.append("no descript")
                    descript_points.append("no descript_point")
                naver_scores.append(naver_score)

                if len(naver_data['items']) > 0:
                    image_data = naver_data['items'][0]['image']
                    movie_datas['boxOfficeResult']['weeklyBoxOfficeList'][idx]['image'] = image_data
                
                # 비디오 정보 가져오기 + 썸네일
                video_datas = requests.get(f"{GOOGLE_URL}{movie_name}예고편").json()
                if 'items' in video_datas:
                    videos.append(video_datas['items'][0]['id']['videoId'])
                    thumbnails.append(video_datas['items'][0]['snippet']['thumbnails']['high']['url'])
                else:
                    videos.append("")
                    thumbnails.append("")


                # 영화감독, 배우 추가            
                if movie_detail_data['movieInfoResult']['movieInfo']['directors']:
                    for one in movie_detail_data['movieInfoResult']['movieInfo']['directors']:
                        directors.add(one['peopleNm'])
                if movie_detail_data['movieInfoResult']['movieInfo']['actors']:
                    for one in movie_detail_data['movieInfoResult']['movieInfo']['actors']:
                        actors.add(one['peopleNm'])
                if movie_detail_data['movieInfoResult']['movieInfo']['genres']:
                    for one in movie_detail_data['movieInfoResult']['movieInfo']['genres']:
                        genres.add(one['genreNm'])
                idx += 1
            if what:
                pass
            else:
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
                    if pubDate == "":
                        pubDate=0
                    userRating = naver_scores[idx]
                    boxoffice = rank[idx]
                    watchGrade = watchgrades[idx]
                    description = descriptions[idx]
                    descript_point = descript_points[idx]
                    showTm = showtimes[idx]
                    video = videos[idx]
                    thumbnail = thumbnails[idx]
                    movie = Movie.objects.get_or_create(title=title, image=image, subtitle=subtitle, pubDate=pubDate, userRating=userRating, boxoffice=boxoffice, 
                    watchGrade=watchGrade, showTm=showTm, description=description, descript_point=descript_point, video=video, thumbnail=thumbnail)[0]
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