from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('inbox', views.inbox, name='inbox'),

    #path('post_details<slug:slug>/', views.post_details, name='post_details'),

]    

