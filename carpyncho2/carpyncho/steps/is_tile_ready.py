#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corral import run, db

from ..models import Tile, PawprintXTile


class IsTileReady(run.Step):

    model = Tile
    conditions = []
    groups = ["daemon"]

    def process(self, tile):
        query = self.session.query(
            PawprintXTile.status
        ).filter(PawprintXTile.tile_id == tile.id)
        is_synced = map(lambda r: r[0] == "sync", query)
        tile.ready = all(is_synced)
