from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('Register', views.Register, name='Register'),

    path('mylogin', views.mylogin, name='mylogin'),
    
    path('mylogout', views.mylogout, name='mylogout'),

    path('Myprofile', views.Myprofile, name='Myprofile'),

    path('MyFriendprofile/<username>', views.MyFriendprofile, name='MyFriendprofile'),

    



    

  
    
]

