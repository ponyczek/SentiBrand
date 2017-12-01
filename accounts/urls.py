from django.conf.urls import url

from . import views
from accounts.views import UserFormView


urlpatterns = [
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^register/$', UserFormView.as_view(), name='register'),

]