from django.conf.urls import url

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^dashboard/search$', views.single_search, name='search'),
    url(r'^dashboard/add_phrase$', views.add_phrase, name='add_phrase'),
    url(r'^dashboard/phrase/(?P<user_phrase_id>[0-9]+)/$', views.phrase_detail, name='phrase_detail'),
    url(r'^dashboard/phrase/(?P<user_phrase_id>[0-9]+)/range$', views.phrase_detail_range, name='phrase_detail_range'),
    url(r'^dashboard/phrase/(?P<user_phrase_id>[0-9]+)/(?P<start_date>[0-9]+)$', views.phrase_detail_day, name='phrase_detail_day'),
    url(r'^dashboard/phrase/(?P<user_phrase_id>[0-9]+)/delete$', views.delete_phrase, name='delete_phrase'),
    url(r'^dashboard/phrase/(?P<user_phrase_id>[0-9]+)/edit$', views.edit_phrase, name='edit_phrase'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)