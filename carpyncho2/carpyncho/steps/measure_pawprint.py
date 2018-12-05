#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile
import os
import copy
import shutil

from corral import run, db

import sh

import numpy as np

from ..models import Pawprint
from .. import bin


PAWPRINTS_DEFAULT_PARAMS = {
    "dtype": {
        "names": [
            'ra_h', 'ra_m', 'ra_s', 'dec_d', 'dec_m', 'dec_s',
            'x', 'y', 'mag', 'mag_err',
            'chip_nro', 'stel_cls', 'elip', 'pos_ang',
        ],
        "formats": [
            int, int, float, int, int, float,
            float, float, float, float,
            int, int, float, float,
        ]
    }
}


class MeasurePawprint(run.Step):

    model = Pawprint
    conditions = [model.status == "raw"]
    procno = 3
    production_procno = 30
    groups = ["measurement"]

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

    def generate(self):
        if not self.chunks:
            return ()
        ids = self.chunks[self.current_proc]
        if not ids:
            return ()
        query = self.session.query(self.model).filter(self.model.id.in_(ids))
        return query

    def setup(self):
        self.work_path = tempfile.mkdtemp("_measure_pawprint")
        self.asc_path = os.path.join(self.work_path, "catalogue.asc")
        if os.path.isfile(self.asc_path):
            raise IOError("Duplicated {}".format(self.asc_path))
        self.fitsio_cat_list = sh.Command(bin.get("fitsio_cat_list"))
        os.chdir(self.work_path)

    def teardown(self, *args, **kwargs):
        if os.path.isdir(self.work_path):
            shutil.rmtree(self.work_path)

    def ra_to_degree(self, arr):
        return 15 * (
            arr['ra_h'] +
            arr['ra_m'] / 60.0 +
            arr['ra_s'] / 3600.0)

    def dec_to_degree(self, arr):
        return np.sign(arr['dec_d']) * (
            np.abs(arr['dec_d']) +
            arr['dec_m'] / 60.0 +
            arr['dec_s'] / 3600.0)

    def to_array(self, path):
        filename = os.path.basename(path)

        tmp_file_path = os.path.join(self.work_path, filename)
        os.symlink(path, tmp_file_path)

        self.fitsio_cat_list(tmp_file_path)

        odata = np.genfromtxt(self.asc_path, **PAWPRINTS_DEFAULT_PARAMS)

        ra_deg = self.ra_to_degree(odata)
        dec_deg = self.dec_to_degree(odata)

        conf = copy.deepcopy(PAWPRINTS_DEFAULT_PARAMS)
        conf["dtype"]["names"].insert(0, "dec_deg")
        conf["dtype"]["names"].insert(0, "ra_deg")
        conf["dtype"]["formats"].insert(0, float)
        conf["dtype"]["formats"].insert(0, float)

        data = np.empty(len(odata), **conf)
        for name in data.dtype.names:
            if name == "ra_deg":
                data[name] = ra_deg
            elif name == "dec_deg":
                data[name] = dec_deg
            else:
                data[name] = odata[name]
        return data

    def process(self, pwp):
        path = pwp.file_path()
        pwp.data = self.to_array(path)
        pwp.data_size = len(pwp.data)
        pwp.data_readed = 0
        pwp.status = "measured"
