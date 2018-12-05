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

from django.core.management.base import BaseCommand

from django.db import transaction

from PyAstronomy import pyasl

import numpy as np

from carpyncho.lcurves.models import *
from skdjango.transaction import commit_after


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("lcurves")


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "List all existing tile names"

    def func(self, match_id):
        match = Match.objects.get(id=match_id)
        m_ra, m_dec = match.master_src.ra_k, match.master_src.dec_k
        p_ra, p_dec = match.pawprint_src.ra_deg, match.pawprint_src.dec_deg

        ras, decs = np.array([m_ra, p_ra]), np.array([m_dec, p_dec])

        match.ra_avg = np.average(ras)
        match.dec_avg = np.average(decs)
        match.ra_std = np.std(ras)
        match.dec_std = np.std(decs)
        match.ra_range = np.abs(np.subtract(*ras))
        match.dec_range = np.abs(np.subtract(*decs))

        match.save()

    def handle(self, *args, **options):
            gen = np.fromiter(Match.objects.filter(ra_avg=0).values_list("id", flat=True), dtype=int)
            commit_after(gen, self.func, 10000)







#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
