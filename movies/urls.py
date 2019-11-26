"""cinesafari URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('datasave/', views.datasave, name="datasave"),
    path('boxoffice_create/', views.boxoffice_create, name="boxoffice_create"),
    path('boxoffice/', views.boxoffice, name="boxoffice"),
    
    path('reviews/', views.reviews, name="reviews"),
    path('review_create/', views.review_create, name="review_create"),
    path('review_update/', views.review_update, name="review_update"),
    path('review_delete/', views.review_delete, name="review_delete"),
    path('user_reviews/', views.user_reviews, name="user_reviews"),

    path('signup/', views.signup, name="signup"),
]
