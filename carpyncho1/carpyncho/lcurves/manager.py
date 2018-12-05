#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Q, F

import numpy as np

from astropy.coordinates import SkyCoord

from skdjango.manager import SciManager, SciQuerySet


# =============================================================================
# MANAGERS
# =============================================================================

class MasterSourceQuerySet(SciQuerySet):

    def conesearch(self, ra, dec, sr):
        # http://www.g-vo.org/pmwiki/Products/HEALPixIndexing

        cos_sr = np.cos(sr)

        coord = SkyCoord(
            ra=ra, dec=dec, unit="deg", frame="icrs"
        ).represent_as("cartesian")
        x_c, y_c, z_c = coord.x.value, coord.y.value, coord.z.value

        expr = F("x") * x_c + F("y") * y_c + F("z") * z_c
        query = self.annotate(xyz=expr).filter(xyz__gte=cos_sr)
        return query


class MasterSourceManager(SciManager):

    def get_queryset(self):
        return MasterSourceQuerySet(self.model)

    get_query_set = get_queryset

