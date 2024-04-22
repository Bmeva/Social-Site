from django.shortcuts import render, redirect
from .models import Post
from django.utils.text import slugify
import random
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Comment
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('Register')# i can use this querry instead of using login required decorator. Register is the url that has the Loginpage as well
    #posts = Post.objects.all() this would display all post but we used a filter below to show active post and visibility is set to everyone
    posts = Post.objects.filter(active=True, visibility='Everyone').order_by("-id")

   
    context = {
        'posts': posts,
    }
    return render(request, 'Core/index.html', context)

@csrf_exempt
def create_post(request):
    if request.method =='POST':
        
        title = request.POST.get('title')
        visibility = request.POST.get('visibility')
        image_thumb = request.FILES.get('image_thumb')
        getrandom = random.randint(1000, 9999)

        if title and image_thumb:
            post = Post(
                title = title,
                image = image_thumb,
                visibility = visibility,
                user = request.user,
                slug = slugify(title[:4]) + '-' + str(getrandom)
            )
            post.save()

            return JsonResponse({
                'data': 'sent',
                'post': { 
                'title': post.title,
                'image': post.image.url,
                'full_name': post.user.profile.image.url,
                'date': timesince(post.date),
                'id': post.id,

            }})
        
        else:
            return JsonResponse({'Error': 'image or title does not exist'})
    else:

        return JsonResponse({'status': 'Failed', 'message': 'Invalid request'})
        


def lke_post(request):
    
    id = request.GET['id'] #get the id of the post but we got it through the js code
    post = Post.objects.get(id = id)
    user = request.user
    thebool = False

    if user in post.likes.all():
        post.likes.remove(user)
        thebool = False
    else:
        post.likes.add(user)
        thebool = True
    
    likes = post.likes.all().count()

    data = {
        'thebool': thebool,
        'likes': likes,

    }
    return JsonResponse({'data': data})


def comment_on_post(request):
    id = request.GET['id']
    comment = request.GET['comment']
    post = Post.objects.get(id = id)
    comment_count = Comment.objects.filter(post=post).count()
    user = request.user

    new_comment = Comment.objects.create(
        post = post,
        comment = comment,
        user = user
    )
    data = {
        'bool': True,
        'comment': new_comment.comment,
        'profile_image': new_comment.user.profile.image.url,
        'date': timesince(new_comment.date),
        'comment_id': new_comment.id,
        'post_id': new_comment.post.id,
        'comment_count':comment_count + int(1)

    }
    return JsonResponse({'data': data})


   