#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# DOCS
#==============================================================================

"""List all existing pawprint name of a given tile

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging
import os

from django.core.management.base import BaseCommand

from carpyncho.lcurves import models


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("lcurves")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "List all existing pawprint name of a given tile"

    args = ["tile_name"]

    def handle(self, *args, **options):
        tile_name, = args
        tile = models.Tile.objects.get(name=tile_name)
        ls = u"[{}] {} - Sources: {} - Matches: {}"
        for pawprint in tile.pawprints.all().order_by("pk"):
            sync = pawprint.pawprintxmodel_set.filter(
                tile=tile, sync=True
            ).exists()
            if sync:
                matches = models.Match.objects.filter(
                    pawprint_src__pawprint=pawprint
                ).count()
            else:
                matches = "NS"
            print ls.format(
                pawprint.pk, unicode(pawprint),
                pawprint.sources.count(), matches
            )


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
