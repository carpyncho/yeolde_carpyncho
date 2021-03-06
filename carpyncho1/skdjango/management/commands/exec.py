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
from django.core import management


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("carpyncho")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "exec file"

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):
        path = options["path"]
        execfile(path, {})


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
