from django.conf.urls import url

from . import views
from accounts.views import UserFormView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^dashboard/search$', views.single_search, name='search'),
    url(r'^dashboard/add_phrase$', views.add_phrase, name='add_phrase'),
    url(r'^dashboard/phrase/(?P<user_phrase_id>[0-9]+)/$', views.phrase_detail, name='phrase_detail'),
]