from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('post_details<slug:slug>/', views.post_details, name='post_details'),

     #Ajax url 
    path('create_post/', views.create_post, name='create_post'),

    path('like_post/', views.like_post, name='like_post'),

    path('comment_on_post/', views.comment_on_post, name='comment_on_post'),

    path('like_comment/', views.like_comment, name='like_comment'),

    
    path('reply_comment/', views.reply_comment, name='reply_comment'),

    path('deleteComment/', views.deleteComment, name='deleteComment'),

    path('deleteCommentReply/', views.deleteCommentReply, name='deleteCommentReply'),
    
    path('addFriend/', views.addFriend, name='addFriend'),

    path('accept_friend_request/', views.accept_friend_request, name='accept_friend_request'),

    path('reject_friend_request/', views.reject_friend_request, name='reject_friend_request'),


    path('unfriend/', views.unfriend, name='unfriend'),


    
]

