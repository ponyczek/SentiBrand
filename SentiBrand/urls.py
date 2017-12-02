from django.conf.urls import include, url
from django.contrib.auth import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings


"""SentiBrand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('accounts.urls')),
    url(r'', include('static_pages.urls')),
    # url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm , 'redirect_authenticated_user': True}, name='login'),
    # url(r'^logout/$', views.logout, {'next_page': '/login'}, name='logout'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)