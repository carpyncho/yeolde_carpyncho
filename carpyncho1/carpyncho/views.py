#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

from json_views.views import JSONDataView, PaginatedJSONListView

from carpyncho.lcurves.models import *


class ServerConf(JSONDataView):

    def get_context_data(self):
        return settings.API_CONF


class ConeSearch(PaginatedJSONListView):

    paginate_by = settings.API_CONF["page_size"]
    count_query = 'count'
    count_only  = False
    serialize_fields = (
        "id", "tile__name",
        "dec_k", "ra_k",  "dec_h", "ra_h", "dec_j", "ra_j",
        "x", "y", "z")

    def get_queryset(self):

        ra = float(self.request.GET["ra"])
        dec = float(self.request.GET["dec"])
        sr = float(self.request.GET["sr"])

        query = MasterSource.objects.conesearch(ra, dec, sr)
        return query.values(*self.serialize_fields)



