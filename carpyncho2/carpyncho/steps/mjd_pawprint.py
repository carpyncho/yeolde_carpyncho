#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corral import run

from astropy.io import fits

from ..models import Pawprint


class MJDPawprint(run.Step):

    model = Pawprint
    conditions = [model.mjd.is_(None)]
    groups = ["measurement"]

    def extract_mjd(self, fpath):
        hdulist = fits.open(fpath)
        return hdulist[0].header["MJD-OBS"]

    def process(self, pwp):
        path = pwp.file_path()
        pwp.mjd = self.extract_mjd(path)
