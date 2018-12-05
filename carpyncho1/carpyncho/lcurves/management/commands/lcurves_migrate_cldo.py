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
from django.db import transaction
from django.forms.models import model_to_dict
from django.conf import settings

import numpy as np

from astroML import crossmatch

from carpyncho.cldo import models as cldomdls
from carpyncho.lcurves import models


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("lcurves")


#==============================================================================
# CONSTANT
#==============================================================================

# 1 arc second
MAX_MATCH = getattr(settings, "MAX_MATCH", 3 * 9.2592592592592588e-5)

MAX_HJD = 0.003


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "Copy all util data from cldo database structure to lcurves db"

    def migrate_data(self):
        migrated_ids = frozenset(
            models.CldoD001Source.objects.all().values_list(
                "orig_pk", flat=True
            )
        )
        to_migrate = cldomdls.D001Var.objects.exclude(
            d001_object__pk__in=migrated_ids
        )
        print to_migrate
        with transaction.atomic():
            for d001var in to_migrate:
                cldo_source = models.CldoD001Source()
                cldo_source.d001_object = d001var.d001_object
                cldo_source.save()

    def match(self):
        query = models.CldoD001Source.objects.filter(
            lcurves_master_source__isnull=True
        ).order_by("id")
        if query.exists():

            def ids():
                return iter(query.values_list("id", flat=True))

            def decs():
                for cldo_var in query:
                    yield cldo_var.d001_object.vars.get().DEC

            def ras():
                for cldo_var in query:
                    yield cldo_var.d001_object.vars.get().RA

            # CLDO
            cldo_query = query.values("id", "DEC", "RA")
            cldo_order = np.fromiter(ids, dtype="i")
            cldo_dec = np.fromiter(decs, dtype="f4")
            cldo_ra = np.fromiter(ras, dtype="f4")

            # LCURVES
            lcurves_query = models.MasterSource.objects.filter(
                tile__name="d001"
            ).order_by("id").values("id", "ra_k", "dec_k")

            lcurves_order = np.fromiter(
                lcurves_query.values_list("id", flat=True), dtype="i"
            )
            lcurves_dec = np.fromiter(
                lcurves_query.values_list("dec_k", flat=True), dtype="f4"
            )
            lcurves_ra = np.fromiter(
                lcurves_query.values_list("ra_k", flat=True), dtype="f4"
            )

            nearestind_cldo, distance_cldo, match_cldo = coords.match_coords(
                lcurves_ra, lcurves_dec, cldo_ra, cldo_dec,
                eps=MAX_MATCH, mode="nearest"
            )
            nearestind_ms, distance_ms, match_ms = coords.match_coords(
                cldo_ra, cldo_dec, lcurves_ra, lcurves_dec,
                eps=MAX_MATCH, mode="nearest"
            )

            with transaction.atomic():
                for idx_cldo, idx_ms in enumerate(nearestind_ms):
                    if match_ms[idx_cldo] and \
                       nearestind_cldo[idx_ms] == idx_cldo \
                       and match_cldo[idx_ms]:
                            cldo = query.get(id=cldo_order[idx_cldo])
                            master = models.MasterSource.objects.get(
                                id=lcurves_order[idx_ms]
                            )
                            cldo.lcurves_master_source = master
                            cldo.save()

    def match_pawprints(self):

        def closest(a, b, mtol=np.inf):
            idxs = np.zeros(a.size, dtype=int)
            deltas = np.zeros(a.size, dtype=float)
            for current, elem in enumerate(a):
                distances = np.abs(b-elem)
                idx = distances.argmin()
                min_distance = distances[idx]
                if min_distance < mtol:
                    idxs[current], deltas[current] = idx, min_distance
                else:
                    idxs[current], deltas[current] = -1, np.nan
            return idxs, deltas

        ba3 = tuple(cldomdls.D001Var.objects.filter(
            ksBestAper=3
        ).values_list("d001_object__pk", flat=True))
        query = models.CldoD001Source.objects.filter(
            lcurves_master_source__isnull=False,
            _orig_pk__in=ba3
        )
        for cldo_source in query:

            lcsquery = (
                cldo_source.d001_object.lcs.all()
            ).values("id", "HJD")
            lc_ids = np.fromiter(
                lcsquery.values_list(
                    "id", flat=True
                ), dtype=int
            )
            lc_hjds = np.fromiter(
                lcsquery.values_list(
                    "HJD", flat=True
                ), dtype=float
            )

            pwpquery = (
                cldo_source.lcurves_master_source.matches.all()
            ).values("pawprint_src__id", "pawprint_src__hjd")
            pw_ids = np.fromiter(
                pwpquery.values_list(
                    "pawprint_src__id", flat=True
                ), dtype=int
            )
            pw_hjds = np.fromiter(
                pwpquery.values_list(
                    "pawprint_src__hjd", flat=True
                ), dtype=float
            )

            pw2lc_idx, pw2lc_deltas = closest(pw_hjds, lc_hjds, MAX_HJD)
            lc2pw_idx, lc2pw_deltas = closest(lc_hjds, pw_hjds, MAX_HJD)

            for pwidx, lcidx in enumerate(pw2lc_idx):
                if lcidx != -1 and lc2pw_idx[lcidx] == pwidx:
                    pw_id, pw_hjd, pw_delta = (
                        pw_ids[pwidx], pw_hjds[pwidx], pw2lc_deltas[pwidx]
                    )
                    lc_id, lc_hjd, lc_delta = (
                        lc_ids[lcidx], lc_hjds[lcidx], lc2pw_deltas[lcidx]
                    )

                    clm = models.CldoLCurvesPawprintMatch()
                    clm.cldo_d001_source = cldo_source
                    clm.d001_lc = cldomdls.D001LC.objects.get(pk=lc_id)
                    clm.pawprint_source = models.PawprintSource.objects.get(
                        pk=pw_id
                    )
                    clm.hjd_avg = np.average([pw_hjd, lc_hjd])
                    clm.hjd_delta_avg = np.average([pw_delta, lc_delta])

                    clm.save()
        print models.CldoLCurvesPawprintMatch.objects.all().count()

    def handle(self, *args, **options):
            try:
                logger.info(u"migrating 'd001'...")
                #self.migrate_data()
            except Exception as err:
                logger.exception(err)
            try:
                logger.info(u"matching 'd001'...")
                #self.match()
            except Exception as err:
                logger.exception(err)
            try:
                logger.info(u"matching 'd001' pawprints...")
                self.match_pawprints()
            except Exception as err:
                logger.exception(err)
            finally:
                logger.info(u"Cleaning...")

#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
