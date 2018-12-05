#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corral import run, db

from ..models import Tile, MasterSource


class ReadTile(run.Step):

    model = Tile
    conditions = [model.status == "measured"]
    procno = 3
    groups = ["read"]
    production_procno = 1

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
                r[0] for r in
                session.query(cls.model.id).filter(*cls.conditions))
        db.engine.dispose()
        cls.chunks = chunk_it(all_ids, cls.get_procno())

    def setup(self):
        self.buff = []

    def generate(self):
        if not self.chunks:
            return ()
        ids = self.chunks[self.current_proc]
        if not ids:
            return ()
        query = self.session.query(self.model).filter(self.model.id.in_(ids))
        return query

    def validate(self, obj):
        assert isinstance(obj, (dict, db.Model))

    def save(self, obj):
        if isinstance(obj, dict):
            self.buff.append(obj)
        else:
            super(ReadTile, self).save(obj)

    def update_tile(self, tile):
        if self.buff:
            self.session.bulk_insert_mappings(MasterSource, self.buff)
            tile.data_readed = tile.data_readed + len(self.buff)
            self.buff = []
            self.session.commit()

    def process(self, tile):
        offset = tile.data_readed
        for order, src in enumerate(tile.data[offset:], offset):
            srcdict = dict(
                tile_id=tile.id, order=order,
                ra_h=src[0], dec_h=src[1],
                ra_j=src[2], dec_j=src[3],
                ra_k=src[4], dec_k=src[5])
            yield srcdict

            if len(self.buff) >= 5000:
                self.update_tile(tile)
        else:
            self.update_tile(tile)
            tile.data_readed = tile.data_size
            tile.status = "loaded"
