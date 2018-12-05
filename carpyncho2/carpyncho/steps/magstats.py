#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from scipy.spatial.distance import euclidean

from corral import run

from ..models import Match


class Magstats(run.Step):

    model = MasterSource

    MasterSource.
    conditions = [model.ra_avg.is_(None)]
    limit = 5000

    def process(self, match):
        ras = np.array((match.pawprint_src.ra_deg, match.master_src.ra_k))
        decs = np.array((match.pawprint_src.dec_deg, match.master_src.dec_k))

        match.ra_avg = np.mean(ras)
        match.dec_avg = np.mean(decs)
        match.ra_std = np.std(ras)
        match.dec_std = np.std(decs)
        match.ra_range = np.max(ras) - np.min(ras)
        match.dec_range = np.max(decs) - np.min(decs)
        match.euc = euclidean((ras[0], decs[0]), (ras[1], decs[1]))
