#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# DOCS
#==============================================================================

"""Load json files from old database

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging
import json

from django.core.management.base import BaseCommand
from django.db import transaction

from carpyncho.cldo import models


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("cldo")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "Load json files from old database"

    args = ["blc", "lc", "plc", "var"]

    def resolve_d001_object(self, objID):
        return models.D001Object.objects.get_or_create(obj_id=objID)[0]

    def import_blc(self, path):
        with open(path) as fp:
            data = json.load(fp)
            for blc_data in data:
                kwargs = {
                    "d001_object": self.resolve_d001_object(blc_data["objID"]),
                    "ksBinHJD": blc_data["ksBinHJD"],
                    "ksBinMag":  blc_data["KsBinMag"],
                    "ksBinMagErr": blc_data["ksBinMagErr"]
                }
                models.D001BLC.objects.create(**kwargs)

    def import_lc(self, path):
        with open(path) as fp:
            data = json.load(fp)
            for lc_data in data:
                lc_data["d001_object"] = self.resolve_d001_object(
                    lc_data.pop("objID")
                )
                models.D001LC.objects.create(**lc_data)

    def import_plc(self, path):
        with open(path) as fp:
            data = json.load(fp)
            for plc_data in data:
                plc_data["d001_object"] = self.resolve_d001_object(
                    plc_data.pop("objID")
                )
                models.D001PLC.objects.create(**plc_data)

    def import_var(self, path):
        with open(path) as fp:
            data = json.load(fp)
            for var_data in data:
                var_data["d001_object"] = self.resolve_d001_object(
                    var_data.pop("objID")
                )
                models.D001Var.objects.create(**var_data)

    def handle(self, *args, **options):
        try:
            blc, lc, plc, var = args
            with transaction.atomic():
                logger.info(u"Proccessing 'blc': {}...".format(blc))
                self.import_blc(blc)
            with transaction.atomic():
                logger.info(u"Proccessing 'lc': {}...".format(lc))
                self.import_lc(lc)
            with transaction.atomic():
                logger.info(u"Proccessing 'plc': {}...".format(plc))
                self.import_plc(plc)
            with transaction.atomic():
                logger.info(u"Proccessing 'var': {}...".format(var))
                self.import_var(var)
        except Exception as err:
            logger.exception(err)
        finally:
            logger.info(u"Cleaning...")


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
