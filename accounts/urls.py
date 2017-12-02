from django.conf.urls import url

from . import views
from accounts.views import UserFormView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^register/$', UserFormView.as_view(), name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
]