from django.conf.urls import url
from django.contrib.auth import views as auth_views

from accounts.views import UserFormView
from . import views

urlpatterns = [
    url(r'^register/$', UserFormView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
]
