#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from webproject.models import CQLAst, CQLQuery

admin.site.register(CQLAst)
admin.site.register(CQLQuery)



