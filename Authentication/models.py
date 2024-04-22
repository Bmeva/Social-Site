from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from .utils import ShortUUIDField
import random
import string
from django.utils.text import slugify
from django.db.models.signals import post_save #to authomatically create a user profile when a user is created
#from django.dispatch import receiver
#from django.db.models.signals import post_save, pre_delete

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return 'user_{0}/{1}'.format(instance.user.id,  filename)
    

# Create your models here.
GENDER = (
    ('female', 'female'),
    ('male', 'male')
)

class User(AbstractUser):
    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=GENDER)
    opt = models.CharField(max_length=10, null=True, blank= True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    #ordering = ['full_name']
    

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


RELATIONSHIP = (
    ('single', 'single'),
    ('married', 'married'),
    ('divorced', 'divorced'),
)   

WHO_CAN_SEE_MY_FRIENDS = (
    ("Only Me","Only Me"),
    ("Everyone","Everyone"),
)
    

random_alphabets = ''.join(random.choices(string.ascii_uppercase, k=5))

class Profile(models.Model):
    pid = ShortUUIDField(max_length=37) # this file is in the utils.py
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank = True, null = True )
    cover_image = models.ImageField(upload_to=user_directory_path, default="cover.jpg", blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    about_me = models.CharField( max_length=1000,null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True, blank=True)
    relationship = models.CharField(max_length=100, choices=RELATIONSHIP, null=True, blank=True, default="single")
    friends_visibility = models.CharField(max_length=100, choices=WHO_CAN_SEE_MY_FRIENDS, null=True, blank=True, default="Everyone")
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    working_at = models.CharField(max_length=1000, null=True, blank=True)
    instagram = models.URLField(default="https://instagram.com/", null=True, blank=True)
    whatsApp = models.CharField(default="+44 (707) 234", max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    followings = models.ManyToManyField(User, blank=True, related_name="followings")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    #groups = models.ManyToManyField("core.Group", blank=True, related_name="groups")
    #pages = models.ManyToManyField("core.Page", blank=True, related_name="pages")
    blocked = models.ManyToManyField(User, blank=True, related_name="blocked")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.username)
        
    