#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil, tempfile, uuid, logging

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from astropy.io import fits

from montage_wrapper import commands as montage

from carpyncho.galaxy import models
from carpyncho.galaxy.libs import pyfpack


#===============================================================================
# LOGGER
#===============================================================================

logger = logging.getLogger("galaxy")


#===============================================================================
# COMMAND
#===============================================================================

class Command(BaseCommand):
    help = "Register a tile file into galaxy search program"
    args = ["tile_id",
            "h_fit_fz_filepath", "j_fit_fz_filepath", "k_fit_fz_filepath"]

    def _save_to_field(self, fpath, field):
        logger.info(u"Saving {} ...".format(fpath))
        fname = os.path.basename(fpath)
        with open(fpath) as fp:
            field.save(fname, File(fp))

    def _unpack(self, fpath):
        logger.info("Unpacking: {} ...".format(fpath))
        tmp_name = "{}.fit".format(os.path.basename(fpath).split(".", 1)[0])
        tmp_path = os.path.join(self.tmpdir, tmp_name)
        pyfpack.unpack(fpath, O=tmp_path)
        return tmp_path

    def _get_hdr(self, fpath):
        logger.info("Extracting hdr: {} ...".format(fpath))
        tmp_name = "{}.hdr".format(os.path.basename(fpath).split(".", 1)[0])
        tmp_path = os.path.join(self.tmpdir, tmp_name)
        montage.mGetHdr(fpath, tmp_path)
        return tmp_path

    def _project(self, fpath, hdrpath):
        logger.info("Projecting: {} ...".format(fpath))
        tmp_name = "{}_projected.hdr".format(
            os.path.basename(fpath).split(".", 1)[0]
        )
        tmp_path = os.path.join(self.tmpdir, tmp_name)
        montage.mProjectPP(fpath, tmp_path, hdrpath, whole=True, hdu=0)
        return tmp_path

    def _merge_jpg(self, tilename, blue, green, red):
        logger.info("Merging...")
        tmp_name = "merged_{}.jpg".format(tilename)
        tmp_path = os.path.join(self.tmpdir, tmp_name)
        cmd = [
            "mJPEG", "-t", "2",
            "-blue", blue, "-0s" "max", "gaussian-log",
            "-green", green, "-0s" "max", "gaussian-log",
            "-red", red, "-0s" "max", "gaussian-log",
            "-out", out
        ]
        return tmp_path


    def _register_tile(self, tile_id, h_fit_fz_filepath,
                       j_fit_fz_filepath, k_fit_fz_filepath):

        k_fit_file_path = self._unpack(k_fit_fz_filepath)
        #~ j_fit_file_path = self._unpack(j_fit_fz_filepath)
        #~ h_fit_file_path = self._unpack(h_fit_fz_filepath)

        # TODO: Fix projections of K


        # extract headers
        hdr_path = self._get_hdr(k_fit_file_path)

        # reproject
        k_fit_file_path = self._project(k_fit_file_path, hdr_path)
        #j_fit_file_path = self._project(j_fit_file_path, hdr_path)
        # h_fit_file_path = self._project(h_fit_file_path, hdr_path)

        #~ tile, crt = models.Tile.objects.get_or_create(tile_id=tile_id)
        #~ self._save_to_field(k_fit_fz_filepath, tile.k_fit_fz)
        #~ self._save_to_field(k_fit_file_path, tile.k_fit)
        #~ self._save_to_field(j_fit_fz_file_path, tile.j_fit_fz)
        #~ self._save_to_field(j_fit_filepath, tile.j_fit)
        #~ self._save_to_field(h_fit_fz_file_path, tile.h_fit_fz)
        #~ self._save_to_field(h_fit_filepath, tile.h_fit)
#~
        #~ tile.save()


    def handle(self, *args, **options):
        tile_number, h_fit_fz_filepath, j_fit_fz_filepath, k_fit_fz_filepath = args
        self.tmpdir = tempfile.mkdtemp("_galaxy_register_tile")
        try:
            logger.info(u"Work on: {}".format(self.tmpdir))
            with transaction.atomic():
                self._register_tile(
                    tile_number, h_fit_fz_filepath, j_fit_fz_filepath, k_fit_fz_filepath
                )
        except Exception as err:
            logger.exception(err)
        finally:
            logger.info(u"Cleaning")
            shutil.rmtree(self.tmpdir)


