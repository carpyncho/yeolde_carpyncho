#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# DOCS
#==============================================================================

"""Move data

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging

from django.core.management.base import BaseCommand
from django.db import transaction

import numpy as np

from carpyncho.lcurves import models as models_lcs
from carpyncho.cube import models


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("cube")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "Move from cube"

    def create_tile_dim(self):
        for tile in models_lcs.Tile.objects.all():
            models.TileDim.objects.get_or_create(name=tile.name)

    def create_pwp_dim(self):
        for pwp in models_lcs.Pawprint.objects.all():
            name = pwp.tile.name + "/" + pwp.name.rsplit("/",1)[-1]
            models.PawprintDim.objects.get_or_create(name=name)

    def create_mag_dim(self):
        query = models_lcs.PawprintSource.objects.all().order_by("mag")
        mags = np.fromiter(
            query.values_list("mag", flat=True).distinct(), dtype="f4"
        )
        for arr in np.split(mags, 48):
            minv, maxv = np.min(arr), np.max(arr)
            arr = np.fromiter(
                query.filter(mag__in=(minv, maxv)).values_list("mag_err", flat=True),
                dtype="f4"
            )
            err = np.average(arr)
            models.MagDim.objects.get_or_create(
                mag="{}-{}".format(minv, maxv), defaults={"mag_err": err}
            )

    def create_mjd_dim(self):
        query = models_lcs.PawprintSource.objects.all().order_by("mjd")
        for mjd in query.values_list("mjd", flat=True).distinct():
            models.MJDDim.objects.get_or_create(mjd=unicode(mjd))

    def create_facts(self):
        values = map(
            lambda x: tuple(map(float, x.split("-"))),
            models.MagDim.objects.all().values_list("mag", flat=True)
        )
        values.sort()
        values.append((values[-1][0] + 1, values[-1][0]))
        values = tuple(values)
        for m in models_lcs.Match.objects.all():
            sk = m.pk
            tile = models.TileDim.objects.get(name=m.master_src.tile.name)
            pawprint = models.PawprintDim.objects.get(
                name=(
                    m.pawprint_src.pawprint.tile.name + "/" +
                    m.pawprint_src.pawprint.name.rsplit("/",1)[-1]
                )
            )
            mag = None
            for idx, data in enumerate(values):
                minv, maxv = data[0], values[idx+1][1]
                if m.pawprint_src.mag >= minv and m.pawprint_src.mag < maxv:
                    name = "{}-{}".format(*data)
                    mag = models.MagDim.objects.get(mag=name)
                    break
            else:
                import ipdb; ipdb.set_trace()
            mjd = models.MJDDim.objects.get(mjd=unicode(m.pawprint_src.mjd))
            ra = m.master_src.ra_k
            dec = m.master_src.dec_k
            models.Fact.objects.get_or_create(
                sk=sk, defaults={
                    "tile":tile, "pawprint":pawprint, "mag":mag,
                    "mjd":mjd, "ra":ra, "dec":dec, "cnt":1
                }
            )

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                #~ self.create_tile_dim()
                #~ self.create_pwp_dim()
                #~ self.create_mag_dim()
                #~ self.create_mjd_dim()
                self.create_facts()
        except Exception as err:
            logger.exception(err)
        finally:
            logger.info(u"Cleaning...")


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
