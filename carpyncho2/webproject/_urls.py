# -*- coding: utf-8 *-*
from django.conf.urls import url

from webproject import views

urlpatterns = [
    # Login, logout and session check
    url(r'^$', views.index, name="index"),
    url(r'^about/$', views.about, name="about"),
    url(r'^cql/$', views.cql_view, name='cql'),
]

