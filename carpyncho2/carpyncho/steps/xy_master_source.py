#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import izip

from corral import run, db

import numpy as np

from astropy.coordinates import SkyCoord

from ..models import MasterSource


class XYMasterSource(run.Step):

    groups = ["extra"]

    limit = 500000

    def generate(self):
        query = self.session.query(
            MasterSource.id, MasterSource.ra_k, MasterSource.dec_k
        ).filter(MasterSource.x.is_(None)).limit(self.limit)
        arr = np.fromiter(
            query, dtype=[("id", int), ("ra", float), ("dec", float)])
        yield arr

    def validate(self, obj):
        assert isinstance(obj, np.ndarray)

    def process(self, arr):
        coord = SkyCoord(
            ra=arr["ra"], dec=arr["dec"], unit="deg", frame="icrs"
        ).represent_as("cartesian")
        maps = []
        for id, x, y, z in izip(arr["id"], *coord.xyz.value):
            maps.append(dict(id=id, x=x, y=y, z=z))

        self.session.bulk_update_mappings(MasterSource, maps)

