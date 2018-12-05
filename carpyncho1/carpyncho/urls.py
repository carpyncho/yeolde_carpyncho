#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings

from carpyncho import views


urlpatterns = patterns('',
    url(r'^serverconf/$', views.ServerConf.as_view()),
    url(r'^conesearch/$', views.ConeSearch.as_view()),

)

