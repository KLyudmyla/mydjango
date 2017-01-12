import datetime
import hashlib
import random
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from registrations.forms import FirstForm
from registrations.models import UserProfile



def index(request):
    return render (request, "index.html")

def profile(request):
    return render (request, "profile.html")


#def logout(request):
#    auth.logout(request)
#    messages.error(request, 'You are logout', extra_tags='info')
#    return redirect('index')

def registration(request):
    if request.method == 'POST':
        form = FirstForm(request.POST)
        if form.is_valid() and form.cleaned_data['password1'] == form.cleaned_data['password2']:
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random()).encode()).hexdigest()[:5]
            activation_key = hashlib.sha1((salt + email).encode()).hexdigest()
            key_expires = datetime.datetime.now() + datetime.timedelta(hours=48)
            # Create and save temp_user profile
            new_profile = UserProfile(username=username,
                                          email=email,
                                          activation_key=activation_key,
                                          key_expires=key_expires,
                                          first_name=form.cleaned_data['first_name'],
                                          last_name=form.cleaned_data['last_name'],
                                          password1=form.cleaned_data['password1'],
                                          password2=form.cleaned_data['password2']
                                          )
            new_profile.save()
            # Send email with activation key
            email_subject = 'Подтверждение регистрации'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            5 minutes https://http://mydjango.pythonanywhere.com//accounts/confirm/%s" % (username, activation_key)
            send_mail(email_subject, email_body, from_email='kaluzhynoval@gmail.com', recipient_list=['kaluzhynova@gmail.com', 'vlyuda@mail.ru'],
                      fail_silently=False)
            messages.success(request, "For success registered we send you email.\n Please confirm your email",
                             extra_tags='info')
            return redirect('index')
        else:
            messages.error(request, "Enter valid info. Please, try again", extra_tags='danger')
            return redirect('registration')
    form = FirstForm()
    return render(request, 'registration.html', {'form': form})

def register_confirm(request, activation_key):
    """
        #check if user is already logged in and if he is redirect him to some other url, e.g. home
    """
    if request.user.is_authenticated():
        messages.warning(request, 'Bro, you already have logined in, don\'t do it', extra_tags='warning')
        return redirect('index')
        # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
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








