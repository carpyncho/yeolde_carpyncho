#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import JsonResponse

import six

class CarpynchoErrorMiddleware(object):

    def process_exception(self, request, err):
        data = {
            "error_type": type(err).__name__,
            "msg": six.text_type(err),
            "path": request.path,
            "error": 500,
        }
        return JsonResponse(data)

