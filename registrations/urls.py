from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'registrations'
urlpatterns = [
url(r'^$', views.hi, name='hi'),
url(r'^(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='detail'),
url(r'^edit/(?P<pk>\d+)/$', views.UserProfileUpdateView.as_view(), name='edit'),
url(r'^edit_add/(?P<pk>\d+)/$', views.UserProfileAddUpdateView.as_view(), name='edit_add'),

]
