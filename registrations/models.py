from django.db import models
from django.contrib.auth.models import User
#from django.conf import settings


class Users(models.Model):
    user = models.OneToOneField(User)
    password1 = models.TextField()
    password2 = models.TextField()     
    
    def __str__(self):
        return self.user.username
