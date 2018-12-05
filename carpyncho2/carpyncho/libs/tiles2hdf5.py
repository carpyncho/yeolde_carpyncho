#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import datetime as dt
import multiprocessing as mp
from contextlib import contextmanager

import numpy as np

import tables as tb

import attr

from corral import db

from ..models import Tile, MasterSource, Match, PawprintSource


# =============================================================================
# CONF AND CONSTANTS
# =============================================================================

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

YIELD_PER = 10000
BUFF_SIZE = 50000


# =============================================================================
# DESCRIPTORS
# =============================================================================

class TileDescriptor(tb.IsDescription):
    id = tb.Int64Col(pos=0)
    name = tb.StringCol(8, pos=1)
    size = tb.Int64Col(pos=2)
    matchs_counted = tb.BoolCol(pos=3)


class SourceDescriptor(tb.IsDescription):
    id = tb.Int64Col(pos=0)
    tile_id = tb.Int64Col(pos=1)
    order = tb.Int64Col(pos=2)
    ra_j = tb.FloatCol(pos=3)
    ra_k = tb.FloatCol(pos=4)
    ra_h = tb.FloatCol(pos=5)
    dec_h = tb.FloatCol(pos=6)
    dec_j = tb.FloatCol(pos=7)
    dec_k = tb.FloatCol(pos=8)
    obs_number = tb.Int64Col(pos=9)


class ObservationDescriptor(tb.IsDescription):
    id = tb.Int64Col(pos=0)
    # pwp
    pwp_id = tb.Int64Col(pos=1)
    pwp_order = tb.Int64Col(pos=2)
    ra = tb.FloatCol(pos=3)
    dec = tb.FloatCol(pos=4)
    mag = tb.FloatCol(pos=5)
    mag_err = tb.FloatCol(pos=6)
    hjd = tb.FloatCol(pos=7)

    chip_nro = tb.FloatCol(pos=8)
    stel_cls = tb.FloatCol(pos=9)
    elip = tb.FloatCol(pos=10)
    pos_ang = tb.FloatCol(pos=11)
    # ms
    tile_id = tb.Int64Col(pos=12)
    source_id = tb.Int64Col(pos=13)


# =============================================================================
# DUMPFILE
# =============================================================================

@attr.s(frozen=True, repr=False)
class DumpFile(object):
    h5file = attr.ib()
    tiles_table = attr.ib()
    src_table = attr.ib()
    obs_table = attr.ib()

    def __repr__(self):
        return repr(self.h5file)


# =============================================================================
# DUMP
# =============================================================================

class Tile2HDF5(mp.Process):

    def __init__(self, title, session, tiles_names, h5_path):
        super(Tile2HDF5, self).__init__()
        self.title = title
        self.session = session
        self.tiles_names = tiles_names
        self.h5_path = h5_path

    def _store_tiles(self, session, tile_id, tiles_table):
        tiles_q = session.query(
            Tile.id, Tile.name, Tile.data_size).filter(Tile.id == tile_id)
        if tiles_table.nrows:
            ptq = "id == {}".format(tile_id)
            ids = [t["id"] for t in tiles_table.where(ptq)]
            if ids:
                return
        tile = tiles_q.first()
        tiles_table.append([list(tile) + [False]])
        tiles_table.flush()

    def _store_sources(self, session, tile_id, src_table):
        src_q = session.query(
            MasterSource.id, MasterSource.tile_id, MasterSource.order,
            MasterSource.ra_j, MasterSource.ra_k, MasterSource.ra_h,
            MasterSource.dec_h, MasterSource.dec_j, MasterSource.dec_k
        ).filter(MasterSource.tile_id == tile_id)
        if src_table.nrows:
            ptq = "tile_id == {}".format(tile_id)
            max_id = np.max([s["id"] for s in src_table.where(ptq)])
            src_q = src_q.filter(MasterSource.id > max_id)

        buff = []
        for src in src_q.order_by(MasterSource.id).yield_per(YIELD_PER):
            buff.append(list(src) + [0])
            if len(buff) > BUFF_SIZE:
                src_table.append(buff)
                logger.info(" Sources-FLUSH")
                src_table.flush()
                buff = []
        if buff:
            src_table.append(buff)
            logger.info(" Sources-FLUSH")
            src_table.flush()

    def _store_observations(self, session, tile_id, obs_table):
        obs_q = session.query(
            Match.pawprint_src_id, Match.pawprint_id, Match.pawprint_src_order,
            Match.pawprint_src_ra, Match.pawprint_src_dec,
            Match.pawprint_src_mag, Match.pawprint_src_mag_err,
            Match.pawprint_src_hjd, Match.pawprint_src_chip_nro,
            Match.pawprint_src_stel_cls, Match.pawprint_src_elip,
            Match.pawprint_src_pos_ang,
            Match.tile_id, Match.master_src_id
        ).filter(Match.tile_id == tile_id)

        if obs_table.nrows:
            ptq = "tile_id == {}".format(tile_id)
            max_id = np.max([s["id"] for s in obs_table.where(ptq)])
            obs_q = obs_q.filter(Match.pawprint_src_id > max_id)

        buff = []
        for src in obs_q.order_by(Match.pawprint_src_id).yield_per(YIELD_PER):
            buff.append(tuple(src))
            if len(buff) > BUFF_SIZE:
                obs_table.append(buff)
                logger.info(" obs-FLUSH")
                obs_table.flush()
                buff = []
        if buff:
            obs_table.append(buff)
            logger.info(" obs-FLUSH")
            obs_table.flush()

    def _sync_obs_number(self, session, tile_id,
                         tiles_table, src_table, obs_table):

        for tile_row in tiles_table.where("id == {}".format(tile_id)):

            if tile_row["matchs_counted"]:
                continue

            query = session.query(
                Match.master_src_id, db.func.count(Match.pawprint_src_id)
            ).filter(
                Match.tile_id == tile_id
            ).group_by(Match.master_src_id).order_by(Match.master_src_id)

            buff = {}
            for row_id, obs_cnt in query.yield_per(YIELD_PER):
                buff[row_id] = obs_cnt
                if len(buff) > BUFF_SIZE:
                    logger.info(" obs-numb-FLUSH")
                    ids = np.array(buff.keys())
                    min_id, max_id = np.min(ids), np.max(ids)
                    src_flt = "(id >= {}) & (id <= {})".format(min_id, max_id)
                    for src_row in src_table.where(src_flt):
                        src_id = src_row["id"]
                        if src_id in buff:
                            src_row["obs_number"] = buff[src_id]
                            src_row.update()
                    buff.clear()
            if buff:
                logger.info(" obs-numb-FLUSH")
                ids = np.array(buff.keys())
                min_id, max_id = np.min(ids), np.max(ids)
                src_flt = "(id >= {}) & (id <= {})".format(min_id, max_id)
                for src_row in src_table.where(src_flt):
                    src_id = src_row["id"]
                    if src_id in buff:
                        src_row["obs_number"] = buff[src_id]
                        src_row.update()
                buff.clear()

            tile_row["matchs_counted"] = True
            tile_row.update()

        src_table.flush()
        tiles_table.flush()

    def run(self):
        tiles = self.session.query(
            Tile.id, Tile.name
        ).filter(Tile.name.in_(self.tiles_names)).order_by(Tile.id).all()

        with dumpopen(self.h5_path, mode="a", title=self.title) as df:
            for tile_id, tile_name in tiles:
                logger.info("Dumping tile '{}'... ".format(tile_name))
                self._store_tiles(self.session, tile_id, df.tiles_table)
                logger.info("Dumping sources of tile '{}'...".format(tile_name))
                self._store_sources(self.session, tile_id, df.src_table)
                logger.info("Dumping obs of tile '{}'...".format(tile_name))
                self._store_observations(self.session, tile_id, df.obs_table)
                logger.info("Sync obs number of tile '{}'...".format(tile_name))
                self._sync_obs_number(self.session, tile_id, df.tiles_table, df.src_table, df.obs_table)
        logger.info("Done")


# =============================================================================
# FUNCTIONS
# =============================================================================

@contextmanager
def dumpopen(path, *args, **kwargs):
    with tb.open_file(path, *args, **kwargs) as h5file:
        if "/tiles" in h5file:
            tiles_table = h5file.get_node("/tiles")
        else:
            tiles_table = h5file.create_table("/", "tiles", TileDescriptor)
            tiles_table.cols.id.create_index()
        if "/sources" in h5file:
            src_table = h5file.get_node("/sources")
        else:
            src_table = h5file.create_table("/", "sources", SourceDescriptor)
            src_table.cols.id.create_index()
            src_table.cols.tile_id.create_index()
        if "/observations" in h5file:
            obs_table = h5file.get_node("/observations")
        else:
            obs_table = h5file.create_table(
                "/", "observations", ObservationDescriptor)
            obs_table.cols.id.create_index()
            obs_table.cols.tile_id.create_index()
            obs_table.cols.source_id.create_index()
            obs_table.cols.pwp_id.create_index()

        df = DumpFile(
            h5file=h5file, tiles_table=tiles_table,
            src_table=src_table, obs_table=obs_table)

        yield df


def dump(session, tiles_names, h5_path, mode="w", procs_n=1, sync=False):

    def chunk_it(seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return [chunk for chunk in sorted(out, reverse=True) if chunk]

    title = "Tiles: {} ({})".format(",".join(tiles_names), dt.datetime.now())
    db.engine.dispose()

    procs = []
    for chunk in chunk_it(tiles_names, procs_n):
        proc = Tile2HDF5(title, session, chunk, h5_path)
        if sync:
            proc.run()
        else:
            proc.start()
        procs.append(proc)
    return tuple(procs)
