#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corral import run, db

from PyAstronomy import pyasl

from ..models import Pawprint, PawprintSource


class HJDPawprintSource(run.Step):

    model = PawprintSource
    conditions = [
        PawprintSource.hjd.is_(None),
        PawprintSource.pawprint.has(Pawprint.mjd.isnot(None))
    ]
    groups = ["extra"]
    procno = 3
    production_procno = 20
    limit = 1000000

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
            query = session.query(
                cls.model.id
            ).filter(
                *cls.conditions
            ).limit(cls.limit)
            all_ids = tuple(r[0] for r in query)
        db.engine.dispose()
        cls.chunks = chunk_it(all_ids, cls.get_procno())

    def setup(self):
        self.buff = []

    def teardown(self, *args, **kwargs):
        self.update_hjds()

    def validate(self, obj):
        assert isinstance(obj, (dict, db.Model))

    def generate(self):
        if not self.chunks:
            return ()
        ids = self.chunks[self.current_proc]
        if not ids:
            return ()
        return self.session.query(self.model).filter(self.model.id.in_(ids))

    def save(self, obj):
        if isinstance(obj, dict):
            if obj:
                self.buff.append(obj)
        else:
            super(HJDPawprintSource, self).save(obj)

    def update_hjds(self):
        if self.buff:
            self.session.bulk_update_mappings(PawprintSource, self.buff)
            self.session.commit()
            self.buff = []

    def process(self, pwp_src):
        hjd = pyasl.helio_jd(
            pwp_src.pawprint.mjd, pwp_src.ra_deg, pwp_src.dec_deg)
        data = {"id": pwp_src.id, "hjd": hjd}
        yield data
        if len(self.buff) >= 500000:
            self.update_hjds()
