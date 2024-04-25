from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    path('post_details<slug:slug>/', views.post_details, name='post_details'),

     #Ajax url 
    path('create_post/', views.create_post, name='create_post'),

    path('lke_post/', views.lke_post, name='lke_post'),

    path('comment_on_post/', views.comment_on_post, name='comment_on_post'),

    path('like_comment/', views.like_comment, name='like_comment'),

    
    path('reply_comment/', views.reply_comment, name='reply_comment'),

    path('deleteComment/', views.deleteComment, name='deleteComment'),

    path('deleteCommentReply/', views.deleteCommentReply, name='deleteCommentReply'),
    
    path('addFriend/', views.addFriend, name='addFriend'),

    

    


   

    



    




    
]

