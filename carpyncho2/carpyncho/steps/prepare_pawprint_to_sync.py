#!/usr/bin/env python
# -*- coding: utf-8 -*-

from corral import run

from ..models import PawprintXTile


class PreparePawprintToSync(run.Step):

    model = PawprintXTile
    conditions = [
        PawprintXTile.status == "raw",
        PawprintXTile.tile.has(status="loaded"),
        PawprintXTile.pawprint.has(status="loaded")
    ]
    limit = 500
    groups = ["match"]

    def process(self, pxt):
        pxt.status = "pending"
