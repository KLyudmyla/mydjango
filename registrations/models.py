from django.db import models
from django.contrib.auth.models import User
import datetime


class Users(models.Model):
#    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())
    username = models.CharField(max_length=16)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    password1 = models.TextField()
    password2 = models.TextField()
#    activation_key = models.CharField(max_length=40, blank=True)
#    key_expires = models.DateTimeField()
    email = models.EmailField()
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'

