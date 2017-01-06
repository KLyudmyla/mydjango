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
            5 minutes https://djangodeploy.herokuapp.com/accounts/confirm/%s" % (username, activation_key)
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



