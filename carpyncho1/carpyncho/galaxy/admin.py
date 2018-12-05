#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

from django.contrib import admin
from galaxy_search import models


for v in vars(models).values():
    if inspect.isclass(v) and issubclass(v, models.models.Model):
        admin.site.register(v)
