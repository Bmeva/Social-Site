from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('inbox', views.inbox, name='inbox'),


    path('inbox_detail/<username>/', views.inbox_detail, name='inbox_detail'),

     path('testing', views.testing, name='testing'),

   

    #path('post_details<slug:slug>/', views.post_details, name='post_details'),

]    

