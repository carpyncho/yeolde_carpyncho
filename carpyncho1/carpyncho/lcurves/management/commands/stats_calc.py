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

import numpy as np
from django.core.management.base import BaseCommand


from skdjango.transaction import commit_after

from carpyncho.lcurves.models import *


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("lcurves")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "List all existing tile names"

    def mag(self, master_src_id):
        ms = MasterSource.objects.get(pk=master_src_id)
        stats = MagStats(stats_from=ms)
        stats.recalc = True
        stats.calculate()
        stats.save()

    def lc(self, master_src_id):
        ms = MasterSource.objects.get(pk=master_src_id)
        mslc = LightCurve(source=ms)
        mslc.recalc = True
        mslc.calculate()
        mslc.save()

    def calculate_all_statistics(self):
        limit = 10000
        end = False
        while not end:
        # lightcurves
            exists = tuple(LightCurve.objects.values_list("source", flat=True))
            gen = tuple(MasterSource.objects.exclude(pk__in=exists).values_list("id", flat=True)[:limit])
            end = True
            if len(gen):
                end = False
                commit_after(gen, self.lc, 1000)

            # mag stats
            exists = tuple(MagStats.objects.values_list("stats_from", flat=True))
            gen = tuple(MasterSource.objects.exclude(pk__in=exists).values_list("id", flat=True)[:limit])
            commit_after(gen, self.mag, 1000)
            end = True
            if len(gen):
                end = False
                commit_after(gen, self.mag, 1000)


    def handle(self, *args, **options):
        self.calculate_all_statistics()



#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
