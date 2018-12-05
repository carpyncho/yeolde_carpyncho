"""webproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from webproject import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/request_user', views.request_user, name="request_user"),
    url(r'^accounts/user_created', views.user_created, name="user_created"),
    url(r'^accounts/password_change', views.password_change, name="password_change"),

    url(r'^$', views.index, name='home'),
    url(r'^carpyncho/', include('webproject._urls', namespace='carpyncho'))
]
