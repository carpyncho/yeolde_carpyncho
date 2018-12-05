#!/usr/bin/env python
# -*- coding: utf-8 -*-

#==============================================================================
# DOCS
#==============================================================================

"""Register a mastersouce in to lcurves

"""


#==============================================================================
# IMPORTS
#==============================================================================

import logging
import os

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from carpyncho.lcurves import models
from carpyncho.lcurves.libs import match

from carpyncho.lcurves.management.commands import (
    reg_tile, reg_pawprint, load_sources, match_pawprints, stats_calc
)


#==============================================================================
# LOGGER
#==============================================================================

logger = logging.getLogger("lcurves")


#==============================================================================
# WRAP OTHER COMMSNFS
#==============================================================================

register_tile = reg_tile.Command().register_tile
register_pawprint = reg_pawprint.Command().register_pawprint
load_sources = load_sources.Command().load_sources
match_unsync_pawprints = match_pawprints.Command().match_unsync_pawprints
calculate_all_statistics = stats_calc.Command().calculate_all_statistics


#==============================================================================
# COMMAND
#==============================================================================

class Command(BaseCommand):
    help = "Register from sources"
    args = ["dirpath"]

    def only_dirs(self, path):
        for dname in os.listdir(path):
            dpath = os.path.abspath(os.path.join(path, dname))
            if os.path.isdir(dpath):
                yield dname, dpath

    def retrieve_master_path(self, path):
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)
            ext = os.path.splitext(fpath)[-1].lower()
            if os.path.isfile(fpath) and ext == ".dat":
                return fpath

    def list_pawprints(self, path):
        pawprints = os.path.join(path, "pawprints")
        for fname in os.listdir(pawprints):
            fpath = os.path.join(pawprints, fname)
            ext = os.path.splitext(fpath)[-1]
            if os.path.isfile(fpath) and ext.lower() == ".fits":
                yield fpath

    def handle(self, *args, **options):
        dirpath, = args
        for tile_name, tile_path in self.only_dirs(dirpath):
            try:

                logger.info(u"Scaning '{}'...".format(tile_path))

                # MASTER SOURCE REGISTERING
                master_path = self.retrieve_master_path(tile_path)
                if master_path:
                    logger.info(
                        u"New Master Found '{}'...".format(master_path)
                    )
                    try:
                        with transaction.atomic():
                            register_tile(tile_name, master_path)
                    except Exception as err:
                        logger.exception(err)
                    else:
                        logger.info(
                            u"Removing file '{}'...".format(master_path)
                        )
                        os.remove(master_path)

                # PAWPRINT REGISTERING
                for pp_path in self.list_pawprints(tile_path):
                    logger.info(
                        u"New Pawprint Found '{}'...".format(pp_path)
                    )
                    try:
                        with transaction.atomic():
                            register_pawprint(tile_name, pp_path)
                    except Exception as err:
                        logger.exception(err)
                    else:
                        logger.info(
                            u"Removing file '{}'...".format(pp_path)
                        )
                        os.remove(pp_path)
            except Exception as err:
                logger.exception(err)
            finally:
                logger.info(u"Ending load...")

        # PAWPRINT LOAD SOURCES
        try:
            with transaction.atomic():
                load_sources()
        except Exception as err:
            logger.exception(err)

        # MATCHING
        match_unsync_pawprints()
        calculate_all_statistics()



#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
