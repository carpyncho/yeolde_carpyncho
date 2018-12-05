#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corral import db
from carpyncho.models import PawprintXTile

tile_names = "b278 b202 b261 b264 b263 b262, b220".split()

with db.session_scope() as session:
    end = False
    for tile_name in tile_names:
        query = session.query(PawprintXTile).filter(
            PawprintXTile.tile.has(name=tile_name) &
            (PawprintXTile.status == "raw") &
            (PawprintXTile.status != "pending")
        )
        for pxt in query:
            pxt.status = "pending"
            print "Pending: {}".format(pxt)
            end = True
        if end:
            break
