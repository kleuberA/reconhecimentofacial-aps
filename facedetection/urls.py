from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name = "home"),
    path('login/',login,name = 'login'),
    path('greeting/<id_usuario>/',Greeting,name='greeting'),
    path('acessoniveldois/',acessoniveldois,name = 'acessoniveldois'),
    path('acessoniveltres/',acessoniveltres,name = 'acessoniveltres'),
]