from django.shortcuts import render

#import datetime
#import hashlib
#import random

from .forms import FirstForm, ProfileForm, ProfileAddForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from registrations.models import UserProfile
#from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
#from django.utils import timezone
#from django.core.mail import send_mail
from django.contrib import messages

class UserDetailView(DetailView):
    model = User
    template_name = 'registrations/detail.html'

class UserProfileUpdateView(UpdateView):
    model = User
    template_name = "registrations/edit.html"
    form_class = ProfileForm
    success_url = reverse_lazy('registrations:hi')

    
    def get_success_url(self):
        super().get_success_url()
        pk = self.kwargs['pk']
        return reverse('registrations:detail', args=(pk,))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ваш профайл изменен")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление профайла' 
        return context

class UserProfileAddUpdateView(UpdateView):
    model = UserProfile
    template_name = "registrations/edit_add.html"
    form_class = ProfileAddForm
    success_url = reverse_lazy('registrations:hi')

    
    def get_success_url(self):
        super().get_success_url()
        pk = self.kwargs['pk']
        return reverse('registrations:edit_add', args=(pk,))

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Ваш профайл изменен")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обновление профайла' 
        return context
    

class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        messages.error(self.request, 'Congratulations you have logined  successfully to our site', extra_tags='success')
        return super(LoginFormView, self).form_valid(form)

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.error(request, 'You are logout', extra_tags='info')
        return HttpResponseRedirect("/")


def hi(request):
    return render (request, "hi.html")


