#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# DOCS
#==============================================================================

"""Register a tile in to lcurves

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging
import os

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from astropy.coordinates import SkyCoord

from carpyncho.lcurves import models
from carpyncho.lcurves.libs import match


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("lcurves")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "Register a tile in to lcurves"

    args = ["name", "filepath"]

    def register_tile(self, name, filepath):
        fname = os.path.basename(filepath)

        with open(filepath, "rb") as fp:
            tile = models.Tile(name=name)
            logger.info(u"Saving {} ...".format(filepath))
            tile.file.save(fname, File(fp))
            tile.save()

            fp.seek(0)
            logger.info(u"Loading sources...")
            for order, src in enumerate(match.read_mastersrc(fp)):
                coord = SkyCoord(
                    ra=src[4], dec=src[5], unit="deg", frame="icrs"
                ).represent_as("cartesian")


                srcmodel = models.MasterSource(
                    tile=tile, order=order,
                    ra_h=src[0], dec_h=src[1],
                    ra_j=src[2], dec_j=src[3],
                    ra_k=src[4], dec_k=src[5],
                    x=coord.x.value, y=coord.y.value, z=coord.z.value)
                logger.info("Master Source number: {}".format(order))
                srcmodel.save()

    def handle(self, *args, **options):
        try:
            name, filepath = args
            with transaction.atomic():
                self.register_tile(name, filepath)
        except Exception as err:
            logger.exception(err)
            transaction.rollback()
        else:
            transaction.commit()
        finally:
            logger.info(u"Cleaning...")


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
