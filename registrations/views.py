from django.shortcuts import render

import datetime
import hashlib
import random

from django.views.generic.edit import FormView
#from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import UserCreateForm
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Users

class RegisterFormView(FormView):
    form_class = UserCreateForm
    success_url = "/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        salt = hashlib.sha1(str(random.random()).encode()).hexdigest()[:5]
        activation_key = hashlib.sha1((salt + email).encode()).hexdigest()
        key_expires = datetime.datetime.now() + datetime.timedelta(minutes=5)
        email_subject = 'Подтверждение регистрации'
        email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            5 minutes http://mydjango.pythonanywhere.com/accounts/confirm/%s" % (username, activation_key)
        send_mail(email_subject, email_body, from_email='kaluzhynoval@gmail.com', recipient_list=[email], fail_silently=False)
        messages.success(self.request, "For success registered we send you email.\n Please confirm your email", extra_tags='info')
            
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")

def register_confirm(request, activation_key):
    """
        #check if user is already logged in and if he is redirect him to some other url, e.g. home
    """
    if request.user.is_authenticated():
        messages.warning(request, 'Bro, you already have logined in, don\'t do it', extra_tags='warning')
        return redirect('index')
        # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(User, activation_key=activation_key)
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



