from distutils.command.upload import upload
from email.policy import default
from signal import default_int_handler
from django.db import models
from django.contrib.auth.models import AbstractUser
import json

# Create your models here.
class CustomUser(AbstractUser):
    section = models.CharField(max_length=2)
    bio = models.TextField(default = "")
    img_src = models.ImageField(upload_to="user/images", default="media/user/images/unknown_user.jpg")
    
    
class PhotoUpload(models.Model):
    photo_id = models.IntegerField(default = 0)
    user_name = models.CharField(max_length = 122)
    user_img_url = models.CharField(max_length = 122, default= "media/user/images/unknown_user.jpg")
    section = models.CharField(max_length = 2)
    photo = models.ImageField(upload_to="uploads/pics")
    caption = models.TextField(default = "")

class Comments(models.Model):
    comment_id = models.IntegerField(default = 0)
    commenting_user_url = models.CharField(max_length = 122, default="")
    commenting_user = models.CharField(max_length = 122)
    commenting_photo_url = models.CharField(max_length = 122)
    comment = models.TextField(default = "")
    replies = models.CharField(max_length = 500 , default="")
    date = models.CharField(max_length = 200 , default="")

class Notification(models.Model):
    for_user =  models.CharField(max_length = 122)
    notification = models.TextField(default = "")
    notification_img_src = models.TextField(default = "")
    notify = models.BooleanField(default = False)

    