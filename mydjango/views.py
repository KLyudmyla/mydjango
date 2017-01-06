from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


import hashlib
import random


#from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages



def index(request):
    return render (request, "index.html")

def register_confirm(request, activation_key):
    """
        #check if user is already logged in and if he is redirect him to some other url, e.g. home
    """
    if request.user.is_authenticated():
        messages.warning(request, 'Bro, you already have logined in, don\'t do it', extra_tags='warning')
        return redirect('index')
        # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(TempUserProfile, activation_key=activation_key)
    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        user_profile.delete()
        messages.error(request, 'Sorry, but your activation key had expired.', extra_tags='danger')
        return redirect('index')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = User.objects.create_user(
        username=user_profile.username,
        email=user_profile.email,
        password=user_profile.password1,
        first_name=user_profile.first_name,
        last_name=user_profile.last_name,
        is_active=True
    )
    user.save()
    user_profile.delete()
    messages.success(request, 'Your email confirmed and you are success registered! Please login in.', extra_tags='success')
    return redirect('index')




