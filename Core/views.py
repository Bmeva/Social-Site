from django.shortcuts import render, redirect
from .models import Post
from django.utils.text import slugify
import random
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Comment, ReplyComment
from Core.models import User, Friend, FriendRequest
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


@login_required(login_url='Register')
def post_details(request, slug): #we want to get the details of a single ppost
    post = Post.objects.get(slug=slug, active=True, visibility='Everyone')

    context = {
        'p': post,
    }
    return render(request, 'Core/post_details.html', context)



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
                "full_name":post.user.profile.full_name,
                'date': timesince(post.date),
                'id': post.id,
                "profile_image":post.user.profile.image.url,

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



def like_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False 

    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool = True 

       
    data = {
        "bool":bool,
        'likes':comment.likes.all().count()
    }
    return JsonResponse({"data":data})



#REPLY COMMENT
def reply_comment(request):

    id = request.GET['id']
    reply = request.GET['reply']

    comment = Comment.objects.get(id=id)
    user = request.user

    new_reply = ReplyComment.objects.create(
        comment=comment,
        reply=reply,
        user=user
    )

    
    data = {
        "bool":True,
        'reply':new_reply.reply,
        "profile_image":new_reply.user.profile.image.url,
        "date":timesince(new_reply.date),
        "reply_id":new_reply.id,
        "post_id":new_reply.comment.post.id,
        
    }
    return JsonResponse({"data":data})


def deleteComment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    comment.delete()
    data = {
        'bool': True
    }
    return JsonResponse({'data': data})



def deleteCommentReply(request):
    id = request.GET['id']
    comment = ReplyComment.objects.get(id=id)
    comment.delete()
    data = {
        'bool': True
    }
    return JsonResponse({'data': data})


def addFriend(request):
    sender = request.user
    receiver_id = request.GET['id']
    bool = False

    if sender.id == int(receiver_id):
        return JsonResponse({'Error': 'You cabt send friend request to yourself'})
    receiver = User.objects.get(id = receiver_id)

    try:
        friend_request = FriendRequest.objects.get(sender=sender, receiver = receiver)
        if friend_request:
            friend_request.delete()
        bool = False
        return JsonResponse({'Error': 'Friend request has been cancealed', 'bool': bool})
    except FriendRequest.DoesNotExist:
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        bool = True
        return JsonResponse({'Success': 'Sent', 'bool': bool})