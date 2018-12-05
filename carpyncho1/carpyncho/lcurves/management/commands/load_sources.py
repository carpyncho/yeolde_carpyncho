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
    help = "Charge pawprint sources to the database"

    def load_sources(self):
        for pw in models.Pawprint.objects.filter(has_sources=False):
            pw.rescan_sources()
            pw.has_sources = True
            pw.save()

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                self.load_sources()
        except Exception as err:
            logger.exception(err)
        finally:
            logger.info(u"Cleaning...")


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
