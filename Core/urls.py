from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    #Ajax url 
    path('create_post/', views.create_post, name='create_post'),

    path('lke_post/', views.lke_post, name='lke_post'),

    path('comment_on_post/', views.comment_on_post, name='comment_on_post'),

    



    




    
]

