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
