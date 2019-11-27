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
    path('datasave/', views.datasave),
    path('boxoffice_create/', views.boxoffice_create),
    path('boxoffice/', views.boxoffice),
    
    path('reviews/<int:id>/', views.reviews),
    path('review-create/', views.review_create),
    path('review-update/<int:id>/', views.review_update),
    path('review-delete/<int:id>/', views.review_delete),
    path('user-reviews/<int:id>/', views.user_reviews),

    path('signup/', views.signup),
    path('recommand/<int:id>/', views.recommand)
]
