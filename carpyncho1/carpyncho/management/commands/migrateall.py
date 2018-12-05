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
from django.conf import settings
from django.core import management


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("carpyncho")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "Sync every databae out there"

    def handle(self, *args, **options):
        for db in settings.DATABASES.keys():
            logger.info("Migrating '{}'...".format(db))
            management.call_command('migrate', database=db)


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
