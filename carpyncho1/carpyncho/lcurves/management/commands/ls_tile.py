#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# DOCS
#==============================================================================

"""List all existing tile names

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
    help = "List all existing tile names"

    def handle(self, *args, **options):
        ls = u"[{}] {} - Sources: {} - Pawprints: {} - Sync: {} - Matches: {}"
        for tile in models.Tile.objects.all():
            print ls.format(
                tile.pk, tile.name,
                tile.sources.count(),
                tile.pawprints.count(),
                tile.pawprints.filter(pawprintxmodel__sync=True).count(),
                models.Match.objects.filter(master_src__tile=tile).count()
            )


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
