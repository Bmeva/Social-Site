from .models import FriendRequest, Notification



def my_context_processor(request):

    try:
        friend_request = FriendRequest.objects.filter(receiver=request.user).order_by('-id')
    except:
        friend_request = None
    
    try:
        notification = Notification.objects.filter(user=request.user).order_by('-id')
    except:
        notification = None

    return {

        "friend_request": friend_request,
        
        "notification": notification, 

    }


