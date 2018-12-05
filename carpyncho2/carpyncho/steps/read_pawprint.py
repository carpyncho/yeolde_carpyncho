#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corral import run, db

from ..models import Pawprint, PawprintSource


class ReadPawprint(run.Step):

    model = Pawprint
    conditions = [model.status == "measured"]
    procno = 3
    groups = ["read"]
    production_procno = 40

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
            super(ReadPawprint, self).save(obj)

    def update_pawprint(self, pwp):
        if self.buff:
            self.session.bulk_insert_mappings(PawprintSource, self.buff)
            pwp.data_readed = pwp.data_readed + len(self.buff)
            self.buff = []
            self.session.commit()

    def process(self, pwp):
        offset = pwp.data_readed
        for order, src in enumerate(pwp.data[offset:], offset):
            srcdict = dict(
                pawprint_id=pwp.id, order=order,
                ra_deg=src[0], dec_deg=src[1],
                ra_h=src[2], ra_m=src[3], ra_s=src[4],
                dec_d=src[5], dec_m=src[6], dec_s=src[7],
                pwp_x=src[8], pwp_y=src[9], mag=src[10], mag_err=src[11],
                chip_nro=src[12], stel_cls=src[13],
                elip=src[14], pos_ang=src[15],
            )
            yield srcdict

            if len(self.buff) >= 5000:
                self.update_pawprint(pwp)
        else:
            self.update_pawprint(pwp)
            pwp.data_readed = pwp.data_size
            pwp.status = "loaded"
