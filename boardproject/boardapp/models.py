from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
import math
from django.utils import timezone
from datetime import datetime

# Create your models here.

class BoardModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    snsimage = models.ImageField(upload_to='')
    good = models.IntegerField(null=True, blank=True, default=1)
    read = models.IntegerField(null=True, blank=True, default=1)
    readtext = models.TextField(null=True, blank=True, default='a')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    image = models.ImageField(upload_to='')
    image2 = models.ImageField(upload_to='')
    image3 = models.ImageField(upload_to='')
    image4 = models.ImageField(upload_to='')
    image5 = models.ImageField(upload_to='')
    gender = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True, default=1)
    location = models.CharField(max_length=30, blank=True)
    introduction_text = models.CharField(max_length=500, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.image = 'ano.png'
        instance.profile.image2 = 'noPhoto.png'
        instance.profile.image3 = 'noPhoto.png'
        instance.profile.image4 = 'noPhoto.png'
        instance.profile.image5 = 'noPhoto.png'


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Likes(models.Model):
    user_id = models.IntegerField()
    liked_user_id = models.IntegerField()
    like_date = models.DateTimeField(default=timezone.now, blank=True)

    def judgeMatching(loginUser):
        likeUsers = Likes.objects.filter(user_id=loginUser.id)
        likeUsers = Likes.objects.filter(user_id=loginUser.id)
        likedUsers = Likes.objects.filter(liked_user_id=loginUser.id)
        # matchingFlag = "false"
        matchingUser = User.objects.get(id=loginUser.id)

        for item in likeUsers:
            for item2 in likedUsers:
                if item.liked_user_id == item2.user_id:
                    aaaa = datetime.now()
                    if 2 > (aaaa.replace(tzinfo=None)-item.like_date.replace(tzinfo=None)).total_seconds():
                        matchingUser = User.objects.get(id=item.liked_user_id)
                        return matchingUser

class Nopes(models.Model):
    user_id = models.IntegerField()
    noped_user_id = models.IntegerField()

class Messages(models.Model):
    room_name = models.CharField(max_length=50, blank=True)
    user_id = models.IntegerField(blank=True)
    talk_user_id = models.IntegerField(blank=True)
    message = models.CharField(max_length=500, blank=True)
    send_date = models.DateTimeField(default=timezone.now)

    def getMessage(loginUser, talkToId, room):
        messages = []

        for dbMessage in Messages.objects.filter(room_name=room):
            # print(type(dbMessage.send_date))
            if dbMessage.user_id == loginUser.id:
                messageDictionary = {"username": loginUser.username, "message": dbMessage.message, "date": str(dbMessage.send_date.strftime('%Y/%m/%d %H:%M'))}
                # messageDictionary = {"username":request.user.username,"message":dbMessage.message}
                messages.append(messageDictionary)
            else:
                messageDictionary1 = {"username": User.objects.get(id=talkToId).username, "message": dbMessage.message, "date": str(dbMessage.send_date.strftime('%Y/%m/%d %H:%M'))}
                # messageDictionary1 = {"username":User.objects.get(id=talkToId).username,"message":dbMessage.message}
                messages.append(messageDictionary1)
        return messages


class GetUser():
    def getMatchingUser(loginUser):
        object_list = []
        allUsers = User.objects.all()

        userGender = "性別"
        if loginUser.profile.gender == "男性":
            userGender = "女性"
        elif loginUser.profile.gender == "女性":
            userGender = "男性"

        for user in allUsers:
            if user.profile.gender == userGender:
                if not Likes.objects.filter(user_id=loginUser.id, liked_user_id=user.id).exists() and not Nopes.objects.filter(user_id=loginUser.id, noped_user_id=user.id).exists() and user.id != loginUser.id:
                    object_list.append(user)
                    break
        if len(object_list) != 0:
            nextUser = object_list[0]
        else:
            nextUser = None
        return nextUser
