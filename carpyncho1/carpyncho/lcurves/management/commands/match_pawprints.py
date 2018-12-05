#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# DOCS
#==============================================================================

"""Match al sources of un 'unmached' pawprints

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from carpyncho.lcurves import models


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("lcurves")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "Match al sources of un 'unmached' pawprints"

    def match_unsync_pawprints(self):
        data_ms = {}
        for pxt in models.PawprintXModel.objects.filter(matched=False):
            try:
                tile_name = pxt.tile.name
                if tile_name not in data_ms:
                    data_ms[tile_name] = pxt.data_ms()

                msg = u"Matching '{}' -> '{}'...".format(
                    pxt.pawprint.name, pxt.tile.name
                )
                logger.info(msg)
                with transaction.atomic():
                    pxt.match(data_ms=data_ms[tile_name])
                    pxt.matched = True
                    pxt.save()
            except Exception as err:
                logger.exception(err)
            finally:
                logger.info(u"Cleaning...")

    def handle(self, *args, **options):
        self.match_unsync_pawprints()

#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
