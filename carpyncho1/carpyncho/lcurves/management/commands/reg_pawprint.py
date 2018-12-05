#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# DOCS
#==============================================================================

"""Register a pawpint and link with their mastersourse in to lcurves

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging
import os

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from astropy.io import fits

from carpyncho.lcurves import models


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("lcurves")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "Register a pawpint and link with their mastersourse in to lcurves"

    args = ["mastersrc_name", "name", "filepath"]

    def _extract_mjd(self, fpath):
        hdulist = fits.open(fpath)
        return hdulist[0].header["MJD-OBS"]

    def register_pawprint(self, mastersrc_name, filepath):

        fname = os.path.basename(filepath)
        name = os.path.splitext(fname)[0]

        mjd = self._extract_mjd(filepath)

        with open(filepath, "rb") as fp:
            master = models.Tile.objects.get(name=mastersrc_name)
            pawprints = models.Pawprint.objects.filter(name=name)
            if pawprints.exists():
                logger.info(u"Pawprint '{}' already exists".format(name))
                pawprint = pawprints.get(name=name)
            else:
                pawprint = models.Pawprint(name=name, mjd=mjd)
                logger.info(u"Saving {} ...".format(filepath))
                pawprint.file.save(fname, File(fp))
                pawprint.save()
            models.PawprintXModel.objects.get_or_create(
                tile=master, pawprint=pawprint
            )

    def handle(self, *args, **options):
        try:
            mastersrc_name, filepath = args
            with transaction.atomic():
                self.register_pawprint(mastersrc_name, filepath)
        except Exception as err:
            logger.exception(err)
        finally:
            logger.info(u"Cleaning...")


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
