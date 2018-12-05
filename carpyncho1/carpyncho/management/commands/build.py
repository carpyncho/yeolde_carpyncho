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

from carpyncho import bin_ext

#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("carpyncho")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "Build the extensions"

    def handle(self, *args, **options):
        bin_ext.build()


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)