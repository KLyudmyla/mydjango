import os

from django.contrib.auth.models import User
from django.db import models


class TempUserProfile(models.Model):
    username = models.CharField(max_length=16)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    password1 = models.TextField()
    password2 = models.TextField()
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField()
    email = models.EmailField()

    def __str__(self):
        return self.username

def avatar_upload_to(instance, filename):
    return os.path.join('static/images/users', instance.user.username + os.path.splitext(filename)[1])

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to=avatar_upload_to, verbose_name='Изображение', null=True, blank= True)
    education = models.TextField(null=True, blank= True)
    job = models.TextField(null=True, blank= True)
    education = models.TextField(null=True, blank= True)
    description = models.TextField(null=True, blank= True)
    date_of_birth=models.DateField(null=True, blank= True) 
 
    def __unicode__(self):
        return self.user
 
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


