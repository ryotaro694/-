from django.conf.urls import url
from django.urls import path
from . import views,api

urlpatterns = [
    path('',views.login,name='login'),
    path('kousei',views.kousei,name='kousei'),
    path('register',views.register,name='register'),
    path('sentence',views.sentence,name='sentence'),
]