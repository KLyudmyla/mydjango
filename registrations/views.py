from django.shortcuts import render

#import datetime
#import hashlib
#import random

from django.views.generic.edit import FormView
#from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.models import User
#from .forms import FirstForm
#from django.utils import timezone
#from django.core.mail import send_mail
from django.contrib import messages
#from django.shortcuts import render, redirect, get_object_or_404



class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        messages.error(request, 'Congratulations you have logined  successfully to our site', extra_tags='success')
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.error(request, 'You are logout', extra_tags='info')
        return HttpResponseRedirect("/")



