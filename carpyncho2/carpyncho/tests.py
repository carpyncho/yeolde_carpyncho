#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created at ${timestamp} by corral ${version}


# =============================================================================
# DOCS
# =============================================================================

"""${project_name} tests

"""


# =============================================================================
# IMPORTS
# =============================================================================

from corral import qa

from carpyncho import models, commands
from carpyncho.steps import is_tile_ready


# =============================================================================
# LOADER
# =============================================================================

class IsTileReadyTest(qa.TestCase):

    subject = is_tile_ready.IsTileReady

    def setup(self):
        self.patch("corral.conf.settings.PATH", "foo")
        tile = models.Tile(name="foo")
        self.save(tile)

    def validate(self):
        self.assertStreamHas(
            models.Tile, models.Tile.name=="foo", models.Tile.ready==True)
        self.assertStreamCount(1, models.Tile)



class IsTileReady2Test(qa.TestCase):

    subject = is_tile_ready.IsTileReady

    def validate(self):
        self.assertStreamHasNot(
            models.Tile, models.Tile.name=="foo", models.Tile.ready==True)
        self.assertStreamCount(0, models.Tile)


class LSTileCommand(qa.TestCase):

    subject = commands.LSTile

    def setup(self):
        tile = models.Tile(name="foo")
        self.save(tile)

    def validate(self):
        pass
