from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
import math

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    #ここから
    def get_age(self):
        age= datetime.date.today()-self.birth_date
        return int((age).days/365.25)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Likes(models.Model):
    user_id = models.IntegerField()
    liked_user_id = models.IntegerField()

class Nopes(models.Model):
    user_id = models.IntegerField()
    noped_user_id = models.IntegerField()