from django.conf.urls import url, include
from django.contrib import admin
from .views import index
from registrations.views import RegisterFormView, LoginFormView, LogoutView

urlpatterns = [
    url(r'^$', index, name='index'),
#    url('^', include('django.contrib.auth.urls')),
    url(r'^register/$', RegisterFormView.as_view(), name = 'register'),
    url(r'^login/$', LoginFormView.as_view(), name = 'login'),
    url(r'^logout/$', LogoutView.as_view(), name = 'logout'),
    url(r'^admin/', admin.site.urls),
]
