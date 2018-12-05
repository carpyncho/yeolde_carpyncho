#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created at 2015-12-07T20:41:54.110455 by corral 0.0.1


# =============================================================================
# DOCS
# =============================================================================

"""carpyncho main loader

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import glob

from corral import run
from corral.conf import settings

from carpyncho.models import Tile, Pawprint, PawprintXTile


# =============================================================================
# LOADER
# =============================================================================

class Loader(run.Loader):
    """Scan the pending directory and register the tiles and pawprint
    found and also store the files in a more convenient way

    """

    def only_dirs(self, path):
        for dname in os.listdir(path):
            dpath = os.path.abspath(os.path.join(path, dname))
            if os.path.isdir(dpath):
                yield dname, dpath

    def retrieve_master_path(self, path):
        pattern = os.path.join(path, "*.dat")
        files = glob.glob(pattern)
        return files[0] if files else None

    def list_pawprints(self, path):
        pattern = os.path.join(path, "pawprints", "*.fits")
        return glob.glob(pattern)

    def setup(self):
        self.stored_tiles_dir = os.path.join(settings.DATA_PATH, "tiles")
        if not os.path.isdir(self.stored_tiles_dir):
            os.makedirs(self.stored_tiles)

        self.stored_pawprints_dir = os.path.join(
            settings.DATA_PATH, "pawprints")
        if not os.path.isdir(self.stored_pawprints_dir):
            os.makedirs(self.stored_pawprints_dir)

        self.tiles, self.pawprints = {}, {}
        for tile_name, dpath in self.only_dirs(settings.INPUT_PATH):
            master_path = self.retrieve_master_path(dpath)
            if master_path:
                self.tiles[tile_name] = master_path
            pawprints = self.list_pawprints(dpath)
            if pawprints:
                self.pawprints[tile_name] = pawprints

    def generate(self):

        for tile_name, tile_path in self.tiles.items():
            tile = Tile(name=tile_name)
            tile.store_file(tile_path)
            yield tile
            self.session.commit()
            os.remove(tile_path)

        for tile_name, pawprints in self.pawprints.items():
            tile = self.session.query(Tile).filter_by(name=tile_name).first()
            for pwp_path in pawprints:
                name = os.path.splitext(os.path.basename(pwp_path))[0]
                pwp = self.session.query(Pawprint).filter_by(name=name).first()
                if pwp is None:
                    pwp = Pawprint(name=name)
                    pwp.store_file(pwp_path)
                    yield pwp

                pxt = self.session.query(PawprintXTile).filter_by(
                    pawprint=pwp, tile=tile).first()
                if pxt is None:
                    pxt = PawprintXTile(pawprint=pwp, tile=tile)
                    yield pxt

                self.session.commit()
                os.remove(pwp_path)
