#!/usr/bin/env python
# -*- coding: utf-8 -*-

from astropysics import coords

from corral import run, db
from corral.conf import settings

from ..models import PawprintXTile, PawprintSource, MasterSource, Match


MAX_MATCH = 3 * 9.2592592592592588e-5


class MatchSources(run.Step):

    model = PawprintXTile
    conditions = [model.status == "pending"]
    procno = 2
    production_procno = 30
    groups = ["match"]

    @classmethod
    def class_setup(cls):

        def chunk_it(seq, num):
            avg = len(seq) / float(num)
            out = []
            last = 0.0
            while last < len(seq):
                out.append(seq[int(last):int(last + avg)])
                last += avg
            return sorted(out, reverse=True)

        with db.session_scope() as session:
            all_ids = tuple(
                r[0]
                for r in session.query(cls.model.id).filter(*cls.conditions))
        db.engine.dispose()
        cls.chunks = chunk_it(all_ids, cls.get_procno())

    def generate(self):
        if not self.chunks:
            return ()
        ids = self.chunks[self.current_proc]
        if not ids:
            return ()
        return self.session.query(self.model).filter(self.model.id.in_(ids))

    def setup(self):
        self._buff = {}

    def get_pwp_src(self, pwp_id, idx):
        if not hasattr(self, "_pwp_sources"):
            self._pwp_sources = self.session.query(
                PawprintSource.id, PawprintSource.order,
                PawprintSource.ra_deg, PawprintSource.dec_deg, PawprintSource.mag,
                PawprintSource.mag_err, PawprintSource.hjd,
                PawprintSource.chip_nro, PawprintSource.stel_cls,
                PawprintSource.elip, PawprintSource.pos_ang
            ).filter_by(
                pawprint_id=pwp_id).order_by(PawprintSource.order).all()
        return self._pwp_sources[idx]

    def get_ms_src(self, tile_id, idx):
        if not hasattr(self, "_master_sources"):
            self._master_sources = self.session.query(
                    MasterSource.id, MasterSource.order,
                    MasterSource.ra_k, MasterSource.dec_k
                ).filter_by(tile_id=tile_id).order_by(MasterSource.order).all()
        return self._master_sources[idx]

    def clean_buff(self):
        if hasattr(self, "_pwp_sources"):
            del self._pwp_sources
        if hasattr(self, "_master_sources"):
            del self._master_sources

    def process(self, pxt):
        maxmatch = MAX_MATCH
        mode = "nearest"

        pwp_data, tile_data = pxt.pawprint.data, pxt.tile.data

        pwp_ra, pwp_dec = pwp_data["ra_deg"], pwp_data["dec_deg"]
        tile_ra, tile_dec = tile_data["ra_k"], tile_data["dec_k"]

        nearestind_pwp, distance_pwp, match_pwp = coords.match_coords(
            tile_ra, tile_dec, pwp_ra, pwp_dec, eps=maxmatch, mode=mode)
        nearestind_ms, distance_ms, match_ms = coords.match_coords(
            pwp_ra, pwp_dec, tile_ra, tile_dec, eps=maxmatch, mode=mode)

        matchs = []
        for idx_pwp, idx_ms in enumerate(nearestind_ms):
            if match_ms[idx_pwp] and \
               nearestind_pwp[idx_ms] == idx_pwp \
               and match_pwp[idx_ms]:
                    pwp_src = self.get_pwp_src(pxt.pawprint_id, idx_pwp)
                    ms = self.get_ms_src(pxt.tile_id, idx_ms)

                    matchs.append({
                        "band": "k",

                        "tile_id": pxt.tile_id,
                        "master_src_id": ms.id, "master_src_order": ms.order,
                        "master_src_ra": ms.ra_k, "master_src_dec": ms.dec_k,

                        "pawprint_id": pxt.pawprint_id,
                        "pawprint_src_id": pwp_src.id,
                        "pawprint_src_order": pwp_src.order,
                        "pawprint_src_ra": pwp_src.ra_deg,
                        "pawprint_src_dec": pwp_src.dec_deg,
                        "pawprint_src_mag": pwp_src.mag,
                        "pawprint_src_mag_err": pwp_src.mag_err,
                        "pawprint_src_hjd": pwp_src.hjd,
                        "pawprint_src_chip_nro": pwp_src.chip_nro,
                        "pawprint_src_stel_cls": pwp_src.stel_cls,
                        "pawprint_src_elip": pwp_src.elip,
                        "pawprint_src_pos_ang": pwp_src.pos_ang})

        self.session.bulk_insert_mappings(Match, matchs)

        pxt.status = "sync"
        self.save(pxt)

        self.session.commit()
        self.clean_buff()
